# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class EnrollmentLesson(Document):
    pass

# Function to create enrollment on successful purchase
def create_enrollment_on_purchase(user, bootcamp):
    """Create enrollment document when user purchases a bootcamp"""
    # Check if enrollment already exists
    existing_enrollment = frappe.db.exists(
        "Enrollment",
        {
            "user": user,
            "bootcamp": bootcamp
        }
    )
    
    if existing_enrollment:
        # Enrollment already exists, return it
        return frappe.get_doc("Enrollment", existing_enrollment)
    
    # Create new enrollment
    enrollment = frappe.get_doc({
        "doctype": "Enrollment",
        "user": user,
        "bootcamp": bootcamp,
        "enrollment_date": nowdate(),
        "completion_status": "In Progress"
    })
    enrollment.insert()
    
    return enrollment

# Function to handle purchase webhook or integration
def handle_successful_purchase(user, bootcamp_item_code):
    """Handle successful purchase and create enrollment"""
    # Get bootcamp from item code
    bootcamp_name = frappe.db.get_value("LMS Bootcamp", {"item": bootcamp_item_code}, "name")
    
    if not bootcamp_name:
        frappe.throw("No bootcamp found for item code: " + bootcamp_item_code)
    
    # Create enrollment
    enrollment = create_enrollment_on_purchase(user, bootcamp_name)
    
    # Log the enrollment creation
    frappe.get_doc({
        "doctype": "Activity Log",
        "subject": "Enrollment Created",
        "content": f"Enrollment created for user {user} in bootcamp {bootcamp_name}",
        "reference_doctype": "Enrollment",
        "reference_name": enrollment.name
    }).insert(ignore_permissions=True)
    
    return enrollment