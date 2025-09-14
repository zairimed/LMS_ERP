# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest

class TestLMSLesson(unittest.TestCase):
    def test_lesson_creation(self):
        """Test creation of LMS Lesson"""
        # Create a new lesson
        lesson = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Test Lesson",
            "description": "This is a test lesson",
            "content_type": "Text",
            "content": "This is the lesson content"
        })
        lesson.insert()
        
        # Verify the lesson was created
        self.assertTrue(lesson.name)
        self.assertEqual(lesson.title, "Test Lesson")
        self.assertEqual(lesson.description, "This is a test lesson")
        self.assertEqual(lesson.content_type, "Text")
        self.assertEqual(lesson.content, "This is the lesson content")
        
    def test_lesson_validation(self):
        """Test that title and content_type are required"""
        lesson = frappe.get_doc({
            "doctype": "LMS Lesson",
            "description": "This is a test lesson without title"
        })
        
        # This should raise an exception because title is required
        with self.assertRaises(frappe.exceptions.ValidationError):
            lesson.insert()
            
    def test_lesson_free_preview(self):
        """Test that is_free_preview field works correctly"""
        # Create a new lesson with free preview enabled
        lesson = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Test Free Preview Lesson",
            "description": "This is a test lesson with free preview",
            "content_type": "Text",
            "content": "This is the lesson content",
            "is_free_preview": 1
        })
        lesson.insert()
        
        # Verify the lesson was created with free preview enabled
        self.assertTrue(lesson.name)
        self.assertEqual(lesson.is_free_preview, 1)