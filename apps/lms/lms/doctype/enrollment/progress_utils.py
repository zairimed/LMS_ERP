# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate

def mark_lesson_as_completed(user, bootcamp, lesson):
    """Mark a lesson as completed for a user in a bootcamp"""
    # Get or create enrollment
    enrollment_name = frappe.db.exists(
        "Enrollment",
        {
            "user": user,
            "bootcamp": bootcamp
        }
    )
    
    if not enrollment_name:
        # Create new enrollment
        enrollment = frappe.get_doc({
            "doctype": "Enrollment",
            "user": user,
            "bootcamp": bootcamp
        })
        enrollment.insert()
        enrollment_name = enrollment.name
    
    # Get enrollment document
    enrollment = frappe.get_doc("Enrollment", enrollment_name)
    
    # Mark lesson as complete
    enrollment.mark_lesson_complete(lesson)

def auto_mark_video_lesson_completed(user, bootcamp, lesson):
    """Automatically mark video lessons as completed when watched"""
    # Get the lesson document
    lesson_doc = frappe.get_doc("LMS Lesson", lesson)
    
    # Check if it's a video lesson
    if lesson_doc.content_type == "Video":
        # Mark as completed
        mark_lesson_as_completed(user, bootcamp, lesson)
        return True
    return False

def auto_mark_text_lesson_completed(user, bootcamp, lesson, time_spent=0):
    """Automatically mark text lessons as completed based on time spent"""
    # Get the lesson document
    lesson_doc = frappe.get_doc("LMS Lesson", lesson)
    
    # Check if it's a text lesson
    if lesson_doc.content_type == "Text":
        # For text lessons, we might want to check if the user spent enough time
        # For now, we'll mark as completed (future implementation could check time)
        mark_lesson_as_completed(user, bootcamp, lesson)
        return True
    return False

def auto_mark_lab_lesson_completed(user, bootcamp, lesson, interaction_count=0):
    """Automatically mark lab lessons as completed based on interactions"""
    # Get the lesson document
    lesson_doc = frappe.get_doc("LMS Lesson", lesson)
    
    # Check if it's a lab lesson
    if lesson_doc.content_type == "Lab":
        # For lab lessons, we might want to check interactions
        # For now, we'll mark as completed (future implementation could check interactions)
        mark_lesson_as_completed(user, bootcamp, lesson)
        return True
    return False

def get_user_progress(user, bootcamp):
    """Get user's progress in a bootcamp"""
    # Get enrollment
    enrollment_name = frappe.db.exists(
        "Enrollment",
        {
            "user": user,
            "bootcamp": bootcamp
        }
    )
    
    if not enrollment_name:
        return 0
    
    # Get enrollment document
    enrollment = frappe.get_doc("Enrollment", enrollment_name)
    
    # Return progress
    return enrollment.get_progress()