from constants import api
import requests
from datetime import datetime
import time
import pytz
import telegram


DEFAULT_MSG_DATA_LEN = 66

def update(context):

    db=  context.job.context
    data = get_sessions(db)
    send_update_to_user(context.bot,db,data)


def get_sessions(db):

    data = { "districts" : {} , "pincodes" : {} }

    districts = db.get_districts()
    pincodes = db.get_pincodes()

    date = datetime.today().strftime('%d-%m-%Y')
    count = 0

    for district in districts:
        params = {
            "district_id" : district[0],
            "date" : date
        }

        while True:

            if count == api.API_CALLS_COUNT:
                time.sleep(api.API_CALLS_INTERVAL)
                count=0

            count+=1    
            response = requests.get(api.SEARCH_BY_DISTRICT_URL,params=params,headers=api.HEADERS)
            if response.status_code == requests.codes.ok : 
                break

        data["districts"][str(district[0])] = response.json()["centers"] 


    for pincode in pincodes:
        params = {
            "pincode" : pincode[0],
            "date" : date
        }

        while True:

            if count == api.API_CALLS_COUNT:
                time.sleep(api.API_CALLS_INTERVAL)
                count=0

            count+=1    
            response = requests.get(api.SEARCH_BY_PINCODE_URL,params=params,headers=api.HEADERS)
            if response.status_code == requests.codes.ok : 
                break

        data["pincodes"][str(pincode[0])] = response.json()["centers"]     


    return data 


def send_update_to_user(bot,db,data):

    IST = pytz.timezone('Asia/Kolkata')
    users = db.get_users()

    for user in users:

        last_sent = user[2]
        now = datetime.now(IST).replace(tzinfo=None)
        UPDATE_INTERVAL = [0.5,1,12,24]
        interval = UPDATE_INTERVAL[user[3]]
        difference = (now - last_sent).seconds / 60

        if difference >= interval*60:

            id = user[1]
            districts = db.get_districts_for_user(id)
            pincodes = db.get_pincodes_for_user(id)

            centers = filter_centers(data,districts,pincodes,user[4:8])
            send_message(db,bot,id,centers,now)


def filter_centers(data,districts,pincodes,pref):

    center_ids = []
    centers = []
    filtered_centers = []

    for district in districts:
        district_centers = data["districts"][str(district[0])]
        for center in district_centers:
            centers.append(center)
            center_ids.append(center["center_id"])

    for pincode in pincodes:
        pincode_centers = data["pincodes"][str(pincode[0])]
        for center in pincode_centers:
            if center["center_id"] not in centers:
                centers.append(center)
                center_ids.append(center["center_id"])  

    (age,dose,vaccine,fee) = pref


    for center in centers:
        if fee==0 or (fee==1 and center["fee_type"]=="Free") or (fee==2 and center["fee_type"]=="Paid"):
            if center.get("sessions",0):
                for session in center["sessions"]:
                    if age==0 or (age==1 and session["min_age_limit"]==18) or (age==2 and (session["min_age_limit"]==40 or session["min_age_limit"]==45)):
                        if vaccine==0 or (vaccine==1 and session["vaccine"]=="COVISHIELD") or (vaccine==2 and session["vaccine"]=="COVAXIN") or (vaccine==3 and session["vaccine"]=="SPUTNIK"):
                            if (dose==0 and (session["available_capacity_dose1"]>0 or session["available_capacity_dose2"]>0)) or (dose==1 and session["available_capacity_dose1"]>0) or (dose==2 and session["available_capacity_dose2"]>0):
                                new_center = center
                                del new_center["sessions"]
                                new_center["session"] = session
                                filtered_centers.append(new_center)
                                break

    return filtered_centers                    


def send_message(db,bot,user_id,centers,now):

    message = format_message(centers)


    if len(message) > DEFAULT_MSG_DATA_LEN:
        
        try:
            bot.send_message(user_id,message,parse_mode="HTML")
            db.update_last_sent(user_id,now)
        except telegram.error.Unauthorized:
            db.remove_user(user_id)


def format_message(centers):
    text = "<b>COWIN VACCINE AVAILABILITY</b>\n\n"

    for center in centers:
        add_text = (f'<b>{center["name"]}</b>\n'
        f'{center["district_name"]}, {center["pincode"]}\n'
        f'{center["session"]["vaccine"]} | {center["session"]["min_age_limit"]}+ | {center["fee_type"]}\n'
        f'DATE : {center["session"]["date"]}\n'
        f'DOSE 1 : {center["session"]["available_capacity_dose1"]} | DOSE 2 : {center["session"]["available_capacity_dose2"]}\n\n')
        

        if len(text+add_text) > 4096:
            text=text+ "<i>Some results are not shown due to message length limit. Add entries more specifically to get better results</i>\n\n"
            break
        else:
            text=text+add_text    

        

    text = text+"Schedule Vaccine : cowin.gov.in"  

    return text


    



        


