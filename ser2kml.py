#!/usr/bin/python3

# Testing on Linux:
# socat -d -d pty,raw,echo=0 pty,raw,echo=0
# TERM1: python3 ser2kml.py /dev/pts/1
# TERM2: cat data.kml > /dev/pts/2

import serial
import sys
from flask import Flask

app = Flask(__name__)

# Settings
if len(sys.argv) < 2:
	print("Usage: python3 ser2kml.py COM1")
	quit()

port = sys.argv[1] #  
baud = 9600 # Serial
tcp = 2021 # web server eg. http://127.0.0.1:2021
interface = "0.0.0.0" # 127.0.0.1 for local clients only

ser = serial.Serial(port, baud, timeout=0)
data = ""

@app.route('/')
def return_data():
	global data
	buffer = ""
	while True:
		if (ser.inWaiting()>0): 
			data_str = ser.read(ser.inWaiting()).decode('ascii') 
			print(data_str, end='') 
			buffer += data_str
		else:
			break
	if len(buffer) > 0:
		data=buffer
	return data

app.run(host=interface, port=tcp)
