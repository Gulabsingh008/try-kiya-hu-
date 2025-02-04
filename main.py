from pyrogram import Client, filters
from config import BOT_TOKEN, API_ID, API_HASH
from time_sync import sync_time  # Import the sync_time function
from time import sleep

# Synchronize time first before continuing
if sync_time():  # Call the function to sync time
    sleep(10)  # Add a longer delay to ensure time is set
else:
    print("Could not synchronize time. Exiting...")
    exit(1)  # Exit if time synchronization fails

# Import threading only after ensuring synchronization is done
import threading

# Start continuous time checking in a separate thread after synchronization is confirmed
threading.Thread(target=continuous_time_check, daemon=True).start()

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to the Video Downloader Bot!\n"
                         "This bot allows you to download videos from a specified URL and upload them to this chat.\n"
                         "To start the download process, use the /download command.")

@app.on_message(filters.command("download"))
async def download(client, message):
    await message.reply("Please enter your username:")

@app.on_message(filters.text)
async def handle_user_input(client, message):
    # Check if it's a valid response and whether the user data exists
    if message.chat.id not in client.user_data:
        # Start a new conversation flow
        client.user_data[message.chat.id] = {"step": "username"}
        await message.reply("Please enter your username:")
    else:
        step = client.user_data[message.chat.id]["step"]

        if step == "username":
            username = message.text
            client.user_data[message.chat.id]["username"] = username
            client.user_data[message.chat.id]["step"] = "password"
            await message.reply(f"Username received: {username}. Please enter your password:")
        
        elif step == "password":
            password = message.text
            client.user_data[message.chat.id]["password"] = password
            client.user_data[message.chat.id]["step"] = "playlist"
            await message.reply("Password received. Please enter the playlist URL:")

        elif step == "playlist":
            playlist_url = message.text
            username = client.user_data[message.chat.id]["username"]
            password = client.user_data[message.chat.id]["password"]

            # Here you would implement the video downloading logic
            await message.reply(f"Downloading video from {playlist_url} with username {username} and password {password}...")

            # After downloading, you can send the video back to the user
            # await app.send_video(message.chat.id, "path_to_downloaded_video.mp4")

            # Optionally, reset the user data after the process is done
            del client.user_data[message.chat.id]

if __name__ == "__main__":
    app.run()
