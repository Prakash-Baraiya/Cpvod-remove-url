import os
import re
import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import Filters

# Rest of the code remains the same...


# Rest of the code remains the same...

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle the /start command
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome! Please send a .txt file containing URLs in name:url format."
    )

# Function to handle file upload
def handle_file(update: Update, _: CallbackContext) -> None:
    file = update.message.document
    if file.mime_type != 'text/plain':
        update.message.reply_text("Please upload a .txt file.")
        return
    
    file_name = f"{file.file_id}.txt"
    file_path = f"{file_name}"
    file.get_file().download(file_path)
    
    # Process the file to remove unwanted URLs
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    filtered_lines = [line for line in lines if not re.search(r'\bcpvod\.testbook\b', line)]
    
    # Save the filtered content to a new file
    output_file_name = f"{file.file_id}_filtered.txt"
    output_file_path = f"{output_file_name}"
    
    with open(output_file_path, 'w') as f:
        f.writelines(filtered_lines)
    
    # Send the output file to the user
    update.message.reply_document(open(output_file_path, 'rb'))
    
    # Clean up: delete the temporary files
    os.remove(file_path)
    os.remove(output_file_path)

# Main function to start the bot
def main() -> None:
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
    updater = Updater("6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s")
    
    dispatcher = updater.dispatcher
    
    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), handle_file))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
