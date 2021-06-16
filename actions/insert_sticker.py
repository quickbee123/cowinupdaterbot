import logging
from telegram.ext import ConversationHandler

import os
from dotenv import load_dotenv

load_dotenv()

def add_sticker(update, context):

    DEVELOPER_ID = int(os.getenv('DEV_ID'))
    id = update.message.from_user.id
    

    if DEVELOPER_ID == id:
        update.message.reply_text(
            'Send me the ID of sticker to be added \n\nSend /cancel to stop'
        )

        return 1

    else:    
        update.message.reply_text(
            'Only the developer is authorized to add stickers to this bot'
        )
        return ConversationHandler.END


def get_sticker_id(update,context):

    sticker_id = update.message.text

    db = context.bot_data["database"]
    stickers = db.add_sticker(sticker_id)
    update.message.reply_text(
            'Sticker added successfully!'
    )

    return 1


def cancel(update,context):

    update.message.reply_text(
            'Finished adding stickers'
    )
    return ConversationHandler.END
    

