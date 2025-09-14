# 6. Project Structure
The project structure at the root will follow the configuration defined in the development charter.

```plaintext
/my-lms-project
|-- apps/
|   |-- lms/                # Our custom application
|   |   |-- lms/
|   |   |   |-- doctype/
|   |   |   |   |-- lms_bootcamp/
|   |   |   |   |-- lms_course/
|   |   |   |   |-- enrollment/
|   |   |-- www/              # Templates for public portals
|   |   |-- templates/
|   |   |-- public/
|   |-- erpnext/            # The ERPNext application
|-- docker-compose.yml      # Core of the environment
|-- sites/                  # Site data (managed by Docker Volume)
|-- README.md
```
