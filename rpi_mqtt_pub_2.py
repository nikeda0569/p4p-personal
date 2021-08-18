#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
import requests

import paho.mqtt.client as mqtt 
from time import sleep

broker_address = "test.mosquitto.org"     #MQTT broker_address
Topic = "kameneko0569"

# publish MQTT
print("creating new instance")
client = mqtt.Client() #create new instance

print("connecting to broker: %s" % broker_address)
client.connect(broker_address) #connect to broker

print("Publishing message: detection or no detction and topic: %s" % (Topic))

# Line notify
url = "https://notify-api.line.me/api/notify"
access_token = "ICgrmOjf0ekBbbsAiqtRJz8Xy4h3niRafzNlwMg6m55"
headers = {'Authorization': 'Bearer ' + access_token}

PIR_OUT_PIN = 11    # pin11

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(PIR_OUT_PIN, GPIO.IN)    # Set BtnPin's mode is input

def loop():
	while True:
		total_count = 1
		n1 = 0
		n2 = 0
		while total_count <= 60:
			if GPIO.input(PIR_OUT_PIN) == GPIO.LOW:
				print(str(total_count) + "...Movement not detected!")
				n1 += 1
			else:
				print(str(total_count)+"...Movement detected!")
				n2 += 1

			total_count += 1
			sleep(1)
			Msg = "detection='" + str(n2) + "' no detection='" + str(n1) + "'"
		client.publish(Topic,Msg)
		print(' ')
		print('1分間に' + str(n2) + '回検知しました')
		print(' ')
		print(' ')
		# Send to Line API
		message = '1分間に' + str(n2) + '回検知しました'
		payload = {'message': message}
		r = requests.post(url, headers=headers, params=payload,)
 
def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
