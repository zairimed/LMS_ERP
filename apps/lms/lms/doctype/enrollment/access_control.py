# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe import _

def is_user_enrolled(user, bootcamp):
    """Check if a user is enrolled in a bootcamp"""
    # Check if enrollment exists for this user and bootcamp
    enrollment_name = frappe.db.exists(
        "Enrollment",
        {
            "user": user,
            "bootcamp": bootcamp
        }
    )
    
    return bool(enrollment_name)

def check_content_access(user, bootcamp):
    """Check if user has access to bootcamp content"""
    # If user is enrolled, they have access
    if is_user_enrolled(user, bootcamp):
        return True
    
    # If user is System Manager or Administrator, they have access
    if frappe.has_permission("Enrollment", "write"):
        return True
    
    return False

def check_lesson_access(user, lesson):
    """Check if user has access to a specific lesson"""
    # Get the lesson document
    lesson_doc = frappe.get_doc("LMS Lesson", lesson)
    
    # If it's a free preview lesson, everyone has access
    if lesson_doc.is_free_preview:
        return True
    
    # Get the course and bootcamp for this lesson
    course = frappe.get_doc("LMS Course", lesson_doc.parent)
    bootcamp = frappe.get_doc("LMS Bootcamp", course.parent)
    
    # Check if user has access to the bootcamp
    return check_content_access(user, bootcamp.name)

def get_enrolled_bootcamps(user):
    """Get all bootcamps a user is enrolled in"""
    # Get all enrollments for this user
    enrollments = frappe.get_all(
        "Enrollment",
        filters={"user": user},
        fields=["bootcamp"]
    )
    
    # Extract bootcamp names
    bootcamp_names = [enrollment.bootcamp for enrollment in enrollments]
    
    # Get bootcamp documents
    bootcamps = []
    for bootcamp_name in bootcamp_names:
        bootcamp = frappe.get_doc("LMS Bootcamp", bootcamp_name)
        bootcamps.append(bootcamp)
    
    return bootcamps