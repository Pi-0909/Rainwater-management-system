import requests
import time

def get_total_precipitation_data(api_key):
    url = f"http://api.weatherapi.com/v1/forecast.json?key=dff7a83506cc4f1bbb6111706260202&q=auto:ip&days=2&aqi=no&alerts=yes"
    response = requests.get(url)

    if response.status_code == 200:
        forecast_data = response.json()
        total_precipitation = 0

        for day in forecast_data['forecast']['forecastday']:
            total_precipitation += day['day'].get('totalprecip_mm', 0)
            total_precipitation += day['day'].get('totalsnow_cm', 0) * 10

        return total_precipitation
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    api_key = 'dff7a83506cc4f1bbb6111706260202'

    while True:
        total_precipitation = get_total_precipitation_data(api_key)

        if total_precipitation is not None:
            print(total_precipitation, "mm")

        time.sleep(3600)