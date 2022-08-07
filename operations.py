import json
import string
import random
from json import JSONDecodeError
from datetime import datetime,date

def AutoGenerate_EventID():
    #generate a random Event ID
    Event_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=3))
    return Event_ID

def Register(type,member_json_file,organizer_json_file,Full_Name,Email,Password):
    '''Register the member/ogranizer based on the type with the given details'''
    if type.lower()=='organizer':
        f=open(organizer_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Email":Email,
            "Password":Password
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()
    else:
        f=open(member_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Email":Email,
            "Password":Password
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()


def Login(type,members_json_file,organizers_json_file,Email,Password):
    '''Login Functionality || Return True if successful else False'''
    d=0
    if type.lower()=='organizer':
        f=open(organizers_json_file,'r+')
    else:
        f=open(members_json_file,'r+')
    try:
        content=json.load(f)
    except JSONDecodeError:
        f.close()
        return False
    for i in range(len(content)):
        if content[i]["Email"]==Email and content[i]["Password"]==Password:
            d=1
            break
    if d==0:
        f.close()
        return False
    f.close()
    return True

def Create_Event(org,event_json_file,Event_ID,Event_Name,Start_Date,Start_Time,End_Date,End_Time,Users_Registered,Capacity,Availability):
    '''Create an Event with the details entered by organizer'''
    detail_of_event={
        "ID": Event_ID,
        "Name": Event_Name,
        "Organizer":org,
        "Start Date": Start_Date,
        "Start Time":Start_Time,
        "End Date":End_Date,
        "End Time":End_Time,
        "Users Registered": Users_Registered,
        "Capacity": Capacity,
        "Seats Available": Availability,
        }
    file=open(event_json_file,'r+')
    try:
        content=json.load(file)
        if detail_of_event not in content:
            content.append(detail_of_event)
            file.seek(0,0)
            file.truncate()
            json.dump(content,file)
    except JSONDecodeError:
        lst=[]
        lst.append(detail_of_event)
        json.dump(lst,file)
    file.close()
    return True
    

def View_Events(org,event_json_file):
    '''Return a list of all events created by the logged in organizer'''
    Detail_of_Event=[]
    file=open(event_json_file,'r+')
    content=json.load(file)
    for i in range(len(content)):
        if content[i]["Organizer"]==org:
            Detail_of_Event.append(content[i])
            continue
    file.close()
    return Detail_of_Event
    

def View_Event_ByID(event_json_file,Event_ID):
    '''Return details of the event for the event ID entered by user'''
    Detail_of_Event=[]
    file=open(event_json_file,'r+')
    content=json.load(file)
    for i in range(len(content)):
        if content[i]["ID"]==Event_ID:
            Detail_of_Event.append(content[i])
            break
    file.close()
    return Detail_of_Event
    

def Update_Event(org,event_json_file,event_id,detail_to_be_updated,updated_detail):
    '''Update Event by ID || Take the key name to be updated from member, then update the value entered by user for that key for the selected event
    || Return True if successful else False'''
    file=open(event_json_file,'r+')
    content=json.load(file)
    for i in range(len(content)):
        if content[i]["ID"]==event_id:
            try:
                a=content[i][detail_to_be_updated]
            except KeyError:
                return False
            content[i][detail_to_be_updated]=updated_detail
            file.seek(0,0)
            file.truncate()
            json.dump(content,file)
            file.close()
            return True
    file.close()
    return False
    

def Delete_Event(org,event_json_file,event_ID):
    '''Delete the Event with the entered Event ID || Return True if successful else False'''
    file=open(event_json_file,'r+')
    content=json.load(file)
    for i in range(len(content)):
        if content[i]['Organizer']==org and content[i]["ID"]==event_ID:
            del content[i]
            file.seek(0,0)
            file.truncate()
            json.dump(content,file)
            file.close()
            return True
        else:
            pass
    file.close()


def Register_for_Event(event_json_file,event_id,Full_Name):
    '''Register the logged in member in the event with the event ID entered by member. 
    (append Full Name inside the "Users Registered" list of the selected event)) 
    Return True if successful else return False'''
    date_today=str(date.today())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    '''Write your code below this line'''
    file=open(event_json_file,'r+')
    content=json.load(file)
    for i in range(len(content)):
        print(content[i])
        if content[i]["ID"]==event_id:
            print("YES")

            try:
                content[i]["Users Registered"]=content[i]["Users Registered"]+[Full_Name]

                file.seek(0,0)
                file.truncate()
                json.dump(content,file)
                file.close()
                return True
            except KeyError:
                return False
        else:
            pass
    file.close()
       

def fetch_all_events(event_json_file,Full_Name,Event_Details,upcoming_ongoing):
    '''View Registered Events | Fetch a list of all events of the logged in memeber'''
    '''Append the details of all upcoming and ongoing events list based on the today's date/time and event's date/time'''
    date_today=str(date.today())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    '''Write your code below this line'''
    Event_Details = []
    file = open(event_json_file, "r+")
    content = json.load(file)
    for i in range(len(content)):
        if Full_Name in content[i]["Users Registered"]:
            if date_today<content[i]["Start Date"] and current_time<=content[i]["Start Time"]:
                upcoming_ongoing.append(content[i])
            elif date_today>=content[i]["End Date"] and current_time>=content[i]["End Time"]:
                upcoming_ongoing.append(content[i])
            else:
                Event_Details.append(content[i])
    file.close()
    return Event_Details

def Update_Password(members_json_file,Full_Name,new_password):
    '''Update the password of the member by taking a new passowrd || Return True if successful else return False'''
    file=open(members_json_file,'r+')
    content=json.load(file)
    for i in range(len(content)):
        for i in range(len(content)):
            if content[i]["Full Name"]==Full_Name:
                content[i]["Password"]=new_password
                file.seek(0)
                file.truncate()
                json.dump(content, file)
                file.close()
        return True

def View_all_events(events_json_file):
    '''Read all the events created | DO NOT change this function'''
    '''Already Implemented Helper Function'''
    details=[]
    f=open(events_json_file,'r')
    try:
        content=json.load(f)
        f.close()
    except JSONDecodeError:
        f.close()
        return details
    for i in range(len(content)):
        details.append(content[i])
    return details
