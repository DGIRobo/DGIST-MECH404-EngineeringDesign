import time
import busio

from board import SCL, SDA
from adafruit_pca9685 import PCA9685

class Motor:
	def __init__(self, IN1, IN2, ENA): 
		'''
		IN1: Pin number of PCA which connect to IN1 at L298N
		IN2: Pin number of PCA which connect to IN2 at L298N
		ENA: Pin number of PCA which connect to ENA at L298N
		'''
		self.dir_pin1 = IN1
		self.dir_pin2 = IN2
		self.throttle_pin = ENA
	
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