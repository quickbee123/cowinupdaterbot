from telegram.ext import ConversationHandler
from actions.inline_keyboard import keyboard
from constants import buttons,states,API_data_states,API_data_districts



def get_searchby(update,context):

    db = context.bot_data["database"]
    id = update.message.from_user.id
    count = db.get_entries_count(id)[0]

    if count == 5:
        update.message.reply_text('You can add only 5 entries maximum. Remove an entry and add a new one\n\nSend /remove to remove an entry')
        return ConversationHandler.END   


    reply_markup = keyboard(buttons.SEARCHBY_BUTTONS,2)
    update.message.reply_text('Choose region to get updates on vaccine availability\nSend /cancel to cancel')
    update.message.reply_text('Search by',reply_markup=reply_markup)

    return states.STATEORPIN



def get_state(update,context):

    query = update.callback_query
    query.answer()

    states_data = API_data_states.states_data
    state_buttons={}

    for id,state in states_data.items():
        state_buttons[state["state_name"]]=id

    reply_markup = keyboard(state_buttons,3)
    query.edit_message_text('Choose state',reply_markup=reply_markup) 

    return states.GETDISTRICT



def get_district(update,context):

    query = update.callback_query
    query.answer()

    state_id = query.data
    states_data = API_data_states.states_data
    districts = API_data_districts.districts_data
    district_ids = states_data[state_id]["districts"]
    district_buttons={}

    for id in district_ids:
        district_buttons[districts[id]]= id

    reply_markup = keyboard(district_buttons,3)
    query.edit_message_text('Choose district',reply_markup=reply_markup)  

    return states.SETDISTRICT       



def get_pincode(update,context):

    query = update.callback_query
    query.answer()

    query.edit_message_text('Send pincode')    

    return states.SETPINCODE



def set_pincode(update,context):

    
    pincode = update.message.text
    if len(pincode) != 6:
        update.message.reply_text('Please enter a valid pincode')  
        return states.SETPINCODE

    else:
        db = context.bot_data["database"]
        id = update.message.from_user.id
        db.add_entry(2,id,int(pincode))

        update.message.reply_text('Entry added successfully')  
        return ConversationHandler.END  



def set_district(update,context):

    query = update.callback_query
    query.answer()

    db = context.bot_data["database"]
    id = update.effective_user.id
    district_id = int(query.data)
    db.add_entry(1,id,district_id)

    query.edit_message_text('Entry added successfully')  
    return ConversationHandler.END      



def cancel(update,context):
    update.message.reply_text('Canceled current operation')  
    return ConversationHandler.END



def timeout(update,context):
    query = update.callback_query
    query.answer()

    query.delete_message()   
    return ConversationHandler.END    
    