from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from src import sapling_api

# BOT INITIALIZATION
def initialize_bot():
    application = ApplicationBuilder().token('7454918531:AAEFXXp6ThE2XdaC3MLv29GTOju40ZzvjLA').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    rephrase_handler = CommandHandler('rephrase', get_replacements)
    application.add_handler(rephrase_handler)
#

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id, "Hello, I'm here to rephrase your informal english..")
    await context.bot.send_message(chat_id, "Use the /rephrase command followed by the sentence")
    await context.bot.send_message(chat_id, "Example:\n/rephrase This job is awesome")
    await context.bot.send_message(chat_id, "You will receive a bunch of suggestions such as:\nThis position is truly remarkable")

async def get_replacements(phrase):
    chat_id = update.effective_chat.id
    try:
        results = await sapling_api.make_request(phrase)
        replacements = sapling_api.extract_rephrases(results)
        await context.bot.send_message(chat_id, "Suggestions:")
        for i in range(len(results)):
            await context.bot.send_message(chat_id, results[i])
    except:
        await context.bot.send_message(chat_id, "Something went wrong, Please try the last command again")
