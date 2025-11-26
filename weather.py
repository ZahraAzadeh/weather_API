import os
import requests

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        print(f"Weather in {city}: {temp}°C, {weather_desc}")
    else:
        print(f"Failed to get weather for {city}. Status code: {response.status_code}")

def main():
    # Get city from environment variable (set in GitHub Actions)
    city = os.getenv("CITY_NAME", "Mashhad")  # default to Mashhad
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        print("Error: WEATHER_API_KEY is not set in environment variables.")
        return

    get_weather(city, api_key)

if __name__ == "__main__":
    main()
