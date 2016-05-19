import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import time
import datetime
#import time, datetime and mqtt and gpio

led_red = 12
led_yellow = 20
led_green = 21
#initialize pin number 12, 20 and 21 as Led

T = 0; D = 0; D_new = 0;
#initialize variable to save temperature and distance

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(led_red, gpio.OUT)
gpio.setup(led_yellow, gpio.OUT)
gpio.setup(led_green, gpio.OUT)
#initialize GPIO
def LEDredBlink():
	gpio.output(led_red, True)
	time.sleep(1)
	gpio.output(led_red, False)
	time.sleep(0.00001)

def LEDyellowBlink():
	gpio.output(led_yellow, True)
	time.sleep(1)
	gpio.output(led_yellow, False)
	time.sleep(0.00001)

def LEDgreenBlink():
	gpio.output(led_green, True)
	time.sleep(1)
	gpio.output(led_green, False)
	time.sleep(0.00001)
#initialize each led light function

def on_connect(client, userdata, rc):
	print("Connected with result coe" + str(rc))
	client.subscribe("environment/temperature")
	client.subscribe("environment/ultrasonic")
#callback if receive CONNACK answer by client_server

#callback if receive PUBLISH message by server
def on_message(client, userdata, msg):
	global T, D, D_new
	#use global variable
	if msg.topic == "environment/temperature":
		T = float(msg.payload)
	#if message topic is temperature data then save in variable T
	elif msg.topic == "environment/ultrasonic":
		D = float(msg.payload)
		D_new = 1
	#if message topic is ultrasonic data then save in variable D
	#init checksum variable to evasion overlap data
	try:
		print ("---------------------------------------------------------")	
		print ("Last valid input: " + str(datetime.datetime.now()))
		print ("Temperature: %d C" % T)			
		print ("Distance: ", D, "cm")
		#print datetime, temperature and distance data
		if (D_new == 1):
		#use checksum data te evasion overlap data
			if (T  >= 20):
			#choose standard temperature to led light On
				if(D >= 100):
					print("LED Color : green")
					LEDgreenBlink()
				elif(D >= 30 and D < 100):
					print("LED Color : yellow")
					LEDyellowBlink()
				elif(D < 30):
					print("LED Color : red")
					LEDredBlink()
				#select Ledlight color by distance data
			else:
				print("Led light Off")
			#if temperature is less than standard then led Off
		D_new = 0
		#init checksum
	except KeyboardInterrupt:
		gpio.cleanup()
	#if keyboardintterrupt than cleanup gpio pin
client = mqtt.Client()
#MQTT Client object create
client.on_connect = on_connect
#on_connect callback create
client.on_message = on_message
#on_message callback create

client.connect("127.0.0.1", 1883, 60)
#MQTT server connect
client.loop_forever()
#loop program

