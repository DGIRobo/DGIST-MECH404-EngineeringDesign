import RPi.GPIO as IO
import encoder
import datetime
import time
import os

IO.setmode(IO.BCM)
IO.setwarnings(False)

PI = 3.141592
BR_encoder = encoder.Encoder(10, 24)

previous_time = datetime.datetime.now().timestamp()
current_time = datetime.datetime.now().timestamp()
incremental_pos = 0
incremental_pos_old = 0
vel = 0
absolute_pos = 0

while True:
		current_time = datetime.datetime.now().timestamp()
		time_interval = current_time - previous_time
		incremental_pos_old = incremental_pos
		incremental_pos = BR_encoder._encoder_pulses * (2 * PI) / (44 * 29)
		vel = (incremental_pos - incremental_pos_old) / time_interval
		absolute_pos = (BR_encoder._encoder_pulses % (44 * 29)) * (2 * PI) / (44 * 29)
		print(f'Incremental position of BR wheel: {incremental_pos}')
		print(f'Absolute position of BR wheel: {absolute_pos}')
		previous_time = datetime.datetime.now().timestamp()
		os.system('clear')