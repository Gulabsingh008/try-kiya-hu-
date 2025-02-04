import yt_dlp
import requests
from telegram import Update
from telegram.ext import CallbackContext

# Function to download video using yt-dlp
def download_video(url, username, password):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'noplaylist': True,
        'username': username,
        'password': password,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Function to upload video to Telegram
def upload_to_telegram(bot_token, chat_id, file_path):
    with open(file_path, 'rb') as file:
        url = f'https://api.telegram.org/bot{bot_token}/sendVideo'
        files = {'video': file}
        data = {'chat_id': chat_id}
        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        print('Video uploaded successfully!')
    else:
        print('Failed to upload video:', response.json())

# Command to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the Video Downloader Bot!\n"
        "This bot allows you to download videos from a specified URL and upload them to this chat.\n"
        "To start the download process, use the /download command."
    )

# Command to initiate the download process
def download(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter your username:")
    return "USERNAME"

# Function to handle username input
def handle_username(update: Update, context: CallbackContext):
    context.user_data['username'] = update.message.text
    update.message.reply_text("Please enter your password:")
    return "PASSWORD"

# Function to handle password input
def handle_password(update: Update, context: CallbackContext):
    context.user_data['password'] = update.message.text
    update.message.reply_text("Please enter the playlist URL:")
    return "PLAYLIST"

# Function to handle playlist URL input
def handle_playlist(update: Update, context: CallbackContext):
    username = context.user_data['username']
    password = context.user_data['password']
    playlist_url = update.message.text
    
    # Download video
    download_video(playlist_url, username, password)
    
    # Upload video to Telegram
    upload_to_telegram(context.bot.token, update.message.chat_id, 'downloaded_video.mp4')
    update.message.reply_text("Video has been downloaded and uploaded successfully!")
