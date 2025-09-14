# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest
from frappe.utils import nowdate

class TestAccessControl(unittest.TestCase):
    def setUp(self):
        """Set up test dependencies"""
        # Create a test user
        if not frappe.db.exists("User", "test-access-user@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-access-user@example.com",
                "first_name": "Test",
                "last_name": "Access User",
                "send_welcome_email": 0
            })
            user.insert()
        
        # Create another test user (not enrolled)
        if not frappe.db.exists("User", "test-unenrolled-user@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-unenrolled-user@example.com",
                "first_name": "Test",
                "last_name": "Unenrolled User",
                "send_welcome_email": 0
            })
            user.insert()
        
        # Create a test bootcamp
        if not frappe.db.exists("LMS Bootcamp", "Test Access Bootcamp"):
            bootcamp = frappe.get_doc({
                "doctype": "LMS Bootcamp",
                "title": "Test Access Bootcamp",
                "description": "A test bootcamp for access control testing"
            })
            bootcamp.insert()
        
        # Create a test course
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "title": "Test Access Course",
            "description": "A test course for access control testing"
        })
        course.parent = "Test Access Bootcamp"
        course.parenttype = "LMS Bootcamp"
        course.parentfield = "courses"
        course.insert()
        
        # Create a test lesson
        lesson = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Test Access Lesson",
            "content_type": "Text",
            "content": "This is a test lesson for access control"
        })
        lesson.parent = course.name
        lesson.parenttype = "LMS Course"
        lesson.parentfield = "lessons"
        lesson.insert()
        
        # Create a free preview lesson
        free_preview_lesson = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Test Free Preview Lesson",
            "content_type": "Text",
            "content": "This is a free preview lesson",
            "is_free_preview": 1
        })
        free_preview_lesson.parent = course.name
        free_preview_lesson.parenttype = "LMS Course"
        free_preview_lesson.parentfield = "lessons"
        free_preview_lesson.insert()
        
        # Create an enrollment for the first user
        if not frappe.db.exists(
            "Enrollment",
            {
                "user": "test-access-user@example.com",
                "bootcamp": "Test Access Bootcamp"
            }
        ):
            enrollment = frappe.get_doc({
                "doctype": "Enrollment",
                "user": "test-access-user@example.com",
                "bootcamp": "Test Access Bootcamp"
            })
            enrollment.insert()
    
    def test_user_enrollment_check(self):
        """Test checking if user is enrolled in a bootcamp"""
        from .access_control import is_user_enrolled
        
        # Test enrolled user
        self.assertTrue(is_user_enrolled("test-access-user@example.com", "Test Access Bootcamp"))
        
        # Test unenrolled user
        self.assertFalse(is_user_enrolled("test-unenrolled-user@example.com", "Test Access Bootcamp"))
    
    def test_content_access_check(self):
        """Test checking content access"""
        from .access_control import check_content_access
        
        # Test enrolled user has access
        self.assertTrue(check_content_access("test-access-user@example.com", "Test Access Bootcamp"))
        
        # Test unenrolled user doesn't have access
        self.assertFalse(check_content_access("test-unenrolled-user@example.com", "Test Access Bootcamp"))
    
    def test_lesson_access_check(self):
        """Test checking lesson access"""
        from .access_control import check_lesson_access
        
        # Get lesson names
        lesson_name = frappe.db.get_value("LMS Lesson", {"title": "Test Access Lesson"}, "name")
        free_preview_lesson_name = frappe.db.get_value("LMS Lesson", {"title": "Test Free Preview Lesson"}, "name")
        
        # Test enrolled user can access regular lesson
        self.assertTrue(check_lesson_access("test-access-user@example.com", lesson_name))
        
        # Test unenrolled user cannot access regular lesson
        self.assertFalse(check_lesson_access("test-unenrolled-user@example.com", lesson_name))
        
        # Test anyone can access free preview lesson
        self.assertTrue(check_lesson_access("test-access-user@example.com", free_preview_lesson_name))
        self.assertTrue(check_lesson_access("test-unenrolled-user@example.com", free_preview_lesson_name))
    
    def test_get_enrolled_bootcamps(self):
        """Test getting enrolled bootcamps for a user"""
        from .access_control import get_enrolled_bootcamps
        
        # Test enrolled user has bootcamps
        bootcamps = get_enrolled_bootcamps("test-access-user@example.com")
        self.assertEqual(len(bootcamps), 1)
        self.assertEqual(bootcamps[0].title, "Test Access Bootcamp")
        
        # Test unenrolled user has no bootcamps
        bootcamps = get_enrolled_bootcamps("test-unenrolled-user@example.com")
        self.assertEqual(len(bootcamps), 0)