import frappe


def workflow():
    create_state()
    create_salesorder_flow()


def create_state():
    list={"Submit":"Warning", "Dispatched":"Inverse", "Order":"Primary", "Complete":"Success"}
    for row in list:
        if not frappe.db.exists('Workflow State', row):
            new_doc = frappe.new_doc('Workflow State')
            new_doc.workflow_state_name = row
            new_doc.style=list[row]
            new_doc.save()
    list=['To Order', 'To Complete', 'To Dispatch']
    for i in list:
        if not frappe.db.exists('Workflow Action Master', i):
            new_doc = frappe.new_doc('Workflow Action Master')
            new_doc.workflow_action_name = i
            new_doc.save()




def create_salesorder_flow():
    if frappe.db.exists('Workflow', 'Sales Order'):
        return
        # frappe.delete_doc('Workflow', 'Quotation Flow')
    workflow = frappe.new_doc('Workflow')
    workflow.workflow_name = 'Sales Order'
    workflow.document_type = 'Sales Order'
    workflow.workflow_state_field = 'workflow_state'
    workflow.is_active = 1
    workflow.send_email_alert = 1
    workflow.append('states', dict(
        state = 'Submit', allow_edit = 'All',doc_status = 0,
    ))
    workflow.append('states', dict(
        state = 'Order', allow_edit = 'All',doc_status = 1,
    ))
    workflow.append('states', dict(
        state = 'Dispatched', allow_edit = 'All',doc_status = 1,
    ))
    workflow.append('states', dict(
        state = 'Complete', allow_edit = 'All',doc_status = 1,
    ))
    
    
    workflow.append('transitions', dict(
        state = 'Submit', action='To Order', next_state = 'Order',
        allowed='All', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Order', action='To Dispatch', next_state = 'Dispatched',
        allowed='All', allow_self_approval= 1,
    ))
    workflow.append('transitions', dict(
        state = 'Dispatched', action='To Complete', next_state = 'Complete',
        allowed='All', allow_self_approval= 1,
    ))
    workflow.insert(ignore_permissions=True)
    return workflow