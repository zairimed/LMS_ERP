# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest

class TestEnrollment(unittest.TestCase):
    def setUp(self):
        """Set up test dependencies"""
        # Create a test user
        if not frappe.db.exists("User", "test-student@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-student@example.com",
                "first_name": "Test",
                "last_name": "Student",
                "send_welcome_email": 0
            })
            user.insert()
        
        # Create a test bootcamp
        if not frappe.db.exists("LMS Bootcamp", "Test Bootcamp"):
            bootcamp = frappe.get_doc({
                "doctype": "LMS Bootcamp",
                "title": "Test Bootcamp",
                "description": "A test bootcamp for enrollment testing"
            })
            bootcamp.insert()
    
    def test_enrollment_creation(self):
        """Test creation of Enrollment"""
        # Create a new enrollment
        enrollment = frappe.get_doc({
            "doctype": "Enrollment",
            "user": "test-student@example.com",
            "bootcamp": "Test Bootcamp"
        })
        enrollment.insert()
        
        # Verify the enrollment was created
        self.assertTrue(enrollment.name)
        self.assertEqual(enrollment.user, "test-student@example.com")
        self.assertEqual(enrollment.bootcamp, "Test Bootcamp")
        self.assertEqual(enrollment.completion_status, "In Progress")
    
    def test_enrollment_validation(self):
        """Test that duplicate enrollments are not allowed"""
        # Create first enrollment
        enrollment1 = frappe.get_doc({
            "doctype": "Enrollment",
            "user": "test-student@example.com",
            "bootcamp": "Test Bootcamp"
        })
        enrollment1.insert()
        
        # Try to create duplicate enrollment
        with self.assertRaises(frappe.exceptions.ValidationError):
            enrollment2 = frappe.get_doc({
                "doctype": "Enrollment",
                "user": "test-student@example.com",
                "bootcamp": "Test Bootcamp"
            })
            enrollment2.insert()
    
    def test_progress_calculation(self):
        """Test progress calculation"""
        # Create an enrollment
        enrollment = frappe.get_doc({
            "doctype": "Enrollment",
            "user": "test-student@example.com",
            "bootcamp": "Test Bootcamp"
        })
        enrollment.insert()
        
        # Test initial progress is 0
        self.assertEqual(enrollment.get_progress(), 0)