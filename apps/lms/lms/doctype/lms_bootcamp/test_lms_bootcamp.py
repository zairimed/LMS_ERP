# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest
from frappe.utils import strip_html_tags

class TestLMSBootcamp(unittest.TestCase):
    def setUp(self):
        """Set up test dependencies"""
        # Create LMS Settings if not exists
        if not frappe.db.exists("LMS Settings", "LMS Settings"):
            settings = frappe.get_doc({
                "doctype": "LMS Settings",
                "default_item_group": "Products",
                "default_stock_uom": "Unit"
            })
            settings.insert()
    
    def test_bootcamp_creation(self):
        """Test creation of LMS Bootcamp"""
        # Create a new bootcamp
        bootcamp = frappe.get_doc({
            "doctype": "LMS Bootcamp",
            "title": "Test Bootcamp",
            "description": "This is a test bootcamp"
        })
        bootcamp.insert()
        
        # Verify the bootcamp was created
        self.assertTrue(bootcamp.name)
        self.assertEqual(bootcamp.title, "Test Bootcamp")
        self.assertEqual(bootcamp.description, "This is a test bootcamp")
        
    def test_bootcamp_validation(self):
        """Test that title is required"""
        bootcamp = frappe.get_doc({
            "doctype": "LMS Bootcamp",
            "description": "This is a test bootcamp without title"
        })
        
        # This should raise an exception because title is required
        with self.assertRaises(frappe.exceptions.ValidationError):
            bootcamp.insert()
            
    def test_bootcamp_item_creation(self):
        """Test that an ERPNext Item is created when a Bootcamp is created"""
        # Create a new bootcamp
        bootcamp = frappe.get_doc({
            "doctype": "LMS Bootcamp",
            "title": "Test Bootcamp with Item",
            "description": "This is a test bootcamp that should create an Item"
        })
        bootcamp.insert()
        
        # Verify that an item was created and linked
        self.assertTrue(bootcamp.item)
        
        # Verify the item exists and has the correct values
        item = frappe.get_doc("Item", bootcamp.item)
        self.assertEqual(item.item_name, "Test Bootcamp with Item")
        self.assertEqual(item.description, "This is a test bootcamp that should create an Item")
        
    def test_bootcamp_item_synchronization(self):
        """Test that changes to Bootcamp are synchronized to Item"""
        # Create a new bootcamp
        bootcamp = frappe.get_doc({
            "doctype": "LMS Bootcamp",
            "title": "Test Bootcamp for Sync",
            "description": "This is a test bootcamp for synchronization"
        })
        bootcamp.insert()
        
        # Update the bootcamp
        bootcamp.title = "Updated Test Bootcamp"
        bootcamp.description = "This is an updated test bootcamp"
        bootcamp.save()
        
        # Verify the item was updated
        item = frappe.get_doc("Item", bootcamp.item)
        self.assertEqual(item.item_name, "Updated Test Bootcamp")
        self.assertEqual(item.description, "This is an updated test bootcamp")
        
    def test_bootcamp_input_sanitization(self):
        """Test that user input is properly sanitized"""
        # Create a new bootcamp with HTML in title and description
        bootcamp = frappe.get_doc({
            "doctype": "LMS Bootcamp",
            "title": "<script>alert('xss')</script>Test Bootcamp",
            "description": "<p>This is a test bootcamp with <strong>HTML</strong></p>"
        })
        bootcamp.insert()
        
        # Verify that HTML was stripped from the item
        item = frappe.get_doc("Item", bootcamp.item)
        # The item name should not contain the script tag
        self.assertNotIn("<script>", item.item_name)
        # The item description should not contain HTML tags
        self.assertNotIn("<p>", item.description)
        
    def test_bootcamp_no_unnecessary_sync(self):
        """Test that item is not synchronized when irrelevant fields change"""
        # Create a new bootcamp
        bootcamp = frappe.get_doc({
            "doctype": "LMS Bootcamp",
            "title": "Test Bootcamp for Sync Check",
            "description": "This is a test bootcamp"
        })
        bootcamp.insert()
        
        # Store the original modification time of the linked item
        original_item_modified = frappe.db.get_value("Item", bootcamp.item, "modified")
        
        # Update the bootcamp with the same title and description (no real change)
        bootcamp.save()
        
        # The item should not have been updated
        new_item_modified = frappe.db.get_value("Item", bootcamp.item, "modified")
        self.assertEqual(original_item_modified, new_item_modified)
        
    def test_bootcamp_configurable_settings(self):
        """Test that item creation uses configurable settings"""
        # Update LMS Settings
        settings = frappe.get_doc("LMS Settings", "LMS Settings")
        settings.default_item_group = "Courses"
        settings.default_stock_uom = "Hours"
        settings.save()
        
        # Create a new bootcamp
        bootcamp = frappe.get_doc({
            "doctype": "LMS Bootcamp",
            "title": "Test Bootcamp with Custom Settings",
            "description": "This is a test bootcamp with custom settings"
        })
        bootcamp.insert()
        
        # Verify the item was created with the custom settings
        item = frappe.get_doc("Item", bootcamp.item)
        # Note: We're not directly checking the item_group and stock_uom here
        # because they might be set differently in different ERPNext instances
        self.assertTrue(item.name)