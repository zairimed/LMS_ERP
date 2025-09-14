# LMS Lesson

## Overview
The LMS Lesson DocType represents the atomic content unit within a Course. Lessons can be of different types (Text, Video, Lab) and can be marked as free preview.

## Fields
- **Title**: The name of the lesson (required)
- **Description**: A detailed description of the lesson
- **Content Type**: The type of content (Text, Video, Lab)
- **Video URL**: URL for video content (only visible when Content Type is Video)
- **Content**: Text content (only visible when Content Type is Text)
- **Is Free Preview**: Checkbox to mark the lesson as free preview

## Functionality
- Lessons are linked to Courses through a child table
- Different content types have different fields that are shown/hidden based on the content type
- Lessons can be marked as free preview to make them accessible to non-registered visitors
- Lessons can be created, edited, and deleted through the Frappe UI

## Creation Process
1. Navigate to the LMS Course that you want to add a lesson to
2. In the Lessons table, click "Add Row"
3. Fill in the required Title field
4. Select the Content Type
5. Fill in the appropriate fields based on the content type:
   - For Text: Add content in the Content field
   - For Video: Add the video URL in the Video URL field
   - For Lab: Add lab instructions in the Content field
6. Optionally mark the lesson as free preview
7. Save the course