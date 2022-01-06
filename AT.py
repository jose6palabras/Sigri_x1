#!/usr/bin/python

import serial
import time
ser = serial.Serial("/dev/ttyUSB2",115200)
ser.flushInput()
power_key = 6
command_input = ''
rec_buff = ''
try:
	while True:
		command_input = input('Please input the AT command:')
		ser.write((command_input + '\r\n').encode())
		time.sleep(0.1)
		if ser.inWaiting():
			time.sleep(0.5)
			rec_buff = ser.read(ser.inWaiting())
		if rec_buff != '':
			print(rec_buff.decode())
			rec_buff = ''
except KeyboardInterrupt:
	if ser != None:
		ser.close()
	