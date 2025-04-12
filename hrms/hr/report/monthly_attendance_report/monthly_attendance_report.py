# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


import frappe

def format_time_in_hours_and_minutes(minutes):
    """Convert minutes into 'x hr, y min' format."""
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours} hr, {mins} min" if mins > 0 else f"{hours} hr"
    else:
        return f"{mins} min"

def execute(filters=None):
    # Define default values for filters
    start_date = filters.get("start_date") or "2024-12-01"
    end_date = filters.get("end_date") or "2024-12-31"
    employee_filter = filters.get("employee")

    # Define columns
    columns = [
        {"fieldname": "employee", "label": "Emp Id", "fieldtype": "Link", "options": "Employee", "width": 100},
        {"fieldname": "employee_name", "label": "Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "department", "label": "Department", "fieldtype": "Link", "options": "Department", "width": 150},
        {"fieldname": "shift", "label": "Shift", "fieldtype": "Data", "width": 120},
        {"fieldname": "shift_start", "label": "Shift Start", "fieldtype": "Time", "width": 120},
        {"fieldname": "shift_end", "label": "Shift End", "fieldtype": "Time", "width": 120},
    ]

    # Calculate number of days in the range
    num_days = frappe.utils.date_diff(end_date, start_date) + 1

    # Add daily columns for the fixed date range
    for i in range(num_days):
        date = frappe.utils.add_days(start_date, i)
        columns.append({
            "fieldname": f"day_{i}",
            "label": frappe.utils.formatdate(date, "dd MMM"),
            "fieldtype": "Data",
            "width": 120,
        })

    # Add aggregate columns
    columns.extend([
        {"fieldname": "total_present", "label": "Total Present", "fieldtype": "Int", "width": 120},
        {"fieldname": "total_absent", "label": "Total Absent", "fieldtype": "Int", "width": 120},
        {"fieldname": "total_late", "label": "Total Late (hrs, mins)", "fieldtype": "Data", "width": 200},
        {"fieldname": "total_early", "label": "Total Early (hrs, mins)", "fieldtype": "Data", "width": 200},
    ])

    # Fetch employees based on the employee filter
    employee_condition = ""
    if employee_filter:
        employee_condition = "AND name = %(employee)s"

    employees = frappe.db.sql(f"""
        SELECT name, employee_name, department
        FROM `tabEmployee`
        WHERE status = 'Active' {employee_condition}
    """, {"employee": employee_filter}, as_dict=True)

    data = []
    for employee in employees:
        row = {
            "employee": employee["name"],
            "employee_name": employee["employee_name"],
            "department": employee["department"],
            "shift": None,
            "shift_start": None,
            "shift_end": None,
        }

        # Fetch shift details for the employee
        shift_data = frappe.db.sql("""
            SELECT DISTINCT 
                shift, 
                TIME(shift_start) AS shift_start, 
                TIME(shift_end) AS shift_end
            FROM `tabEmployee Checkin`
            WHERE employee = %s
            LIMIT 1
        """, (employee["name"],), as_dict=True)

        if shift_data:
            row["shift"] = shift_data[0]["shift"]
            row["shift_start"] = shift_data[0]["shift_start"]
            row["shift_end"] = shift_data[0]["shift_end"]

        # Initialize daily attendance and aggregates
        total_present, total_absent, total_late, total_early = 0, 0, 0, 0

        for i in range(num_days):
            date = frappe.utils.add_days(start_date, i)

            daily_data = frappe.db.sql("""
                SELECT 
                    MAX(CASE WHEN log_type = 'IN' THEN TIME(time) END) AS check_in,
                    MAX(CASE WHEN log_type = 'OUT' THEN TIME(time) END) AS check_out,
                    CASE
                        WHEN MAX(CASE WHEN log_type = 'IN' THEN TIME(time) END) > TIME(shift_start) THEN 
                            TIMESTAMPDIFF(MINUTE, TIME(shift_start), MAX(CASE WHEN log_type = 'IN' THEN TIME(time) END)) - 15
                        ELSE 0
                    END AS late_minutes,
                    CASE
                        WHEN MAX(CASE WHEN log_type = 'OUT' THEN TIME(time) END) < TIME(shift_end) THEN 
                            TIMESTAMPDIFF(MINUTE, MAX(CASE WHEN log_type = 'OUT' THEN TIME(time) END), TIME(shift_end))
                        ELSE 0
                    END AS early_minutes
                FROM `tabEmployee Checkin`
                WHERE employee = %s AND DATE(time) = %s
            """, (employee["name"], date), as_dict=True)

            if daily_data and daily_data[0]["check_in"]:
                check_in = daily_data[0]["check_in"]
                check_out = daily_data[0]["check_out"] or "--"

                late_minutes = max(0, daily_data[0]["late_minutes"])
                early_minutes = max(0, daily_data[0]["early_minutes"])

                total_late += late_minutes
                total_early += early_minutes

                # Mark the day as present
                row[f"day_{i}"] = f"<span style='color:green;'>P</span><br>{check_in}<br>{check_out}"
                total_present += 1
            else:
                # Mark the day as absent
                row[f"day_{i}"] = f"<span style='color:red;'>A</span>"
                total_absent += 1

        # Convert total_late and total_early into 'x hr, y min' format
        row.update({
            "total_present": total_present,
            "total_absent": total_absent,
            "total_late": format_time_in_hours_and_minutes(total_late),
            "total_early": format_time_in_hours_and_minutes(total_early),
        })

        data.append(row)

    return columns, data
