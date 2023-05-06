import frappe

def salesorder_status():
    due_diligence=frappe.get_all("Due Diligence",filters={"diligence_status":"Accepted Digitally"},fields=["document_name"])
    frappe.errprint(due_diligence)

    for i in due_diligence:
        status=frappe.get_doc("Sales Order",i.document_name)
        print(status.workflow_state)
        if(status.workflow_state=="Order"):
            frappe.db.set_value("Sales Order",i.document_name,"workflow_state", 'Dispatch')
            print(status.workflow_state)

