import requests
import time

def get_hourly_precipitation_data(api_key):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q=auto:ip&days=2&aqi=no&alerts=no"
    response = requests.get(url)

    if response.status_code == 200:
        forecast_data = response.json()

        for day in forecast_data['forecast']['forecastday']:
            for hour in day['hour']:
                precip = hour.get('precip_mm', 0)
                print(f" {precip}")

    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    api_key = 'dff7a83506cc4f1bbb6111706260202'

    while True:
        get_hourly_precipitation_data(api_key)
        time.sleep(3600)
