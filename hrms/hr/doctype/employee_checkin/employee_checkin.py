import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, nowdate

from hrms.hr.doctype.shift_assignment.shift_assignment import get_actual_start_end_datetime_of_shift
from hrms.hr.utils import (
    get_distance_between_coordinates,
    set_geolocation_from_coordinates,
    validate_active_employee,
)


class CheckinRadiusExceededError(frappe.ValidationError):
    pass


class EmployeeCheckin(Document):
    def validate(self):
        """Validate Employee Check-in."""
        if self.is_work_from_home_approved():
            return

        validate_active_employee(self.employee)
        self.validate_duplicate_log()
        self.fetch_shift()
        self.set_geolocation()
        self.validate_distance_from_shift_location()

    def validate_duplicate_log(self):
        """Check if an employee has duplicate check-in logs."""
        doc = frappe.db.exists(
            "Employee Checkin",
            {
                "employee": self.employee,
                "time": self.time,
                "name": ("!=", self.name),
                "log_type": self.log_type,
            },
        )
        if doc:
            doc_link = frappe.get_desk_link("Employee Checkin", doc)
            frappe.throw(
                _("This employee already has a log with the same timestamp.{0}").format("<br>" + doc_link)
            )

    @frappe.whitelist()
    def set_geolocation(self):
        """Set geolocation for the check-in."""
        set_geolocation_from_coordinates(self)

    @frappe.whitelist()
    def fetch_shift(self):
        """Fetch shift details based on check-in time."""
        shift_actual_timings = get_actual_start_end_datetime_of_shift(
            self.employee, get_datetime(self.time), True
        )

        if not shift_actual_timings:
            self.shift = None
            return

        if (
            shift_actual_timings.shift_type.determine_check_in_and_check_out
            == "Strictly based on Log Type in Employee Checkin"
            and not self.log_type
            and not self.skip_auto_attendance
        ):
            frappe.throw(
                _("Log Type is required for check-ins falling in the shift: {0}.").format(
                    shift_actual_timings.shift_type.name
                )
            )

        if not self.attendance:
            self.shift = shift_actual_timings.shift_type.name
            self.shift_actual_start = shift_actual_timings.actual_start
            self.shift_actual_end = shift_actual_timings.actual_end
            self.shift_start = shift_actual_timings.start_datetime
            self.shift_end = shift_actual_timings.end_datetime

    def validate_distance_from_shift_location(self):
        """Validate the employee's location for check-in."""
        if self.is_work_from_home_approved():
            return

        if not frappe.db.get_single_value("HR Settings", "allow_geolocation_tracking"):
            return

        if not (self.latitude or self.longitude):
            frappe.throw(_("Latitude and longitude values are required for checking in."))

        assignment_locations = frappe.get_all(
            "Shift Assignment",
            filters={
                "employee": self.employee,
                "shift_type": self.shift,
                "start_date": ["<=", self.time],
                "shift_location": ["is", "set"],
                "docstatus": 1,
            },
            or_filters=[["end_date", ">=", self.time], ["end_date", "is", "not set"]],
            pluck="shift_location",
        )

        if not assignment_locations:
            return

        checkin_radius, latitude, longitude = frappe.db.get_value(
            "Shift Location", assignment_locations[0], ["checkin_radius", "latitude", "longitude"]
        )

        if checkin_radius <= 0:
            return

        distance = get_distance_between_coordinates(latitude, longitude, self.latitude, self.longitude)
        if distance > checkin_radius:
            frappe.throw(
                _("You must be at your work location to check in/out"),
                exc=CheckinRadiusExceededError,
            )

    def is_work_from_home_approved(self):
        """Check if the employee has an approved Work From Home request for the current date."""
        current_date = get_datetime(self.time).date()
        return frappe.db.exists(
            "Work From Home",
            {
                "employee": self.employee,
                "status": "Approved",
                "from_date": ["<=", current_date],
                "to_date": [">=", current_date],
            },
        )


def calculate_working_hours(logs, check_in_out_type, working_hours_calc_type):
    """
    Calculate working hours based on check-ins and check-outs.
    Skips if WFH is approved.
    """
    if logs and frappe.db.exists(
        "Work From Home",
        {
            "employee": logs[0].employee,
            "status": "Approved",
            "from_date": ["<=", nowdate()],
            "to_date": [">=", nowdate()],
        },
    ):
        return 0, None, None

    if not logs or len(logs) < 2:
        return 0, None, None

    first_checkin = logs[0].time
    last_checkout = logs[-1].time
    working_hours = (last_checkout - first_checkin).total_seconds() / 3600

    return working_hours, first_checkin, last_checkout


def mark_attendance_and_link_log(logs, status, date, working_hours=None):
    """
    Marks attendance based on logs and links them.
    Skips if WFH is approved.
    """
    if not logs:
        return None

    employee = logs[0].employee

    if frappe.db.exists(
        "Work From Home",
        {
            "employee": employee,
            "status": "Approved",
            "from_date": ["<=", date],
            "to_date": [">=", date],
        },
    ):
        return None

    attendance = frappe.get_doc({
        "doctype": "Attendance",
        "employee": employee,
        "status": status,
        "attendance_date": date,
        "working_hours": working_hours or 0,
    })
    attendance.insert(ignore_permissions=True)

    for log in logs:
        frappe.db.set_value("Employee Checkin", log.name, "attendance", attendance.name)

    return attendance
