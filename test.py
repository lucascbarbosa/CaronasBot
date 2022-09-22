
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

def ajuda(bot, update):
    response_message = 'Olá.'
    bot.sendMessage(chat_id=update.message.chat_id,
                        text=response_message, disable_web_page_preview=True)

def main():
    
    # Create the Updater and pass it your bot's token.
    token = '5725480727:AAEi6lXGnvJzQMPm0R76Uss8HWtdhnmWdFY'

    # initiliaze class that contains the callback functions for caronas
    updater = Updater(token=token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(
            CommandHandler('help', ajuda)
        )

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()

