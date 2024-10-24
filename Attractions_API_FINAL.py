import requests
import math

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
 
def get_city_radius(city_area_km2):
    """Calculate radius in meters from the city's area in square kilometers."""
    radius_km = math.sqrt(city_area_km2 / math.pi)
    return radius_km * 1000  # Convert to meters

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
 