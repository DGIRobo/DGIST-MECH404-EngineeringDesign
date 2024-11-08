import time
import busio
import encoder
import filter

from board import SCL, SDA
from adafruit_pca9685 import PCA9685

class Motor:
	def __init__(self, IN1, IN2, ENA, encPinA, encPinB, cutoff): 
		'''
		IN1: Pin number of PCA which connect to IN1 at L298N
		IN2: Pin number of PCA which connect to IN2 at L298N
		ENA: Pin number of PCA which connect to ENA at L298N
		encPinA: Pin number of RPI which connect to A phase at encoder
		encPinB: Pin number of RPI which connect to B phase at encoder
		cutoff: cutoff frequency(Hz) which used at velocity derivation(tustin derivative)
		'''
		self.dir_pin1 = IN1
		self.dir_pin2 = IN2
		self.throttle_pin = ENA
		self._encoder = encoder.Encoder(encPinA, encPinB)
		self._cutoff = cutoff # Dimension: Hz
		self._motor_pos = 0 # Dimension: Radian
		self._motor_pos_old = 0 # Dimension: Radian
		self._motor_vel = 0 # Dimension: Rad/s
		self._motor_vel_old = 0 # Dimension: Rad/s
	
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
			self._motor_pos_old = self._motor_pos
			self._motor_pos = self._encoder._encoder_pos
			self._motor_vel_old = self._motor_vel
			self._motor_vel = filter.tustin_derivative(self._motor_pos, self._motor_pos_old, self._motor_vel_old, self._cutoff)