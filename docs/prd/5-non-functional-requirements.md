# 5. Non-Functional Requirements
* **Internationalization (i18n):** The application interface must use Frappe's translation method `_("string")`. Content fields of DocTypes (title, description) must be marked as "Translatable".
* **Testing:** Critical business logic (commission calculation, access verification, progress calculation) must be covered by Unit Tests to ensure stability and non-regression.
* **Security:** Access to affiliate portal and student portal data must be strictly compartmentalized to the logged-in user via Frappe's "User Permissions".
