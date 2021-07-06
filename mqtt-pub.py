#!usr/bin/env python
# -*- coding: utf-8 -*- 

import paho.mqtt.client as mqtt 
from time import sleep

broker_address = "192.168.10.106"
Topic = "case10"
Msg = "hello mqtt"

def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, flag, rc):
  if rc != 0:
     print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
  print("publish: {0}".format(mid))

def main():
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_disconnect = on_disconnect
  client.on_publish = on_publish

  client.connect(broker_address, 1883, 60)

  client.loop_start()

  while True:
    client.publish(Topic,Msg) 
    sleep(1) 

if __name__ == '__main__': 
  main()