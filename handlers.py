from telegram.ext import Handler,CommandHandler, ConversationHandler, Filters, MessageHandler, CallbackQueryHandler


from actions.start import start
from actions.show import show
from actions.entry import *
from actions.preference import *
from actions.remove import *

from constants import states


handlers = {
    CommandHandler: [
        ({"command":["start","help","h"],"callback":start},),
        ({"command":["show"],"callback":show},)
    ],
    ConversationHandler: [
        ({
            "entry_points":[CommandHandler('add',get_searchby)],
            "states":{
                states.STATEORPIN : [
                    CallbackQueryHandler(get_state,pattern='^1$'),
                    CallbackQueryHandler(get_pincode,pattern='^2$')
                ],
                states.GETDISTRICT : [CallbackQueryHandler(get_district)],
                states.SETPINCODE : [MessageHandler(Filters.text & ~Filters.command,set_pincode)],
                states.SETDISTRICT : [CallbackQueryHandler(set_district)],
                ConversationHandler.TIMEOUT : [CallbackQueryHandler(timeout)]
            },
            "fallbacks": [
                CommandHandler('add',get_searchby),
                CommandHandler('cancel',cancel)],
            "conversation_timeout": 300
        },),
        ({
            "entry_points":[CommandHandler('preference',get_age)],
            "states":{
                states.DOSE : [CallbackQueryHandler(get_dose)],
                states.VACCINE : [CallbackQueryHandler(get_vaccine)],
                states.FEE : [CallbackQueryHandler(get_fee)],
                states.INTERVAL : [CallbackQueryHandler(get_interval)],
                states.UPDATED: [CallbackQueryHandler(preference_added)],
                ConversationHandler.TIMEOUT : [CallbackQueryHandler(inactive)]
            },
            "fallbacks": [CommandHandler('preference',get_age)],
            "conversation_timeout": 300
        },),
        ({
            "entry_points":[CommandHandler('remove',get_entry_to_remove)],
            "states":{
                states.REMOVE : [CallbackQueryHandler(remove_entry)]
            },
            "fallbacks": [
                CommandHandler('remove',get_entry_to_remove)],
            "conversation_timeout": 300
        },)
    ]
}