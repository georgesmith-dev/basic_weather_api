import requests
import sys

def get_user_input():
    while True:
            location = input("Enter location:").strip().title()
            if any(char.isdigit() for char in location):
                 print("Invalid input, try again")
                 continue
            return location

def get_api_key(key):
    if not isinstance(key, str):
        print("Invalid key")
        return
    
    clean_key = key.strip()
    if not clean_key:
        print("Invalid key")
        return
    
    try:
        with open(clean_key, "r", encoding="utf-8") as k:
            return k.read()
    except(FileNotFoundError, PermissionError, UnicodeDecodeError):
        print("Invalid key")
        return
    
def get_weather_summary(base_url, location, api_key):
    url = base_url
    query_params = {"q": location, "units": "metric", "appid": api_key}

    try:
        response = requests.get(url, params=query_params)
    except requests.exceptions.RequestException as e:
        print(f"Unexpected error: {e}")
        return
    
    if not response.ok:
        print(f"Error: failed to retrieve weather data: {response.status_code}")
        return
    
    result = response.json()
    if not result:
        print("Error: failed to retrieve weather data")
        return
    
    weather_list = result.get('weather', [])
    if not weather_list:
        print("Error: failed to retrieve weather description")
        return
    weather = weather_list[0]

    city_name = result.get('name', 'unknown')
    description = weather.get('description', 'unknown').title()
    temp = result.get('main', {}).get('temp', 'unknown')
    feels_like = result.get('main', {}).get('feels_like', 'unknown')
    humidity = result.get('main', {}).get('humidity', 'unknown')

    print(
        f"\n{city_name}\n"
        f"{description}\n"
        f"\nTemperature: {temp}°C\n"
        f"Feels like: {feels_like}°C\n"
        f"Humidity: {humidity} %\n"
    )
    
if __name__ == "__main__":
    verified_api_key = get_api_key('api_key.txt')
    if not verified_api_key:
        sys.exit("Failed to retrieve api key")
    get_weather_summary('http://api.openweathermap.org/data/2.5/weather', location= get_user_input(), api_key= verified_api_key)

