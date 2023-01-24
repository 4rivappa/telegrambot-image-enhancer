import os
from random import randint
import re
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

load_dotenv()
API_KEY = os.getenv('API_KEY')
print(API_KEY)
bot = telebot.TeleBot(API_KEY)

def clean_line(input):
    input = re.sub("\s\s+", " ", input)
    input = input.strip()
    return input

def collect_quotes():
    return_arr = []
    quotes_file = open('./data-collection/quotes.txt', 'r', encoding='utf-8')
    for line in quotes_file.readlines():
        if line == "":
            continue
        parts = line.split('―')
        quote = clean_line(parts[0])
        author = clean_line(parts[1])
        return_arr.append([quote, author])
    quotes_file.close()
    return return_arr

def get_random_quote(arr):
    length = len(arr)
    # comment below line to get all quotes
    length = 50
    index = randint(0, length-1)
    return arr[index]

quotes = collect_quotes()
# print(len(quotes))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # print(message)
    # print(message.chat.id)
    bot.send_message(message.chat.id, "Hey glad to meet you.. \nSend me image to enhance it...")

@bot.message_handler(commands=['motivate', 'quote'])
def send_quote(message):
    random_quote = get_random_quote(quotes)
    curr_button = InlineKeyboardButton(text="/motivate", callback_data="/motivate")
    # curr_button = KeyboardButton(text="/motivate")
    curr_markup = InlineKeyboardMarkup()
    curr_markup = curr_markup.add(curr_button)
    bot.send_message(message.chat.id, random_quote[0])
    bot.send_message(message.chat.id, '― ' + random_quote[1], reply_markup=curr_markup)
    # bot.send_message(message.chat.id, "", reply_markup=curr_markup)

@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    file_name = file_info.file_path.replace("/", "_")

    with open("./images/original/" + file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    ## thread to run the cmd command
    os.system("python C:\\Users\\ARIVAPPA\\personal\\explore\\ai\\GFPGAN\\inference_gfpgan.py -i C:\\Users\\ARIVAPPA\\personal\\telegram-bot\\images\\original\\" + file_name  + " -o C:\\Users\\ARIVAPPA\\personal\\telegram-bot\\images\\results -v 1.3 -s 2")

    bot.send_message(message.chat.id, "processing...")

    restored_photo = "./images/results/restored_imgs/" + file_name
    bot.send_photo(message.chat.id, photo=open(restored_photo, 'rb'))
    print("Restored image sent....")


# error issues with this below line
# bot.polling()
bot.infinity_polling(timeout=10, long_polling_timeout = 5)
