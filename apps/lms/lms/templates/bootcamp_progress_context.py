# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe import _

def get_bootcamp_progress_context(bootcamp_name, user):
    """Get context for bootcamp progress page"""
    # Get bootcamp
    bootcamp = frappe.get_doc("LMS Bootcamp", bootcamp_name)
    
    # Get enrollment
    enrollment_name = frappe.db.exists(
        "Enrollment",
        {
            "user": user,
            "bootcamp": bootcamp_name
        }
    )
    
    if enrollment_name:
        enrollment = frappe.get_doc("Enrollment", enrollment_name)
        progress = enrollment.get_progress()
        completed_lessons = len(enrollment.completed_lessons)
    else:
        enrollment = None
        progress = 0
        completed_lessons = 0
    
    # Get total lessons
    total_lessons = get_total_lessons_in_bootcamp(bootcamp_name)
    remaining_lessons = total_lessons - completed_lessons
    
    # Get courses with lessons
    courses = []
    for course_row in bootcamp.courses:
        course = frappe.get_doc("LMS Course", course_row.name)
        
        # Add lessons with completion status
        lessons = []
        for lesson_row in course.lessons:
            lesson = frappe.get_doc("LMS Lesson", lesson_row.name)
            is_completed = enrollment and enrollment.is_lesson_completed(lesson.name) if enrollment else False
            
            lessons.append({
                "name": lesson.name,
                "title": lesson.title,
                "description": lesson.description,
                "content_type": lesson.content_type,
                "is_free_preview": lesson.is_free_preview,
                "is_completed": is_completed,
                "is_enrolled": bool(enrollment)
            })
        
        courses.append({
            "name": course.name,
            "title": course.title,
            "description": course.description,
            "lessons": lessons
        })
    
    # Find next lesson
    next_lesson = None
    if enrollment and courses:
        for course in courses:
            for lesson in course["lessons"]:
                if not lesson["is_completed"]:
                    next_lesson = lesson
                    break
            if next_lesson:
                break
    
    return {
        "bootcamp": bootcamp,
        "progress": progress,
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons,
        "remaining_lessons": remaining_lessons,
        "courses": courses,
        "next_lesson": next_lesson
    }

def get_total_lessons_in_bootcamp(bootcamp_name):
    """Get total number of lessons in a bootcamp"""
    bootcamp = frappe.get_doc("LMS Bootcamp", bootcamp_name)
    
    total_lessons = 0
    for course_row in bootcamp.courses:
        course = frappe.get_doc("LMS Course", course_row.name)
        total_lessons += len(course.lessons)
    
    return total_lessons