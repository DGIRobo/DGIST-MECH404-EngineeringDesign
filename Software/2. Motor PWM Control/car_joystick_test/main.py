import time
import Batt_UMG

if __name__ == '__main__':
	car = Batt_UMG.Batt_UMG()
	while True:
		car.Joystick_PWM_Controller()
	car.shut_down()