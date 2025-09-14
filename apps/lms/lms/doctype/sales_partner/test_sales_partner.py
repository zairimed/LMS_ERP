# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest

class TestSalesPartner(unittest.TestCase):
    def setUp(self):
        """Set up test dependencies"""
        # Create a test user
        if not frappe.db.exists("User", "test-sales-partner@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-sales-partner@example.com",
                "first_name": "Test",
                "last_name": "Sales Partner",
                "send_welcome_email": 0
            })
            user.insert()
        
        # Create another test user
        if not frappe.db.exists("User", "test-sales-partner-2@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test-sales-partner-2@example.com",
                "first_name": "Test",
                "last_name": "Sales Partner 2",
                "send_welcome_email": 0
            })
            user.insert()
    
    def test_sales_partner_creation(self):
        """Test creation of Sales Partner"""
        # Create a new Sales Partner
        sales_partner = frappe.get_doc({
            "doctype": "Sales Partner",
            "sales_partner_name": "Test Sales Partner",
            "commission_rate": 10,
            "user": "test-sales-partner@example.com"
        })
        sales_partner.insert()
        
        # Verify the Sales Partner was created
        self.assertTrue(sales_partner.name)
        self.assertEqual(sales_partner.sales_partner_name, "Test Sales Partner")
        self.assertEqual(sales_partner.commission_rate, 10)
        self.assertEqual(sales_partner.user, "test-sales-partner@example.com")
    
    def test_sales_partner_validation(self):
        """Test Sales Partner validation"""
        # Create first Sales Partner
        sales_partner1 = frappe.get_doc({
            "doctype": "Sales Partner",
            "sales_partner_name": "Test Sales Partner 1",
            "commission_rate": 10,
            "user": "test-sales-partner@example.com"
        })
        sales_partner1.insert()
        
        # Try to create second Sales Partner with same user
        with self.assertRaises(frappe.exceptions.ValidationError):
            sales_partner2 = frappe.get_doc({
                "doctype": "Sales Partner",
                "sales_partner_name": "Test Sales Partner 2",
                "commission_rate": 15,
                "user": "test-sales-partner@example.com"
            })
            sales_partner2.insert()
    
    def test_user_linking(self):
        """Test linking user to Sales Partner"""
        # Create a Sales Partner with user
        sales_partner = frappe.get_doc({
            "doctype": "Sales Partner",
            "sales_partner_name": "Test User Linking",
            "commission_rate": 10,
            "user": "test-sales-partner-2@example.com"
        })
        sales_partner.insert()
        
        # Verify User Permission was created
        user_perm = frappe.db.exists(
            "User Permission",
            {
                "user": "test-sales-partner-2@example.com",
                "allow": "Sales Partner",
                "for_value": sales_partner.name
            }
        )
        self.assertTrue(user_perm)
    
    def test_user_permission_updates(self):
        """Test updating user permissions when Sales Partner is updated"""
        # Create a Sales Partner with user
        sales_partner = frappe.get_doc({
            "doctype": "Sales Partner",
            "sales_partner_name": "Test Permission Updates",
            "commission_rate": 10,
            "user": "test-sales-partner@example.com"
        })
        sales_partner.insert()
        
        # Verify initial User Permission
        user_perm = frappe.db.exists(
            "User Permission",
            {
                "user": "test-sales-partner@example.com",
                "allow": "Sales Partner",
                "for_value": sales_partner.name
            }
        )
        self.assertTrue(user_perm)
        
        # Update Sales Partner with new user
        sales_partner.user = "test-sales-partner-2@example.com"
        sales_partner.save()
        
        # Verify old User Permission was removed
        old_user_perm = frappe.db.exists(
            "User Permission",
            {
                "user": "test-sales-partner@example.com",
                "allow": "Sales Partner",
                "for_value": sales_partner.name
            }
        )
        self.assertFalse(old_user_perm)
        
        # Verify new User Permission was created
        new_user_perm = frappe.db.exists(
            "User Permission",
            {
                "user": "test-sales-partner-2@example.com",
                "allow": "Sales Partner",
                "for_value": sales_partner.name
            }
        )
        self.assertTrue(new_user_perm)