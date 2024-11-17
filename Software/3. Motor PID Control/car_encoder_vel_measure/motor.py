import time
import datetime
import busio

from board import SCL, SDA
from adafruit_pca9685 import PCA9685

PI = 3.141592

class Motor:
	def __init__(self, IN1, IN2, ENA, dT): 
		'''
		IN1: Pin number of PCA which connect to IN1 at L298N
		IN2: Pin number of PCA which connect to IN2 at L298N
		ENA: Pin number of PCA which connect to ENA at L298N
		'''
		self.dir_pin1 = IN1
		self.dir_pin2 = IN2
		self.throttle_pin = ENA
		self._dT = dT
		self._incremental_pos = 0 # Dimension: rad
		self._incremental_pos_old = 0 # Dimension: rad
		self._vel = 0 # Dimension: rad/s
		self._absolute_pos = 0 # Dimension: rad
	
	def PWM_Controller(self, pca, throttle):
		'''
		throttle: -1~1 PWM Ratio
		'''
		if throttle < 0:
			pca.channels[self.dir_pin1].duty_cycle = 0x0000
			pca.channels[self.dir_pin2].duty_cycle = 0xFFFF
		else:
			pca.channels[self.dir_pin1].duty_cycle = 0xFFFF
			pca.channels[self.dir_pin2].duty_cycle = 0x0000
		throttle = round(abs(throttle) * 65535)
		if throttle > 0xFFFF:
			pca.channels[self.throttle_pin].duty_cycle = 0xFFFF
		else:
			pca.channels[self.throttle_pin].duty_cycle = throttle
	
	def motor_state_estimation(self, encoder_pulses):
		self._incremental_pos_old = self._incremental_pos # Dimension: rad
		self._incremental_pos = encoder_pulses * (2 * PI) / (44 * 29) # Dimension: rad
		self._vel = (self._incremental_pos - self._incremental_pos_old) / self._dT # Dimension: rad/s
		self._absolute_pos = (encoder_pulses % (44 * 29)) * (2 * PI) / (44 * 29) # Dimension: rad