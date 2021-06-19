from telegram.ext import ConversationHandler
from actions.inline_keyboard import keyboard
from constants import buttons,states,API_data_districts



def get_entry_to_remove(update,context):

    db = context.bot_data["database"]
    id = update.effective_user.id

    remove_buttons={}
    districts = db.get_districts_for_user(id)
    pincodes = db.get_pincodes_for_user(id)

    districts_data = API_data_districts.districts_data

    for district in districts:
        name = "District : " + districts_data[str(district[0])]
        remove_buttons[name]= str(district[0])

    for pincode in pincodes:
        remove_buttons["Pincode : " + str(pincode[0])]= str(pincode[0])    

    if len(remove_buttons) != 0:    

        reply_markup = keyboard(remove_buttons,1)
        update.message.reply_text('Choose entry to be removed',reply_markup=reply_markup)
        return states.REMOVE

    else:
        update.message.reply_text('No entries to be removed\n\nSend /add to add entry')
        return ConversationHandler.END


def remove_entry(update,context):

    query = update.callback_query
    query.answer()

    db = context.bot_data["database"]
    id = update.effective_user.id

    if len(query.data) == 6:
        db.remove_pincode(id,int(query.data))

    else:
       db.remove_district(id,int(query.data))     


    query.edit_message_text('Removed Successfully!!')

     
    return ConversationHandler.END


    