import paho.mqtt.client as mqtt
import time
import smbus
import json
import datetime
from datetime import datetime
#datetime.datetime.now()
from mpu6050 import mpu6050
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Set up the MQTT client
myMQTTClient = AWSIoTMQTTClient("clientid")
myMQTTClient.configureEndpoint("a3sllhn7oev934-ats.iot.eu-central-1.amazonaws.com", 8883) 
#Provide your AWS IoT Core endpoint 

myMQTTClient.configureCredentials ("/home/guest/Downloads/RaspberryPiawsiot/AmazonRootCA1.pem", "/home/guest/Downloads/RaspberryPiawsiot/private.pem.key", "/home/guest/Downloads/RaspberryPiawsiot/certificate.pem.crt") 

myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
  
myMQTTClient.connect()

sensor = mpu6050(0x68)
time.sleep(1)
start_time = time.time()
end_time = start_time + 60 * 60 #  Run for 15 minutes

while time.time() < end_time:
    current_time = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")

    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    temp = sensor.get_temp()

    # Extract the acceleration and gyroscope values
    ax = accel_data['x']
    ay = accel_data['y']
    az = accel_data['z']
    gx = gyro_data['x']
    gy = gyro_data['y']
    gz = gyro_data['z']

    # Create a dictionary object with the sensor data
    sensor_data = {
        "timestamp": current_time,
        "acceleration": {
            "x": ax,
            "y": ay,
            "z": az
        },
        "gyroscope": {
            "x": gx,
            "y": gy,
            "z": gz
        },
        "temperature": temp 
    }

    # Convert the dictionary object to a JSON string
    json_data = json.dumps(sensor_data)

    # Publish the sensor data to the MQTT broker
    myMQTTClient.publish(topic="mpu6050", payload=json_data, QoS=1)

    # Wait for 1 second before reading again
    time.sleep(1)
    print('Sucess')

# Disconnect the MQTT client
myMQTTClient.disconnect()
print("Completed")
