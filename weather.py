import requests
import json
import os
import time

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CACHE_DURATION = 600  # 10 minutes

def get_cached_weather(city):
    filename = f"{city.lower()}.json"
    if not os.path.exists(filename):
        return None
    file_age = time.time() - os.path.getmtime(filename)
    if file_age < CACHE_DURATION:
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None
    return None

def save_weather(city, data):
    filename = f"{city.lower()}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def fetch_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error:", e)
        return None

def display_weather(data):
    try:
        temp = data["main"]["temp"]
        sky = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]
        print(f"Temperature: {temp}°C")
        print(f"Sky: {sky}")
        print(f"Humidity: {humidity}%")
    except KeyError:
        print("Unexpected data format")

def main():
    city = input("Enter city name: ").strip()
    cached = get_cached_weather(city)
    if cached:
        print("Using cached data...")
        display_weather(cached)
        return
    print("Fetching from API...")
    data = fetch_weather(city)
    if data and data.get("cod") == 200:
        display_weather(data)
        save_weather(city, data)
    else:
        print("Failed to fetch weather data.")

if __name__ == "__main__":
    main()
