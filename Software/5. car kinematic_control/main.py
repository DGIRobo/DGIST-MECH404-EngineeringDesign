import time
import datetime

import os

import Batt_UMG

if __name__ == '__main__':
	car = Batt_UMG.Batt_UMG()

	starting_time = datetime.datetime.now().timestamp() # Dimension: sec
	previous_time = datetime.datetime.now().timestamp() # Dimension: sec

	while True:
		previous_time = current_time
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
		print('-----------------------------------------------------------')
		print(f'X position of car: {car._x}')
		print(f'Y position of car: {car._y}')
		print(f'Yaw position of car: {car._yaw}')
		print('-----------------------------------------------------------')
		print(f'X velocity of car: {car._vx}')
		print(f'Y velocity of car: {car._vx}')
		print(f'Yaw velocity of car: {car._yaw_rate}')

		# position PID
		#car.car_pos_PID(0.01, 1, 0, 0)
		# velocity PID
		#car.car_vel_PID(0.01, 1, 0, 0)

		os.system('clear') 
	car.shut_down()