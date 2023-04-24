import requests
from emoji import emojize
from datetime import datetime as dt
from config import openWeatherToken, tgBotToken
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tgBotToken)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])

async def startCommand(message: types.Message):
    await message.reply('Hello choose city, and i will show you a weather ')

@dp.message_handler(content_types=['text'])
async def getWeather(message: types.Message):

    text = str(message.text).lower()

    emojis = {
        'Clear': 'Sun :sun:',
        'Clouds': 'Cloud :cloud:',
        'Rain': 'Rain :cloud with rain:',
        'Drizzle': 'Drizzle :umbrella with rain drops:',
        'Thunderstorm': 'Thunderstorm :high voltage:',
        'Snow': 'Snow :snowflake:',
        'Mist': 'Mist :fog:'
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={text}&appid={openWeatherToken}&units=metric"
        )
        data = r.json()

        city = data['name']
        curWeather = data['main']['temp']

        wheatherDescription = data['weather'][0]['main']
        if wheatherDescription in emojis:
            wd = emojize(emojis[wheatherDescription])
        else:
            wd = 'Look out the window'

        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        sunriseTimeStamp = dt.fromtimestamp(data['sys']['sunrise'])
        sunsetTimeStamp = dt.fromtimestamp(data['sys']['sunset'])
        lenghtOfDay = dt.fromtimestamp(data['sys']['sunset']) - dt.fromtimestamp(
            data['sys']['sunrise'])
        message_date = "*** {:%d-%m-%Y  %H:%M} ***"
        await message.reply(f'{message_date.format(dt.now())}\n'
              f'Weather in city: {city}\nCelsius: {curWeather} C° {wd}\n'
              f'Humidity: {humidity} %\nWind: {wind} mmHg\n'
              f'Sunrise: {sunriseTimeStamp}\n'
              f'Sunset: {sunsetTimeStamp}\n'
              f'Day Lenght: {lenghtOfDay}\n'
              f'Good Luck!'
              )
    except:
        await message.reply('Check name of city')

if __name__ == '__main__':
    executor.start_polling(dp)