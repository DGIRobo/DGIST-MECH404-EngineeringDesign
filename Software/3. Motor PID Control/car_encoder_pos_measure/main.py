import time
import datetime
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
		print(f'incremental position of FL wheel: {car.FL_motor._incremental_pos}')
		print(f'incremental position of FR wheel: {car.FR_motor._incremental_pos}')
		print(f'incremental position of BL wheel: {car.BL_motor._incremental_pos}')
		print(f'incremental position of BR wheel: {car.BR_motor._incremental_pos}')
		print('-----------------------------------------------------------')
		print(f'absolute position of FL wheel: {car.FL_motor._absolute_pos}')
		print(f'absolute position of FR wheel: {car.FR_motor._absolute_pos}')
		print(f'absolute position of BL wheel: {car.BL_motor._absolute_pos}')
		print(f'absolute position of BR wheel: {car.BR_motor._absolute_pos}')

		car.Joystick_PWM_Controller()

		previous_time = datetime.datetime.now().timestamp() # Dimension: sec
	car.shut_down()