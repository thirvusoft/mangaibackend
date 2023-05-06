import http.client
import os
import json
import validators
from time import sleep
import frappe
from frappe.model.document import Document
from frappe.utils.password import get_decrypted_password
import mimetypes
from frappe.utils.pdf import get_pdf


FILETYPE = {
            'Document':['doc', 'docx', 'odt', 'xls', 'xlsx', 'ods', 'ppt', 'pptx', 'odp', 'pdf', 'csv'],
            'Video':['3gp', 'mp4', 'm4v', 'mkv', 'webm', 'mov', 'avi', 'wmv', 'mpg', 'flv'],
            'Image':['dwg', 'xcf', 'jpg', 'jpeg', 'jpx', 'png', 'apng', 'gif', 'webp', 'cr2', 'svg', 'tif', 'bmp', 'jxr', 'psd', 'ico', 'heic', 'avif'],
        }

class TSWhatsappSettings(Document):
    pass

@frappe.whitelist()
def get_media_type(path):
    try:
        kind = mimetypes.guess_type(path)
        extension = mimetypes.guess_extension(kind[0] if kind else None) 
        for _type in FILETYPE:
            if((extension.split('.')[1] if (extension and len(extension.split('.'))>1)  else extension) in FILETYPE[_type]):
                return _type
    except:
        return None

@frappe.whitelist()
def whatsapp(number = "", language_code="en_US", countrycode = "", message = [], payload_1 = "", template = "", token = "", headerValues = [], filename = "",  media_type = ""):
    if(frappe.db.get_single_value("TS Whatsapp Settings", "whatsapp_the_pdf")):
        whatsappsettings = frappe.get_single("TS Whatsapp Settings")
        conn = http.client.HTTPSConnection(whatsappsettings.api)
        if isinstance(headerValues, str):
            headerValues=[headerValues]
        if isinstance(message, str):
            message=[message]
        message=[frappe.utils.strip_html_tags(msg) for msg in message]
        headerValues=[frappe.utils.get_url()+url if(url and validators.url(url)!=True) else url for url in headerValues]
        if(not template and not media_type and headerValues):
            media_type = get_media_type(path=headerValues[0])
        if((not template) and media_type):
            for row in whatsappsettings.template:
                if((row.media_type or "").lower() == (media_type or "").lower()):
                    template = row.template_name
                    language_code=row.language_code
        elif((not template) and (not media_type)):
            for row in whatsappsettings.template:
                if(row.media_type == "None"):
                    template = row.template_name
                    language_code=row.language_code
        payload = json.dumps({
            "countryCode": countrycode or whatsappsettings.default_country_code,
            "phoneNumber": number,
            "type": "Template",
            "template": {
                "name": template,
                "languageCode": language_code,
                "bodyValues": message,
                "headerValues": headerValues,
                "filename": filename
            }
        })
        headers = {
            'Authorization':  get_decrypted_password("TS Whatsapp Settings", "TS Whatsapp Settings", "authorization_token"),
            'Content-Type': 'application/json',
            'Cookie': 'ApplicationGatewayAffinity=a8f6ae06c0b3046487ae2c0ab287e175; ApplicationGatewayAffinityCORS=a8f6ae06c0b3046487ae2c0ab287e175'
        }
        conn.request("POST", "/v1/public/message/", payload_1 or payload, headers)
        res = conn.getresponse()
        data = res.read()
        return res
    else:
        data = "Enable message through whatsapp in Whatsapp Settings."
        return data

def sales_order(self,event):
    whats_enable=frappe.get_value("Company",self.company,"enbale")
    if whats_enable:
        html = frappe.get_print("Sales Order", self.name, doc=None, print_format="TS Sales Order",no_letterhead=0)
        file = frappe.get_doc({
            "doctype": "File",
            "file_name": f"{self.name}.pdf",
            "is_private": 0,
            "content": get_pdf(html),
            "attached_to_doctype":  self.doctype,
            "attached_to_name": self.name
            }) 
        file.save(ignore_permissions=True)
        # distributor=frappe.get_value("Sales Partner",self.sales_partner,"mobile_no","")
        sales_person_no=self.sales_team[0].sales_person
        sales_person_no=frappe.get_value("Sales Person",sales_person_no,"mobile_no")
        customer_no=frappe.get_value("Customer",self.customer,"mobile_no")
        whatsapp_number=frappe.get_single("OXO Settings")
        number=[]
        name =[]
        for j in whatsapp_number.whatsapp_number:
            whatsapp_number=j.number
            whats_name=j.name1
            frappe.errprint(j)
            number.append(whatsapp_number)
            name.append(whats_name)
        # number.append(distributor)
        name.append(self.sales_partner)
        number.append(sales_person_no)
        name.append(self.sales_team[0].sales_person)
        number.append(customer_no)
        name.append(self.customer)
        frappe.errprint(j)
        if self.sales_team:
            sales_person=self.sales_team[0].sales_person
            for i in range (0,len(number),1):
                whatsapp(number=number[i],message=[name[i],sales_person],headerValues=[frappe.utils.get_url()+file.file_url],filename=file.file_name)
            
    