import time
import numpy as np
import busio
import RPi.GPIO as IO
import motor
import gamepads

from board import SCL, SDA
from adafruit_pca9685 import PCA9685

class Batt_UMG:
	def __init__(self):
		self.r = 0.04 # dimension: m
		self.lx = 0.22 # dimension: m
		self.ly = 0.18 # dimension: m
		self.J_Forward = (self.r/4) * np.array([[1, 1, 1, 1],
												[-1, 1, 1, -1],
												[-1/(self.lx+self.ly), 1/(self.lx+self.ly), -1/(self.lx+self.ly), 1/(self.lx+self.ly)]])
		self.J_Inverse = (1/self.r) * np.array([[1, -1, -(self.lx+self.ly)],
												[1, 1, (self.lx+self.ly)],
												[1, 1, -(self.lx+self.ly)],
												[1, -1, (self.lx+self.ly)]])
		self.i2c = busio.I2C(SCL, SDA)
		self.pca = PCA9685(self.i2c, address=0x40)
		self.pca.frequency = 100 # Dimension: Hz
		IO.setmode(IO.BCM)
		IO.setwarnings(False)
		self.cutoff = 10 # Dimension: Hz
		self.FL_motor = motor.Motor(0, 1, 4, 4, 17, self.cutoff)
		self.FR_motor = motor.Motor(3, 2, 5, 27, 18, self.cutoff)
		self.BL_motor = motor.Motor(8, 9, 6, 22, 23, self.cutoff)
		self.BR_motor = motor.Motor(11, 10, 7, 10, 24, self.cutoff)
		self.shanwan_gamepad = gamepads.ShanWanGamepad()

	def PWM_Controller(self, throttles):
		self.FL_motor.PWM_Controller(self.pca, throttles[0])
		self.FR_motor.PWM_Controller(self.pca, throttles[1])
		self.BL_motor.PWM_Controller(self.pca, throttles[2])
		self.BR_motor.PWM_Controller(self.pca, throttles[3])
		
	def Forward_Kinematics(self, wheel_angular_velocities):
		'''
		wheel_angular_velocities = [omega_FL, omega_FR, omega_BL, omeg_BR]^T
		'''
		car_velocity_states = self.J_Forward @ wheel_angular_velocities
		return car_velocity_states
	
	def Inverse_Kinematics(self, car_velocity_states):
		'''
		car_velocity_states = [v_x, v_y, yaw]^T
		'''
		wheel_angular_velocities = self.J_Inverse @ car_velocity_states
		return wheel_angular_velocities 
		
	def Joystick_PWM_Controller(self):
		gamepad_input = self.shanwan_gamepad.read_data()
		vx = gamepad_input.analog_stick_left.y * (0.02) # range = -0.02~0.02
		vy = gamepad_input.analog_stick_left.x * (-0.02) # range = -0.02~0.02
		yaw = gamepad_input.analog_stick_right.x * (-self.lx-self.ly)
		print(f'vx={vx}, vy={vy}, yaw={yaw}')
		car_velocity_states = np.transpose(np.array([vx, vy, yaw]))
		wheel_angular_velocities = self.Inverse_Kinematics(car_velocity_states)
		self.PWM_Controller(wheel_angular_velocities)
	
	def shut_down(self):
		self.pca.deinit()