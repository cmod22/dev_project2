import requests
import math
 
# Function to get weather information using OpenWeather API
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
 
# Function to get latitude and longitude using Geocoding API
def get_lat_lng(api_key, city, state):
    """Convert city and state to latitude and longitude using Geocoding API."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": f"{city}, {state}",
        "key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None
 
# Function to calculate city radius based on area
def get_city_radius(city_area_km2):
    """Calculate radius in meters from the city's area in square kilometers."""
    radius_km = math.sqrt(city_area_km2 / math.pi)
    return radius_km * 1000  # Convert to meters
 
# Function to get local attractions using Google Places API
def get_local_attractions(api_key, city, state, city_area_km2):
    """Fetch local attractions using Google Places API based on city and state."""
    lat, lng = get_lat_lng(api_key, city, state)
    if lat is None or lng is None:
        return {"error": "Failed to geocode city and state"}
    radius = get_city_radius(city_area_km2)
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": api_key,
        "location": f"{lat},{lng}",  # Format "latitude,longitude"
        "radius": radius,  # Radius in meters
        "type": "tourist_attraction"  # Filters to attractions only
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": "Request failed"}
 
# Function to print tourist attractions
def print_attractions(attractions):
    """Print tourist attractions in a neat format."""
    results = attractions.get('results', [])
    if not results:
        print("No attractions found.")
        return
    print(f"Found {len(results)} attractions:")
    for place in results:
        name = place.get('name')
        address = place.get('vicinity')
        rating = place.get('rating', 'No rating')
        print("\n-------------------")
        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"Rating: {rating}")
        if 'opening_hours' in place:
            open_now = place['opening_hours'].get('open_now', False)
            print(f"Open Now: {'Yes' if open_now else 'No'}")
    print("\n-------------------")
 
# Function to print weather information
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
        print(f"Description: {description.capitalize()}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    print("\n-------------------")
 
# Example Usage
google_api_key = "AIzaSyCLulEXA1cv0f2NImemkHC6IRVvM7E5rPQ"  # Your Google API Key
openweather_api_key = "95214e4c7c7fd67e8892046031b5563d"  # Your OpenWeather API Key
 
city = input("Enter city: ")  # E.g., New York
state = input("Enter state: ")  # E.g., NY
city_area_km2 = 105.4  # For example, area of New York in km²
 
# Get and print local attractions
attractions = get_local_attractions(google_api_key, city, state, city_area_km2)
print_attractions(attractions)
 
# Get and print weather
weather = get_weather(openweather_api_key, city)
print_weather(weather)