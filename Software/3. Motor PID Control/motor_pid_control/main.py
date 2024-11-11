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

		car.car_state_estimation()

		print('-----------------------------------------------------------')
		print(f'current time: {current_time - starting_time}')
		print(f'time interval: {current_time - previous_time}')
		print('-----------------------------------------------------------')
		print(f'position of FL wheel: {car.FL_motor._incremental_pos}')
		print(f'position of FR wheel: {car.FR_motor._incremental_pos}')
		print(f'position of BL wheel: {car.BL_motor._incremental_pos}')
		print(f'position of BR wheel: {car.BR_motor._incremental_pos}')
		print('-----------------------------------------------------------')
		print(f'velocity of FL wheel: {car.FL_motor._vel}')
		print(f'velocity of FR wheel: {car.FR_motor._vel}')
		print(f'velocity of BL wheel: {car.BL_motor._vel}')
		print(f'velocity of BR wheel: {car.BR_motor._vel}')

		# target motor setting
		target_motor = 'FL_motor'
		# position PID
		#car.single_motor_incremental_pos_control(target_motor, 2*3.14, 1, 0, 0)
		# velocity PID
		#car.single_motor_vel_control(target_motor, 1, 1, 0, 0)
		
		previous_time = datetime.datetime.now().timestamp() # Dimension: sec

		os.system('clear') 
	car.shut_down()