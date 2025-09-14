# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
import unittest
from frappe.utils import nowdate, add_days

class TestPricingRule(unittest.TestCase):
    def setUp(self):
        """Set up test dependencies"""
        # Create a test sales partner
        if not frappe.db.exists("Sales Partner", "Test Promo Code Partner"):
            sales_partner = frappe.get_doc({
                "doctype": "Sales Partner",
                "sales_partner_name": "Test Promo Code Partner",
                "commission_rate": 10
            })
            sales_partner.insert()
        
        # Create another test sales partner
        if not frappe.db.exists("Sales Partner", "Test Promo Code Partner 2"):
            sales_partner = frappe.get_doc({
                "doctype": "Sales Partner",
                "sales_partner_name": "Test Promo Code Partner 2",
                "commission_rate": 15
            })
            sales_partner.insert()
    
    def test_pricing_rule_creation_with_sales_partner(self):
        """Test creation of Pricing Rule with Sales Partner link"""
        # Create a new Pricing Rule with Sales Partner
        pricing_rule = frappe.get_doc({
            "doctype": "Pricing Rule",
            "title": "Test Promo Code",
            "selling": 1,
            "apply_on": "Item Code",
            "items": [{
                "item_code": "Test Bootcamp Item"
            }],
            "price_or_discount": "Discount Percentage",
            "discount_percentage": 10,
            "sales_partner": "Test Promo Code Partner"
        })
        pricing_rule.insert()
        
        # Verify the Pricing Rule was created
        self.assertTrue(pricing_rule.name)
        self.assertEqual(pricing_rule.title, "Test Promo Code")
        self.assertEqual(pricing_rule.sales_partner, "Test Promo Code Partner")
    
    def test_pricing_rule_validation(self):
        """Test Pricing Rule validation"""
        # Try to create Pricing Rule with invalid Sales Partner
        with self.assertRaises(frappe.exceptions.ValidationError):
            pricing_rule = frappe.get_doc({
                "doctype": "Pricing Rule",
                "title": "Test Invalid Promo Code",
                "selling": 1,
                "apply_on": "Item Code",
                "items": [{
                    "item_code": "Test Bootcamp Item"
                }],
                "price_or_discount": "Discount Percentage",
                "discount_percentage": 10,
                "sales_partner": "Non-existent Sales Partner"
            })
            pricing_rule.insert()
    
    def test_get_promo_codes_for_sales_partner(self):
        """Test getting promo codes for a sales partner"""
        from .pricing_rule import get_promo_codes_for_sales_partner
        
        # Create a Pricing Rule with Sales Partner
        pricing_rule = frappe.get_doc({
            "doctype": "Pricing Rule",
            "title": "Test Sales Partner Promo Code",
            "selling": 1,
            "apply_on": "Item Code",
            "items": [{
                "item_code": "Test Bootcamp Item"
            }],
            "price_or_discount": "Discount Percentage",
            "discount_percentage": 10,
            "sales_partner": "Test Promo Code Partner"
        })
        pricing_rule.insert()
        
        # Get promo codes for the sales partner
        promo_codes = get_promo_codes_for_sales_partner("Test Promo Code Partner")
        
        # Verify we got the promo code
        self.assertTrue(len(promo_codes) > 0)
        found = False
        for promo_code in promo_codes:
            if promo_code.name == pricing_rule.name:
                found = True
                break
        self.assertTrue(found)
    
    def test_promo_code_usage_validation(self):
        """Test validating promo code usage"""
        from .pricing_rule import validate_promo_code_usage
        
        # Create a Pricing Rule with Sales Partner and validity dates
        pricing_rule = frappe.get_doc({
            "doctype": "Pricing Rule",
            "title": "Test Validity Promo Code",
            "selling": 1,
            "apply_on": "Item Code",
            "items": [{
                "item_code": "Test Bootcamp Item"
            }],
            "price_or_discount": "Discount Percentage",
            "discount_percentage": 10,
            "sales_partner": "Test Promo Code Partner",
            "valid_from": add_days(nowdate(), -1),  # Yesterday
            "valid_upto": add_days(nowdate(), 30)   # 30 days from now
        })
        pricing_rule.insert()
        
        # Validate promo code usage - should pass
        self.assertTrue(validate_promo_code_usage(pricing_rule.name, "Test Promo Code Partner"))
        
        # Try to validate with wrong sales partner - should fail
        with self.assertRaises(frappe.exceptions.ValidationError):
            validate_promo_code_usage(pricing_rule.name, "Test Promo Code Partner 2")