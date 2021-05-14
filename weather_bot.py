import requests
import telebot
from telebot import types
from geopy.geocoders import Nominatim
import random

url = 'http://api.openweathermap.org/data/2.5/weather' #open weather url
api_open_weather = '966cc6ce89188b2bc797546a3487bf55'#ключ open weather api
api_telegram_token = '1773699578:AAFWpnvES0Zqzky7g1k8iBPHbEh0UF3htnI' #токен telegram api

print("")
print("initialize") #сообщение в консоль

bot = telebot.TeleBot(api_telegram_token)

link1 = "https://ivi.ru"
link2 = "https://litres.ru"
link3 = "https://lamoda.ru"
link4 = "https://leroymerlin.ru"

message1 = "Сегодня холодно, оставайтесь дома! А чтобы скрасить вечер можете посмотреть фильм! \n"
message2 = "Если нет желания сегодня гулять, можно устроиться дома в кресле и почитать любую книгу из онлайн-каталога! \n"
message3 = "Если вы еще сменили верхнюю одежду, самое время это сделать! С ассортиментом можете ознакомиться на сайте магазина по ссылке ниже. \n"
message4 = "Дачный сезон можно считать открытым! Семена, рассада, лейки, лопаты, грабли, газонокосилки и прочий садовый инвентарь можно купить в магазине, представленном ниже. \n"

random_message1 = random.choice(message1)
random_message2 = random.choice(message2)
random_message3 = random.choice(message3)
random_message4 = random.choice(message4)

@bot.message_handler(commands=['start']) #старт
def start(message):
    markup=types.ReplyKeyboardMarkup().add(types.KeyboardButton(text = 'Отправить местоположение', request_location=True))
    bot.send_message(message.chat.id, f'Привет!  {message.from_user.first_name}'
                                      f', напиши название города или отправь геолокацию, а я тебе скажу погоду в нем!', reply_markup = markup) #Сообщение при запуске

@bot.message_handler(content_types=['text']) #обработчик
def city_weather(message):
    city = message.text
    weather(message , city)

    

@bot.message_handler(content_types=['location'])
def location_weather(message):
    geolocator = Nominatim(user_agent='telebot', timeout=3)
    location = geolocator.reverse(str(message.location.latitude) + ', ' + str(message.location.longitude), exactly_one=True, language='ru')
    try:
        city = location.raw['address']['city']
        weather(message, city)
    except:
        city = location.raw['address']['town']
        weather(message, city)
        
def weather(message, city):
    try:
        params = {'APPID': api_open_weather, 'q': city, 'units': 'metric', 'lang': 'ru'}
        result = requests.get(url, params=params)#параметры api open weather
        weather = result.json()#экспорт параметров

        if weather["main"]['temp'] < -10:   #от -бесконечно до -10
            status = bot.send_photo(message.chat.id, 'http://f0535055.xsph.ru/1/ivi.jpeg', "Сейчас в городе " + str(weather["name"]) + " температура " +
                         str(weather["main"]['temp']) + "°C" + "\n" +
                         "Влажность: " + str(int(weather['main']['humidity'])) + "%" + "\n" +
                         "На улице сейчас " + str(weather['weather'][0]["description"]+"\n"+message1), reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Перейти на сайт', url = link1)))
        elif weather["main"]['temp'] < 0:   # - 10 - 0
            status = bot.send_photo(message.chat.id, 'http://f0535055.xsph.ru/1/litres.jpeg', "Сейчас в городе " + str(weather["name"]) + " температура " +
                         str(weather["main"]['temp']) + "°C" + "\n" +
                         "Влажность: " + str(int(weather['main']['humidity'])) + "%" + "\n" +
                         "На улице сейчас " + str(weather['weather'][0]["description"]+"\n"+message2), reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Перейти на сайт', url = link2)))
        elif weather["main"]['temp'] < 10:  #от 0 до +10
            status = bot.send_photo(message.chat.id, 'http://f0535055.xsph.ru/1/lamoda.jpeg', "Сейчас в городе " + str(weather["name"]) + " температура " +
                         str(weather["main"]['temp']) + "°C" + "\n" +
                         "Влажность: " + str(int(weather['main']['humidity'])) + "%" + "\n" +
                         "На улице сейчас " + str(weather['weather'][0]["description"]+"\n"+message3), reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Перейти на сайт', url = link3)))

        else:   #при +10+
            status = bot.send_photo(message.chat.id, 'http://f0535055.xsph.ru/1/sad.jpeg', "Сейчас в городе " + str(weather["name"]) + " температура " +
                         str(weather["main"]['temp']) + "°C" + "\n" +
                         "Влажность: " + str(int(weather['main']['humidity'])) + "%" + "\n" +
                         "На улице сейчас " + str(weather['weather'][0]["description"]+"\n"+message4), reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text = 'Перейти на сайт', url = link4)))
	


    except:
        bot.send_photo(message.chat.id, 'https://darkside.guru/files/404city.png', "Город " + city_name + " не найден") # сообщение в случае если город не найден
print("Started!")#сообщение в консоль
bot.polling(none_stop=True)
print("")
print("Stopped!")#сообщение в консоль
