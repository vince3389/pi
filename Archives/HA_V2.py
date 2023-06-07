import RPi.GPIO as GPIO
import Adafruit_DHT
from flask import Flask, jsonify
from w1thermsensor import W1ThermSensor

app = Flask(__name__)

# Set up the DS18B20 temperature sensor
ds_sensor = W1ThermSensor()
  
# Set up the DHT11 sensors
dht_pins = {
    'zone1': 5,
    'zone2': 17,
    'zone3': 27
} # GPIO pins connected to the DHT11 sensors

def read_temperature():
    temperature = ds_sensor.get_temperature()
    return temperature

def read_humidity():
    humidities = {}
    for location, pin in dht_pins.items():
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
        if humidity is not None:
            humidities[location] = humidity
    return humidities

def read_temperature_humidity():
    temperature_humidity = {}
    for location, pin in dht_pins.items():
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
        if humidity is not None:
            temperature_humidity[location] = {'temperature': temperature, 'humidity': humidity}
    return temperature_humidity

@app.route('/')
def home():
    return 'Welcome to the Raspberry Pi!'

@app.route('/temperature')
def temperature():
    temperature = read_temperature()
    return jsonify({'pool': temperature})

@app.route('/humidity')
def humidity():
    humidities = read_humidity()
    return jsonify(humidities)

@app.route('/temperature_humidity')
def temperature_humidity():
    temperature_humidity = read_temperature_humidity()
    return jsonify(temperature_humidity)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
