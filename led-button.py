#!/usr/bin/env python3
 
import RPi.GPIO as GPIO
import time
import requests

LedPin = 15    # pin15 --- led
BtnPin = 12    # pin12 --- button

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to make led off

# Line notify
url = "https://notify-api.line.me/api/notify"
access_token = "ICgrmOjf0ekBbbsAiqtRJz8Xy4h3niRafzNlwMg6m55"
headers = {'Authorization': 'Bearer ' + access_token}

def loop():
    while True:
        if GPIO.input(BtnPin) == GPIO.LOW: # Check whether the button is pressed.
            #print ('...led on')
            # Send to Line API
            message = '緊急ボタンの通知を検知しました'
            payload = {'message': message}
            r = requests.post(url, headers=headers, params=payload,)
            
            GPIO.output(LedPin, GPIO.LOW)  # led on
        else:
            #print ('led off...')
            GPIO.output(LedPin, GPIO.HIGH) # led off
        time.sleep(0.5)

def destroy():
    GPIO.output(LedPin, GPIO.HIGH)     # led off
    GPIO.cleanup()                     # Release resource
    print('-- cleanup GPIO!! --')

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
