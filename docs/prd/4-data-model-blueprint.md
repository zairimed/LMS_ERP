# 4. Data Model (Blueprint)
The "LMS" application will contain the following DocTypes:

* **LMS Bootcamp:** The main program container. Linked to an ERPNext Item for sales. Contains a table of LMS Course.
* **LMS Course:** A module or section of a Bootcamp. Contains a table of LMS Lesson.
* **LMS Lesson (Child DocType):** The atomic content unit. Contains content_type, video_url fields, and the is_free_preview field (Checkbox).
* **Enrollment:** Links a User to an LMS Bootcamp. Contains progress tracking fields (e.g., completed_lessons table).
* **Sales Partner (Standard DocType):** Customized with a user field (Link to User) for portal access.
