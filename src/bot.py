from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from src import sapling_api
import os


# BOT INITIALIZATION
def initialize_bot():
    api_key = os.getenv("tgbot_key")
    application = ApplicationBuilder().token(api_key).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    rephrase_handler = CommandHandler('rephrase', get_replacements)
    application.add_handler(rephrase_handler)

    application.run_polling()
#

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id, "Hello, I'm here to rephrase your informal english..")
    await context.bot.send_message(chat_id, "Use the /rephrase command followed by the sentence")
    await context.bot.send_message(chat_id, "Example:\n/rephrase This job is awesome")
    await context.bot.send_message(chat_id, "You will receive a bunch of suggestions such as:")
    await context.bot.send_message(chat_id, "This position is truly remarkable")

async def get_replacements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        command, *args = update.message.text.split(' ', 1)
        phrase = args[0] if args else ''
        if not phrase.strip():
            await update.message.reply_text("Please type the sentence you want me to rephrase after the command")
            return
        
        results = sapling_api.make_request(phrase)
        replacements = sapling_api.extract_rephrases(results)
        await context.bot.send_message(chat_id, "Suggestions:")
        for i in range(len(replacements)):
            await context.bot.send_message(chat_id, replacements[i])
    except Exception as error:
        print(error)
        await context.bot.send_message(chat_id, "Something went wrong, Please try the last command again")
