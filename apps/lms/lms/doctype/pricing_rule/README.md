# Promo Code Management

## Overview
This document describes how to manage Promo Codes in the LMS system. Promo Codes are implemented using ERPNext's Pricing Rules functionality, with extensions to link them to specific Sales Partners for affiliate tracking.

## Creating a Promo Code

### Via the Web Interface
1. Navigate to the Pricing Rules list in the Frappe Desk
2. Click the "New" button to create a new Pricing Rule (Promo Code)
3. Fill in the required fields:
   - **Title**: A descriptive name for the promo code
   - **Apply On**: Select what the promo code applies to (e.g., Item Code)
   - **Items**: Select the specific items the promo code applies to
   - **Price or Discount**: Select whether this is a price override or discount
   - **Discount Percentage** or **Discount Amount**: Enter the discount value
   - **Sales Partner**: Link to a Sales Partner for affiliate tracking (optional)
   - **Valid From**: Start date for promo code validity (optional)
   - **Valid Upto**: End date for promo code validity (optional)
4. Save the Pricing Rule

### Via the API
Pricing Rules (Promo Codes) can also be created via the Frappe REST API:

```http
POST /api/resource/Pricing Rule
Content-Type: application/json

{
  "title": "SUMMER2025",
  "selling": 1,
  "apply_on": "Item Code",
  "items": [
    {
      "item_code": "BOOTCAMP-001"
    }
  ],
  "price_or_discount": "Discount Percentage",
  "discount_percentage": 15,
  "sales_partner": "Influencer Name",
  "valid_from": "2025-06-01",
  "valid_upto": "2025-08-31"
}
```

## Linking Promo Codes to Sales Partners

To enable affiliate tracking, you can link Promo Codes to specific Sales Partners:

1. When creating or editing a Pricing Rule, select a Sales Partner in the "Sales Partner" field
2. The system will automatically track usage of the promo code by the linked Sales Partner
3. Reports will show which Sales Partner generated which sales through promo code usage

## Managing Validity Dates

Promo Codes can have validity periods:

1. Set the "Valid From" date to specify when the promo code becomes active
2. Set the "Valid Upto" date to specify when the promo code expires
3. If no dates are set, the promo code is valid indefinitely
4. The system automatically validates promo code usage against these dates

## Tracking Promo Code Usage

The system provides tracking for promo code usage:

1. Activity Logs are created when Promo Codes are created or updated
2. Sales reports can be filtered by Sales Partner to see promo code effectiveness
3. Usage statistics show which promo codes are driving the most conversions

## Filtering and Searching Promo Codes

The Pricing Rules list page provides several ways to find specific promo codes:

1. **Search Bar**: Search by title, sales partner, or other text fields
2. **Filters**: Use the filter sidebar to narrow down results by:
   - Sales Partner
   - Validity dates
   - Creation date
   - Active status
3. **Sorting**: Sort columns by clicking on headers
4. **Visual Indicators**:
   - Color-coded status badges (Active, Expired, Scheduled)
   - Progress bars showing time until expiration
   - Icons indicating linked Sales Partners

## Permissions

Pricing Rules (Promo Codes) have the following permissions:
- System Managers and Administrators can create, read, write, and delete Pricing Rules
- Sales Partners can view Pricing Rules linked to them
- Promo Code usage is validated against the linked Sales Partner

## Best Practices

1. **Descriptive Titles**: Use descriptive titles for easy identification
2. **Validity Dates**: Always set validity dates for time-limited promotions
3. **Sales Partner Linking**: Link promo codes to Sales Partners for proper affiliate tracking
4. **Regular Audits**: Periodically review promo code performance and usage
5. **Documentation**: Keep records of promo code campaigns and their results
6. **Testing**: Test promo codes before launching campaigns to ensure they work correctly

## Troubleshooting

### Promo Code Not Applying
1. Verify the promo code is within its validity period
2. Check that the promo code applies to the correct items
3. Ensure the promo code is active (not disabled)

### Incorrect Sales Partner Tracking
1. Verify the Sales Partner is correctly linked to the Pricing Rule
2. Check that users are using the correct promo code for their Sales Partner

### Expired Promo Code Still Working
1. Verify the "Valid Upto" date is correctly set
2. Check that the system date is correct
3. Clear any caches that might be affecting date validation

## API Endpoints

### Create Promo Code
```http
POST /api/resource/Pricing Rule
```

### Get Promo Codes for Sales Partner
```http
GET /api/resource/Pricing Rule?filters={"sales_partner":"Sales Partner Name"}
```

### Update Promo Code
```http
PUT /api/resource/Pricing Rule/{promo_code_name}
```

### Delete Promo Code
```http
DELETE /api/resource/Pricing Rule/{promo_code_name}
```

### Get Promo Code Statistics
```http
GET /api/method/lms.lms.doctype.pricing_rule.pricing_rule.get_promo_code_statistics?sales_partner=Sales Partner Name
```