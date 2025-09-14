# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PricingRule(Document):
    def validate(self):
        """Validate Pricing Rule before saving"""
        # Ensure sales partner is valid if specified
        if self.sales_partner:
            if not frappe.db.exists("Sales Partner", self.sales_partner):
                frappe.throw("Invalid Sales Partner specified")
    
    def after_insert(self):
        """Actions after inserting Pricing Rule"""
        # Log creation of promo code
        if self.sales_partner:
            self.log_promo_code_creation()
    
    def on_update(self):
        """Actions when Pricing Rule is updated"""
        # Log updates to promo code
        if self.sales_partner:
            self.log_promo_code_update()
    
    def log_promo_code_creation(self):
        """Log the creation of a promo code"""
        # Create a log entry for promo code creation
        log_entry = frappe.get_doc({
            "doctype": "Activity Log",
            "subject": "Promo Code Created",
            "content": f"Promo code {self.name} created for Sales Partner {self.sales_partner}",
            "reference_doctype": "Pricing Rule",
            "reference_name": self.name
        })
        log_entry.insert(ignore_permissions=True)
    
    def log_promo_code_update(self):
        """Log updates to a promo code"""
        # Create a log entry for promo code update
        log_entry = frappe.get_doc({
            "doctype": "Activity Log",
            "subject": "Promo Code Updated",
            "content": f"Promo code {self.name} updated for Sales Partner {self.sales_partner}",
            "reference_doctype": "Pricing Rule",
            "reference_name": self.name
        })
        log_entry.insert(ignore_permissions=True)

# Function to get promo codes for a sales partner
def get_promo_codes_for_sales_partner(sales_partner):
    """Get all promo codes linked to a sales partner"""
    # Add index hint for better performance with large datasets
    return frappe.get_all(
        "Pricing Rule",
        filters={"sales_partner": sales_partner},
        fields=["name", "title", "selling", "applicable_for", "valid_from", "valid_upto"],
        order_by="creation desc"
    )

# Function to validate promo code usage
def validate_promo_code_usage(promo_code, sales_partner):
    """Validate that a promo code is being used by the correct sales partner"""
    pricing_rule = frappe.get_doc("Pricing Rule", promo_code)
    
    # Check if sales partner matches
    if pricing_rule.sales_partner != sales_partner:
        frappe.throw("Promo code is not valid for this Sales Partner")
    
    # Check if promo code is within validity period
    from frappe.utils import getdate, nowdate
    today = getdate(nowdate())
    
    if pricing_rule.valid_from and today < pricing_rule.valid_from:
        frappe.throw("Promo code is not yet valid")
    
    if pricing_rule.valid_upto and today > pricing_rule.valid_upto:
        frappe.throw("Promo code has expired")
    
    return True

# Function to get sales partner from promo code
def get_sales_partner_from_promo_code(promo_code):
    """Get the sales partner linked to a promo code"""
    pricing_rule = frappe.get_doc("Pricing Rule", promo_code)
    return pricing_rule.sales_partner

# Function to get promo code statistics for a sales partner
def get_promo_code_statistics(sales_partner):
    """Get statistics for promo codes of a sales partner"""
    # Use frappe.db.sql for better performance with aggregate functions
    query = """
        SELECT 
            COUNT(*) as total_promo_codes,
            COUNT(CASE WHEN valid_upto >= CURDATE() OR valid_upto IS NULL THEN 1 END) as active_promo_codes,
            COUNT(CASE WHEN valid_upto < CURDATE() THEN 1 END) as expired_promo_codes
        FROM `tabPricing Rule`
        WHERE sales_partner = %s
    """
    
    result = frappe.db.sql(query, (sales_partner,), as_dict=True)
    return result[0] if result else {}

# Enhanced security function to check promo code access
def check_promo_code_access(promo_code, user):
    """Check if a user has access to a promo code"""
    # Get the pricing rule
    pricing_rule = frappe.get_doc("Pricing Rule", promo_code)
    
    # Check if user is System Manager or Administrator
    if frappe.has_permission("Pricing Rule", "write"):
        return True
    
    # Check if user is linked to the sales partner
    if pricing_rule.sales_partner:
        sales_partner = frappe.get_doc("Sales Partner", pricing_rule.sales_partner)
        if sales_partner.user and sales_partner.user == user:
            return True
    
    return False

# Enhanced security function to get accessible promo codes for user
def get_accessible_promo_codes_for_user(user):
    """Get all promo codes accessible to a user"""
    # System Managers and Administrators can access all promo codes
    if frappe.has_permission("Pricing Rule", "write"):
        return frappe.get_all("Pricing Rule", fields=["name", "title", "selling", "applicable_for", "valid_from", "valid_upto"])
    
    # Regular users can only access promo codes linked to their Sales Partner
    # Get the Sales Partner linked to the user
    sales_partner = frappe.db.exists("Sales Partner", {"user": user})
    
    if sales_partner:
        return frappe.get_all(
            "Pricing Rule",
            filters={"sales_partner": sales_partner},
            fields=["name", "title", "selling", "applicable_for", "valid_from", "valid_upto"]
        )
    
    # User is not linked to any Sales Partner
    return []