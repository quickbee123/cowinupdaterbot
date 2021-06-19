from telegram.ext import ConversationHandler
from actions.inline_keyboard import keyboard
from constants import buttons,states



def get_age(update,context):

    context.user_data["preference"]={}

    reply_markup = keyboard(buttons.AGE_BUTTONS,3)
    update.message.reply_text('Choose preferences to filter updates')
    update.message.reply_text('Select preferred age',reply_markup=reply_markup)

    return states.DOSE



def get_dose(update,context):

    query = update.callback_query
    query.answer()

    context.user_data["preference"]["age"]= query.data

    reply_markup = keyboard(buttons.DOSE_BUTTONS,3)
    query.edit_message_text('Select dose number',reply_markup=reply_markup)

    return states.VACCINE



def get_vaccine(update,context):

    query = update.callback_query
    query.answer()

    context.user_data["preference"]["dose"]= query.data

    reply_markup = keyboard(buttons.VACCINE_BUTTONS,2)
    query.edit_message_text('Select preferred vaccine',reply_markup=reply_markup)

    return states.FEE



def get_fee(update,context):

    query = update.callback_query
    query.answer()

    context.user_data["preference"]["vaccine"]= query.data

    reply_markup = keyboard(buttons.FEE_BUTTONS,3)
    query.edit_message_text('Select fee',reply_markup=reply_markup)

    return states.INTERVAL


def get_interval(update,context):

    query = update.callback_query
    query.answer()

    context.user_data["preference"]["fee"]= query.data

    reply_markup = keyboard(buttons.INTERVAL_BUTTONS,1)
    query.edit_message_text('Select update interval',reply_markup=reply_markup)

    return states.UPDATED  




def preference_added(update,context):

    query = update.callback_query
    query.answer()

    context.user_data["preference"]["interval"]= query.data

    pref = context.user_data["preference"]

    if pref.get("age",0) and pref.get("dose",0) and pref.get("vaccine",0) and pref.get("fee",0):
        db = context.bot_data["database"]
        id = update.effective_user.id
        db.set_preference(pref,id)
        query.edit_message_text('Preference updated!!')

    else:
        query.edit_message_text('Some error occurred.\n\nSend /add to add entry')
     
    return ConversationHandler.END



def inactive(update,context):
    query = update.callback_query
    query.answer()

    query.delete_message()   
    return ConversationHandler.END    
    