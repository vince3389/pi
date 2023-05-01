sensor:
  - platform: rest
    resource: http://10.1.1.172:8000/temperature
    name: Temperature Sensor
    value_template: '{{ value_json.temperature }}'
    unit_of_measurement: '°C'
    scan_interval: 5
  - platform: rest
    resource: http://10.1.1.172:8000/temperature
    name: Humidity Sensor
    value_template: '{{ value_json.humidity }}'
    unit_of_measurement: '%'
    scan_interval: 5
  - platform: rest
    resource: http://10.1.1.172:8000/motion
    name: Motion Sensor
    value_template: '{{ value_json.motion }}'
    scan_interval: 5
      
      
      
      
      
