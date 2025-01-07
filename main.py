from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# Bot configuration
token: final = "7415361855:AAEgxPFZj1Lpn1nDe0Ur1Rx7iC9cISdSIXM"
bot_username: final = "@chatwithroshibot"

# Office settings
office_hours = {
    "start": 9,  # Office start time (9 AM)
    "end": 17,   # Office end time (5 PM)
}
out_of_office_message = (
    "Thank you for your message. Our office hours are from 9 AM to 5 PM, Monday to Friday. "
    "Please DM me on @chatwithroshibot, and I will get back to you during office hours. "
    "For urgent matters, contact mailto:sha@iqventures.vc."
)

# File to store chat logs
log_file = "chat_logs.txt"

# Helper function to log user activity
def log_user_activity(username: str, user_id: int):
    """Log the username and time of user activity to a file."""
    with open(log_file, "a") as file:
        file.write(f"{datetime.now()} - User: {username} (ID: {user_id}) triggered /start\n")

# Commands
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! This is an office-only bot. Please DM me on @chatwithroshibot. "
        "To add me to groups, add @chatwithroshibot and upgrade me to admin. "
        "For urgent queries, contact mailto:sha@iqventures.vc."
    )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username or "Unknown"
    user_id = update.effective_user.id
    log_user_activity(username, user_id)  # Log activity only on /start

    await update.message.reply_text(
        "Welcome! This bot is designed for office communication. Feel free to send your messages, "
        "and I will assist you. Note: Responses may be delayed outside office hours."
    )

# Message handling
def is_office_hours() -> bool:
    """Check if the current time is within office hours."""
    now = datetime.now()
    return office_hours["start"] <= now.hour < office_hours["end"]

def handle_response(text: str) -> str:
    """Generate a response based on the input text."""
    processed: str = text.lower()

    if "hello" in processed:
        return "Hi there! How can I assist you today?"
    if "urgent" in processed:
        return "If this is urgent, please contact mailto:sha@iqventures.vc."
    
    return "Thank you for reaching out. How can I assist you?"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages from users."""
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response = handle_response(text)  # Always generate a response

    if not is_office_hours():
        # Append out-of-office notice if it's outside office hours
        response = f"{out_of_office_message}\n\n{response}"

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    print(f"Update {update} caused error {context.error}")

# Main function
if __name__ == "__main__":
    print("Starting Bot...")

    app = Application.builder().token(token).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Message handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handling
    app.add_error_handler(error)

    # Start polling
    print("Polling")
    app.run_polling(poll_interval=3)
from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import os

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


# Bot configuration
token: final = os.environ["BOT_TOKEN"]
bot_username: final = "@chatwithroshibot"

# Office settings
office_hours = {
    "start": 9,  # Office start time (9 AM)
    "end": 17,  # Office end time (5 PM)
}
out_of_office_message = (
    "Thank you for your message. Our office hours are from 9 AM to 5 PM, Monday to Friday. "
    "Please DM me on @chatwithroshibot, and I will get back to you during office hours. "
    "For urgent matters, contact mailto:sha@iqventures.vc.")

# File to store chat logs
log_file = "chat_logs.txt"


# Helper function to log user activity
def log_user_activity(username: str, user_id: int):
    """Log the username and time of user activity to a file."""
    with open(log_file, "a") as file:
        file.write(
            f"{datetime.now()} - User: {username} (ID: {user_id}) triggered /start\n"
        )


# Commands
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! This is an office-only bot. Please DM me on @chatwithroshibot. "
        "To add me to groups, add @chatwithroshibot and upgrade me to admin. "
        "For urgent queries, contact mailto:sha@iqventures.vc.")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username or "Unknown"
    user_id = update.effective_user.id
    log_user_activity(username, user_id)  # Log activity only on /start

    await update.message.reply_text(
        "Welcome! This bot is designed for office communication. Feel free to send your messages, "
        "and I will assist you. Note: Responses may be delayed outside office hours."
    )


# Message handling
def is_office_hours() -> bool:
    """Check if the current time is within office hours."""
    now = datetime.now()
    return office_hours["start"] <= now.hour < office_hours["end"]


def handle_response(text: str) -> str:
    """Generate a response based on the input text."""
    processed: str = text.lower()

    if "hello" in processed:
        return "Hi there! How can I assist you today?"
    if "urgent" in processed:
        return "If this is urgent, please contact mailto:sha@iqventures.vc."

    return "Thank you for reaching out. How can I assist you?"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages from users."""
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response = handle_response(text)  # Always generate a response

    if not is_office_hours():
        # Append out-of-office notice if it's outside office hours
        response = f"{out_of_office_message}\n\n{response}"

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    print(f"Update {update} caused error {context.error}")


# Main function
if __name__ == "__main__":
    print("Starting Bot...")
    keep_alive()  # Start the web server
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)
    print("Polling")
    app.run_polling(poll_interval=3)
