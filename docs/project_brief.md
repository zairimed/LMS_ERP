# Project Brief: Multi-School LMS Platform
Version: 1.0

Author: Mary (Analyst)

Date: September 7, 2025

Reference: PRD v1.1, Architecture v1.0

## 1. Executive Summary
This project aims to create a network of specialized and independent e-learning platforms ("Schools"), powered by a common LMS application built on the Frappe/ERPNext framework. The solution will enable content creators to launch their own online schools with strong branding, while benefiting from centralized technical management, all within a containerized environment with Docker for maximum portability.

## 2. Problem Statement
Experts and content creators wishing to monetize their knowledge through online courses often face a dilemma: either dilute themselves in a generalist marketplace (like Udemy), or face the technical complexity and high costs of creating a proprietary platform. This project solves this problem by offering a "multi-site" solution where each school is independent and customizable, but maintained by a single codebase, thereby drastically reducing complexity and maintenance costs.

## 3. Proposed Solution
We will develop a custom Frappe application, named "LMS", which will contain all business logic for course management (Bootcamps, lessons, progression) and an affiliate system. This application will be installed on a multi-site Frappe Bench infrastructure, enabling rapid deployment of new schools, each with its own database, domain, and visual identity.

## 4. Target Users
* **The Administrator (You):** The content creator who manages courses, finances, and partnerships for all schools from a centralized interface.
* **The Student:** The end customer who registers, pays, and follows a course within a single school, benefiting from an immersive and distraction-free experience.
* **The Influencer:** The commercial partner who promotes a school and tracks their commissions via a dedicated portal.

## 5. Objectives & Success Metrics
* **Business Objective:** Launch at least two independent schools (e.g., tech, cooking) within 6 months following v1.0 deployment.
* **User Objective (Student):** Achieve a course completion rate of 70% or higher, indicating an engaging experience.
* **Technical Objective:** Deploying a new school must take less than 30 minutes (excluding content creation).

## 6. MVP Scope (Version 1.0)
* **Included:**
    * Course structure creation (Bootcamp > Course > Lesson).
    * Course access for students after enrollment.
    * Student progress tracking.
    * "Free preview" lessons for marketing.
    * Basic affiliate system with tracking portal for influencers.

* **Excluded:**
    * Quizzes, certifications, community forums.
    * Centralized marketplace.

## 7. Constraints and Assumptions
* **Technical Constraint:** The project will be entirely built on the Frappe v15.20.0 framework and deployed via Docker.
* **Financial Constraint:** The goal is to maintain a cost of €0 during the development phase and minimize production costs (<€10/month) at launch.
* **Assumption:** Frappe's multi-site model is flexible enough to handle customization for each school brand.

## 8. Next Steps
The project has passed Product Owner validation. The next step is to move to the **Development Phase** in an IDE, starting by invoking the **Scrum Master** agent to prepare the first story for development.