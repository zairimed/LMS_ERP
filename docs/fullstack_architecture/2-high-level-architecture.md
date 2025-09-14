# 2. High-Level Architecture

## 2.1. Technical Summary
The architecture is a **multi-site** web system based on the Frappe/ERPNext framework, fully containerized with Docker. A single shared codebase powers multiple independent "Schools", each with its own database and domain, ensuring complete isolation. The main business logic is contained in a custom Frappe application ("LMS").

## 2.2. Platform and Infrastructure
* **Platform:** Self-hosted on a cloud server (VPS) running Linux (Ubuntu 22.04 LTS recommended).
* **Containerization:** Docker and Docker Compose are used to manage the entire development and production environment, ensuring consistency and reproducibility.
* **Key Services:** Nginx (reverse proxy), Gunicorn (Python application server), MariaDB (database), Redis (cache and queues).

## 2.3. Repository Structure
* **Structure:** Monorepo. A single Git repository will contain the Docker configuration, custom `lms` application code, and site configuration.

## 2.4. Architecture Diagram
This diagram illustrates the interactions between the main system components.

```mermaid
graph TD
    subgraph "Production Server (VM/Cloud)"
        Nginx(Nginx - Reverse Proxy)

        subgraph "Frappe Bench (via Docker)"
            Gunicorn(Gunicorn - Python Workers)

            subgraph "Shared Codebase"
                FrappeApp[Frappe Framework]
                ERPNextApp[ERPNext Application]
                LMSApp[<b>Custom LMS Application</b>]
            end
            
            subgraph "Site Instances"
                Site_A[Site A: tech-school.com]
                Site_B[Site B: cuisine-school.com]
            end

            Gunicorn -- Executes --> FrappeApp & ERPNextApp & LMSApp
            
            Site_A -- uses --> Gunicorn
            Site_B -- uses --> Gunicorn
        end

        subgraph "Data Services"
            DB_A[(MariaDB for Site A)]
            DB_B[(MariaDB for Site B)]
            Redis(Redis - Cache & Queues)
        end

        Nginx -- Routes requests to --> Site_A & Site_B
        Site_A -- Reads/writes to --> DB_A
        Site_B -- Reads/writes to --> DB_B
        Site_A & Site_B -- Use --> Redis
    end
```
