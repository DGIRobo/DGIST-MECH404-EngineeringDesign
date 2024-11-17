import time
import datetime
import numpy as np
import busio
import RPi.GPIO as IO
import motor
import gamepads

from board import SCL, SDA
from adafruit_pca9685 import PCA9685

class Batt_UMG:
	def __init__(self):
		# Car state variables
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
		self._vx = 0
		self._vy = 0
		self._yaw_rate = 0
		self._x = 0
		self._y = 0
		self._yaw = 0
		# Car Control variables
		self.car_pos_error = np.zeros((3, 1))
		self.car_pos_error_old = np.zeros((3, 1))
		self.car_pos_error_derivative = np.zeros((3, 1))
		self.car_pos_error_accumulate = np.zeros((3, 1))
		self.car_vel_error = np.zeros((3, 1))
		self.car_vel_error_old = np.zeros((3, 1))
		self.car_vel_error_derivative = np.zeros((3, 1))
		self.car_vel_error_accumulate = np.zeros((3, 1))
		# Time variables for control
		self._system_starting_time = datetime.datetime.now().timestamp() # Dimension: sec
		self._prev_time = datetime.datetime.now().timestamp() # Dimension: sec
		self._starting_time = datetime.datetime.now().timestamp() # Dimension: sec
		self._end_time = datetime.datetime.now().timestamp() # Dimension: sec
		self._running_time = self._starting_time - self._system_starting_time # Dimension: sec
		self._dT = 0.02 # Dimension: sec
		# Hardware init settings
		self.i2c = busio.I2C(SCL, SDA)
		self.pca = PCA9685(self.i2c, address=0x40)
		self.pca.frequency = 1000 # Dimension: Hz
		self.FL_motor = motor.Motor(0, 1, 4, self._dT)
		self.FR_motor = motor.Motor(3, 2, 5, self._dT)
		self.BL_motor = motor.Motor(8, 9, 6, self._dT)
		self.BR_motor = motor.Motor(11, 10, 7, self._dT)
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
		vx = gamepad_input.analog_stick_left.y # range = -1~1
		vy = gamepad_input.analog_stick_left.x * (-1) # range = -1~1
		yaw = gamepad_input.analog_stick_right.x * (-1) # range = -1~1
		print(f'vx={vx}, vy={vy}, yaw={yaw}')
		car_velocity_states = np.transpose(np.array([vx, vy, yaw]))
		wheel_angular_velocities = self.Inverse_Kinematics(car_velocity_states)
		self.PWM_Controller(wheel_angular_velocities)
	
	def car_state_estimation(self, FL_encoder_pulses, FR_encoder_pulses, BL_encoder_pulses, BR_encoder_pulses):
		self._running_time = self._starting_time - self._system_starting_time # Dimension: sec
		# motor state update
		self.FL_motor.motor_state_estimation(FL_encoder_pulses)
		self.FR_motor.motor_state_estimation(FR_encoder_pulses)
		self.BL_motor.motor_state_estimation(BL_encoder_pulses)
		self.BR_motor.motor_state_estimation(BR_encoder_pulses)
		# car velocity update
		wheel_angular_velocities = np.transpose(np.array([self.FL_motor._vel, self.FR_motor._vel, self.BL_motor._vel, self.BR_motor._vel]))
		car_velocity_states = self.Forward_Kinematics(wheel_angular_velocities)
		self._vx = car_velocity_states[0]
		self._vy = car_velocity_states[1]
		self._yaw_rate = car_velocity_states[2]
		# car position update
		wheel_angular_positions = np.transpose(np.array([self.FL_motor._incremental_pos, self.FR_motor._incremental_pos, self.BL_motor._incremental_pos, self.BR_motor._incremental_pos]))
		car_position_states = self.Forward_Kinematics(wheel_angular_positions)
		self._x = car_position_states[0]
		self._y = car_position_states[1]
		self._yaw = car_position_states[2]
	
	def single_motor_incremental_pos_control(self, target_motor, incremental_pos_ref, kp, kd, ki):
		if target_motor == 'FL_motor':
			self.FL_motor.motor_incremental_pos_PID(self.pca, incremental_pos_ref, kp, kd, ki)
		if target_motor == 'FR_motor':
			self.FR_motor.motor_incremental_pos_PID(self.pca, incremental_pos_ref, kp, kd, ki)
		if target_motor == 'BL_motor':
			self.BL_motor.motor_incremental_pos_PID(self.pca, incremental_pos_ref, kp, kd, ki)
		if target_motor == 'BR_motor':
			self.BR_motor.motor_incremental_pos_PID(self.pca, incremental_pos_ref, kp, kd, ki)

	def single_motor_absolute_pos_control(self, target_motor, absolute_pos_ref, kp, kd, ki):
		if target_motor == 'FL_motor':
			self.FL_motor.motor_absolute_pos_PID(self.pca, absolute_pos_ref, kp, kd, ki)
		if target_motor == 'FR_motor':
			self.FR_motor.motor_absolute_pos_PID(self.pca, absolute_pos_ref, kp, kd, ki)
		if target_motor == 'BL_motor':
			self.BL_motor.motor_absolute_pos_PID(self.pca, absolute_pos_ref, kp, kd, ki)
		if target_motor == 'BR_motor':
			self.BR_motor.motor_absolute_pos_PID(self.pca, absolute_pos_ref, kp, kd, ki)

	def single_motor_vel_control(self, target_motor, vel_ref, kp, kd, ki):
		if target_motor == 'FL_motor':
			self.FL_motor.motor_vel_PID(self.pca, vel_ref, kp, kd, ki)
		if target_motor == 'FR_motor':
			self.FR_motor.motor_vel_PID(self.pca, vel_ref, kp, kd, ki)
		if target_motor == 'BL_motor':
			self.BL_motor.motor_vel_PID(self.pca, vel_ref, kp, kd, ki)
		if target_motor == 'BR_motor':
			self.BR_motor.motor_vel_PID(self.pca, vel_ref, kp, kd, ki)
	
	def car_pos_PID(self, car_pos_ref, kp, kd, ki):
		self.car_pos_error_old = self.car_pos_error
		self.car_pos_error = car_pos_ref - np.transpose(np.array([self._x, self._y, self._yaw]))
		self.car_pos_error_derivative = (self.car_pos_error - self.car_pos_error_old) / self._dT
		self.car_pos_error_accumulate = self.car_pos_error_accumulate + self.car_pos_error * self._dT
		ctr_output = kp * self.car_pos_error + kd * self.car_pos_error_derivative + ki * self.car_pos_error_accumulate
		wheel_angular_positions = self.Inverse_Kinematics(ctr_output)
		self.PWM_Controller(wheel_angular_positions/26)

	def car_vel_PID(self, car_vel_ref, kp, kd, ki):
		self.car_vel_error_old = self.car_vel_error
		self.car_vel_error = car_vel_ref - np.transpose(np.array([self._vx, self._vy, self._yaw_rate]))
		self.car_vel_error_derivative = (self.car_vel_error - self.car_vel_error_old) / self._dT
		self.car_vel_error_accumulate = self.car_vel_error_accumulate + self.car_vel_error * self._dT
		ctr_output = kp * self.car_vel_error + kd * self.car_vel_error_derivative + ki * self.car_vel_error_accumulate
		wheel_angular_velocities = self.Inverse_Kinematics(ctr_output)
		self.PWM_Controller(wheel_angular_velocities/26)
	
	def shut_down(self):
		self.FL_motor.PWM_Controller(self.pca, 0)
		self.FR_motor.PWM_Controller(self.pca, 0)
		self.BL_motor.PWM_Controller(self.pca, 0)
		self.BR_motor.PWM_Controller(self.pca, 0)
		self.pca.deinit()