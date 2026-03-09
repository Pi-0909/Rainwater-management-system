import RPi.GPIO as GPIO
import requests
import schedule
import time

PUMP_WATER_PIN = 23
PUMP_SEWER_PIN = 18
SENSOR_TRIGGER_PIN = 21
SENSOR_ECHO_PIN = 20
API_KEY = 'dff7a83506cc4f1bbb6111706260202'
EMPTY_TANK_DISTANCE = 0  # measure the depth, then set the cm manually

GPIO.setmode(GPIO.BCM)
GPIO.setup(PUMP_WATER_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PUMP_SEWER_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SENSOR_TRIGGER_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SENSOR_ECHO_PIN, GPIO.IN)

def get_distance():
    GPIO.output(SENSOR_TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(SENSOR_TRIGGER_PIN, GPIO.LOW)

    while GPIO.input(SENSOR_ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(SENSOR_ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def check_heavy_rain():
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q=auto:ip&days=2&aqi=no&alerts=no"
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

def run_pump(pin):
    GPIO.output(pin, GPIO.HIGH)

    while True:
        distance = get_distance()
        if distance > EMPTY_TANK_DISTANCE:
            print(f"Tank empty at {distance} cm, stopping pump")
            break
        time.sleep(1)

    GPIO.output(pin, GPIO.LOW)

def watering_job():
    heavy_rain = check_heavy_rain()

    if heavy_rain is None:
        print("Could not retrieve weather data, skipping cycle")
        return

    if heavy_rain:
        print("Heavy rain detected, dumping to sewers")
        run_pump(PUMP_SEWER_PIN)
    else:
        print("No heavy rain, watering plants")
        run_pump(PUMP_WATER_PIN)

schedule.every().day.at("13:00").do(watering_job)

try:
    print("Watering system running")
    while True:
        schedule.run_pending()
        time.sleep(60)

except KeyboardInterrupt:
    print("Shutting down")
    GPIO.cleanup()
