#import context
import paho.mqtt.client as mqtt
import os
import json
import base64
from AzureBridge import sendToAzure

#Azure connection string
CONNECTION_STRING_1 = "HostName=Slim-Kippenhok-IoTHub.azure-devices.net;DeviceId=Pycom-SK;SharedAccessKey=5Hu6t9/O6s7OX2m3pu0m7td178cGHO4wEHDTT3vJgXM="


#Topics of the The Things Network built-in broker
TOPIC_DEV_1 = "dieterlopytest/devices/lopy42/up"

port = 1883
username = "dieterlopytest"
password = "ttn-account-v2.jEiezMxXcD0s9AoEp5lXuRZs1AIm0ml_sllESoTpQ88"
host = "eu.thethings.network"
clientid = "azure-bridge"
cleansession = True
keepalive = 600
qos = 0

#Callback method on message received
def on_message(mqttc, obj, msg):
	print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
	#Get TTN auto generated json for message
	payload_json = json.loads(msg.payload)
	#Decode the payload of the final message from json -- it is the json we are looking for
	message = base64.b64decode(payload_json.get('payload_raw').encode('ascii')).decode('ascii')
	#send to azure
	print("Sending to azure: ", message)
	#Send to the right device
	if msg.topic == TOPIC_DEV_1 : sendToAzure(CONNECTION_STRING_1, message)

mqttc = mqtt.Client(clientid,cleansession)

#Set callback method
mqttc.on_message = on_message

mqttc.username_pw_set(username, password)
print("Connecting to "+host+" port: "+ str(port))
mqttc.connect(host, port, keepalive)
mqttc.subscribe(TOPIC_DEV_1, qos)
mqttc.loop_forever()
