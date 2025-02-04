from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from bot import start, download, handle_username, handle_password, handle_playlist

def main():
    updater = Updater("YOUR_BOT_TOKEN")
    dp = updater.dispatcher

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("download", download)],
        states={
            "USERNAME": [MessageHandler(Filters.text & ~Filters.command, handle_username)],
            "PASSWORD": [MessageHandler(Filters.text & ~Filters.command, handle_password)],
            "PLAYLIST": [MessageHandler(Filters.text & ~Filters.command, handle_playlist)],
        },
        fallbacks=[],
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()