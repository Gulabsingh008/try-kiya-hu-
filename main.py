from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ConversationHandler
from bot import start, download, handle_username, handle_password, handle_playlist

def main():
    updater = Updater("YOUR_BOT_TOKEN")
    dp = updater.dispatcher

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

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
