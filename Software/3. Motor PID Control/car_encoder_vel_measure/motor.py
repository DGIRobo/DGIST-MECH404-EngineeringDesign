import time
import datetime
import busio
import encoder

from board import SCL, SDA
from adafruit_pca9685 import PCA9685

PI = 3.141592

class Motor:
	def __init__(self, IN1, IN2, ENA, encPinA, encPinB): 
		'''
		IN1: Pin number of PCA which connect to IN1 at L298N
		IN2: Pin number of PCA which connect to IN2 at L298N
		ENA: Pin number of PCA which connect to ENA at L298N
		encPinA: Pin number of RPI which connect to A phase at encoder
		encPinB: Pin number of RPI which connect to B phase at encoder
		'''
		self.dir_pin1 = IN1
		self.dir_pin2 = IN2
		self.throttle_pin = ENA
		self._encoder = encoder.Encoder(encPinA, encPinB)
		self._previous_time = datetime.datetime.now().timestamp() # Dimension: sec
		self._current_time = datetime.datetime.now().timestamp() # Dimension: sec
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
	
	def motor_state_estimation(self):
		self._current_time = datetime.datetime.now().timestamp() # Dimension: sec
		time_interval = self._current_time - self._previous_time # Dimension: sec
		self._incremental_pos_old = self._incremental_pos # Dimension: rad
		self._incremental_pos = self._encoder._encoder_pulses * (2 * PI) / (44 * 29) # Dimension: rad
		self._vel = (self._incremental_pos - self._incremental_pos_old) / time_interval # Dimension: rad/s
		self._absolute_pos = (self._encoder._encoder_pulses % (44 * 29)) * (2 * PI) / (44 * 29) # Dimension: rad
		self._previous_time = datetime.datetime.now().timestamp() # Dimension: sec