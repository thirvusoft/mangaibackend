
import frappe
from frappe.utils import cint

def autoname(self, event=None):
	self.name=self.partner_name +"-"+ (self.territory or "")
	return
	try:
		if len(self.territory) >= 3:
			territory = self.territory[0:3].upper()
		else:
			territory = (self.territory or "").upper()
		naming_series = "DI-"
		doc = frappe.db.sql (f""" select * from tabSeries where name = "{naming_series}" """)
		if len(doc)==0:
			frappe.db.sql(f""" INSERT INTO tabSeries VALUES ("{naming_series}",0) """)
		series = frappe.db.sql (f""" select current from tabSeries where name = "{naming_series}" """)
		if(series and series[0]):
			series = series[0][0]

		frappe.db.sql("update `tabSeries` set current = %s where name = %s",
					(cint(series)+1, naming_series))
		series = frappe.db.sql (f""" select current from tabSeries where name = "{naming_series}" """)
		if(series and series[0]):
			series = series[0][0]
		name = f"{naming_series}{territory}-{('0'*(2-len(str(series)))) if(len(str(series))<2) else ''}{series}"
		if(not frappe.db.exists(self.doctype, name)):
			self.name = name
	except:
		frappe.errprint(frappe.get_traceback())
		pass


def update_series(self, event=None):
    if(frappe.get_all(self.doctype) and frappe.get_last_doc(self.doctype).name==self.name):
        naming_series = "DI-"
        series = frappe.db.sql (f""" select current from tabSeries where name = "{naming_series}" """)
        if(series and series[0]):
            series = series[0][0]
            frappe.db.sql("update `tabSeries` set current = %s where name = %s",
                    (cint(series)-1 if cint(series)-1>=0 else 0, naming_series))


def rename(self,event=None):
	if(self.name!=self.partner_name +"-"+ (self.territory or "")):
		self.rename(self.partner_name +"-"+ (self.territory or ""))
