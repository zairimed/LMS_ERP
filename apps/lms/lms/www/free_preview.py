# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe import _

def get_context(context):
    """Context for free preview lessons page"""
    # Get all bootcamps that have free preview lessons
    bootcamps = frappe.get_all("LMS Bootcamp", fields=["name", "title", "description"])
    
    # Add courses and lessons to each bootcamp
    for bootcamp in bootcamps:
        # Get courses for this bootcamp
        courses = frappe.get_all("LMS Course", 
                                filters={"parent": bootcamp.name, "parenttype": "LMS Bootcamp"},
                                fields=["name", "title", "description"])
        
        # Add lessons to each course
        for course in courses:
            # Get free preview lessons for this course
            lessons = frappe.get_all("LMS Lesson",
                                   filters={"parent": course.name, "parenttype": "LMS Course", "is_free_preview": 1},
                                   fields=["name", "title", "description", "content_type", "video_url", "content"])
            course.free_preview_lessons = lessons
            
        bootcamp.courses = [course for course in courses if course.free_preview_lessons]
    
    # Filter out bootcamps with no free preview lessons
    context.bootcamps = [bootcamp for bootcamp in bootcamps if bootcamp.courses]
    
    context.title = _("Free Preview Lessons")
    return context

@frappe.whitelist(allow_guest=True)
def get_free_preview_lesson(lesson_name):
    """Get a specific free preview lesson"""
    try:
        # Get the lesson
        lesson = frappe.get_doc("LMS Lesson", lesson_name)
        
        # Check if it's marked as free preview
        if not lesson.is_free_preview:
            frappe.throw(_("This lesson is not available for free preview"), frappe.PermissionError)
        
        # Get the course and bootcamp for this lesson
        course = frappe.get_doc("LMS Course", lesson.parent)
        bootcamp = frappe.get_doc("LMS Bootcamp", course.parent)
        
        # Return the lesson data along with its context
        return {
            "lesson": lesson,
            "course": course,
            "bootcamp": bootcamp
        }
    except frappe.DoesNotExistError:
        frappe.throw(_("Lesson not found"), frappe.DoesNotExistError)
    except frappe.PermissionError:
        raise
    except Exception:
        frappe.throw(_("Unable to retrieve lesson"), frappe.ValidationError)