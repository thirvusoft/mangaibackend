// Copyright (c) 2023, thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Dealer Sales order count"] = {
	"filters": [
		{
			"fieldname":"Customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"default": frappe.defaults.get_user_default("Customer"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
	]
};
