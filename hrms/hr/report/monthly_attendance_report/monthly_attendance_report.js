// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

// frappe.query_reports["Monthly Attendance Report"] = {
// 	"filters": [

// 	]
// };


frappe.query_reports["Monthly Attendance Report"] = {
    "filters": [
        {
            "fieldname": "start_date",
            "label": __("Start Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.now_date(), -1), // Default to one month ago
            "reqd": 1 // Mandatory field
        },
        {
            "fieldname": "end_date",
            "label": __("End Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.now_date(), // Default to today
            "reqd": 1 // Mandatory field
        },
        {
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee", // Links to the Employee doctype
            "reqd": 0 // Optional field
        }
    ]
};
