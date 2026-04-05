import re
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

TOKEN = os.getenv("TOKEN")
CHANNEL_2_ID = -1002192056669  # apna channel id

counter = 1

# 🔥 SET COMMAND
async def set_counter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global counter
    try:
        counter = int(context.args[0])
        await update.message.reply_text(f"✅ Counter set to {counter}")
    except:
        await update.message.reply_text("❌ Use like: /set 5")

# 🔥 MAIN FUNCTION
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global counter

    if update.channel_post:
        post = update.channel_post

        text = post.caption or post.text or ""
        new_text = re.sub(r"@\w+", "@LearnWithVishnu", text)

        chat_id = post.chat_id
        message_id = post.message_id

        link = f"https://t.me/c/{str(chat_id)[4:]}/{message_id}"

        final_text = f"{counter}. {new_text}\n\n{link}\n\n@LearnWithVishnu ✔️"

        if post.photo:
            await context.bot.send_photo(CHANNEL_2_ID, post.photo[-1].file_id, caption=final_text)

        elif post.video:
            await context.bot.send_video(CHANNEL_2_ID, post.video.file_id, caption=final_text)

        elif post.document:
            await context.bot.send_document(CHANNEL_2_ID, post.document.file_id, caption=final_text)

        else:
            await context.bot.send_message(CHANNEL_2_ID, final_text)

        counter += 1

# 🚀 RUN BOT (FIXED FOR RENDER)
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("set", set_counter))
    app.add_handler(MessageHandler(filters.ALL, handle))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
