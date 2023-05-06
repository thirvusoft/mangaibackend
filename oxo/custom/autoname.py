import frappe
from frappe.model.naming import parse_naming_series
from erpnext.accounts.utils import get_fiscal_year

def get_fiscal_year_short_form():
    a=[]
    fy =  frappe.db.get_single_value('Global Defaults', 'current_fiscal_year')    
    fy1 =  frappe.db.get_single_value('Global Defaults', 'current_fiscal_year') 
    a.append(fy.split('-')[0][2:] )
    a.append(fy1.split('-')[1][2:] )

    return a




def name_sales_order(doc, action):    
    a = get_fiscal_year_short_form()
    doc.name = parse_naming_series(f"SAL-ORD-{a[0]}-{a[1]}-.###")



