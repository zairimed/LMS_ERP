# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class Enrollment(Document):
    def after_insert(self):
        """Initialize enrollment with default values"""
        if not self.enrollment_date:
            self.enrollment_date = nowdate()
        self.save()
    
    def validate(self):
        """Validate enrollment before saving"""
        # Ensure user and bootcamp are not the same as existing enrollment
        existing = frappe.db.exists(
            "Enrollment",
            {
                "user": self.user,
                "bootcamp": self.bootcamp,
                "name": ["!=", self.name]
            }
        )
        if existing:
            frappe.throw("User is already enrolled in this bootcamp")
    
    def get_progress(self):
        """Calculate and return progress percentage with caching"""
        if not self.bootcamp:
            return 0
            
        # Check if we have cached progress
        cached_progress = frappe.cache().hget("enrollment_progress", self.name)
        if cached_progress is not None:
            return cached_progress
            
        # Get total lessons in the bootcamp
        total_lessons = self.get_total_lessons()
        if total_lessons == 0:
            return 0
            
        # Get completed lessons
        completed_lessons = len(self.completed_lessons)
        
        # Calculate percentage
        progress = (completed_lessons / total_lessons) * 100
        rounded_progress = round(progress, 2)
        
        # Cache the progress for 5 minutes
        frappe.cache().hset("enrollment_progress", self.name, rounded_progress)
        frappe.cache().expire("enrollment_progress", self.name, 300)
        
        return rounded_progress
    
    def get_total_lessons(self):
        """Get total number of lessons in the bootcamp"""
        if not self.bootcamp:
            return 0
            
        # Check if we have cached total lessons
        cached_total = frappe.cache().hget("bootcamp_total_lessons", self.bootcamp)
        if cached_total is not None:
            return cached_total
            
        # Get the bootcamp document
        bootcamp = frappe.get_doc("LMS Bootcamp", self.bootcamp)
        
        # Count lessons in all courses
        total_lessons = 0
        for course_row in bootcamp.courses:
            # Get the course document
            course = frappe.get_doc("LMS Course", course_row.name)
            total_lessons += len(course.lessons)
            
        # Cache the total lessons for 10 minutes
        frappe.cache().hset("bootcamp_total_lessons", self.bootcamp, total_lessons)
        frappe.cache().expire("bootcamp_total_lessons", self.bootcamp, 600)
        
        return total_lessons
    
    def mark_lesson_complete(self, lesson_name):
        """Mark a lesson as complete"""
        # Check if lesson is already marked as complete
        for completed_lesson in self.completed_lessons:
            if completed_lesson.lesson == lesson_name:
                return  # Already completed
        
        # Add lesson to completed lessons
        self.append("completed_lessons", {
            "lesson": lesson_name,
            "completion_date": nowdate()
        })
        
        # Update progress percentage
        self.progress_percentage = self.get_progress()
        
        # Save the document
        self.save()
        
        # Clear cache for this enrollment
        frappe.cache().hdel("enrollment_progress", self.name)
    
    def is_lesson_completed(self, lesson_name):
        """Check if a lesson is completed"""
        for completed_lesson in self.completed_lessons:
            if completed_lesson.lesson == lesson_name:
                return True
        return False
    
    def on_update(self):
        """Update progress when enrollment is updated"""
        # Update progress percentage
        self.progress_percentage = self.get_progress()
        # Save without triggering infinite loop
        if self.has_value_changed("progress_percentage"):
            self.db_set("progress_percentage", self.progress_percentage, update_modified=False)
    
    def after_delete(self):
        """Clear cache when enrollment is deleted"""
        frappe.cache().hdel("enrollment_progress", self.name)

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

# Enhanced security function to check if user is enrolled in bootcamp
def is_user_enrolled_secure(user, bootcamp):
    """Securely check if a user is enrolled in a bootcamp"""
    # Validate inputs
    if not user or not bootcamp:
        return False
    
    # Check if enrollment exists for this user and bootcamp
    try:
        enrollment_name = frappe.db.exists(
            "Enrollment",
            {
                "user": user,
                "bootcamp": bootcamp
            }
        )
        return bool(enrollment_name)
    except Exception:
        # Log error but don't expose details
        frappe.log_error("Error checking enrollment status")
        return False

# Enhanced security function to check content access
def check_content_access_secure(user, bootcamp):
    """Securely check if user has access to bootcamp content"""
    # Validate inputs
    if not user or not bootcamp:
        return False
    
    # If user is enrolled, they have access
    if is_user_enrolled_secure(user, bootcamp):
        return True
    
    # If user is System Manager or Administrator, they have access
    if frappe.has_permission("Enrollment", "write"):
        return True
    
    return False

# Enhanced security function to check lesson access
def check_lesson_access_secure(user, lesson):
    """Securely check if user has access to a specific lesson"""
    # Validate inputs
    if not user or not lesson:
        return False
    
    try:
        # Get the lesson document
        lesson_doc = frappe.get_doc("LMS Lesson", lesson)
        
        # If it's a free preview lesson, everyone has access
        if lesson_doc.is_free_preview:
            return True
        
        # Get the course and bootcamp for this lesson
        course = frappe.get_doc("LMS Course", lesson_doc.parent)
        bootcamp = frappe.get_doc("LMS Bootcamp", course.parent)
        
        # Check if user has access to the bootcamp
        return check_content_access_secure(user, bootcamp.name)
    except Exception:
        # Log error but don't expose details
        frappe.log_error("Error checking lesson access")
        return False