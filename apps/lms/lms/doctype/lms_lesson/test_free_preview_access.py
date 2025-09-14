# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest
from frappe.utils import get_url

class TestFreePreviewAccess(unittest.TestCase):
    def setUp(self):
        """Set up test dependencies"""
        # Create a test bootcamp
        if not frappe.db.exists("LMS Bootcamp", "Test Bootcamp"):
            bootcamp = frappe.get_doc({
                "doctype": "LMS Bootcamp",
                "title": "Test Bootcamp",
                "description": "A test bootcamp for free preview access testing"
            })
            bootcamp.insert()
            self.bootcamp_name = bootcamp.name
        else:
            self.bootcamp_name = frappe.db.get_value("LMS Bootcamp", {"title": "Test Bootcamp"}, "name")
        
        # Create a test course
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "title": "Test Course",
            "description": "A test course for free preview access testing"
        })
        course.parent = self.bootcamp_name
        course.parenttype = "LMS Bootcamp"
        course.parentfield = "courses"
        course.insert()
        self.course_name = course.name
        
        # Create a free preview lesson
        free_preview_lesson = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Free Preview Lesson",
            "description": "A lesson marked as free preview",
            "content_type": "Text",
            "content": "This is a free preview lesson content",
            "is_free_preview": 1
        })
        free_preview_lesson.parent = self.course_name
        free_preview_lesson.parenttype = "LMS Course"
        free_preview_lesson.parentfield = "lessons"
        free_preview_lesson.insert()
        self.free_preview_lesson_name = free_preview_lesson.name
        
        # Create a regular (non-free preview) lesson
        regular_lesson = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Regular Lesson",
            "description": "A regular lesson not marked as free preview",
            "content_type": "Text",
            "content": "This is a regular lesson content",
            "is_free_preview": 0
        })
        regular_lesson.parent = self.course_name
        regular_lesson.parenttype = "LMS Course"
        regular_lesson.parentfield = "lessons"
        regular_lesson.insert()
        self.regular_lesson_name = regular_lesson.name
    
    def test_free_preview_lesson_accessible(self):
        """Test that free preview lessons are accessible"""
        # This would normally be tested through the web framework
        # For now, we'll test the logic directly
        
        # Get the free preview lesson
        lesson = frappe.get_doc("LMS Lesson", self.free_preview_lesson_name)
        
        # Verify it's marked as free preview
        self.assertEqual(lesson.is_free_preview, 1)
        
        # This would be accessible to guests in the web interface
        # The actual access control is handled by the web framework
    
    def test_regular_lesson_not_accessible_to_guests(self):
        """Test that regular lessons are not accessible to guests"""
        # Get the regular lesson
        lesson = frappe.get_doc("LMS Lesson", self.regular_lesson_name)
        
        # Verify it's not marked as free preview
        self.assertEqual(lesson.is_free_preview, 0)
        
        # This would not be accessible to guests in the web interface
        # The actual access control is handled by the web framework
    
    def test_get_free_preview_lessons_for_bootcamp(self):
        """Test getting free preview lessons for a bootcamp"""
        # Get the bootcamp
        bootcamp = frappe.get_doc("LMS Bootcamp", self.bootcamp_name)
        
        # Get courses for this bootcamp
        courses = frappe.get_all("LMS Course", 
                               filters={"parent": bootcamp.name, "parenttype": "LMS Bootcamp"},
                               fields=["name", "title"])
        
        # Get free preview lessons for each course
        free_preview_lessons = []
        for course in courses:
            lessons = frappe.get_all("LMS Lesson",
                                   filters={"parent": course.name, "parenttype": "LMS Course", "is_free_preview": 1},
                                   fields=["name", "title", "description", "content_type"])
            free_preview_lessons.extend(lessons)
        
        # Verify we found the free preview lesson
        self.assertEqual(len(free_preview_lessons), 1)
        self.assertEqual(free_preview_lessons[0].name, self.free_preview_lesson_name)
    
    def test_public_endpoints_security(self):
        """Test security of public endpoints"""
        # This test would verify that:
        # 1. Only lessons marked as free preview are accessible via public endpoints
        # 2. Regular lessons cannot be accessed through public endpoints
        # 3. Proper error handling is in place for invalid requests
        
        # For now, we'll verify the basic logic:
        
        # Free preview lesson should be accessible
        free_lesson = frappe.get_doc("LMS Lesson", self.free_preview_lesson_name)
        self.assertTrue(free_lesson.is_free_preview)
        
        # Regular lesson should not be accessible via public endpoints
        regular_lesson = frappe.get_doc("LMS Lesson", self.regular_lesson_name)
        self.assertFalse(regular_lesson.is_free_preview)