#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# MQTT broker configuration
mqtt_broker = "10.1.1.16"  # Change to the IP address of your MQTT broker
mqtt_port = 1883
mqtt_username = "homeassistant"  # Replace with your MQTT username
mqtt_password = "ul2aip8oe4kuu5ooruf4ishah1naig5ae8ookaich5iech9Ied2ookoonuquaiGh"  # Replace with your MQTT password
mqtt_topic = "home/sensors"  # MQTT topic for publishing sensor readings

# GPIO Configuration
reed_pins = [5, 26, 16, 20, 21]  # Replace with the actual GPIO pins connected to the reed sensors
pir_pins = [6, 13, 19]  # Replace with the actual GPIO pins connected to the PIR sensors

GPIO.setmode(GPIO.BCM)
for pin in reed_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in pir_pins:
    GPIO.setup(pin, GPIO.IN)

# Set up MQTT client
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, mqtt_port, 60)

while True:
    # Read reed sensor states
    reed_states = [GPIO.input(pin) for pin in reed_pins]

    # Read PIR sensor states
    pir_states = [GPIO.input(pin) for pin in pir_pins]

    # Publish reed sensor states via MQTT
    for i, state in enumerate(reed_states):
        client.publish(f"{mqtt_topic}/reed_sensor_{i+1}_state", state)

    # Publish PIR sensor states via MQTT
    for i, state in enumerate(pir_states):
        client.publish(f"{mqtt_topic}/pir_sensor_{i+1}_state", state)

    time.sleep(1)  # Publish the data every 1 second

# Clean up GPIO
GPIO.cleanup()
