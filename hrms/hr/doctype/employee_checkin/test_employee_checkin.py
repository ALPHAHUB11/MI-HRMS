from datetime import datetime, timedelta
import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import now_datetime, nowdate

# Import EmployeeCheckin dynamically to prevent circular imports
import importlib
employee_checkin = importlib.import_module("hrms.hr.doctype.employee_checkin.employee_checkin")
calculate_working_hours = employee_checkin.calculate_working_hours


class TestEmployeeCheckin(IntegrationTestCase):
    def setUp(self):
        """Set up test environment by cleaning existing Employee Checkin data."""
        frappe.db.delete("Shift Type")
        frappe.db.delete("Shift Assignment")
        frappe.db.delete("Employee Checkin")
        frappe.db.delete("Work From Home")

        frappe.db.set_single_value("HR Settings", "allow_geolocation_tracking", 0)

    def test_calculate_working_hours_with_wfh(self):
        """
        Ensure that if an employee has an approved WFH request,
        the working hours calculation is skipped.
        """
        employee = "test_employee_wfh@example.com"

        frappe.get_doc(
            {
                "doctype": "Work From Home",
                "employee": employee,
                "status": "Approved",
                "from_date": nowdate(),
                "to_date": nowdate(),
            }
        ).insert()

        logs = [
            frappe._dict({"employee": employee, "time": now_datetime() - timedelta(minutes=390)}),
            frappe._dict({"employee": employee, "time": now_datetime() - timedelta(minutes=300)}),
        ]

        working_hours, first_checkin, last_checkout = calculate_working_hours(logs, "SomeType", "SomeMethod")

        self.assertEqual(working_hours, 0)
        self.assertIsNone(first_checkin)
        self.assertIsNone(last_checkout)

    def test_employee_can_checkin_when_wfh_is_approved(self):
        """
        Ensure that an employee can check in and check out freely when WFH is approved,
        bypassing geolocation and shift validation.
        """
        employee = "test_employee_checkin_wfh@example.com"

        frappe.get_doc(
            {
                "doctype": "Work From Home",
                "employee": employee,
                "status": "Approved",
                "from_date": nowdate(),
                "to_date": nowdate(),
            }
        ).insert()

        checkin = frappe.get_doc(
            {
                "doctype": "Employee Checkin",
                "employee": employee,
                "time": now_datetime(),
                "log_type": "IN",
            }
        ).insert()

        self.assertEqual(checkin.employee, employee)
        self.assertEqual(checkin.log_type, "IN")


if __name__ == "__main__":
    frappe.connect()
    frappe.db.commit()
