import time
import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import serial

# MQTT broker configuration
mqtt_broker = "10.1.1.16"  # Change to the IP address of your MQTT broker
mqtt_port = 1883
mqtt_username = "homeassistant"  # Replace with your MQTT username
mqtt_password = "ul2aip8oe4kuu5ooruf4ishah1naig5ae8ookaich5iech9Ied2ookoonuquaiGh"  # Replace with your MQTT password
mqtt_topic = "home/sensors"  # MQTT topic for publishing sensor readings

# Set up MQTT client
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, mqtt_port, 60)

# Main loop
while True:
   
    # Open serial connection for PMS5003 sensor
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=2.0)

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

    # Close serial connection for PMS5003 sensor
    ser.close()

    time.sleep(5)  # Delay between readings



# PMS5003 works with this script but not the other sensors.