import frappe

@frappe.whitelist(allow_guest=True)
def get_csrf_token():
    """Generates and returns a CSRF token."""
    csrf_token = frappe.generate_hash()
    frappe.response["csrf_token"] = csrf_token
    return {"csrf_token": csrf_token}

# import frappe

# @frappe.whitelist(allow_guest=True)
# def get_csrf_token():
#     """
#     Returns the existing CSRF token for the logged-in session.
#     """
#     csrf_token = frappe.sessions.get_csrf_token()
#     return {"csrf_token": csrf_token}
