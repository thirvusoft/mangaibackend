import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def create_sales_person_custom_fields():
    custom_fields = {
		"Sales Person": [
            dict(fieldname='designation', label='Designation',
				fieldtype='Link', options="Designation", insert_after='sales_person_name')  ,     
			dict(fieldname='mobile_no', label='Mobile No',
				fieldtype='Data', insert_after='designation')
            ]
    }
    create_custom_fields(custom_fields)