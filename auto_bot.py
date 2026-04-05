import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

TOKEN = os.getenv("TOKEN")
CHANNEL_2_ID = -100XXXXXXXXXX   # yahan apna 2nd channel ID daal

counter = 1

# 🔥 SET COMMAND (manual numbering)
async def set_counter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global counter
    try:
        counter = int(context.args[0])
        await update.message.reply_text(f"✅ Counter set to {counter}")
    except:
        await update.message.reply_text("❌ Use like: /set 5")

# 🔥 MAIN BOT FUNCTION
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global counter

    if update.channel_post:
        post = update.channel_post

        # caption ya text
        text = post.caption or post.text or ""

        # username replace
        new_text = re.sub(r"@\w+", "@LearnWithVishnu", text)

        # link create
        chat_id = post.chat_id
        message_id = post.message_id
        link = f"https://t.me/c/{str(chat_id)[4:]}/{message_id}"

        final_text = f"{counter}. {new_text}\n\n{link}\n\n@LearnWithVishnu ✔️"

        # 📸 PHOTO HANDLE
        if post.photo:
            photo = post.photo[-1].file_id
            await context.bot.send_photo(
                chat_id=CHANNEL_2_ID,
                photo=photo,
                caption=final_text
            )

        # 🎥 VIDEO HANDLE
        elif post.video:
            video = post.video.file_id
            await context.bot.send_video(
                chat_id=CHANNEL_2_ID,
                video=video,
                caption=final_text
            )

        # 📄 DOCUMENT HANDLE
        elif post.document:
            doc = post.document.file_id
            await context.bot.send_document(
                chat_id=CHANNEL_2_ID,
                document=doc,
                caption=final_text
            )

        # 📝 TEXT ONLY
        else:
            await context.bot.send_message(
                chat_id=CHANNEL_2_ID,
                text=final_text
            )

        counter += 1

# 🚀 RUN BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("set", set_counter))
app.add_handler(MessageHandler(filters.ALL, handle))

app.run_polling()
