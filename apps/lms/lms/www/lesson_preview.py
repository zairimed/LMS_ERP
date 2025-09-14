# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe import _

def get_context(context):
    """Context for individual lesson preview page"""
    # Get the lesson name from URL parameters
    lesson_name = frappe.form_dict.get("lesson")
    
    if not lesson_name:
        frappe.throw(_("Lesson parameter is required"), frappe.ValidationError)
    
    # Get the lesson
    lesson = frappe.get_doc("LMS Lesson", lesson_name)
    
    # Check if it's marked as free preview
    if not lesson.is_free_preview:
        frappe.throw(_("This lesson is not available for free preview"), frappe.PermissionError)
    
    # Get the course and bootcamp for this lesson
    course = frappe.get_doc("LMS Course", lesson.parent)
    bootcamp = frappe.get_doc("LMS Bootcamp", course.parent)
    
    # Set context variables
    context.lesson = lesson
    context.course = course
    context.bootcamp = bootcamp
    
    # Get other free preview lessons in the same course for navigation
    other_lessons = frappe.get_all("LMS Lesson",
                                  filters={"parent": course.name, "parenttype": "LMS Course", "is_free_preview": 1, "name": ["!=", lesson.name]},
                                  fields=["name", "title"])
    context.other_lessons = other_lessons
    
    context.title = lesson.title
    return context