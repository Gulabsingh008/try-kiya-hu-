from pyrogram import Client, filters
from config import BOT_TOKEN, API_ID, API_HASH
from time_sync import sync_time  # Import only sync_time since we won't use continuous_time_check
from time import sleep
import pytz
from datetime import datetime

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

def get_current_time_in_timezone(timezone_str):
    timezone = pytz.timezone(timezone_str)
    current_time = datetime.now(timezone)
    return current_time

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to the Video Downloader Bot!\n"
                         "This bot allows you to download videos from a specified URL and upload them to this chat.\n"
                         "To start the download process, use the /download command.")

@app.on_message(filters.command("download"))
async def download(client, message):
    await message.reply("Please enter your username:")
    await app.send_message(message.chat.id, "Please enter your username:")

@app.on_message(filters.text)
async def handle_username(client, message):
    username = message.text
    await message.reply(f"Username received: {username}. Please enter your password:")
    
    client.user_data[message.chat.id] = {"username": username}

@app.on_message(filters.text)
async def handle_password(client, message):
    if message.chat.id in client.user_data:
        password = message.text
        username = client.user_data[message.chat.id]["username"]
        await message.reply(f"Password received for {username}. Please enter the playlist URL:")
        
        client.user_data[message.chat.id]["password"] = password

@app.on_message(filters.text)
async def handle_playlist(client, message):
    if message.chat.id in client.user_data:
        playlist_url = message.text
        username = client.user_data[message.chat.id]["username"]
        password = client.user_data[message.chat.id]["password"]
        
        await message.reply(f"Downloading video from {playlist_url} with username {username} and password {password}...")
        
        # Get current time in a specific timezone
        kolkata_time = get_current_time_in_timezone("Asia/Kolkata")
        await message.reply(f"Current time in Kolkata: {kolkata_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Synchronize time before starting the bot
    if sync_time():
        sleep(10)  # Add a longer delay to ensure time is set
    else:
        print("Could not synchronize time. Exiting...")
        exit(1)  # Exit if time synchronization fails

    app.run()
