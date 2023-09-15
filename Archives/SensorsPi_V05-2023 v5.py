######################
# THIS SCRIPT IS WORKING AS OF JUNE 16TH @ 22:52
# NOW INCLUDING PM2.5 AND PM10
###################################################


import RPi.GPIO as GPIO
import time
import serial
import paho.mqtt.client as mqtt
import Adafruit_DHT
from w1thermsensor import W1ThermSensor

# MQTT broker configuration
mqtt_broker = ""  # Change to the IP address of your MQTT broker
mqtt_port = 1883
mqtt_username = "homeassistant"  # Replace with your MQTT username
mqtt_password = ""  # Replace with your MQTT password
mqtt_topic = "home/sensors"  # MQTT topic for publishing sensor readings

# Disable UART on GPIO14
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)

# Open serial connection
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=2.0)

# Set up MQTT client
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, mqtt_port, 60)

# Request PMS5003 sensor data
ser.write(b'\x42\x4D\xE1\x00\x00\x01\x71')

# Read PMS5003 sensor data
response = ser.read(32)

# Check if the response has enough bytes
if len(response) >= 32:
    # Parse PMS5003 sensor data
    data = list(response)
    pm_2_5 = (data[10] << 8) | data[11]
    pm_10 = (data[12] << 8) | data[13]

    # Publish PMS5003 sensor readings via MQTT
    client.publish(f"{mqtt_topic}/pms5003_pm25", pm_2_5)
    client.publish(f"{mqtt_topic}/pms5003_pm10", pm_10)
else:
    print("Error: Insufficient PMS5003 data received")

# Read DHT11 sensors
dht_sensors = [
    {"name": "dht11_1", "pin": 22},
    {"name": "dht11_2", "pin": 17},
    {"name": "dht11_3", "pin": 27}
]

for sensor in dht_sensors:
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, sensor["pin"])

    if humidity is not None and temperature is not None:
        # Publish DHT11 sensor readings via MQTT
        client.publish(f"{mqtt_topic}/{sensor['name']}_temperature", round(temperature, 2))
        client.publish(f"{mqtt_topic}/{sensor['name']}_humidity", round(humidity, 2))
    else:
        print(f"Error: Failed to read DHT11 sensor data for {sensor['name']}")

# Read DS18B20 sensor data
ds18b20_sensor = W1ThermSensor()

try:
    ds18b20_temperature = ds18b20_sensor.get_temperature()

    # Publish DS18B20 sensor reading via MQTT
    client.publish(f"{mqtt_topic}/ds18b20_temperature", round(ds18b20_temperature, 2))
except Exception as e:
    print(f"Error reading DS18B20 sensor: {e}")

# Close serial connection
ser.close()

# Re-enable UART on GPIO14
GPIO.setup(14, GPIO.OUT)

# Clean up GPIO
GPIO.cleanup()
