# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest
from frappe.utils import nowdate

class TestEnrollmentIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test dependencies"""
        # Create a test user
        if not frappe.db.exists("User", "test-purchase-user@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-purchase-user@example.com",
                "first_name": "Test",
                "last_name": "Purchase User",
                "send_welcome_email": 0
            })
            user.insert()
        
        # Create a test bootcamp with item
        if not frappe.db.exists("LMS Bootcamp", "Test Purchase Bootcamp"):
            # First create item
            if not frappe.db.exists("Item", "Test Purchase Item"):
                item = frappe.get_doc({
                    "doctype": "Item",
                    "item_code": "TEST-PURCHASE-ITEM",
                    "item_name": "Test Purchase Item",
                    "item_group": "Products",
                    "is_sales_item": 1,
                    "stock_uom": "Unit"
                })
                item.insert()
            
            bootcamp = frappe.get_doc({
                "doctype": "LMS Bootcamp",
                "title": "Test Purchase Bootcamp",
                "description": "A test bootcamp for purchase integration testing",
                "item": "TEST-PURCHASE-ITEM"
            })
            bootcamp.insert()
    
    def test_create_enrollment_on_purchase(self):
        """Test creating enrollment on purchase"""
        from .enrollment import create_enrollment_on_purchase
        
        # Create enrollment
        enrollment = create_enrollment_on_purchase("test-purchase-user@example.com", "Test Purchase Bootcamp")
        
        # Verify enrollment was created
        self.assertTrue(enrollment.name)
        self.assertEqual(enrollment.user, "test-purchase-user@example.com")
        self.assertEqual(enrollment.bootcamp, "Test Purchase Bootcamp")
        self.assertEqual(enrollment.completion_status, "In Progress")
        
        # Test duplicate enrollment creation
        enrollment2 = create_enrollment_on_purchase("test-purchase-user@example.com", "Test Purchase Bootcamp")
        
        # Should return the same enrollment
        self.assertEqual(enrollment.name, enrollment2.name)
    
    def test_handle_successful_purchase(self):
        """Test handling successful purchase"""
        from .enrollment_lesson import handle_successful_purchase
        
        # Handle purchase
        enrollment = handle_successful_purchase("test-purchase-user@example.com", "TEST-PURCHASE-ITEM")
        
        # Verify enrollment was created
        self.assertTrue(enrollment.name)
        self.assertEqual(enrollment.user, "test-purchase-user@example.com")
        self.assertEqual(enrollment.bootcamp, "Test Purchase Bootcamp")
        
        # Verify activity log was created
        activity_log = frappe.get_all(
            "Activity Log",
            filters={
                "reference_doctype": "Enrollment",
                "reference_name": enrollment.name
            }
        )
        self.assertTrue(activity_log)