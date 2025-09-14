# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest
from frappe.utils import nowdate

class TestTemplateContext(unittest.TestCase):
    def setUp(self):
        """Set up test dependencies for template context"""
        # Create a test user
        if not frappe.db.exists("User", "test-context-user@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-context-user@example.com",
                "first_name": "Test",
                "last_name": "Context User",
                "send_welcome_email": 0
            })
            user.insert()
        
        # Create a test bootcamp with courses and lessons
        if not frappe.db.exists("LMS Bootcamp", "Test Context Bootcamp"):
            bootcamp = frappe.get_doc({
                "doctype": "LMS Bootcamp",
                "title": "Test Context Bootcamp",
                "description": "A test bootcamp for context testing"
            })
            bootcamp.insert()
            
            # Create a test course
            course = frappe.get_doc({
                "doctype": "LMS Course",
                "title": "Test Context Course",
                "description": "A test course for context testing"
            })
            course.parent = "Test Context Bootcamp"
            course.parenttype = "LMS Bootcamp"
            course.parentfield = "courses"
            course.insert()
            
            # Create test lessons
            lesson1 = frappe.get_doc({
                "doctype": "LMS Lesson",
                "title": "Context Lesson 1",
                "content_type": "Text",
                "content": "This is context lesson 1"
            })
            lesson1.parent = course.name
            lesson1.parenttype = "LMS Course"
            lesson1.parentfield = "lessons"
            lesson1.insert()
            
            lesson2 = frappe.get_doc({
                "doctype": "LMS Lesson",
                "title": "Context Lesson 2",
                "content_type": "Video",
                "video_url": "https://example.com/video-context.mp4",
                "is_free_preview": 1
            })
            lesson2.parent = course.name
            lesson2.parenttype = "LMS Course"
            lesson2.parentfield = "lessons"
            lesson2.insert()
    
    def test_bootcamp_progress_context(self):
        """Test bootcamp progress context generation"""
        from ..templates.bootcamp_progress_context import get_bootcamp_progress_context, get_total_lessons_in_bootcamp
        
        # Test total lessons calculation
        total_lessons = get_total_lessons_in_bootcamp("Test Context Bootcamp")
        self.assertEqual(total_lessons, 2)
        
        # Test context without enrollment
        context = get_bootcamp_progress_context("Test Context Bootcamp", "test-context-user@example.com")
        
        # Verify context structure
        self.assertIn("bootcamp", context)
        self.assertIn("progress", context)
        self.assertIn("completed_lessons", context)
        self.assertIn("total_lessons", context)
        self.assertIn("remaining_lessons", context)
        self.assertIn("courses", context)
        self.assertIn("next_lesson", context)
        
        # Verify values without enrollment
        self.assertEqual(context["progress"], 0)
        self.assertEqual(context["completed_lessons"], 0)
        self.assertEqual(context["total_lessons"], 2)
        self.assertEqual(context["remaining_lessons"], 2)
        
        # Verify courses structure
        self.assertEqual(len(context["courses"]), 1)
        course = context["courses"][0]
        self.assertEqual(course["title"], "Test Context Course")
        self.assertEqual(len(course["lessons"]), 2)
        
        # Verify lessons structure
        lesson1 = course["lessons"][0]
        lesson2 = course["lessons"][1]
        self.assertEqual(lesson1["title"], "Context Lesson 1")
        self.assertEqual(lesson2["title"], "Context Lesson 2")
        self.assertFalse(lesson1["is_completed"])
        self.assertFalse(lesson2["is_completed"])
        self.assertTrue(lesson2["is_free_preview"])
        
        # Test next lesson (should be the first one)
        self.assertIsNotNone(context["next_lesson"])
        self.assertEqual(context["next_lesson"]["title"], "Context Lesson 1")