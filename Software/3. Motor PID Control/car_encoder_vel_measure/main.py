import time
import Batt_UMG

if __name__ == '__main__':
	car = Batt_UMG.Batt_UMG()
	while True:
		car.FL_motor.motor_state_estimation()
		car.FR_motor.motor_state_estimation()
		car.BL_motor.motor_state_estimation()
		car.BR_motor.motor_state_estimation()

		print('-----------------------------------------------------------')
		print(f'velocity of FL wheel: {car.FL_motor._vel}')
		print(f'velocity of FR wheel: {car.FR_motor._vel}')
		print(f'velocity of BL wheel: {car.BL_motor._vel}')
		print(f'velocity of BR wheel: {car.BR_motor._vel}')

		car.Joystick_PWM_Controller()
		
		time.sleep(0.5)
	car.shut_down()