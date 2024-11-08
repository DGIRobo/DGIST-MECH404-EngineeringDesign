import RPi.GPIO as IO
import encoder
import time

IO.setmode(IO.BCM)
IO.setwarnings(False)

BR_encoder = encoder.Encoder(10, 24)

while True:
		print(f'position of BR wheel: {BR_encoder._encoder_pos}')
		time.sleep(0.5)