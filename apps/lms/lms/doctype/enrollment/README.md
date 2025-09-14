# Enrollment

## Overview
The Enrollment DocType links a User to an LMS Bootcamp and tracks their progress through the bootcamp. It also manages access control for bootcamp content.

## Fields
- **User**: Link to the User who is enrolled
- **Bootcamp**: Link to the LMS Bootcamp the user is enrolled in
- **Enrollment Date**: Date when the enrollment was created
- **Completion Status**: Current status of the enrollment (In Progress or Completed)
- **Completed Lessons**: Table of lessons that have been completed
- **Progress Percentage**: Calculated percentage of completed lessons

## Functionality
- Prevents duplicate enrollments for the same user and bootcamp
- Calculates progress percentage based on completed lessons
- Tracks individual lesson completion with dates
- Automatically sets enrollment date to current date
- Manages access control for bootcamp content

## Access Control
- Enrolled users can access all content within their enrolled bootcamps
- Non-enrolled users can only access lessons marked as "Free Preview"
- System Managers and Administrators have access to all content

## Creation Process
1. Enrollment is automatically created when a user purchases a bootcamp
2. Can also be manually created by administrators
3. Each enrollment links one user to one bootcamp

## Progress Tracking
- Progress is automatically calculated based on the ratio of completed lessons to total lessons
- Individual lessons are marked as complete using the `mark_lesson_complete` method
- Completion status can be manually updated to "Completed" when appropriate

## Integration with Purchases
- `create_enrollment_on_purchase(user, bootcamp)` - Create enrollment on purchase
- `handle_successful_purchase(user, bootcamp_item_code)` - Handle purchase webhook
- Automatically creates enrollment when user purchases a bootcamp through ERPNext

## API Functions
- `is_user_enrolled(user, bootcamp)` - Check if a user is enrolled in a bootcamp
- `check_content_access(user, bootcamp)` - Check if user has access to bootcamp content
- `check_lesson_access(user, lesson)` - Check if user has access to a specific lesson
- `get_enrolled_bootcamps(user)` - Get all bootcamps a user is enrolled in