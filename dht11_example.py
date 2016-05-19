import RPi.GPIO as gpio
import dht11
import time
import datetime

# initialize GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.cleanup()

# read data using pin 5
instance = dht11.DHT11(pin = 5)

try:

	while True:
		result = instance.read()
		if result.is_valid():
			print("Last valid input: " + str(datetime.datetime.now()))
			print("Temperature: %d C" % result.temperature)
			print("Humidity: %d %%" % result.humidity)
    		
		time.sleep(1)

except KeyboardInterrupt:
	gpio.cleanup()
