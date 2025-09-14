# 3. Technology Stack (Tech Stack)
This stack is defined by the Development Charter and serves as the source of truth for the entire project.

| Category | Technology | Version | Role |
|----------|------------|---------|------|
| Framework | Frappe | v15.20.0 | System foundation (ORM, Admin UI) |
| Back-Office | ERPNext | v15.20.0 | Sales, customer, partner management |
| Database | MariaDB | 10.6 | Data storage for each site |
| Cache | Redis | 6.2-alpine | Performance caching |
| Queues | Redis | 6.2-alpine | Asynchronous task management |
| Web Server | Nginx | latest | Reverse proxy and multi-domain management |
| Backend Language | Python | (defined by Frappe image) | LMS application business logic |
| Frontend Language | JavaScript | (defined by Frappe image) | Public portals and client scripts |
| Testing | Python Unit Tests | (integrated with Frappe) | Critical business logic validation |
