import frappe
@frappe.whitelist()
def get_current_employee_info() -> dict:
    """Fetches current logged-in employee's information including WFH eligibility"""
    current_user = frappe.session.user

    employee = frappe.db.get_value(
        "Employee",
        {"user_id": current_user, "status": "Active"},
        [
            "name",
            "first_name",
            "employee_name",
            "designation",
            "department",
            "company",
            "custom_eligible_for_work_from_home",  
            "user_id",
        ],
        as_dict=True,
    )

    # Return employee data if found, else return empty dictionary
    return employee if employee else {}
