import frappe

def customer_abb(self, event):
    # customer_name=[word[0] for word in self.customer_name.split()]
    # abb=""
    # for a in customer_name:
    #     abb=abb+a
    
    # self.delear_abb = abb.upper()
    if(self.ts_mobilenumber):
        self.name=(self.ts_mobilenumber or "")+ "-" + (self.customer_name.upper() or "")

