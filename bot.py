#!/usr/bin/env python3

import memes
import logging
import secret  # See secret_template.py
import secrets
from telegram import Chat, ChatMember, ChatMemberUpdated, ParseMode, Update
from telegram.ext import CallbackContext, ChatMemberHandler, CommandHandler, Updater


logger = logging.getLogger(__name__)

MEMES = None


def cmd_trap(update: Update, _context: CallbackContext) -> None:
    #if update.effective_user.username != secret.OWNER:
    #    return

    update.effective_message.reply_text('Noch kann ich das nicht.')


def cmd_start(update: Update, _context: CallbackContext) -> None:
    update.effective_message.reply_text(
        f'Hi {update.effective_user.first_name}!'
        f'\nJedes Mal wenn jemand /trap schreibt, dann antworte ich mit einem "It\'s a trap!" meme.'
        f'\nSchicke mir im Privatchat ein Bild, dann wird es (irgendwann) als Meme verwendet :D'
    )


def init_memes():
    global MEMES
    MEMES = memes.Storage()


def run():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Alive")

    init_memes()

    # Create the Updater and pass it your bot's token.
    updater = Updater(secret.TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', cmd_start))
    dispatcher.add_handler(CommandHandler('trap', cmd_trap))

    # Start the Bot
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    updater.start_polling(allowed_updates=Update.ALL_TYPES)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    logger.info("Begin idle loop")
    updater.idle()


if __name__ == '__main__':
    run()
