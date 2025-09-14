# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest
from frappe.utils import nowdate

class TestContentContext(unittest.TestCase):
    def setUp(self):
        """Set up test dependencies"""
        # Create a test user
        if not frappe.db.exists("User", "test-context-user2@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-context-user2@example.com",
                "first_name": "Test",
                "last_name": "Context User 2",
                "send_welcome_email": 0
            })
            user.insert()
        
        # Create another test user (not enrolled)
        if not frappe.db.exists("User", "test-unenrolled-user2@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-unenrolled-user2@example.com",
                "first_name": "Test",
                "last_name": "Unenrolled User 2",
                "send_welcome_email": 0
            })
            user.insert()
        
        # Create a test bootcamp
        if not frappe.db.exists("LMS Bootcamp", "Test Content Context Bootcamp"):
            bootcamp = frappe.get_doc({
                "doctype": "LMS Bootcamp",
                "title": "Test Content Context Bootcamp",
                "description": "A test bootcamp for content context testing"
            })
            bootcamp.insert()
        
        # Create a test course
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "title": "Test Content Context Course",
            "description": "A test course for content context testing"
        })
        course.parent = "Test Content Context Bootcamp"
        course.parenttype = "LMS Bootcamp"
        course.parentfield = "courses"
        course.insert()
        
        # Create test lessons
        lesson1 = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Content Context Lesson 1",
            "content_type": "Text",
            "content": "This is content context lesson 1"
        })
        lesson1.parent = course.name
        lesson1.parenttype = "LMS Course"
        lesson1.parentfield = "lessons"
        lesson1.insert()
        
        lesson2 = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Content Context Lesson 2",
            "content_type": "Video",
            "video_url": "https://example.com/video-context2.mp4"
        })
        lesson2.parent = course.name
        lesson2.parenttype = "LMS Course"
        lesson2.parentfield = "lessons"
        lesson2.insert()
        
        # Create an enrollment for the first user
        if not frappe.db.exists(
            "Enrollment",
            {
                "user": "test-context-user2@example.com",
                "bootcamp": "Test Content Context Bootcamp"
            }
        ):
            enrollment = frappe.get_doc({
                "doctype": "Enrollment",
                "user": "test-context-user2@example.com",
                "bootcamp": "Test Content Context Bootcamp"
            })
            enrollment.insert()
    
    def test_my_bootcamps_context(self):
        """Test my bootcamps context generation"""
        from .content_context import get_my_bootcamps_context
        
        # Test with enrolled user
        frappe.set_user("test-context-user2@example.com")
        context = get_my_bootcamps_context()
        self.assertIn("bootcamps", context)
        self.assertEqual(len(context["bootcamps"]), 1)
        self.assertEqual(context["bootcamps"][0].title, "Test Content Context Bootcamp")
        
        # Test with unenrolled user
        frappe.set_user("test-unenrolled-user2@example.com")
        context = get_my_bootcamps_context()
        self.assertIn("bootcamps", context)
        self.assertEqual(len(context["bootcamps"]), 0)
        
        # Reset user
        frappe.set_user("Administrator")
    
    def test_bootcamp_content_context(self):
        """Test bootcamp content context generation"""
        from .content_context import get_bootcamp_content_context
        
        # Test with enrolled user
        frappe.set_user("test-context-user2@example.com")
        context = get_bootcamp_content_context("Test Content Context Bootcamp")
        self.assertIn("bootcamp", context)
        self.assertIn("progress", context)
        self.assertIn("courses", context)
        self.assertEqual(context["bootcamp"].title, "Test Content Context Bootcamp")
        self.assertEqual(len(context["courses"]), 1)
        self.assertEqual(len(context["courses"][0]["lessons"]), 2)
        
        # Test with unenrolled user (should raise permission error)
        frappe.set_user("test-unenrolled-user2@example.com")
        with self.assertRaises(frappe.PermissionError):
            get_bootcamp_content_context("Test Content Context Bootcamp")
        
        # Reset user
        frappe.set_user("Administrator")
    
    def test_lesson_content_context(self):
        """Test lesson content context generation"""
        from .content_context import get_lesson_content_context
        
        # Get lesson name
        lesson_name = frappe.db.get_value("LMS Lesson", {"title": "Content Context Lesson 1"}, "name")
        free_preview_lesson_name = frappe.db.get_value("LMS Lesson", {"title": "Free Preview Lesson"}, "name")
        
        # Test with enrolled user
        frappe.set_user("test-context-user2@example.com")
        context = get_lesson_content_context(lesson_name)
        self.assertIn("lesson", context)
        self.assertIn("course", context)
        self.assertIn("bootcamp", context)
        self.assertEqual(context["lesson"].title, "Content Context Lesson 1")
        
        # Test with unenrolled user (should raise permission error for non-free preview)
        frappe.set_user("test-unenrolled-user2@example.com")
        with self.assertRaises(frappe.PermissionError):
            get_lesson_content_context(lesson_name)
        
        # Reset user
        frappe.set_user("Administrator")