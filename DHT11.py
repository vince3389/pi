import time
import json
import Adafruit_DHT
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# ... (MQTT and other configurations) ...

#MQTT broker configuration
mqtt_broker = "10.1.1.16"  # Change to the IP address of your MQTT broker
mqtt_port = 1883
mqtt_username = "homeassistant"  # Replace with your MQTT username
mqtt_password = "ul2aip8oe4kuu5ooruf4ishah1naig5ae8ookaich5iech9Ied2ookoonuquaiGh"  # Replace with your MQTT password
mqtt_topic = "home/sensors"  # MQTT topic for publishing sensor readings

# Connect to the MQTT broker with authentication
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker, mqtt_port, 60)


def publish_sensor_reading(sensor_name, sensor_value):
    payload = {
        "sensor_name": sensor_name,
        "sensor_value": sensor_value
    }
    mqtt_topic_with_sensor = f"{mqtt_topic}/{sensor_name}"
    client.publish(mqtt_topic_with_sensor, json.dumps(payload))

def read_and_publish_sensor_data(sensor):
    try:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, sensor["pin"])
        if humidity is not None and temperature is not None:
            publish_sensor_reading(sensor["name"] + "_temperature", round(temperature, 2))
            publish_sensor_reading(sensor["name"] + "_humidity", round(humidity, 2))
        else:
            print(f"Failed to read sensor data for {sensor['name']}")
    except Exception as e:
        print(f"Error reading sensor {sensor['name']}: {str(e)}")

while True:
    for sensor in dht_sensors:
        read_and_publish_sensor_data(sensor)
    
    time.sleep(5)
