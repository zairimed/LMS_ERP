# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalesPartner(Document):
    def validate(self):
        """Validate Sales Partner before saving"""
        # Ensure user is not already linked to another Sales Partner
        if self.user:
            existing = frappe.db.exists(
                "Sales Partner",
                {
                    "user": self.user,
                    "name": ["!=", self.name]
                }
            )
            if existing:
                frappe.throw("User is already linked to another Sales Partner")
    
    def after_insert(self):
        """Set up permissions for linked user"""
        if self.user:
            self.setup_user_permissions()
            self.setup_user_role()
    
    def on_update(self):
        """Update permissions when Sales Partner is updated"""
        if self.has_value_changed("user"):
            # Remove permissions from old user
            old_user = self.get_doc_before_save().user
            if old_user:
                self.remove_user_permissions(old_user)
                self.remove_user_role(old_user)
            
            # Set up permissions for new user
            if self.user:
                self.setup_user_permissions()
                self.setup_user_role()
    
    def setup_user_permissions(self):
        """Set up permissions for the linked user"""
        if not self.user:
            return
        
        # Create User Permission for Sales Partner
        if not frappe.db.exists("User Permission", {"user": self.user, "allow": "Sales Partner", "for_value": self.name}):
            user_perm = frappe.get_doc({
                "doctype": "User Permission",
                "user": self.user,
                "allow": "Sales Partner",
                "for_value": self.name,
                "apply_to_all_doctypes": 1
            })
            user_perm.insert(ignore_permissions=True)
    
    def remove_user_permissions(self, user):
        """Remove permissions for a user"""
        if not user:
            return
        
        # Remove User Permission for Sales Partner
        user_perms = frappe.get_all(
            "User Permission",
            filters={"user": user, "allow": "Sales Partner", "for_value": self.name}
        )
        
        for perm in user_perms:
            frappe.delete_doc("User Permission", perm.name, ignore_permissions=True)
    
    def setup_user_role(self):
        """Set up Sales Partner role for the linked user"""
        if not self.user:
            return
        
        # Get the User document
        user = frappe.get_doc("User", self.user)
        
        # Check if user already has Sales Partner role
        has_role = False
        for role in user.roles:
            if role.role == "Sales Partner":
                has_role = True
                break
        
        # Add Sales Partner role if not present
        if not has_role:
            user.append("roles", {"role": "Sales Partner"})
            user.save()
    
    def remove_user_role(self, user):
        """Remove Sales Partner role from a user"""
        if not user:
            return
        
        # Get the User document
        user_doc = frappe.get_doc("User", user)
        
        # Remove Sales Partner role if present
        roles = []
        for role in user_doc.roles:
            if role.role != "Sales Partner":
                roles.append(role)
        
        user_doc.roles = roles
        user_doc.save()