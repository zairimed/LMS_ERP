# Access Bootcamp Content After Purchase

## Overview
This document describes how students can access bootcamp content after successfully purchasing a bootcamp. The access is managed through Enrollment documents that link users to bootcamps.

## How Access Works

### 1. Enrollment Creation
When a student successfully purchases a bootcamp, an Enrollment document is automatically created that links the user to the bootcamp. This enrollment grants the student access to all content within that bootcamp.

### 2. Access Control
Access to bootcamp content is controlled through the enrollment system:
- Enrolled users can access all lessons within their enrolled bootcamps
- Non-enrolled users can only access lessons marked as "Free Preview"
- System Managers and Administrators have access to all content for administrative purposes

### 3. Content Access Process
1. Student purchases a bootcamp through the standard ERPNext sales process
2. System automatically creates an Enrollment document linking the student to the bootcamp
3. Student can now access the bootcamp content through their "My Bootcamps" dashboard

## User Interface

### My Bootcamps Page
Students can access their enrolled bootcamps through the "My Bootcamps" page, which shows:
- List of all bootcamps they are enrolled in
- Quick access links to bootcamp content
- Option to continue from where they left off

### Bootcamp Content Page
Within each bootcamp, students can:
- Browse courses and lessons
- View lesson content (text, video, lab)
- Track their progress
- Mark lessons as complete
- Navigate between lessons

### Lesson Content Page
For each lesson, students can:
- View the lesson content based on its type (text, video, lab)
- Mark the lesson as complete
- Navigate to previous and next lessons
- See which bootcamp and course the lesson belongs to

## Technical Implementation

### Access Control Functions
The system provides several functions to check access:
- `is_user_enrolled(user, bootcamp)` - Check if a user is enrolled in a bootcamp
- `check_content_access(user, bootcamp)` - Check if user has access to bootcamp content
- `check_lesson_access(user, lesson)` - Check if user has access to a specific lesson

### Context Providers
Template context is provided for:
- My Bootcamps page
- Bootcamp Content page
- Lesson Content page

### Enrollment Creation
Enrollments are automatically created through:
- `create_enrollment_on_purchase(user, bootcamp)` - Create enrollment on purchase
- `handle_successful_purchase(user, bootcamp_item_code)` - Handle purchase webhook

## Security
- Access control is enforced at both the page and lesson level
- Free preview lessons are accessible to everyone
- All other content requires proper enrollment
- System Managers and Administrators have elevated access for administrative purposes

## Troubleshooting
If a student cannot access content they should have access to:
1. Verify the student is properly enrolled in the bootcamp
2. Check that the enrollment document is active
3. Ensure the student is logged in with the correct account
4. Contact system administrator if issues persist