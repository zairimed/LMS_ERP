# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest

class TestLMSCourse(unittest.TestCase):
    def test_course_creation(self):
        """Test creation of LMS Course"""
        # Create a new course
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "title": "Test Course",
            "description": "This is a test course"
        })
        course.insert()
        
        # Verify the course was created
        self.assertTrue(course.name)
        self.assertEqual(course.title, "Test Course")
        self.assertEqual(course.description, "This is a test course")
        
    def test_course_validation(self):
        """Test that title is required"""
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "description": "This is a test course without title"
        })
        
        # This should raise an exception because title is required
        with self.assertRaises(frappe.exceptions.ValidationError):
            course.insert()