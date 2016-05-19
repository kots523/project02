import RPi.GPIO as gpio
import dht11
import time
import datetime
#import time,datetime, dht11 and gpio
recenttemp = 20; recenthum = 20;
#initialize first temperature and humidity as 20
trig_pin = 13
echo_pin = 19
instance = dht11.DHT11(pin = 5)
led_red = 12
led_yellow = 20
led_green = 21
# initialize each pin

# initialize GPIO
gpio.setmode(gpio.BCM)
gpio.setup(trig_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)
gpio.setwarnings(False)
gpio.setup(led_red, gpio.OUT)
gpio.setup(led_yellow, gpio.OUT)
gpio.setup(led_green, gpio.OUT)

def LEDredBlink():
	gpio.output(led_red, True)
	time.sleep(3)
	gpio.output(led_red, False)
	time.sleep(1)

def LEDyellowBlink():
	gpio.output(led_yellow, True)
	time.sleep(3)
	gpio.output(led_yellow, False)
	time.sleep(1)

def LEDgreenBlink():
	gpio.output(led_green, True)
	time.sleep(3)
	gpio.output(led_green, False)
	time.sleep(1)
#initialize each led light function
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
		result = instance.read()
		#save temperature and humidity index to result
		if(result.temperature != 0 and result.humidity != 0):
			recenttemp = result.temperature
			recenthum = result.humidity
		#if dht11 have delay then use recent temp and humidity data
		print ("---------------------------------------------------------")	
		print ("Last valid input: " + str(datetime.datetime.now()))
		print ("Temperature: %d C" % recenttemp)
		print ("Distance: ", distance, "cm")
		#print datetime, temperature and distance index
		if (recenttemp >= 20):
		#choose standard temperature to led light On 
			if(distance >= 100):
				print("LED Color : green")
				LEDgreenBlink()
			elif(distance >= 30 and distance < 100):
				print("LED Color : yellow")
				LEDyellowBlink()
			elif(distance < 30):
				print("LED Color : red")
				LEDredBlink()
		#select Ledlight color by distance data
		else:
			print("Led light Off")
		#if temperature is less than standard then led Off
		time.sleep(1)

except KeyboardInterrupt:
	gpio.cleanup()
#if keyboardinterrupt than cleanup gpio pin
