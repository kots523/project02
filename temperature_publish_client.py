import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import dht11
import time
#import time, dht11 and mqtt and gpio

recenttemp = 20
#initailize first temperature as 20

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.cleanup()
#initialize GPIO
instance = dht11.DHT11(pin = 5)
#initialize Pin number at 5
mqttc = mqtt.Client("Temperature_pub")
#MQTT client object create
mqttc.connect("127.0.0.1", 1883)
#MQTT server connect
try:
	while True:
		result = instance.read()
		#save temp and humidity index to result
		if(result.temperature != 0):
			recenttemp = result.temperature
		#if dht11 have delay then  use recent temperature
		mqttc.publish("environment/temperature", recenttemp)
		#publish recent temperature index
		print "temperature : " + str(recenttemp)
		#print temperature index
		time.sleep(1)
		mqttc.loop(1)
		
except KeyboardInterrupt:
	gpio.cleanup()
#if keyboardinterrupt than cleanup gpio pin

