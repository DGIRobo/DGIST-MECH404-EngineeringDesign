import time
import datetime

import os

import Batt_UMG

if __name__ == '__main__':
	car = Batt_UMG.Batt_UMG()

	starting_time = datetime.datetime.now().timestamp() # Dimension: sec
	previous_time = datetime.datetime.now().timestamp() # Dimension: sec

	while True:
		current_time = datetime.datetime.now().timestamp() # Dimension: sec

		car.FL_motor.motor_state_estimation()
		car.FR_motor.motor_state_estimation()
		car.BL_motor.motor_state_estimation()
		car.BR_motor.motor_state_estimation()

		print('-----------------------------------------------------------')
		print(f'current time: {current_time - starting_time}')
		print(f'time interval: {current_time - previous_time}')
		print('-----------------------------------------------------------')
		print(f'velocity of FL wheel: {car.FL_motor._vel}')
		print(f'velocity of FR wheel: {car.FR_motor._vel}')
		print(f'velocity of BL wheel: {car.BL_motor._vel}')
		print(f'velocity of BR wheel: {car.BR_motor._vel}')

		car.Joystick_PWM_Controller()
		
		previous_time = datetime.datetime.now().timestamp() # Dimension: sec

		os.system('clear') 
	car.shut_down()