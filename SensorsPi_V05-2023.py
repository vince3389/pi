import time
import json
import Adafruit_DHT
from w1thermsensor import W1ThermSensor
import paho.mqtt.client as mqtt

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

    # Read DS18B20 sensor
    ds18b20_temperature = ds18b20_sensor.get_temperature()
    publish_sensor_reading("ds18b20_temperature", round(ds18b20_temperature, 2))

    time.sleep(5)  # Publish the data every 5 seconds
