import time
import Adafruit_DHT
import paho.mqtt.client as mqtt

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


# Function to read DHT11 sensor data and publish via MQTT
def read_dht11_sensor(pin, sensor_name):
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)

        if humidity is not None and temperature is not None:
            # Publish DHT11 sensor readings via MQTT
            client.publish(f"{mqtt_topic}/{sensor_name}_temperature", round(temperature, 2))
            client.publish(f"{mqtt_topic}/{sensor_name}_humidity", round(humidity, 2))
        else:
            print(f"Error: Failed to read DHT11 sensor data for {sensor_name}")

        time.sleep(5)


# Example usage for DHT11 sensors
dht_sensors = [
    {"pin": 22, "name": "dht11_1"},
    {"pin": 17, "name": "dht11_2"},
    {"pin": 27, "name": "dht11_3"}
]

for sensor in dht_sensors:
    # Create a new thread for each DHT11 sensor
    thread = threading.Thread(target=read_dht11_sensor, args=(sensor["pin"], sensor["name"]))
    thread.start()
