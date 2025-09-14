# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest
from frappe.utils import nowdate

class TestEnrollmentComprehensive(unittest.TestCase):
    def setUp(self):
        """Set up comprehensive test dependencies"""
        # Create a test user
        if not frappe.db.exists("User", "test-student-comprehensive@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-student-comprehensive@example.com",
                "first_name": "Test",
                "last_name": "Student Comprehensive",
                "send_welcome_email": 0
            })
            user.insert()
        
        # Create a test bootcamp with courses and lessons
        if not frappe.db.exists("LMS Bootcamp", "Test Comprehensive Bootcamp"):
            bootcamp = frappe.get_doc({
                "doctype": "LMS Bootcamp",
                "title": "Test Comprehensive Bootcamp",
                "description": "A comprehensive test bootcamp"
            })
            bootcamp.insert()
            
            # Create a test course
            course = frappe.get_doc({
                "doctype": "LMS Course",
                "title": "Test Comprehensive Course",
                "description": "A comprehensive test course"
            })
            course.parent = "Test Comprehensive Bootcamp"
            course.parenttype = "LMS Bootcamp"
            course.parentfield = "courses"
            course.insert()
            
            # Create test lessons
            lesson1 = frappe.get_doc({
                "doctype": "LMS Lesson",
                "title": "Test Lesson 1",
                "content_type": "Text",
                "content": "This is test lesson 1"
            })
            lesson1.parent = course.name
            lesson1.parenttype = "LMS Course"
            lesson1.parentfield = "lessons"
            lesson1.insert()
            
            lesson2 = frappe.get_doc({
                "doctype": "LMS Lesson",
                "title": "Test Lesson 2",
                "content_type": "Video",
                "video_url": "https://example.com/video2.mp4"
            })
            lesson2.parent = course.name
            lesson2.parenttype = "LMS Course"
            lesson2.parentfield = "lessons"
            lesson2.insert()
    
    def test_enrollment_full_lifecycle(self):
        """Test full enrollment lifecycle"""
        # Create enrollment
        enrollment = frappe.get_doc({
            "doctype": "Enrollment",
            "user": "test-student-comprehensive@example.com",
            "bootcamp": "Test Comprehensive Bootcamp"
        })
        enrollment.insert()
        
        # Verify initial state
        self.assertEqual(enrollment.completion_status, "In Progress")
        self.assertEqual(enrollment.get_progress(), 0)
        self.assertEqual(len(enrollment.completed_lessons), 0)
        
        # Get total lessons
        total_lessons = enrollment.get_total_lessons()
        self.assertEqual(total_lessons, 2)
        
        # Mark first lesson complete
        enrollment.mark_lesson_complete("Test Lesson 1")
        
        # Verify progress updated
        self.assertEqual(len(enrollment.completed_lessons), 1)
        self.assertEqual(enrollment.get_progress(), 50.0)
        
        # Mark second lesson complete
        enrollment.mark_lesson_complete("Test Lesson 2")
        
        # Verify completion
        self.assertEqual(len(enrollment.completed_lessons), 2)
        self.assertEqual(enrollment.get_progress(), 100.0)
        
        # Test duplicate completion
        initial_count = len(enrollment.completed_lessons)
        enrollment.mark_lesson_complete("Test Lesson 1")  # Try to complete again
        self.assertEqual(len(enrollment.completed_lessons), initial_count)  # Should not change
        
        # Test is_lesson_completed
        self.assertTrue(enrollment.is_lesson_completed("Test Lesson 1"))
        self.assertTrue(enrollment.is_lesson_completed("Test Lesson 2"))
        self.assertFalse(enrollment.is_lesson_completed("Non-existent Lesson"))