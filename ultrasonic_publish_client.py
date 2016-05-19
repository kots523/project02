import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import time
#import time and mqtt and gpio

trig_pin = 13
echo_pin = 19
#initialize pin number 13 and 19

gpio.setmode(gpio.BCM)
gpio.setup(trig_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)
#initialize GPIO

mqttc = mqtt.Client("ultrasonic_pub")
#MQTT client object create
mqttc.connect("127.0.0.1", 1883)
#MQTT server connect

try:
	while True:
		gpio.output(trig_pin, False)
		time.sleep(1)
		gpio.output(trig_pin, True)
		time.sleep(0.00001)
		gpio.output(trig_pin, False)
		
		while gpio.input(echo_pin) == 0:
			pulse_start = time.time()
		
		while gpio.input(echo_pin) == 1:
			pulse_end = time.time()
		#use ultrasonic sensor
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17000
		distance = round(distance, 2)
		#calcurate distance by measured ultrasonic data
		mqttc.publish("environment/ultrasonic", distance)
		#publish distance index
		print "distance : " + str(distance) + "cm"
		#print distance index
		mqttc.loop(1)

except KeyboardInterrupt:
	gpio.cleanup()
#if keyboardinterrupt than cleanup gpio pin
