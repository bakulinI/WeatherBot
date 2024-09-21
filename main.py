import telebot
from telebot import types
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
bot = telebot.TeleBot(os.getenv('botApi'))
API = os.getenv('API')
@bot.message_handler(commands= ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Введи название города')
@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    try:
        res.raise_for_status()
        data = json.loads(res.text)
        temp = data['main']["temp"]
        bot.reply_to(message, f'Сейчас погода: {temp}')
        if temp >= 25.0:
            image = 'hotasf.jpg'
        elif temp >=15.0:
            image = 'norm.jpg'
        elif temp >=5.0:
            image = 'coldd.jpg'
        else:
            image = 'coldasf.jpg'
        with open('./' + image, 'rb') as file:
            bot.send_photo(message.chat.id, file)
    except requests.exceptions.HTTPError as err:
        bot.reply_to(message,'Город указан неверно')
bot.polling(none_stop=True)