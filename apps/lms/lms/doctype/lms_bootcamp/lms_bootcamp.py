# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import sanitize_html, strip_html_tags

class LMSBootcamp(Document):
    def after_insert(self):
        """Create an ERPNext Item when a Bootcamp is created"""
        self.create_linked_item()
    
    def on_update(self):
        """Synchronize fields between Bootcamp and Item"""
        # Only synchronize if relevant fields have changed
        if self.has_value_changed("title") or self.has_value_changed("description"):
            if self.item:
                self.update_linked_item()
    
    def create_linked_item(self):
        """Create an ERPNext Item linked to this Bootcamp"""
        if not self.item:
            # Sanitize inputs before creating item
            sanitized_title = self.sanitize_input(self.title)
            sanitized_description = self.sanitize_input(self.description or "")
            
            # Get configurable values from settings or use defaults
            item_group = frappe.db.get_single_value("LMS Settings", "default_item_group") or "Products"
            stock_uom = frappe.db.get_single_value("LMS Settings", "default_stock_uom") or "Unit"
            
            item = frappe.get_doc({
                "doctype": "Item",
                "item_code": self.name,
                "item_name": sanitized_title,
                "description": sanitized_description,
                "item_group": item_group,
                "is_sales_item": 1,
                "stock_uom": stock_uom
            })
            item.insert()
            self.item = item.name
            
            # Use db_set to avoid triggering on_update
            self.db_set("item", self.item, update_modified=False)
    
    def update_linked_item(self):
        """Synchronize fields between Bootcamp and Item"""
        if self.item:
            # Sanitize inputs before updating item
            sanitized_title = self.sanitize_input(self.title)
            sanitized_description = self.sanitize_input(self.description or "")
            
            item = frappe.get_doc("Item", self.item)
            item.item_name = sanitized_title
            item.description = sanitized_description
            item.save()
    
    def sanitize_input(self, input_text):
        """Sanitize user input to prevent security issues"""
        if not input_text:
            return ""
        
        # Strip HTML tags and sanitize
        sanitized = strip_html_tags(input_text)
        # Additional sanitization can be added here if needed
        return sanitized.strip()