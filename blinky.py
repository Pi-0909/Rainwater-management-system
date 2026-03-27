### Hallo! Dit is onze code voor de raspberry pi competitie 25-26, onze code is helemaal geschreven in Python met Engels dialoog vanwege TTO (TweeTalig-Onderwijs)
### Hello! This is our code for the Dutch raspberry pi competition 25-26, our code is fully writen in python.


import RPi.GPIO as GPIO
import requests
import time

# GPIO Pin Definitions
PUMP_WATER_PIN = 23
PUMP_SEWER_PIN = 18
TRIG = 21
ECHO = 20

API_KEY = 'dff7a83506cc4f1bbb6111706260202'
EMERGENCY_DISTANCE = 14.0   # cm -> tank empty threshold
OVERFLOW_THRESHOLD = 3.0    # cm -> sewer pump active if exceeded
DRAIN_TARGET = 4.0          # cm -> target after draining
PRECIP_THRESHOLD = 20.0     # mm -> heavy rain threshold

# Timeouts and durations
ECHO_TIMEOUT = 0.03
DRAIN_MAX_SECONDS = 120
WATER_PUMP_DURATION = 10
CHECK_INTERVAL = 3600  # seconds between repeated evaluation cycles
TEST_MODE = False
if TEST_MODE:
    CHECK_INTERVAL = 10

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PUMP_WATER_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PUMP_SEWER_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    """Return distance in cm or None on failure."""
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    pulse_start = None
    while time.time() - start < ECHO_TIMEOUT:
        if GPIO.input(ECHO) == 1:
            pulse_start = time.time()
            break
    if pulse_start is None:
        print("get_distance: timeout waiting for echo start")
        return None

    start = time.time()
    pulse_end = None
    while time.time() - start < ECHO_TIMEOUT:
        if GPIO.input(ECHO) == 0:
            pulse_end = time.time()
            break
    if pulse_end is None:
        print("get_distance: timeout waiting for echo end")
        return None

    duration = pulse_end - pulse_start
    distance = round(duration * 17150, 2)
    print(f"Distance measured: {distance} cm")
    return distance

def level_state(distance):
    """
    Return one of: 'ok', 'high', 'low'
    Interpret distance as water level in cm from sensor:
      - 'high' means water level above overflow threshold (distance small)
      - 'low' means tank effectively empty (distance > EMERGENCY_DISTANCE)
      - 'ok' otherwise
    """
    if distance is None:
        return None
    if distance > EMERGENCY_DISTANCE:
        return 'low'
    if distance <= OVERFLOW_THRESHOLD:
        return 'high'
    return 'ok'

def check_heavy_rain():
    """Return True if heavy rain (> PRECIP_THRESHOLD) expected, False if not, None on error."""
    print("Checking for heavy rain...")
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q=auto:ip&days=2&aqi=no&alerts=no"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        heavy = any(
            (hour.get('precip_mm') or 0) > PRECIP_THRESHOLD
            for day in data.get('forecast', {}).get('forecastday', [])
            for hour in day.get('hour', [])
        )
        print("Heavy rain expected." if heavy else "No heavy rain expected.")
        return heavy
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def control_pump(pin, state):
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
    print(f"{'Activating' if state else 'Deactivating'} pump on pin {pin}")

def drain_excess_water():
    """Drain until at or above DRAIN_TARGET or until safety timeout."""
    control_pump(PUMP_SEWER_PIN, True)
    print("Sewer pump activated to drain excess water.")
    start = time.time()
    try:
        while time.time() - start < DRAIN_MAX_SECONDS:
            dist = get_distance()
            if dist is None:
                print("Sensor read failed during draining; stopping drain for safety.")
                break
            print(f"Drain loop - current distance: {dist} cm")
            if dist <= DRAIN_TARGET:
                print(f"Reached drain target: {dist} cm")
                break
            time.sleep(1)
    finally:
        control_pump(PUMP_SEWER_PIN, False)
        print("Sewer pump deactivated.")

def water_plants(duration=WATER_PUMP_DURATION):
    control_pump(PUMP_WATER_PIN, True)
    print(f"Water pump activated for {duration} seconds.")
    time.sleep(duration)
    control_pump(PUMP_WATER_PIN, False)
    print("Water pump deactivated.")

def run_flow_once():
    """
    Run a single full pass of the flowchart decisions and actions.
    Returns True if any action was taken (drain or water), False otherwise.
    """
    action_taken = False

    dist = get_distance()
    lvl = level_state(dist)
    if lvl is None:
        print("Cannot determine level state (sensor error). Treating as no-action for safety.")
        return False

    # 1) Are there any showers coming (>20mm)?
    heavy = check_heavy_rain()
    if heavy is None:
        print("Weather unavailable; skip shower path and continue to drought/level checks.")
    elif heavy:
        print("Shower >20mm: Dump the water through the sewer pump.")
        drain_excess_water()
        action_taken = True
        # End of shower branch -> return to start (caller will decide whether to loop)
        return action_taken
    else:
        print("No heavy showers predicted: do nothing in shower branch.")

    # 2) Drought?
    # Drought meaning: precipitation below threshold; here heavy==False implies no heavy rain,
    # so we ask "Drought?" as a separate decision. For this implementation we treat drought as
    # the same boolean as 'no heavy rain' for the flowchart's binary branching.
    drought = not heavy if heavy is not None else False

    if not drought:
        print("Drought? No -> nothing.")
    else:
        print("Drought? Yes -> Check if we have enough water.")
        # 3) Do we have enough water? (14 - distance measured in a 14x14cm tank)
        # Interpretation: if distance <= EMERGENCY_DISTANCE then there is water available.
        if dist is None:
            print("Sensor failure while checking tank; cannot water.")
        elif dist <= EMERGENCY_DISTANCE:
            # We have enough water -> water plants
            print("We have enough water -> watering plants.")
            water_plants()
            action_taken = True
            return action_taken
        else:
            print("We do not have enough water -> nothing for watering branch.")

    # 4) Water level branch: Ok/High/Low
    print(f"Water level state: {lvl}")
    if lvl == 'ok':
        print("Level OK -> nothing.")
    elif lvl == 'high':
        print("Level HIGH -> empty half (drain half).")
        drain_excess_water()
        action_taken = True
    elif lvl == 'low':
        print("Level LOW -> register that we do not have enough water (for drought phase).")
        # Nothing to do now; this flag would inform future drought checks. No immediate action.

    return action_taken

# Repeat interval (hours) — change this to control how often the full flow runs
REPEAT_HOURS = 2       # <- main variable to change (default: 6 hours)

# Debug override: when True, uses DEBUG_SECONDS instead of REPEAT_HOURS
DEBUG_MODE = False        # <- set True for fast testing
DEBUG_SECONDS = 10        # <- short interval used only when DEBUG_MODE is True

# Derived interval (seconds)
CHECK_INTERVAL = DEBUG_SECONDS if DEBUG_MODE else REPEAT_HOURS * 3600

# Main loop (use this in place of the previous main loop)
try:
    print("Starting flowchart-driven watering/drainage loop...")
    while True:
        # Run one full pass of the flowchart (no immediate repeating)
        run_flow_once()
        print(f"Cycle complete. Sleeping for {CHECK_INTERVAL} seconds before next run.")
        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    GPIO.cleanup()
    print("GPIO cleanup done.")
