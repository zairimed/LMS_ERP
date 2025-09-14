# Content Structuring Guide for LMS

## Overview
This guide explains how to structure educational content in the LMS using Bootcamps, Courses, and Lessons.

## Content Hierarchy
The LMS organizes content in a three-level hierarchy:

1. **Bootcamp** - The main container for a complete study program
2. **Course** - A module or section within a Bootcamp
3. **Lesson** - The atomic content unit within a Course

## Creating Content

### 1. Creating a Bootcamp
1. Navigate to the LMS Bootcamp list in the Frappe UI
2. Click "New" to create a new bootcamp
3. Fill in the required Title field
4. Optionally add a Description
5. Save the bootcamp
6. An ERPNext Item will be automatically created and linked to the bootcamp

### 2. Adding Courses to a Bootcamp
1. Open an existing bootcamp or create a new one
2. In the Courses table, click "Add Row"
3. Fill in the required Title field for the course
4. Optionally add a Description
5. Save the bootcamp

### 3. Adding Lessons to a Course
1. Open an existing bootcamp
2. Find the course you want to add lessons to
3. In the Lessons table within that course, click "Add Row"
4. Fill in the required Title field for the lesson
5. Select the Content Type (Text, Video, or Lab)
6. Depending on the content type:
   - For Text: Add content in the Content field
   - For Video: Add the video URL in the Video URL field
   - For Lab: Add lab instructions in the Content field
7. Optionally mark the lesson as free preview
8. Save the bootcamp

## Content Types

### Text Lessons
Text lessons are ideal for written content such as articles, tutorials, or instructions. Use the built-in text editor to format your content with headings, lists, links, and other formatting options.

### Video Lessons
Video lessons allow you to embed video content from external sources. Simply provide the URL to the video, and it will be embedded in the lesson.

### Lab Lessons
Lab lessons are for hands-on activities or exercises. Provide detailed instructions in the content field, and students can follow along to complete the lab.

## Free Preview
You can mark specific lessons as "Free Preview" to make them accessible to non-registered visitors. This is a great way to let potential students sample your content before purchasing.

To mark a lesson as free preview:
1. When creating or editing a lesson, check the "Is Free Preview" checkbox
2. Save the lesson

## Best Practices

### Organizing Content
- Group related lessons into courses
- Keep courses focused on specific topics or skills
- Use descriptive titles for all content
- Provide clear descriptions to help students understand what each piece of content covers

### Using Content Types
- Use Text lessons for detailed explanations and written content
- Use Video lessons for demonstrations or lectures
- Use Lab lessons for hands-on activities and exercises

### Free Preview Strategy
- Select your best or most representative lessons to offer as free preview
- Include a mix of content types in your free preview
- Make sure free preview lessons provide enough value to encourage purchases while leaving enough premium content to justify the purchase

## Example Structure
Here's an example of how you might structure a web development bootcamp:

**Bootcamp**: Full Stack Web Development

**Course 1**: HTML & CSS Fundamentals
- **Lesson 1**: Introduction to HTML (Text)
- **Lesson 2**: HTML Elements and Tags (Text)
- **Lesson 3**: Basic CSS Styling (Video)
- **Lesson 4**: HTML/CSS Lab (Lab)

**Course 2**: JavaScript Programming
- **Lesson 1**: JavaScript Basics (Text)
- **Lesson 2**: Variables and Data Types (Video)
- **Lesson 3**: Functions and Scope (Text)
- **Lesson 4**: JavaScript Lab (Lab)

**Course 3**: Backend Development with Node.js
- **Lesson 1**: Introduction to Node.js (Text)
- **Lesson 2**: Express.js Framework (Video)
- **Lesson 3**: Database Integration (Text)
- **Lesson 4**: Node.js Lab (Lab)