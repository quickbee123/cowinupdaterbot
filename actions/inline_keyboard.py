from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def keyboard(buttons:dict, columns:int):
    keyboard = []
    row=[]
    count = 0
    for name,data in buttons.items():
        count+=1
        row.append(InlineKeyboardButton(name,callback_data=data))
        if count ==columns:
            keyboard.append(row)
            count=0
            row=[]

    reply_markup = InlineKeyboardMarkup(keyboard)    
    return reply_markup
