from constants.queries import UPDATE_LAST_SENT
from constants import API_data_districts

def show(update, context):
    db = context.bot_data["database"]
    id = update.effective_user.id

    districts = db.get_districts_for_user(id)
    pincodes = db.get_pincodes_for_user(id)
    data = "<b>Entries</b>\n\n"
    count=0

    districts_data = API_data_districts.districts_data

    for district in districts:
        count+=1
        name = str(count) + ". " + districts_data[str(district[0])] + " (District)\n"
        data = data+name

    for pincode in pincodes:
        count+=1
        name = str(count) + f". <i>{str(pincode[0])}</i>" + " (Pincode)\n"
        data = data+name

    if count == 0:
        data = data + "<i>No entries yet</>\n"


    pref = db.get_pref_for_user(id) 
 
    AGE = ["Both","18+","45+"]
    DOSE = ["Both","1","2"]
    VACCINE = ["Any","Covishield","Covaxine","Sputnik"]
    FEE = ["Both","Free","Paid"]
    UPDATE_INTERVAL = ["Every 30 minutes","Every 1 hour","Every 12 hours","Every 24 hours"]
 

    
    pref_text = ('\n<b>Preferences</b>\n\n'
                 f'Age  : {AGE[pref[0]]}\n'
                 f'Dose : {DOSE[pref[1]]}\n'
                 f'Vaccine : {VACCINE[pref[2]]}\n'
                 f'Fee : {FEE[pref[3]]}\n'
                 f'Update Interval : {UPDATE_INTERVAL[pref[4]]}\n\n')
 
    
    update.message.reply_text(data+pref_text+"Send /add to add an entry\nSend /remove to remove an entry",parse_mode="HTML")