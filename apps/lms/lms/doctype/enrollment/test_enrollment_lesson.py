# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest

class TestEnrollmentLesson(unittest.TestCase):
    def test_enrollment_lesson_creation(self):
        """Test creation of Enrollment Lesson"""
        # Create a test lesson
        if not frappe.db.exists("LMS Lesson", "Test Lesson"):
            lesson = frappe.get_doc({
                "doctype": "LMS Lesson",
                "title": "Test Lesson",
                "content_type": "Text",
                "content": "This is a test lesson"
            })
            lesson.insert()
        
        # Create a test enrollment lesson
        enrollment_lesson = frappe.get_doc({
            "doctype": "Enrollment Lesson",
            "lesson": "Test Lesson",
            "completion_date": "2025-01-01"
        })
        
        # Verify the enrollment lesson was created
        self.assertEqual(enrollment_lesson.lesson, "Test Lesson")
        self.assertEqual(enrollment_lesson.completion_date, "2025-01-01")