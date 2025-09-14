# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe import _

def get_my_bootcamps_context(page=1, page_size=10):
    """Get context for my bootcamps page with pagination"""
    # Get current user
    user = frappe.session.user
    
    # Get enrolled bootcamps with pagination
    from ..doctype.enrollment.access_control import get_enrolled_bootcamps
    all_bootcamps = get_enrolled_bootcamps(user)
    
    # Apply pagination
    total_bootcamps = len(all_bootcamps)
    total_pages = (total_bootcamps + page_size - 1) // page_size
    
    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, total_bootcamps)
    bootcamps = all_bootcamps[start_index:end_index]
    
    return {
        "bootcamps": bootcamps,
        "current_page": page,
        "total_pages": total_pages,
        "total_bootcamps": total_bootcamps,
        "has_previous": page > 1,
        "has_next": page < total_pages,
        "previous_page": page - 1,
        "next_page": page + 1
    }

def get_bootcamp_content_context(bootcamp_name):
    """Get context for bootcamp content page"""
    # Get current user
    user = frappe.session.user
    
    # Get bootcamp
    bootcamp = frappe.get_doc("LMS Bootcamp", bootcamp_name)
    
    # Check access
    from ..doctype.enrollment.access_control import check_content_access
    if not check_content_access(user, bootcamp_name):
        frappe.throw(_("You are not enrolled in this bootcamp"), frappe.PermissionError)
    
    # Get enrollment for progress
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
    total_lessons = 0
    if enrollment:
        total_lessons = enrollment.get_total_lessons()
    
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
                "is_completed": is_completed
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

def get_lesson_content_context(lesson_name):
    """Get context for lesson content page"""
    # Get current user
    user = frappe.session.user
    
    # Get lesson
    lesson = frappe.get_doc("LMS Lesson", lesson_name)
    
    # Get course and bootcamp
    course = frappe.get_doc("LMS Course", lesson.parent)
    bootcamp = frappe.get_doc("LMS Bootcamp", course.parent)
    
    # Check access
    from ..doctype.enrollment.access_control import check_lesson_access
    if not check_lesson_access(user, lesson_name):
        frappe.throw(_("You do not have access to this lesson"), frappe.PermissionError)
    
    # Get enrollment for completion status
    enrollment_name = frappe.db.exists(
        "Enrollment",
        {
            "user": user,
            "bootcamp": bootcamp.name
        }
    )
    
    is_completed = False
    if enrollment_name:
        enrollment = frappe.get_doc("Enrollment", enrollment_name)
        is_completed = enrollment.is_lesson_completed(lesson_name)
    
    # Get previous and next lessons
    previous_lesson = None
    next_lesson = None
    
    # Get all lessons in the course
    all_lessons = []
    for lesson_row in course.lessons:
        all_lessons.append(lesson_row.name)
    
    # Find current lesson index
    try:
        current_index = all_lessons.index(lesson_name)
        if current_index > 0:
            previous_lesson = frappe.get_doc("LMS Lesson", all_lessons[current_index - 1])
        if current_index < len(all_lessons) - 1:
            next_lesson = frappe.get_doc("LMS Lesson", all_lessons[current_index + 1])
    except ValueError:
        # Lesson not found in course
        pass
    
    return {
        "lesson": lesson,
        "course": course,
        "bootcamp": bootcamp,
        "is_completed": is_completed,
        "previous_lesson": previous_lesson,
        "next_lesson": next_lesson
    }