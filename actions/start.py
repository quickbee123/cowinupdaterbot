def start(update, context):
    db = context.bot_data["database"]
    id = update.message.from_user.id
    db.add_user(id)
    text = ('This bot updates you whenever a slot is available matching your entries and preference\n\n'
           '/add - To add an entry\n'
           '/remove - To remove an entry\n'
           '/show - To show all entries\n'
           '/preference - To set preferneces\n'
           )
    update.message.reply_text(text)