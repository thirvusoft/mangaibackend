# Copyright (c) 2023, thirvusoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(),get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{"label": "Customer", "fieldname": "Customer", "fieldtype": "Links"},
		{
			"label": "Total Amount",
			"fieldname": "total_amount",
			"fieldtype": "Data",
			
		},
		
	]
	return columns

def get_data(filters=None):
	filter={}
	data=[]
	query_params = {        
		"customer": filters.get("Customer"),
		"from_date": filters.get("from_date"),
		"to_date": filters.get("to_date")
    }
	frappe.errprint(query_params)
	mop_exe = frappe.db.sql("""
    SELECT COUNT(name) as order_count
    FROM `tabSales Order`
    WHERE customer = %(customer)s
        AND transaction_date BETWEEN %(from_date)s AND %(to_date)s
	""", query_params, as_dict=True)
	for i in mop_exe:
		sum_data={}
		sum_data["Customer"]=filters.get("Customer")
		sum_data["total_amount"]=i["order_count"]
		data.append(sum_data)
	return data