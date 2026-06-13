from telegram import (
Update,
InlineKeyboardButton,
InlineKeyboardMarkup
)

from telegram.ext import *

from config import TOKEN
from downloader import download

import os


async def start(update,context):

    await update.message.reply_text(
    "Instagram link bhejo 🔥"
    )



async def link(update,context):

    url=update.message.text

    context.user_data["url"]=url


    kb=[
    [
    InlineKeyboardButton(
    "🎬 Video",
    callback_data="video"
    ),

    InlineKeyboardButton(
    "🎵 Audio",
    callback_data="audio"
    )
    ]
    ]


    await update.message.reply_text(
    "Select:",
    reply_markup=InlineKeyboardMarkup(kb)
    )



async def button(update,context):

    q=update.callback_query

    await q.answer()


    await q.edit_message_text(
    "Downloading..."
    )


    url=context.user_data["url"]

    file=download(
    url,
    q.data
    )


    if q.data=="video":

        await q.message.reply_video(
        open(file,"rb")
        )

    else:

        await q.message.reply_audio(
        open(file,"rb")
        )


    os.remove(file)



app=Application.builder().token(TOKEN).build()


app.add_handler(
CommandHandler("start",start)
)


app.add_handler(
MessageHandler(
filters.TEXT,
link
)
)


app.add_handler(
CallbackQueryHandler(button)
)


print("RUNNING")


app.run_polling()