# Working active SCript before implentation of PM2.5 PMS5003


############################################################
####### SCRIPT LAST VERSION MAY 30TH 2023 11H33  ############
############################################################
# BY VINCENT CHARRON

#Set up MQTT broker:

#Install and configure an MQTT broker on the Raspberry Pi. Mosquitto is a popular MQTT broker that you can install by running the command: 
#       sudo apt-get install mosquitto mosquitto-clients
#Start the Mosquitto service: 
#       sudo systemctl start mosquitto
#You may also want to enable the Mosquitto service to start on boot: 
#       sudo systemctl enable mosquitto 

#Install necessary libraries:
#   Install the w1thermsensor library for reading the temperature from the DS18B20 sensor by running: 
#       sudo pip install w1thermsensor
#   Install the paho-mqtt library for MQTT communication by running: 
#       sudo pip install paho-mqtt

#Create a Python script:

# nano SensorsPi_V05-2023.py

# Version June 28th 2023

import time
import json
import Adafruit_DHT
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt
import subprocess

# Define the command to run the script in the background
command1 = ["python3", "/home/sensor/Alarmpi.py", "&"]
command2 = ["python3", "/home/sensor/Pms5003.py", "&"]

# Run the command in the background
subprocess.Popen(command1)
subprocess.Popen(command2)

# MQTT broker configuration
mqtt_broker = "10.1.1.16"  # Change to the IP address of your MQTT broker
mqtt_port = 1883
mqtt_username = "homeassistant"  # Replace with your MQTT username
mqtt_password = "ul2aip8oe4kuu5ooruf4ishah1naig5ae8ookaich5iech9Ied2ookoonuquaiGh"  # Replace with your MQTT password
mqtt_topic = "home/sensors"  # MQTT topic for publishing sensor readings

# Connect to the MQTT broker with authentication
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, mqtt_port, 60)

# Publish sensor readings
def publish_sensor_reading(sensor_name, sensor_value):
    payload = {
        "sensor_name": sensor_name,
        "sensor_value": sensor_value
    }
    mqtt_topic_with_sensor = f"{mqtt_topic}/{sensor_name}"
    client.publish(mqtt_topic_with_sensor, json.dumps(payload))

# DHT11 Sensor Configuration
dht_sensors = [
    {"name": "dht11_1", "pin": 22},
    {"name": "dht11_2", "pin": 17},
    {"name": "dht11_3", "pin": 27}
]

# DS18B20 Sensor Configuration
ds18b20_sensor = W1ThermSensor()


while True:
    # Read DHT11 sensors
    for sensor in dht_sensors:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, sensor["pin"])
        if humidity is not None and temperature is not None:
            publish_sensor_reading(sensor["name"] + "_temperature", round(temperature, 2))
            publish_sensor_reading(sensor["name"] + "_humidity", round(humidity, 2))

    # Read DS18B20 sensor * un comment for Celsius
    ds18b20_temperature = ds18b20_sensor.get_temperature()

    #MY Test Farenheit * comment for celsius
    #ds18b20_temperature = round(ds18b20_sensor.get_temperature() * 9/5 + 32, 2)
    
    publish_sensor_reading("ds18b20_temperature", round(ds18b20_temperature, 2))
    
    time.sleep(5)  # Publish the data every 5 seconds










# Make sure the script runs in the background at restart by adding it here:
# sudo nano /etc/rc.local
# add a line with:
# python3 /home/sensor/SensorsPi_V05-2023.py



### Finaly I had to create the script as a service to be able to run in at boot in the background

