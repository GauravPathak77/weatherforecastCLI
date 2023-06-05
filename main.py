import shutil
import requests
from pyfiglet import Figlet
from termcolor import colored
import sys

def get_weather(location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    api_key = 'c3a14b64fd3eb5f994230183700f79d1'
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        f = Figlet(font='big')
        ascii_text = f.renderText(location)
        colored_text = colored(ascii_text, 'green')

        print(f"{colored_text}")
        print_weather_info(weather_data)
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")

def print_weather_icon(weather_code):
    weather_icon = {
        '01': '☀️',  # Clear sky
        '02': '🌤️',  # Few clouds
        '03': '🌥️',  # Scattered clouds
        '04': '☁️',  # Broken clouds
        '09': '🌧️',  # Shower rain
        '10': '🌦️',  # Rain
        '11': '⛈️',  # Thunderstorm
        '13': '🌨️',  # Snow
        '50': '🌫️'  # Mist
    }

    code_prefix = str(weather_code)[:2] 

    if code_prefix in weather_icon:
        return weather_icon[code_prefix]
    else:
        return '❓'

def print_weather_info(weather_data):
    terminal_width = shutil.get_terminal_size().columns
    temperature = weather_data['main']['temp']
    description = weather_data['weather'][0]['description'].capitalize()
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    ic = print_weather_icon(weather_data['weather'][0]['icon'])

    f = Figlet(font='mini')
    ascii_text = f.renderText(str(temperature)+ '°C')
    colored_temp = colored(ascii_text, 'blue')
    ascii_text = f.renderText(description)
    colored_desc = colored(ascii_text, 'red')
    centered_des = colored_desc.center(terminal_width)

    print()
    print(f"{ic}     {colored_temp}")
    print(f"Description: {centered_des}")
    print()
    print(f"Humidity:  {humidity}%")
    print(f"Pressure:  {pressure}%")
    print()
    print(f"Wind Speed:  {wind_speed} m/s")
    print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide a location and API key.")
    else:
        location = ' '.join(sys.argv[1:])
        get_weather(location)
