import frappe
from frappe.utils import now
from datetime import datetime

# @frappe.whitelist()
def appointment():
    open_list=frappe.get_all("Appointment",filters={"status":"Open"},fields=["scheduled_time","status","name"])
    for a in open_list:
        if str(a["scheduled_time"]) < now():
          
            frappe.db.set_value("Appointment",a["name"],"status","Closed")
            frappe.db.commit()