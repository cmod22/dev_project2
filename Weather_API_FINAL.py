import requests

def get_weather(api_key, city):
    """Fetch current weather for a city using OpenWeather API."""
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # To get temperature in Celsius
    }
 
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": "Request failed"}

def print_weather(weather):
    """Print the weather information."""
    if 'error' in weather:
        print(f"Failed to get weather data: {weather['message']}")
    else:
        temp = weather['main']['temp']
        description = weather['weather'][0]['description']
        humidity = weather['main']['humidity']
        wind_speed = weather['wind']['speed']
        print("\nCurrent Weather:")
        print(f"Temperature: {temp}°C")
        print(f"Temperature: {temp * 9/5 + 32}°F")
        print(f"Description: {description.capitalize()}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    print("\n-------------------")