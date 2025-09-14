# Sales Partner Management

## Overview
This document describes how to manage Sales Partners in the LMS system. Sales Partners are used to track influencers and affiliates who promote bootcamps, with commission rates assigned to each partner.

## Creating a Sales Partner

### Via the Web Interface
1. Navigate to the Sales Partners list in the Frappe Desk
2. Click the "New" button to create a new Sales Partner
3. Fill in the required fields:
   - **Sales Partner Name**: The name of the influencer or affiliate
   - **Commission Rate**: The percentage commission for this partner
   - **User**: Link to a User account for portal access (optional)
4. Save the Sales Partner

### Via the API
Sales Partners can also be created via the Frappe REST API:

```http
POST /api/resource/Sales Partner
Content-Type: application/json

{
  "sales_partner_name": "Influencer Name",
  "commission_rate": 15,
  "user": "influencer@example.com"
}
```

## Linking Users to Sales Partners

To allow Sales Partners to access the affiliate portal, you can link them to User accounts:

1. Create a User account for the Sales Partner if one doesn't exist
2. When creating or editing a Sales Partner, link the User account in the "User" field
3. The system will automatically:
   - Create the necessary permissions
   - Assign the "Sales Partner" role to the User

## Managing Commission Rates

Commission rates are set per Sales Partner and can be modified at any time:

1. Navigate to the Sales Partner in the Frappe Desk
2. Edit the "Commission Rate" field
3. Save the changes

Changes to commission rates will apply to future sales, not historical ones.

## Permissions

Sales Partners have the following permissions:
- System Managers and Administrators can create, read, write, and delete Sales Partners
- Linked Users can view and edit their own Sales Partner record
- Commission rates are visible to System Managers and Administrators

## Role-Based Access Control

The system implements role-based access control for Sales Partners:
- A new "Sales Partner" role is automatically assigned to linked Users
- This role grants appropriate permissions for affiliate portal access
- Removing the User link also removes the Sales Partner role

## Best Practices

1. **Unique Users**: Each User should only be linked to one Sales Partner
2. **Regular Audits**: Periodically review commission rates and Sales Partner performance
3. **Documentation**: Keep records of agreements with influencers and affiliates
4. **Training**: Ensure Sales Partners understand how to access and use the affiliate portal
5. **Security**: Regularly review User accounts and permissions for Sales Partners

## Troubleshooting

### User Cannot Access Affiliate Portal
1. Verify the Sales Partner record has a User linked
2. Check that the User has the "Sales Partner" role
3. Verify the User Permission for the Sales Partner exists

### Commission Rate Not Applying
1. Ensure the commission rate is saved on the Sales Partner record
2. Verify that new sales are being attributed to the correct Sales Partner

### Duplicate User Link
1. The system prevents linking the same User to multiple Sales Partners
2. If you need to change the User link, first remove the existing link