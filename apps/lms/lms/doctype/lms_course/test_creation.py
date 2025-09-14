# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe

def test_course_and_lesson_creation():
    """Test creation of LMS Course and LMS Lesson"""
    try:
        # Create a new course
        course = frappe.get_doc({
            "doctype": "LMS Course",
            "title": "Test Course",
            "description": "This is a test course"
        })
        course.insert()
        print("Course created successfully")
        
        # Create a new lesson
        lesson = frappe.get_doc({
            "doctype": "LMS Lesson",
            "title": "Test Lesson",
            "description": "This is a test lesson",
            "content_type": "Text",
            "content": "This is the lesson content"
        })
        lesson.insert()
        print("Lesson created successfully")
        
        # Create a course with lessons
        course_with_lessons = frappe.get_doc({
            "doctype": "LMS Course",
            "title": "Test Course with Lessons",
            "description": "This is a test course with lessons",
            "lessons": [
                {
                    "title": "Lesson 1",
                    "description": "First lesson",
                    "content_type": "Text",
                    "content": "Content of lesson 1"
                },
                {
                    "title": "Lesson 2",
                    "description": "Second lesson",
                    "content_type": "Video",
                    "video_url": "https://example.com/video.mp4"
                }
            ]
        })
        course_with_lessons.insert()
        print("Course with lessons created successfully")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_course_and_lesson_creation()