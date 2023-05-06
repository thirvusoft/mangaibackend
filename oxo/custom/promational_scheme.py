import frappe

def schemelevel(self,event):
    self.update({
        "scheme_": {}
    })

    item_group_list = []

    for i in self.pricing_rules:
        if i.pricing_rule not in item_group_list or not item_group_list:

            precentage=frappe.get_value("Pricing Rule", i.pricing_rule, "discount_percentage")
            form_date=frappe.get_value("Pricing Rule", i.pricing_rule, "valid_from")
            to_date=frappe.get_value("Pricing Rule", i.pricing_rule, "valid_upto")
            item_group=frappe.get_value("Item", i.item_code, "item_group")


            self.append("scheme_", {
                "item_group": item_group,
                "scheme_level": precentage,
                "form_date":form_date,
                "to_date":to_date

            })

            item_group_list.append(i.pricing_rule)
