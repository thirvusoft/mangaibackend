# Copyright (c) 2023, thirvusoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{"label": "Sales Person", "fieldname": "sales_person", "fieldtype": "Links", "width": 150},
		{
			"label": "Total Amount",
			"fieldname": "total_amount",
			"fieldtype": "Data",
			"width": 100,
		},
		
	]
	return columns

def get_data(filters=None):
	fil = {}
	if filters.get("sales_person"):
		email=frappe.get_doc("User",{"full_name":filters.get("sales_person")})
		employee=frappe.get_doc("Employee",{"user_id":email.name})
		frappe.errprint(email.email)

		fil["owner"] = email.email
	if filters.get("from_date") and filters.get("to_date"):
		fil["creation"]= ["between", [filters.get("from_date"), filters.get("to_date")]]
	data=[]
	doc=frappe.get_list("Sales Order",filters = fil, fields=["sum(rounded_total)","owner"],group_by="owner")
	
	for i in doc:
		sum_data={}
		sum_data["sales_person"]=i["owner"]
		sum_data["total_amount"]=i["sum(rounded_total)"]
		data.append(sum_data)
	return data
