from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import TOKEN
from downloader import download

import os
import asyncio


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 Instagram Downloader Bot\n\n"
        "Reel link bhejo 👇\n\n"
        "🎬 Video = High Quality\n"
        "🎵 Audio = 320kbps"
    )



async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()


    if "instagram.com" not in url:

        await update.message.reply_text(
            "❌ Valid Instagram link bhejo"
        )

        return


    context.user_data["url"] = url


    buttons = [

        [
            InlineKeyboardButton(
                "🎬 Video HD",
                callback_data="video"
            ),

            InlineKeyboardButton(
                "🎵 Audio MP3",
                callback_data="audio"
            )
        ]

    ]


    await update.message.reply_text(
        "Download type choose karo 👇",
        reply_markup=InlineKeyboardMarkup(buttons)
    )




async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query

    await q.answer()


    url = context.user_data.get("url")


    if not url:

        await q.edit_message_text(
            "❌ Link expired. Dobara bhejo."
        )

        return



    msg = await q.edit_message_text(
        "🚀 Preparing download..."
    )



    async def progress(percent):

        blocks = int(percent / 10)

        bar = "█"*blocks + "░"*(10-blocks)


        try:

            await msg.edit_text(
f"""
🔥 Downloading

{bar}

📥 {percent}%

⚡ High Quality Mode
"""
            )

        except:
            pass



    try:


        file = await download(
            url,
            q.data,
            progress
        )



        await msg.edit_text(
            "✅ Uploading file..."
        )



        if q.data == "video":


            await q.message.reply_video(
                video=open(file,"rb"),
                caption="🔥 HD Video Done"
            )


        else:


            await q.message.reply_audio(
                audio=open(file,"rb"),
                caption="🎵 MP3 320kbps Done"
            )



        os.remove(file)



    except Exception as e:


        print(e)


        await q.message.reply_text(
            "❌ Download failed\nTry again."
        )




def main():


    app = Application.builder().token(
        TOKEN
    ).build()



    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )



    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            link
        )
    )



    app.add_handler(
        CallbackQueryHandler(
            button
        )
    )



    print("🔥 BOT RUNNING")

    app.run_polling()



if __name__ == "__main__":

    main()