def delete(update, context):
    db = context.bot_data["database"]
    id = update.message.from_user.id
    db.delete_details(id)
    text = ('Your details have been deleted successfully. You will no longer get updates\n\nSend /add to add an entry')
    update.message.reply_text(text)