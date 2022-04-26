#!/usr/bin/env python3

import memes
import logging
import os
import secret  # See secret_template.py
import secrets
from telegram import Chat, ChatMember, ChatMemberUpdated, ParseMode, Update
from telegram.ext import (
    CallbackContext,
    ChatMemberHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

logger = logging.getLogger(__name__)

MEMES = None
BOT = None


def cmd_trap(update: Update, _context: CallbackContext) -> None:
    with open(MEMES.fetch_random_accepted(), 'rb') as fp:
        update.effective_message.reply_photo(fp, caption="It's a /trap!")


def cmd_start(update: Update, _context: CallbackContext) -> None:
    update.effective_message.reply_text(
        f'Hi {update.effective_user.first_name}!'
        f'\nJedes Mal wenn jemand /trap schreibt, dann antworte ich mit einem "It\'s a trap!" meme.'
        f'\nSchicke mir im Privatchat ein Bild, dann wird es (irgendwann) als Meme verwendet :D'
    )


def cmd_summary(update: Update, _context: CallbackContext) -> None:
    if update.effective_user.username != secret.OWNER:
        return

    update.effective_message.reply_text(f'Im Moment gibt es {MEMES.len_suggested()} vorgeschlagene und {MEMES.len_accepted()} akzeptierte Memes.')


def cmd_accept_reject(update: Update, _context: CallbackContext) -> None:
    if update.effective_user.username != secret.OWNER:
        return

    text = update.message.text

    if text.startswith('/accept_'):
        text = text[len('/accept_'):]
        errmsg = MEMES.do_accept(text)
        if errmsg is None:
            update.effective_message.reply_text('Success!')
        else:
            update.effective_message.reply_text(f'Failure! {errmsg}')
    elif text.startswith('/reject_'):
        text = text[len('/reject_'):]
        errmsg = MEMES.do_reject(text)
        if errmsg is None:
            update.effective_message.reply_text('Success!')
        else:
            update.effective_message.reply_text(f'Failure! {errmsg}')


def cmd_receive_pic(update: Update, _context: CallbackContext) -> None:
    if len(update.message.photo) == 0:
        update.message.reply_text(
            'Hmm? Schick mir einfach ein Bild zu, um es vorzuschlagen.'
        )
        return

    photo_file = update.message.photo[-1].get_file()
    hexname = secrets.token_hex(24)  # Longer is too long for telegram commands
    incoming_name = f'trap_pics/incoming/{hexname}.jpg'
    if os.path.exists(incoming_name):
        raise AssertionError('wtf')
    logger.info(f'Downloading meme from user @{update.effective_user.username} into {incoming_name}')
    photo_file.download(incoming_name)
    assert os.path.exists(incoming_name)
    suggested_name = f'trap_pics/suggested/{hexname}.jpg'
    logger.info(f'Success! Moving to {suggested_name}')
    os.rename(incoming_name, suggested_name)
    MEMES.do_suggest(hexname)
    update.message.reply_text(
        'Awesome! Vielleicht werde ich das bald verwenden. Sorry, es wird kein Feedback darüber geben, das war mir zu kompliziert zu implementieren.'
    )
    BOT.send_photo(secret.OWNER_ID, photo_file.file_id, caption=f'New meme from @{update.effective_user.username}! Click /accept_{hexname} to accept, or /reject_{hexname} to reject.')


def init_memes():
    global MEMES
    MEMES = memes.Storage()


def run():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Alive")

    init_memes()

    # Create the Updater and pass it your bot's token.
    updater = Updater(secret.TOKEN)
    global BOT
    BOT = updater.bot

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', cmd_start))
    dispatcher.add_handler(CommandHandler('trap', cmd_trap))
    dispatcher.add_handler(CommandHandler('summary', cmd_summary))

    dispatcher.add_handler(MessageHandler(~Filters.text & ~Filters.command, cmd_receive_pic))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.command, cmd_accept_reject))

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
