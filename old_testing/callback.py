def start(bot, update):
    chat_id = update.message.chat_id
    text = """
            Hello! Welcome to the ESD Stock Bot!
            """

    bot.send_message(chat_id=chat_id, text="lelel")

def echo(bot, update):
    chat_id = update.message.chat_id
    # the message from the user
    user_message = update.message.text

    bot.send_message(chat_id=chat_id, text=user_message)

