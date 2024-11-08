import RPi.GPIO as IO

class Encoder:
	def __init__(self, encPinA, encPinB):
		'''
		encPinA: Pin number of RPI which connect to A phase at encoder
		encPinB: Pin number of RPI which connect to B phase at encoder
		'''
		self._enc_pin_A = encPinA
		self._enc_pin_B = encPinB
		self._encoder_pulses = 0 # Dimension: Pulses
		IO.setup(self._enc_pin_A, IO.IN, pull_up_down=IO.PUD_UP)
		IO.setup(self._enc_pin_B, IO.IN, pull_up_down=IO.PUD_UP)
		IO.add_event_detect(self._enc_pin_A, IO.BOTH, callback=self.encoderA)
		IO.add_event_detect(self._enc_pin_B, IO.BOTH, callback=self.encoderB)
	
	def encoderA(self, channel):
		if IO.input(self._enc_pin_A) == IO.input(self._enc_pin_B):
			self._encoder_pulses += 1
		else:
			self._encoder_pulses -= 1
    #print('PinA : %d, encoder : %d' %(channel, encoderPos))

	def encoderB(self, channel):
		if IO.input(self._enc_pin_A) == IO.input(self._enc_pin_B):
			self._encoder_pulses -= 1
		else:
			self._encoder_pulses += 1
    #print('PinB : %d, encoder : %d' %(channel, encoderPos))