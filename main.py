import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
from bot import start, download, handle_username, handle_password, handle_playlist

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("download", download)],
        states={
            "USERNAME": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username)],
            "PASSWORD": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password)],
            "PLAYLIST": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_playlist)],
        },
        fallbacks=[],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
