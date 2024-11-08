import time
import Batt_UMG

if __name__ == '__main__':
	car = Batt_UMG.Batt_UMG()
	while True:
		car.Joystick_PWM_Controller()
		print(f'position of FL wheel: {car.FL_motor._encoder._encoder_pos}')
		print(f'position of FR wheel: {car.FR_motor._encoder._encoder_pos}')
		print(f'position of BL wheel: {car.BL_motor._encoder._encoder_pos}')
		print(f'position of BR wheel: {car.BR_motor._encoder._encoder_pos}')
		time.sleep(0.1)
	car.shut_down()