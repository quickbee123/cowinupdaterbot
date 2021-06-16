from telegram.ext import ConversationHandler
from actions.inline_keyboard import keyboard
from constants import buttons,states,API_data



def get_age(update,context):

    reply_markup = keyboard(buttons.AGE_BUTTONS,3)
    update.message.reply_text('Choose preferences to filter updates')
    update.message.reply_text('Select preferred age',reply_markup=reply_markup)

    return states.DOSE



def get_dose(update,context):

    query = update.callback_query
    query.answer()

    reply_markup = keyboard(buttons.DOSE_BUTTONS,3)
    query.edit_message_text('Select dose number',reply_markup=reply_markup)

    return states.VACCINE



def get_vaccine(update,context):

    query = update.callback_query
    query.answer()

    reply_markup = keyboard(buttons.VACCINE_BUTTONS,2)
    query.edit_message_text('Select preferred vaccine',reply_markup=reply_markup)

    return states.FEE



def get_fee(update,context):

    query = update.callback_query
    query.answer()

    reply_markup = keyboard(buttons.FEE_BUTTONS,3)
    query.edit_message_text('Select fee',reply_markup=reply_markup)

    return states.UPDATED  




def preference_added(update,context):

    query = update.callback_query
    query.answer()

    query.edit_message_text('Preference updated!!')  
    return ConversationHandler.END



def inactive(update,context):
    query = update.callback_query
    query.answer()

    query.delete_message()   
    return ConversationHandler.END    
    