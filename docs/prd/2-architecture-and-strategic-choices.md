# 2. Architecture and Strategic Choices
* **Architectural Model:** The project will follow a Multi-Site architecture (Scenario B). Each "School" will be an independent Frappe site with its own database, ensuring complete isolation of data, branding, and users.
* **Technology Stack:**
    * Framework: Frappe v15.20.0
    * Back-Office: ERPNext v15.20.0
    * Core Application: A custom Frappe "LMS" application containing all course business logic.
    * Database: MariaDB
    * Cache & Queues: Redis
