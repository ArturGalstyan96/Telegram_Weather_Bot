import requests
from config import openWeatherToken
from emoji import emojize

import datetime

def getWeather(city, openWeatherToken):

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
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openWeatherToken}&units=metric"
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
        sunriseTimeStamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunsetTimeStamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        lenghtOfDay = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        print(f'***{datetime.datetime.now()}***\n'
              f'Weather in city: {city}\nCelsius: {curWeather} C° {wd}\n'
              f'Humidity: {humidity} %\nWind: {wind} mmHg\n'
              f'Sunrise: {sunriseTimeStamp}\n'
              f'Sunset: {sunsetTimeStamp}\n'
              f'Day Lenght: {lenghtOfDay}\n'
              f'Good Luck!'
              )
    except Exception as ex:
        print(ex)
        print('Check name of city')
    pass

def main():
    city = input('Enter City: ')
    getWeather(city, openWeatherToken)

if __name__ == '__main__':
    main()