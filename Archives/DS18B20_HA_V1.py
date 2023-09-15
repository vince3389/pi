import time
import paho.mqtt.client as mqtt
from w1thermsensor import W1ThermSensor

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


# Function to read DS18B20 sensor data and publish via MQTT
def read_ds18b20_sensor():
    sensor = W1ThermSensor()

    while True:
        try:
            temperature = sensor.get_temperature()

            # Publish DS18B20 sensor reading via MQTT
            client.publish(f"{mqtt_topic}/ds18b20_temperature", round(temperature, 2))
        except Exception as e:
            print(f"Error reading DS18B20 sensor: {e}")

        time.sleep(5)


# Run the DS18B20 sensor script
read_ds18b20



###################
# OLD SCRIPT
#from w1thermsensor import W1ThermSensor
#import paho.mqtt.client as mqtt
#import time
#import json

# MQTT broker configuration
#mqtt_broker = "10.1.1.16"  # Change to the IP address of your MQTT broker
#mqtt_port = 1883
#mqtt_username = "homeassistant"  # Replace with your MQTT username
#mqtt_password = "ul2aip8oe4kuu5ooruf4ishah1naig5ae8ookaich5iech9Ied2ookoonuquaiGh"  # Replace with your MQTT password
#mqtt_topic = "home/sensors"  # MQTT topic for publishing sensor readings

# Connect to the MQTT broker with authentication
#client = mqtt.Client()
#client.username_pw_set(mqtt_username, mqtt_password)
#client.connect(mqtt_broker, mqtt_port, 60)

# Publish sensor readings
#def publish_sensor_reading(sensor_name, sensor_value):
#    payload = {
#        "sensor_name": sensor_name,
#        "sensor_value": sensor_value
#    }
#    mqtt_topic_with_sensor = f"{mqtt_topic}/{sensor_name}"
#    client.publish(mqtt_topic_with_sensor, json.dumps(payload))


# DS18B20 Sensor Configuration
#ds18b20_sensor = W1ThermSensor()

#while True:
    # Read DS18B20 sensor
#    ds18b20_temperature = ds18b20_sensor.get_temperature()
#    publish_sensor_reading("ds18b20_temperature", round(ds18b20_temperature, 2))


#time.sleep(5)  # Publish the data every 5 seconds