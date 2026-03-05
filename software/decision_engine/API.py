import requests

def check_heavy_rain(api_key):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q=auto:ip&days=2&aqi=no&alerts=no"
    response = requests.get(url)

    if response.status_code == 200:
        forecast_data = response.json()

        for day in forecast_data['forecast']['forecastday']:
            for hour in day['hour']:
                if hour.get('precip_mm', 0) >= 20:
                    return True
        return False

    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    api_key = 'dff7a83506cc4f1bbb6111706260202'
    heavy_rain = check_heavy_rain(api_key)
    print(heavy_rain)
