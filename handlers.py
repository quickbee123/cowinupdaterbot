from telegram.ext import Handler,CommandHandler, InlineQueryHandler, ConversationHandler, Filters, MessageHandler, CallbackQueryHandler


from actions.start import start
from actions.entry import *
from actions.preference import *
from actions.inlinequery import inlinequery

from constants import states


handlers = {
    CommandHandler: [
        ({"command":["start","help","h"],"callback":start},),
    ],
    InlineQueryHandler: [
        ({"callback":inlinequery},)
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
                states.UPDATED: [CallbackQueryHandler(preference_added)],
                ConversationHandler.TIMEOUT : [CallbackQueryHandler(inactive)]
            },
            "fallbacks": [CommandHandler('preference',get_age)],
            "conversation_timeout": 300
        },)
    ]
}