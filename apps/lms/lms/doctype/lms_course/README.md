# LMS Course

## Overview
The LMS Course DocType represents a module or section of a Bootcamp. Each course can contain multiple lessons.

## Fields
- **Title**: The name of the course (required)
- **Description**: A detailed description of the course
- **Lessons**: A table of LMS Lessons that make up the course

## Functionality
- Courses are linked to Bootcamps through a child table
- Each course can contain multiple lessons of different types (Text, Video, Lab)
- Courses can be created, edited, and deleted through the Frappe UI

## Creation Process
1. Navigate to the LMS Course list in the Frappe UI
2. Click "New" to create a new course
3. Fill in the required Title field
4. Optionally add a Description
5. Add lessons to the course using the Lessons table
6. Save the course