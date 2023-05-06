import frappe;
from frappe.auth import LoginManager
from frappe.utils import nowdate, time_diff_in_hours
import json
import datetime
from datetime import timedelta

from datetime import datetime

from frappe.core.doctype.user.user import generate_keys
from frappe.utils.password import get_decrypted_password
from oxo.custom.appointmnet import appointment

@frappe.whitelist()
def generate_token(user):
    user_details = frappe.get_doc("User", user)
    api_key = user_details.api_key
    changes = 0
    if not user_details.api_secret:
        api_secret = frappe.generate_hash(length=15)
        user_details.api_secret = api_secret
        changes = 1
    else:
        api_secret = get_decrypted_password("User", user, "api_secret")
    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
        changes = 1
    if(changes):
        user_details.save(ignore_pernmissions=True)

    return f'token {api_key}:{api_secret}'

@frappe.whitelist( allow_guest=True )
def login(mobile,password):
#  args=json.loads(args)
    try:
       login_manager = frappe.auth.LoginManager()
       login_manager.authenticate(user=mobile, pwd=password)
       login_manager.post_login()

    except frappe.exceptions.AuthenticationError:
       frappe.clear_messages()
       frappe.local.response["message"] = "Incorrect Username or Password"
       return
    api_generate = generate_keys(frappe.session.user)
    frappe.db.commit()
    user = frappe.get_doc('User', frappe.session.user)
    frappe.local.response['token']="token "+user.api_key+":"+api_generate["api_secret"]
    frappe.local.response['message']='Logined Sucessfully'



# @frappe.whitelist( allow_guest=True )
# def login(mobile,password):
#     try:
#        login_manager = frappe.auth.LoginManager()
#        login_manager.authenticate(user=mobile, pwd=password)
#        login_manager.post_login()
#        token = generate_token(frappe.session.user)
#        frappe.local.response['token']=token

       
       
#        frappe.local.response['message']='Logined Sucessfully'
#     except frappe.exceptions.AuthenticationError:
#        frappe.clear_messages()
#        frappe.local.response.http_status_code = 500
#        frappe.local.response["message"]="Incorrect Mobile number or Password"

    

    
@frappe.whitelist( allow_guest=True)
def template_list(item_group,category=""):
    tem_list1=frappe.db.get_all("Item",fields=["name as item_code","item_name", "standard_rate", "item_group"],filters={"item_group":item_group,"has_variants":1})
    frappe.local.response['message']=tem_list1

@frappe.whitelist( allow_guest=True)
def categories_list():
    tab_list=[]
    tem_list=frappe.db.get_all("Item Group",fields=["name"],filters={"parent_item_group":"All Item Groups","is_group":1})
    for i in tem_list:
        tab_list.append(i["name"])
    frappe.local.response['message']=tab_list

@frappe.whitelist( allow_guest=True)
def varient_list(item):
    
    if frappe.db.get_value("Item",item,'has_variants'):   
        var_list1=frappe.db.get_all("Item",fields=["name as item_code","item_name", "standard_rate", "item_group","image"],filters={"variant_of":item})
     
      
    else:
        var_list1=frappe.db.get_all("Item",fields=["name as item_code","item_name", "standard_rate", "item_group","image"],filters={"name":item})
    for i in var_list1:
        if i["image"]:
            i["image"]="https://"+frappe.local.request.host+i["image"]
    frappe.local.response['message']=var_list1


def state(allow_guest=True):
    state=frappe.get_meta("Address").fields
    s=""
    for i in state:
        if i.fieldname=="gst_state":
            s=i.options
            break
    if s:
        state=s.split("\n")
    else:
        state=[]
    state=[i for i in state if i]
    frappe.local.response["message"]=state
    
@frappe.whitelist( allow_guest=True)
def customer_list():
    cus_list=frappe.db.get_all("Customer",pluck='name')
    user_list=frappe.db.get_all("User",pluck='username')
    sales_partner=frappe.db.get_all("Sales Partner",pluck='name')
    frappe.local.response['Dealer']=cus_list
    frappe.local.response['User']=user_list
    frappe.local.response['sales_partner']=sales_partner

@frappe.whitelist( allow_guest=True)
def distributor(): 
    distributor=frappe.db.get_all("Sales Partner",{'partner_type':"Distributor"},pluck='name')
    frappe.local.response['message']=distributor
    
    
@frappe.whitelist()
def sales_order(cus_name,items,due_date,distributor,sales_person,Competitors):
    """
        Sales order creation
    """
    if sales_person:
        # frappe.session.user=sales_person
        email=frappe.get_doc("User",{"full_name":sales_person})
        employee=frappe.get_doc("Employee",{"user_id":email.name})
        salesperson=frappe.get_doc("Sales Person",{"employee":employee.name})
    # frappe.log_error(title='items', message=items)
    # frappe.db.commit()
    items=json.loads(items)
    
    
    # def sort_items(item):
    #     item_template = frappe.db.get_value("Item", item.get("item_code"), "variant_of")
    #     attr_val = frappe.db.get_value("Item Variant Attribute", {"parenttype": "Item", "parent": item.get("item_code"), "attribute": "Size"}, "attribute_value") or ""
    #     attr = frappe.db.get_value('Item Attribute Value', {'parenttype': 'Item Attribute', 'parent': 'Size', 'attribute_value': attr_val}, 'abbr')
    #     return (item_template,attr.isnumeric(), '0'*(9-len(str(attr)))+attr)
    # def sort_items(item):
    # item_template = frappe.db.get_value("Item", item.get("item_code"), "item_template")
    # attr_val = frappe.db.get_value("Item Variant Attribute", {"parenttype": "Item", "parent": item.get("item_code"), "attribute": "Size"}, "attribute_value") or ""
    # attr = frappe.db.get_value('Item Attribute Value', {'parenttype': 'Item Attribute', 'parent': 'Size', 'attribute_value': attr_val}, 'abbr')
    # return (item_template, attr.isnumeric(), '0'*(9-len(str(attr)))+attr)



    # items.sort(key = sort_items)
    # sorted_items = sorted(items, key=sort_items)

    doc=frappe.new_doc("Sales Order")
    frappe.session.user=email.name
   
    doc.update(
        {
            "customer":cus_name,
            "delivery_date":due_date or nowdate(),
            "items":[{"item_code":i.get('item_code'),"qty":i.get("qty")} for i in items if float(i.get('qty')) ],
            "sales_partner":distributor,
            "competitors":Competitors,
            "sales_team":[{'sales_person':salesperson.name,"allocated_percentage":100}],
            "company":"mangai"
        })
    doc.flags.ignore_permissions = True
    try:
        doc.save()
        doc.submit()
        frappe.db.commit()
        frappe.local.response["message"] = "Order saved Successfully"
    except frappe.ValidationError as e:
        frappe.local.response.http_status_code = 417
        frappe.local.response["message"] = e


    

@frappe.whitelist()
def new_customer(full_name, doorno, phone_number,address,state,districts,user,customer_group,landline_number="",territory="",latitude="",longitude="",auto_pincode="",pincode=""
):
    """
        customer creation  
    """
    api_key = frappe.request.headers.get('Authorization').split(' ')[1].split(':')[0]
    user = frappe.db.get_value("User", {"api_key": api_key})
    frappe.session.user=user
    doc=frappe.new_doc("Customer")
    name=full_name
    full_name=(phone_number)+ "-" + (full_name.upper())
    
    if not frappe.db.exists("Customer",{"name":["like",f'%{phone_number}%']}):
        
        # try:
        doc.update(
            {
                "customer_name":name,
                "territory":territory,
                "ts_mobilenumber":phone_number,
                # "mobile_no":phone_number["p"][0],
                "latitude":latitude,
                "longitude":longitude,

                "pincode":auto_pincode,
                "customer_group":customer_group
                
            })      
        frappe.db.begin()
        doc.flags.ignore_permissions = True
        doc.flags.ignore_mandatory = True
        doc.save(ignore_permissions = True)
       
        contact_doc=frappe.new_doc("Contact")
        contact_doc.first_name=doc.name
        
        if phone_number:
            contact_doc.append("phone_nos",{
            "phone":phone_number,
            "is_primary_phone": 1,
            "is_primary_mobile_no": 0 
            })
        if landline_number:
            contact_doc.append("phone_nos",{
            "phone":landline_number,
            "is_primary_phone": 0,
            "is_primary_mobile_no": 0 
            })
        if phone_number or landline_number:
            contact_doc.append("links",{
                "link_doctype":"Customer",
                "link_name":doc.name
                })
            try:
                contact_doc.flags.ignore_permissions = True
                contact_doc.save(ignore_permissions = True)
                frappe.db.commit()
            except:
                frappe.db.rollback()
                frappe.local.response.http_status_code = 417
                frappe.local.response["message"] = "Validation Failed"
    
        # try:
        #     contact_doc.save()
           
        #     # if contact_doc:
        #     #     doc.rename((contact_doc.mobile_no or "")+ "-" + (doc.customer_name or ""))
        #     #     doc.reload()
        #     # frappe.db.commit()
        #     return contact_doc
        # except:
        #     # if( frappe.local.response.http_status_code == 409):
        #     frappe.local.response["message"] = " Customer is already existing."
        #     # else :   
        #     #     frappe.local.response["message"] = e

        address_doc=frappe.new_doc("Address")
        address_doc.update(
            {
                "address_title": full_name,
                "address_line1":doorno,
                "address_line2":address,

                "city":districts,
                "is_primary_address":1,
                "state":state,
                "gst_state":state,  
                "pincode":pincode,
                "territory":territory,
                "links":[{"link_doctype":"Customer","link_name":doc.name}]
            })
        try:
            doc.flags.ignore_permissions = True

            doc.save(ignore_permissions = True)
            address_doc.flags.ignore_permissions = True
            address_doc.save(ignore_permissions = True)
            frappe.db.commit()
            
            if full_name:
                frappe.db.set_value("Customer", full_name, "customer_primary_address", address_doc.name)
                frappe.db.set_value("Customer", full_name, "customer_primary_contact", contact_doc.name)
               
            frappe.db.commit()
            frappe.local.response["message"]="Dealer Created."
            frappe.local.response["customer"]=doc.name
        except frappe.ValidationError as e:
            frappe.db.rollback()
            frappe.local.response.http_status_code = 417
            frappe.local.response["message"] = "Validation Failed"
    

        # except frappe.ValidationError as e:
        #     if(  frappe.local.response.http_status_code == 409):
        #         frappe.local.response["message"] = " Customer is already existing."
        #     else :   
        #         frappe.local.response["message"] = e
    else: 
        frappe.local.response.http_status_code = 408
        frappe.local.response["message"] = "Dealer is already existing."    


@frappe.whitelist()
def sales_order_status(doc_name):
    doc=frappe.get_doc("Sales Order",doc_name)
    doc.update({
        'workflow_state':"Delivered"
    })
    try:
        doc.save()
        frappe.db.commit()
        frappe.local.response["message"]="Sales Order Delivered"
    except frappe.ValidationError as e:
        frappe.db.rollback()
        frappe.local.response.http_status_code = 417
        frappe.local.response["message"] = "Validation Failed"

@frappe.whitelist( allow_guest=True)
def location_list():
    location=frappe.db.get_all("Customer",fields=["latitude","longitude","name","pincode"],filters={"latitude":["!=","0.0"],"longitude":["!=","0.0"],"pincode":["is","set"],})
    last_location=location[-25:]
    frappe.local.response['message']=last_location

# @frappe.whitelist( allow_guest=True)
# def customer_list():
#     customerlist=frappe.db.get_all("Customer",pluck="name")
#     frappe.local.response['message']=customerlistx``


@frappe.whitelist( allow_guest=True)
def notification():
    notification=frappe.db.get_all("Sales Order",pluck='name', filters={'workflow_state':'Draft','delivery_date':[">=",(date.today() - timedelta(days=3))]}) 
    frappe.local.response['message']=notification
    

@frappe.whitelist( allow_guest=True)
def Appointment_creation(usertype,date_time,customer_name,email,user,sales_executive=""):
    sales_executive=frappe.get_value("User",filters={"username":sales_executive},pluck="name")
    doc=frappe.new_doc("Appointment")
    doc.update({
        'scheduled_time':date_time,
        'customer_name':customer_name,
        'customer_email':email,
        'appointment_with':usertype,
        'party':customer_name
    })
   
    try:
        doc.save(ignore_permissions=True)

        frappe.db.commit()
        frappe.local.response["message"]="Appointment Scheduled"
        if user=="super":
            assign=frappe.new_doc("ToDo")
            assign.update({ 
            'description':f"Assignment for Appointment {doc.name}",
            'allocated_to':sales_executive,
            'reference_type':"Appointment",
            'reference_name':doc.name
            })
            assign.save()
            frappe.db.commit()
        
    except frappe.ValidationError as e:
        frappe.db.rollback()
        frappe.local.response.http_status_code = 417
        frappe.local.response["message"] = "Validation Failed"
    
@frappe.whitelist( allow_guest=True)
def appointment_notifications(username): 
    email=frappe.get_doc("User",{"full_name":username})
    appointment_notification=frappe.db.get_all("Appointment",fields=['name','scheduled_time'], filters={'status':'Open',"owner":email}, order_by="scheduled_time",limit=1) 
    frappe.local.response['message'] = appointment_notification
    # appointment()



@frappe.whitelist( allow_guest=True)
def notification_list(username):
    email=frappe.get_doc("User",{"full_name":username})
    
    notification=[]
    to_do=frappe.get_all("ToDo",filters={"status":'open',"allocated_to":email.name,"reference_type":"Appointment"},fields=["reference_name"])
    
    notification=frappe.get_all("Appointment",fields=["scheduled_time","name"],filters={'status':'open',"owner":email})
    for i in to_do:
        notification += frappe.get_all("Appointment",{"name":i.reference_name},["scheduled_time","name"])
      
    frappe.local.response['message']=notification
    # frappe.local.response['n']=notification
    # frappe.local.response['message']=notification_list

@frappe.whitelist()
def notification_status(name):
    doc=frappe.get_doc("Appointment",name)
    doc.status = "Completed"
    try:
        doc.save()
        frappe.db.commit()
        frappe.local.response['message']="Appointment Closed"
    except:
        frappe.local.response['message']="Please try again"

@frappe.whitelist(allow_guest=True)
def territory(state):
    territory=frappe.get_all("Territory",filters={"is_group":1,"parent_territory":state}, fields=["name"] )
    state=[]
    total_list = []
    # ter_list=[]
    temp={}

    for i in territory:
        
        state.append(i["name"])
    for j in state:
        ter_list=[]
        if j:
            # ter_list.append(i["parent_territory"])

            a = frappe.get_all("Territory",{"parent_territory":j}, "name")
            for x in a:
                ter_list.append(x["name"])
                   
        # total_list.append(ter_list)
        temp[j] = ter_list
    frappe.local.response["State"] = state
    frappe.local.response["Area"] = [temp]

@frappe.whitelist()
def area_list(latitude, longitude):
    if isinstance(latitude, str):
        try:
            latitude = float(latitude)
        except:
            frappe.log_error(f"API - area list {frappe.get_traceback()}")
            frappe.db.commit()
    if isinstance(longitude, str):
        try:
            longitude = float(longitude)
        except:
            frappe.log_error(f"API - area list {frappe.get_traceback()}")
            frappe.db.commit()
    
    radius = frappe.db.get_single_value("OXO Settings", "radius") or 0
    radius = radius / 110.574

    territory=frappe.get_all("Territory",filters=[
            ["is_group", '=', 0],
            ["latitude", ">=", latitude - radius],
            ["latitude", "<=", latitude + radius],
            ["longitude", ">=", longitude - radius],
            ["longitude", "<=", longitude + radius],
        ], fields=["name","latitude","longitude"] )
    # customer=frappe.get_all("Customer",filters["territory":])
    territory_names = [] 
    customer_name =[]
    for t in territory:
        territory_names.append(t.name)
        customers=frappe.get_all("Customer",filters={"territory":t.name},fields=["name"])
        for i in customers:
            i["territory"]=t.name
            i["latitude"]=t.latitude
            i["longitude"]=t.longitude
        customer_name.extend(customers)
    frappe.local.response["State"] = customer_name
    # frappe.local.response["State1"] = territory


@frappe.whitelist(allow_guest=True)
def sales_partner(area):
    name_=[]
    customer_name=[]
    districts=frappe.get_all("Territory",filters={"parent_territory":area}, pluck="name")
    for i in districts:
        customer=frappe.get_all("Customer",filters={"territory":i}, pluck="name")
        customer_name.extend(customer)
    sales_partner_list=frappe.get_all("Sales Partner",filters={"territory":area}, fields=["name" ] ) 
    for sales_partner in sales_partner_list:
        name_.append(sales_partner["name"])
    frappe.local.response["sales_partner"] = name_
    frappe.local.response["Dealer"] = customer_name
    # frappe.local.response["messege_3"] = districts


@frappe.whitelist()
def state_list():
    territory=frappe.get_all("Territory",filters={"parent_territory":"All Territories"}, pluck="name")
    territory_state=frappe.get_all("Territory",filters={"parent_territory":["in",territory]}, pluck="name")
    frappe.local.response["state"] = list(set(territory_state))

@frappe.whitelist()
def district_list():
    territory=frappe.get_all("Territory",filters={"parent_territory":"All Territories"}, pluck="name")
    territory_state=frappe.get_all("Territory",filters={"parent_territory":["in",territory]}, pluck="name")
    territory_=frappe.get_all("Territory",filters={"parent_territory":["in",territory_state]}, pluck="name")
    frappe.local.response["district_list"] = list(set(territory_))
    

@frappe.whitelist(allow_guest=True)

def category_list():
    category_list3=frappe.db.get_all("Item Group",fields=["name"],filters={"parent_item_group":"Mangai-Petticoats"})
    category_list1=frappe.db.get_all("Item Group",fields=["name"],filters={"parent_item_group":"Night Suits"})
    category_list2=frappe.db.get_all("Item Group",fields=["name"],filters={"parent_item_group":"Nighties"})
    frappe.local.response['message1']=category_list3
    frappe.local.response['message2']=category_list1
    frappe.local.response['message3']=category_list2
    
@frappe.whitelist(allow_guest =True)
def existing_customer(mobile_number):
      
    try:
        Contact=frappe.get_doc("Contact Phone",{'phone':mobile_number})
        # for i in Contact:
        #     Contact=frappe.get_doc("Contact Phone",{'phone':mobile_number})

        contact_cus=frappe.get_doc("Dynamic Link",{'parent':Contact.parent,'link_doctype':'Customer'})
        customer=frappe.get_all("Customer",filters={"name":contact_cus.link_name},fields=["name","customer_name","customer_group","territory","customer_primary_address"])
        if customer:
            address1=frappe.get_all("Address",filters={"name":customer[0].customer_primary_address},fields=["address_line1","address_line2","city","state","pincode"])        
            frappe.local.response["address"] =address1
            frappe.local.response['customer'] =customer    
            
            
    except:
           frappe.local.response["Message"]= "Contact"       

@frappe.whitelist()
def add_phone_number(contact_id, new_number,user):
    frappe.session.user=user
    try:
        contact_doc = frappe.get_doc("Contact", contact_id)

        contact_doc.append("phone_nos", {
            "phone" : new_number,
            "is_primary_phone" : 0,
            "is_primary_mobile_no" : 0 
        })
        contact_doc.flags.ignore_permissions = True
        contact_doc.save()
        frappe.db.commit()
        frappe.local.response['Message'] ="Mobile number added"   
    except:
        frappe.local.response['Message'] ="Mobile number added"

    
@frappe.whitelist()
def sales_order_list(distributor):
    email=frappe.get_doc("User",{"full_name":distributor})
    sales_order=frappe.db.get_all("Sales Order",fields=["name"],filters={"owner":email.name,"workflow_state":"Order"})
    Dispatched=frappe.db.get_all("Sales Order",fields=["name"],filters={"owner":email.name,"workflow_state":"Dispatched"})
    frappe.local.response['Order']=sales_order
    frappe.local.response['Dispatched']=Dispatched


@frappe.whitelist()
def dispatched(name,user):
    frappe.session.user=user
    frappe.db.set_value("Sales Order",name,"workflow_state", 'Complete')
    frappe.db.commit()
    frappe.local.response['Dispatched']="Complete"


@frappe.whitelist()
def attendance_(due_date,user_name,status,lat="",long="",doc_name=None,in_time=None,out_time=None):
    email=frappe.get_doc("User",{"full_name":user_name})
    employee=frappe.get_doc("Employee",{"user_id":email.name})
    
    # if(frappe.db.exists("Attendance", {"employee":employee.employee,
    #         "attendance_date":due_date or nowdate(),
    #         "status":status,'docstatus':['!=', 2]})):
    #         return "Already Exists"

    if doc_name:
        doc_name=frappe.get_doc("Attendance",doc_name)
        doc_name.update(
        {
          
            "attendance_date":due_date or nowdate(),
            "out_time":out_time,
            "status":status,
            "lat":lat,
            "long":long,
            "total_working_hours": time_diff_in_hours(out_time, doc_name.in_time)
            
        })
    
        doc_name.save()
        doc_name.submit()
        frappe.local.response["1"]="1"
        

    else :
        doc=frappe.new_doc("Attendance")
        doc.update(
            {
                "employee":employee.employee,
                "attendance_date":due_date or nowdate(),
                "in_time":in_time,
                "status":status,
                "lat":lat,
                "long":long,
                
            })
        doc.save()
        frappe.local.response["Attendance"]=doc.name
       
    frappe.db.commit()
    frappe.local.response['message']="Attendance and successfully"
   
   


