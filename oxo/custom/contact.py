import frappe
from frappe.utils import cstr, has_gravatar
from frappe.model.naming import append_number_if_name_exists
from frappe.contacts.doctype.contact.contact import Contact

class TSContact(Contact):
	def autoname(self):
		# concat first and last name
		self.name = " ".join(
			filter(None, [cstr(self.get(f)).strip() for f in ["first_name", "last_name"]])
		)

		if frappe.db.exists("Contact", self.name):
			self.name = append_number_if_name_exists("Contact", self.name)

		# concat party name if reqd
		# for link in self.links:
		# 	self.name = self.name + "-" + link.link_name.strip()
		# 	break

# def rename():
#     a = frappe.db.sql("""Select first_name, name from  `tabContact` where first_name != name""", as_dict=True)
#     success=0
#     for i in a:
#         try:
#             frappe.get_doc("Contact", i.name).rename(i.first_name)
#             success+=1
#         except:
#             print(frappe.get_traceback())
#     print(success)