import requests
import os
import telebot

bot = telebot.TeleBot('6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Send me a txt or .txt file contains urls in name:url format')

@bot.message_handler(content_types=['text'])
def handle_file(message):
    file_name = message.document.file_name
    if file_name.endswith('.txt'):
        file_content = message.document.file_data
        lines = file_content.decode('utf-8').splitlines()
        new_lines = []
        for i, line in enumerate(lines):
            if 'cpvod.testbook' not in line:
                new_lines.append(line)
            else:
                if i < len(lines) - 1:
                    new_lines.append(lines[i+1])
        output_file_name = file_name.split('.')[0] + '_processed.txt'
        with open(output_file_name, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        bot.send_document(message.chat.id, open(output_file_name, 'rb'))

bot.polling()
