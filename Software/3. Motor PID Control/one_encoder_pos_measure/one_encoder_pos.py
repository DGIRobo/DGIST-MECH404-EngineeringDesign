import RPi.GPIO as IO
import datetime
import time
import os

# BR wheel encoder interrupt setting
BR_encPinA = 10
BR_encPinB = 24
IO.setmode(IO.BCM)
IO.setwarnings(False)
IO.setup(BR_encPinA, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(BR_encPinB, IO.IN, pull_up_down=IO.PUD_UP)
BR_encoderPulses = 0
def BR_encoderA(channel):
    global BR_encoderPulses
    if IO.input(BR_encPinA) == IO.input(BR_encPinB):
        BR_encoderPulses += 1
    else:
        BR_encoderPulses -= 1
def BR_encoderB(channel):
    global BR_encoderPulses
    if IO.input(BR_encPinA) == IO.input(BR_encPinB):
        BR_encoderPulses -= 1
    else:
        BR_encoderPulses += 1
IO.add_event_detect(BR_encPinA, IO.BOTH, callback=BR_encoderA)
IO.add_event_detect(BR_encPinB, IO.BOTH, callback=BR_encoderB)

# model variables init
PI = 3.141592
dT = 0.01
previous_time = datetime.datetime.now().timestamp()
current_time = datetime.datetime.now().timestamp()
BR_incremental_pos = 0
BR_incremental_pos_old = 0
BR_vel = 0
BR_absolute_pos = 0

while True:
	os.system('clear')
	current_time = datetime.datetime.now().timestamp()
	BR_incremental_pos_old = BR_incremental_pos
	BR_incremental_pos = BR_encoderPulses * (2 * PI) / (44 * 29)
	BR_vel = (BR_incremental_pos - BR_incremental_pos_old) / dT
	BR_absolute_pos = (BR_encoderPulses % (44 * 29)) * (2 * PI) / (44 * 29)
	print(f'Incremental position of BR wheel: {BR_incremental_pos}')
	print(f'Absolute position of BR wheel: {BR_absolute_pos}')
	if (datetime.datetime.now().timestamp() - current_time) < dT:
			time.sleep(dT - (datetime.datetime.now().timestamp() - current_time))