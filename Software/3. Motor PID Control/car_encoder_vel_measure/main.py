import RPi.GPIO as IO
import datetime
import time
import os

import Batt_UMG

IO.setmode(IO.BCM)
IO.setwarnings(False)

# FL wheel encoder interrupt setting
FL_encPinA = 4
FL_encPinB = 17
IO.setup(FL_encPinA, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(FL_encPinB, IO.IN, pull_up_down=IO.PUD_UP)
FL_encoderPulses = 0
def FL_encoderA(channel):
    global FL_encoderPulses
    if IO.input(FL_encPinA) == IO.input(FL_encPinB):
        FL_encoderPulses += 1
    else:
        FL_encoderPulses -= 1
def FL_encoderB(channel):
    global FL_encoderPulses
    if IO.input(FL_encPinA) == IO.input(FL_encPinB):
        FL_encoderPulses -= 1
    else:
        FL_encoderPulses += 1
IO.add_event_detect(FL_encPinA, IO.BOTH, callback=FL_encoderA)
IO.add_event_detect(FL_encPinB, IO.BOTH, callback=FL_encoderB)

# FR wheel encoder interrupt setting
FR_encPinA = 27
FR_encPinB = 18
IO.setup(FR_encPinA, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(FR_encPinB, IO.IN, pull_up_down=IO.PUD_UP)
FR_encoderPulses = 0
def FR_encoderA(channel):
    global FR_encoderPulses
    if IO.input(FR_encPinA) == IO.input(FR_encPinB):
        FR_encoderPulses += 1
    else:
        FR_encoderPulses -= 1
def FR_encoderB(channel):
    global FR_encoderPulses
    if IO.input(FR_encPinA) == IO.input(FR_encPinB):
        FR_encoderPulses -= 1
    else:
        FR_encoderPulses += 1
IO.add_event_detect(FR_encPinA, IO.BOTH, callback=FR_encoderA)
IO.add_event_detect(FR_encPinB, IO.BOTH, callback=FR_encoderB)

# BL wheel encoder interrupt setting
BL_encPinA = 22
BL_encPinB = 23
IO.setup(BL_encPinA, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(BL_encPinB, IO.IN, pull_up_down=IO.PUD_UP)
BL_encoderPulses = 0
def BL_encoderA(channel):
    global BL_encoderPulses
    if IO.input(BL_encPinA) == IO.input(BL_encPinB):
        BL_encoderPulses += 1
    else:
        BL_encoderPulses -= 1
def BL_encoderB(channel):
    global BL_encoderPulses
    if IO.input(BL_encPinA) == IO.input(BL_encPinB):
        BL_encoderPulses -= 1
    else:
        BL_encoderPulses += 1
IO.add_event_detect(BL_encPinA, IO.BOTH, callback=BL_encoderA)
IO.add_event_detect(BL_encPinB, IO.BOTH, callback=BL_encoderB)

# BR wheel encoder interrupt setting
BR_encPinA = 10
BR_encPinB = 24
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

if __name__ == '__main__':
	car = Batt_UMG.Batt_UMG()
	starting_time = datetime.datetime.now().timestamp() # Dimension: sec
	current_time = datetime.datetime.now().timestamp() # Dimension: sec
	previous_time = datetime.datetime.now().timestamp() # Dimension: sec

	while True:
		os.system('clear') 
        
		current_time = datetime.datetime.now().timestamp() # Dimension: sec

		car.FL_motor.motor_state_estimation(FL_encoderPulses)
		car.FR_motor.motor_state_estimation(FR_encoderPulses)
		car.BL_motor.motor_state_estimation(BL_encoderPulses)
		car.BR_motor.motor_state_estimation(BR_encoderPulses)

		print('-----------------------------------------------------------')
		print(f'current time: {current_time - starting_time}')
		print(f'time interval: {current_time - previous_time}')
		print('-----------------------------------------------------------')
		print(f'velocity of FL wheel: {car.FL_motor._vel}')
		print(f'velocity of FR wheel: {car.FR_motor._vel}')
		print(f'velocity of BL wheel: {car.BL_motor._vel}')
		print(f'velocity of BR wheel: {car.BR_motor._vel}')

		#car.Joystick_PWM_Controller()
		
		previous_time = datetime.datetime.now().timestamp() # Dimension: sec
	car.shut_down()