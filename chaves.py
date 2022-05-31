#! /usr/bin/python2
# -*- Coding: UTF-8 -*-
#coding: utf-8
import RPi.GPIO as GPIO
import time
import threading
import sys
import smtplib, ssl

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

EMULATE_HX711=False

cred = credentials.Certificate("/home/pi/Documents/NEECKey/serviceAccountKey.json")
referenceUnit = 1
sender = "testedojosedossantos"
sender_mail = "sede.neec@gmail.com"
password = "cQEG8N7XLlxBSnPtPB"
receiver_mail = "contacto@neecist.org"
mode = 0
open_message = """\
Subject: Sede Status - Opened

A sede esta aberta!"""

close_message = """\
Subject: Sede Status - Closed

A sede esta fechada!"""

time.sleep(1)

if not EMULATE_HX711:
	import RPi.GPIO as GPIO
	from hx711 import HX711
else:
	from emulated_hx711 import HX711

def cleanAndExit():
	print("Cleaning...")

	if not EMULATE_HX711:
		GPIO.cleanup()
		
	print("Bye!")
	sys.exit()

#LIGAR O FIO DOUT AO GPIO5
#LIGAR O FIO SCK AO GPIO6
hx = HX711(5, 6)

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()

# server = smtplib.SMTP("smtp.gmail.com", port = 587)
# server.starttls()
# server.login(sender, password)

firebase_admin.initialize_app(cred, {'databaseURL': 'https://neec-chaves-default-rtdb.europe-west1.firebasedatabase.app/'})

while True:
	try:
		# These three lines are usefull to debug wether to use MSB or LSB in the reading formats
		# for the first parameter of "hx.set_reading_format("LSB", "MSB")".
		# Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
		
		# np_arr8_string = hx.get_np_arr8_string()
		# binary_string = hx.get_binary_string()
		# print binary_string + " " + np_arr8_string
		
		# Prints the weight. Comment if you're debbuging the MSB and LSB issue.
		val = hx.get_weight(5)
		# print(val)

		if val > 20000 and mode == 0:
			# server.sendmail(sender_mail, receiver_mail, open_message)
			mode = 1
			print("Sede aberta!")
			ref = db.reference('Sede')
			ref.update({'Open': 'True'})

		if val < 10000 and mode == 1:
			# server.sendmail(sender_mail, receiver_mail, close_message)
			mode = 0
			print("Sede fechada!")
			ref = db.reference('Sede')
			ref.update({'Open': 'False'})

			# To get weight from both channels (if you have load cells hooked up 
			# to both channel A and B), do something like this
			#val_A = hx.get_weight_A(5)
			#val_B = hx.get_weight_B(5)
			#print "A: %s  B: %s" % ( val_A, val_B )

			hx.power_down()
			hx.power_up()
			time.sleep(0.1)
		
		time.sleep(10)

	except (KeyboardInterrupt, SystemExit):
		cleanAndExit()
