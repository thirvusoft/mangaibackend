from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def create_sales_partner_custom_fields():
    custom_fields = {
		"Sales Partner": [
            dict(fieldname='state', label='State',
				fieldtype='Link', options="State", insert_after='territory')  ,     
			dict(fieldname='mobile_no', label='Mobile No',
				fieldtype='Data', insert_after='commission_rate')
            ]
    }
    create_custom_fields(custom_fields)