#!/usr/bin/env python3

import memes
import logging
import os
import secret  # See secret_template.py
import secrets
from telegram import Chat, ChatMember, ChatMemberUpdated, Update
from telegram.ext import (
    Application,
    CallbackContext,
    ChatMemberHandler,
    CommandHandler,
    filters,
    MessageHandler,
    Updater,
)

logger = logging.getLogger(__name__)

MEMES = None
BOT = None


def cmd_trap(update: Update, _context: CallbackContext) -> None:
    with open(MEMES.fetch_random_accepted(), 'rb') as fp:
        update.effective_message.reply_photo(fp, caption="It's a /trap!\n\n(Übrigens, du kannst mir neue Bilder einfach so zuschicken!)")


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
        # FIXME: In group chats, just silently ignore.
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

    application = Application.builder().token(secret.TOKEN).build()
    global BOT
    BOT = application.bot

    application.add_handler(CommandHandler('start', cmd_start))
    application.add_handler(CommandHandler('trap', cmd_trap))
    application.add_handler(CommandHandler('summary', cmd_summary))

    application.add_handler(MessageHandler(filters.PHOTO, cmd_receive_pic))
    application.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, cmd_accept_reject))

    logger.info("Begin idle loop")
    # ALL_TYPES = ['message', 'edited_message', 'channel_post', 'edited_channel_post', 'inline_query', 'chosen_inline_result', 'callback_query', 'shipping_query', 'pre_checkout_query', 'poll', 'poll_answer', 'my_chat_member', 'chat_member', 'chat_join_request']
    # However, we're only interested in actual messages.
    application.run_polling(allowed_updates=['message'])


if __name__ == '__main__':
    run()
