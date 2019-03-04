# REF: https://github.com/python-telegram-bot/python-telegram-bot/wiki

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import logging
import callback

updater = Updater(token="SUP3R S3CR3T K3Y")
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# handler for when users enter "start" on the bot
start_handler = CommandHandler("start", callback.start)
echo_handler = MessageHandler(Filters.text, callback.echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

print("Bot is running - press ctrl + c to stop the bot")
updater.start_polling()

# Another way to shutdown the bot other than ctrl+c? 
# ref: https://github.com/python-telegram-bot/python-telegram-bot/issues/801
updater.idle()