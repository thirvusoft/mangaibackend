import frappe 
import json
from erpnext.controllers.item_variant import make_variant_item_code

@frappe.whitelist()
def create_attribute_value(data):
    if isinstance(data, str):
        data = json.loads(data)
    doc = frappe.new_doc('Item Attribute Value')
    idx = frappe.db.get_value('Item Attribute Value', {
        'parent':data['item_attribute'],
        'parentfield':'item_attribute_values',
        'parenttype': "Item Attribute",
    }, 'idx', order_by = 'idx desc') or 0
    doc.update({
        'parent':data['item_attribute'],
        'parentfield':'item_attribute_values',
        'parenttype': "Item Attribute",
        'abbr': data['abbr'],
        'attribute_value': data['attribute_value'],
        'idx':idx+1,
    })
    doc.save()
    
def item_rename(self, old_name, new_name=None, merge=None, event=None):
    variants = frappe.db.get_all("Item", {"variant_of":self.name})
    for i in variants:
        variant=frappe.get_doc("Item", i.name)
        variant.item_code = None
        make_variant_item_code(self.item_code, self.item_name, variant)
        frappe.set_value("Item", variant.name, "item_name", variant.item_name)