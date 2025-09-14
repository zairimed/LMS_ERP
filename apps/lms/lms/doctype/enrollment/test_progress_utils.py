# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest
from frappe.utils import nowdate

class TestProgressUtils(unittest.TestCase):
    def setUp(self):
        """Set up test dependencies"""
        # Create a test user
        if not frappe.db.exists("User", "test-student2@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-student2@example.com",
                "first_name": "Test",
                "last_name": "Student2",
                "send_welcome_email": 0
            })
            user.insert()
        
        # Create a test bootcamp
        if not frappe.db.exists("LMS Bootcamp", "Test Bootcamp 2"):
            bootcamp = frappe.get_doc({
                "doctype": "LMS Bootcamp",
                "title": "Test Bootcamp 2",
                "description": "A test bootcamp for progress utils testing"
            })
            bootcamp.insert()
        
        # Create a test course
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "title": "Test Course",
            "description": "A test course"
        })
        course.parent = "Test Bootcamp 2"
        course.parenttype = "LMS Bootcamp"
        course.parentfield = "courses"
        course.insert()
        
        # Create a test video lesson
        video_lesson = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Test Video Lesson",
            "content_type": "Video",
            "video_url": "https://example.com/video.mp4"
        })
        video_lesson.parent = course.name
        video_lesson.parenttype = "LMS Course"
        video_lesson.parentfield = "lessons"
        video_lesson.insert()
        
        # Create a test text lesson
        text_lesson = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Test Text Lesson",
            "content_type": "Text",
            "content": "This is a test text lesson"
        })
        text_lesson.parent = course.name
        text_lesson.parenttype = "LMS Course"
        text_lesson.parentfield = "lessons"
        text_lesson.insert()
    
    def test_mark_lesson_completed(self):
        """Test marking a lesson as completed"""
        from .progress_utils import mark_lesson_as_completed
        
        # Mark a lesson as completed
        mark_lesson_as_completed(
            "test-student2@example.com",
            "Test Bootcamp 2",
            "Test Video Lesson"
        )
        
        # Verify enrollment was created
        enrollment_name = frappe.db.exists(
            "Enrollment",
            {
                "user": "test-student2@example.com",
                "bootcamp": "Test Bootcamp 2"
            }
        )
        self.assertTrue(enrollment_name)
        
        # Verify lesson was marked as completed
        enrollment = frappe.get_doc("Enrollment", enrollment_name)
        self.assertTrue(enrollment.is_lesson_completed("Test Video Lesson"))
    
    def test_auto_mark_video_lesson(self):
        """Test automatically marking video lesson as completed"""
        from .progress_utils import auto_mark_video_lesson_completed
        
        # Auto mark video lesson
        result = auto_mark_video_lesson_completed(
            "test-student2@example.com",
            "Test Bootcamp 2",
            "Test Video Lesson"
        )
        
        # Should return True for video lesson
        self.assertTrue(result)
        
        # Verify lesson was marked as completed
        enrollment_name = frappe.db.exists(
            "Enrollment",
            {
                "user": "test-student2@example.com",
                "bootcamp": "Test Bootcamp 2"
            }
        )
        enrollment = frappe.get_doc("Enrollment", enrollment_name)
        self.assertTrue(enrollment.is_lesson_completed("Test Video Lesson"))
    
    def test_get_user_progress(self):
        """Test getting user progress"""
        from .progress_utils import mark_lesson_as_completed, get_user_progress
        
        # Mark one lesson as completed
        mark_lesson_as_completed(
            "test-student2@example.com",
            "Test Bootcamp 2",
            "Test Video Lesson"
        )
        
        # Get user progress
        progress = get_user_progress("test-student2@example.com", "Test Bootcamp 2")
        
        # Should be 50% (1 out of 2 lessons completed)
        self.assertEqual(progress, 50.0)