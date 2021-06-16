from uuid import uuid4
from telegram import InlineQueryResultCachedSticker
from db.database import Database


def inlinequery(update, context):

    db = context.bot_data["database"]
    stickers = db.get_stickers()
    results=[]

    for item in stickers:
       results.append(
           InlineQueryResultCachedSticker(
            id=str(uuid4()),
            sticker_file_id=item[1]
            
        )
       )
    
    
    update.inline_query.answer(results,auto_pagination=True)    