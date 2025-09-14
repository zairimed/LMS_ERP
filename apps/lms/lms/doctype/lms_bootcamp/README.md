# LMS Bootcamp

## Overview
The LMS Bootcamp DocType represents a complete study program that can be sold on a school site. Each bootcamp is linked to an ERPNext Item for sales functionality.

## Fields
- **Title**: The name of the bootcamp (required)
- **Description**: A detailed description of the bootcamp
- **Item**: A link to the associated ERPNext Item (automatically created)
- **Courses**: A table of LMS Courses that make up the bootcamp

## Functionality
- When a new LMS Bootcamp is created, an ERPNext Item is automatically created and linked
- Changes to the bootcamp title or description are synchronized to the linked Item
- The bootcamp can be sold through the standard ERPNext sales process using the linked Item
- Input sanitization prevents security vulnerabilities
- Performance optimization prevents unnecessary synchronization
- Configurable settings allow customization of item creation

## Security Features
- Input sanitization for all user-provided data
- Prevention of infinite recursion in save operations
- Proper error handling for edge cases

## Performance Features
- Item synchronization only occurs when relevant fields change
- Efficient save operations that don't trigger unnecessary updates

## Configuration
- Item group and stock UOM can be configured through LMS Settings
- Default values are used if settings are not configured

## Creation Process
1. Navigate to the LMS Bootcamp list in the Frappe UI
2. Click "New" to create a new bootcamp
3. Fill in the required Title field
4. Optionally add a Description
5. Save the bootcamp
6. An ERPNext Item will be automatically created and linked to the bootcamp

## Editing Process
1. Navigate to the LMS Bootcamp list and select a bootcamp to edit
2. Click "Edit"
3. Make changes to the Title or Description
4. Save the changes
5. The linked ERPNext Item will be automatically updated with the new information (only if title or description changed)