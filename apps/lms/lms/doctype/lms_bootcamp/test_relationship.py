# Copyright (c) 2025, Your Company Name. All rights reserved.
# For license information, please see license.txt

import frappe

def test_bootcamp_course_lesson_relationship():
    """Test the relationship between Bootcamp, Course, and Lesson"""
    try:
        # Create a new bootcamp with courses and lessons
        bootcamp = frappe.get_doc({
            "doctype": "LMS Bootcamp",
            "title": "Test Bootcamp with Courses and Lessons",
            "description": "This is a test bootcamp with courses and lessons",
            "courses": [
                {
                    "title": "Course 1",
                    "description": "First course",
                    "lessons": [
                        {
                            "title": "Lesson 1.1",
                            "description": "First lesson of first course",
                            "content_type": "Text",
                            "content": "Content of lesson 1.1"
                        },
                        {
                            "title": "Lesson 1.2",
                            "description": "Second lesson of first course",
                            "content_type": "Video",
                            "video_url": "https://example.com/video1.mp4"
                        }
                    ]
                },
                {
                    "title": "Course 2",
                    "description": "Second course",
                    "lessons": [
                        {
                            "title": "Lesson 2.1",
                            "description": "First lesson of second course",
                            "content_type": "Text",
                            "content": "Content of lesson 2.1"
                        }
                    ]
                }
            ]
        })
        bootcamp.insert()
        print("Bootcamp with courses and lessons created successfully")
        
        # Verify the structure
        bootcamp.reload()
        print(f"Bootcamp has {len(bootcamp.courses)} courses")
        
        for i, course in enumerate(bootcamp.courses):
            print(f"Course {i+1}: {course.title}")
            print(f"  Course has {len(course.lessons)} lessons")
            for j, lesson in enumerate(course.lessons):
                print(f"    Lesson {j+1}: {lesson.title} ({lesson.content_type})")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_bootcamp_course_lesson_relationship()