from pyrogram import Client, filters
from config import BOT_TOKEN, API_ID, API_HASH
from time_sync import sync_time, continuous_time_check  # Import the sync_time and continuous_time_check functions
from time import sleep
import threading

# Start continuous time checking in a separate thread
threading.Thread(target=continuous_time_check, daemon=True).start()

# Synchronize time
if sync_time():  # Call the function to sync time
    sleep(10)  # Add a longer delay to ensure time is set
else:
    print("Could not synchronize time. Exiting...")
    exit(1)  # Exit if time synchronization fails

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

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
    
    # Store the username in user data (you can implement a more robust storage)
    client.user_data[message.chat.id] = {"username": username}

@app.on_message(filters.text)
async def handle_password(client, message):
    if message.chat.id in client.user_data:
        password = message.text
        username = client.user_data[message.chat.id]["username"]
        await message.reply(f"Password received for {username}. Please enter the playlist URL:")
        
        # Store the password in user data
        client.user_data[message.chat.id]["password"] = password

@app.on_message(filters.text)
async def handle_playlist(client, message):
    if message.chat.id in client.user_data:
        playlist_url = message.text
        username = client.user_data[message.chat.id]["username"]
        password = client.user_data[message.chat.id]["password"]
        
        # Here you would implement the video downloading logic
        await message.reply(f"Downloading video
