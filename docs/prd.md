# Product Requirements Document: Multi-School LMS Platform
Version: 1.1

Author: DevArchitect (Coach), [Your Name] (Product Owner)

Date: September 7, 2025

Status: Approved for Development

## 1. Vision and Objectives

### 1.1. Product Vision
Create a network of specialized and independent e-learning platforms (Schools), each with its own brand and domain, but all powered by a common LMS application and a robust ERPNext back-office. The project aims to offer a premium and targeted experience to students, away from generalist marketplaces.

### 1.2. Problem to Solve
Expert content creators need to launch online schools that reflect a strong and professional brand image in their niche. Marketplace-type platforms (like Udemy) dilute this brand image. This project offers a solution that combines brand autonomy and centralized code management efficiency.

### 1.3. Key Personas
* **The Administrator (You):** Manages all sites, creates course content, manages finances and the affiliate program.
* **The Student (Client):** Registers, purchases and follows courses within a specific school. Their experience is compartmentalized to that school.
* **The Influencer (Commercial Partner):** Promotes a school via links or coupons and tracks their performance and commissions via a dedicated portal.

## 2. Architecture and Strategic Choices
* **Architectural Model:** The project will follow a Multi-Site architecture (Scenario B). Each "School" will be an independent Frappe site with its own database, ensuring complete isolation of data, branding, and users.
* **Technology Stack:**
    * Framework: Frappe v15.20.0
    * Back-Office: ERPNext v15.20.0
    * Core Application: A custom Frappe "LMS" application containing all course business logic.
    * Database: MariaDB
    * Cache & Queues: Redis

## 3. Features (Epics & User Stories)

### EPIC 1: Foundation, Educational Content and Deployment
Description: Provide the Administrator with tools to create content and establish the technical foundations of the project.

* **[PO Update]** **US-1.0: As an Administrator, I want a step-by-step deployment guide to be able to deploy new schools to production autonomously and securely.**
* **US-1.1:** As an Administrator, I want to create Bootcamps as complete study programs, each being the main product sold on a site.
* **US-1.2:** As an Administrator, I want to structure a Bootcamp into Courses/Modules, and each Course into Lessons (video, text, lab).
* **US-1.3:** As an Administrator, I want to be able to mark specific Lessons as "Free Preview" so they are accessible to non-registered visitors.

### EPIC 2: Student Experience
Description: Provide a smooth and engaging learning experience for enrolled students.

* **US-2.1:** As a Visitor, I want to be able to view lessons marked as "Free Preview" to evaluate a bootcamp before purchasing.
* **US-2.2:** As a Student, I want to see my progress in a bootcamp (e.g., 3/25 lessons completed) to stay motivated.
    * **[PO Update]** Note: Lesson completion is triggered automatically (e.g., end of a video).
* **US-2.3:** As a Student, I want to be able to access bootcamp content after a successful purchase, managed via an Enrollment document.

### EPIC 3: Affiliate Program for Influencers
Description: Set up a system for partners to promote schools and receive commissions.

* **US-3.1:** As an Administrator, I want to be able to create Commercial Partners (Sales Partners) for each influencer, assigning them a commission rate.
* **US-3.2:** As an Administrator, I want to generate unique Promo Codes (via Pricing Rules) and link them to a specific Partner, with validity dates.
* **US-3.3:** As an Influencer, I want to log into a dedicated portal to see my sales statistics and commission amounts in real-time.
    * **[PO Update]** Permission rule: The influencer can see the number of referred sales and their total commissions, but not students' personal information.

## 4. Data Model (Blueprint)
The "LMS" application will contain the following DocTypes:

* **LMS Bootcamp:** The main program container. Linked to an ERPNext Item for sales. Contains a table of LMS Course.
* **LMS Course:** A module or section of a Bootcamp. Contains a table of LMS Lesson.
* **LMS Lesson (Child DocType):** The atomic content unit. Contains content_type, video_url fields, and the is_free_preview field (Checkbox).
* **Enrollment:** Links a User to an LMS Bootcamp. Contains progress tracking fields (e.g., completed_lessons table).
* **Sales Partner (Standard DocType):** Customized with a user field (Link to User) for portal access.

## 5. Non-Functional Requirements
* **Internationalization (i18n):** The application interface must use Frappe's translation method `_("string")`. Content fields of DocTypes (title, description) must be marked as "Translatable".
* **Testing:** Critical business logic (commission calculation, access verification, progress calculation) must be covered by Unit Tests to ensure stability and non-regression.
* **Security:** Access to affiliate portal and student portal data must be strictly compartmentalized to the logged-in user via Frappe's "User Permissions".

## 6. Out-of-Scope (Post-MVP v1.0)
The following features are not part of the first version:

* A unified Udemy-type marketplace.
* Complex quiz and assessment systems.
* Discussion forums or community features.
* Live courses or webinars.

## 7. Next Steps
* Begin development of the "LMS" application skeleton by creating the DocTypes described in section 4.
* Set up a first development site (tech.dev.local) to test the application.
* Develop student portal logic to display bootcamp content (with free preview management).

This document will serve as a guide. Any changes or additions must be discussed and result in an update to this PRD.