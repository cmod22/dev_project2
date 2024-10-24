import Weather_API_FINAL
import Restaraunt_API_FINAL
import Attractions_API_FINAL
#Enter the full file path for where you store both of these values, code may break if not fully specified
GAPI = open("C:\VSC_Coding_projects\dev_project2\dev_project2\GoogleAPI.txt","r")
WAPI = open("C:\VSC_Coding_projects\dev_project2\dev_project2\WeatherAPI.txt", "r")

google_api_key = GAPI.read()
openweather_api_key = WAPI.read()
 
GAPI.close()
WAPI.close()

city = input("Enter city: ")  
state = input("Enter state: ")  
city_area_km2 = float(input("Enter area to search (in km squared): "))

try:
    # Get and print weather
    weather = Weather_API_FINAL.get_weather(openweather_api_key, city)
    Weather_API_FINAL.print_weather(weather)

    # Get and print restaurant suggestions
    restaurants = Restaraunt_API_FINAL.get_restaurants(google_api_key, city, state, city_area_km2)
    Restaraunt_API_FINAL.print_restaurants(restaurants)

    # Get and print local attractions
    attractions = Attractions_API_FINAL.get_local_attractions(google_api_key, city, state, city_area_km2)
    Attractions_API_FINAL.print_attractions(attractions)
except ValueError as e:
    print('Error, please try entering your number as digits (i.e. "60" instead of "sixty.")')