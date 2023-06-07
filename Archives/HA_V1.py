

####################################  
# Script for Pi


import Adafruit_DHT
import RPi.GPIO as GPIO
from flask import Flask, jsonify

app = Flask(__name__)

# Set up the temperature sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17

# Set up the PIR sensor
PIR_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

@app.route('/temperature')
def get_temperature():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return jsonify({'temperature': temperature, 'humidity': humidity})
    else:
        return jsonify({'error': 'Failed to read sensor data'})

@app.route('/motion')
def get_motion():
    if GPIO.input(PIR_PIN):
        return jsonify({'motion': True})
    else:
        return jsonify({'motion': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
   
      
      
