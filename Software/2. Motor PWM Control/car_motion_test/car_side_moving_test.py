import time
import busio

from board import SCL, SDA
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c, address=0x40)
pca.frequency = 100

# Car's Left Wheel Moving Direction Setting
# Front Left Wheel Rotation Direction Setting
pca.channels[0].duty_cycle = 0xFFFF # Front Dirction
pca.channels[1].duty_cycle = 0x0000
# Front Right Wheel Rotation Direction Setting
pca.channels[2].duty_cycle = 0x0000 # Front Dirction
pca.channels[3].duty_cycle = 0xFFFF
# Back Left Wheel Rotation Direction Setting
pca.channels[8].duty_cycle = 0xFFFF # Front Dirction
pca.channels[9].duty_cycle = 0x0000
# Back Right Wheel Rotation Direction Setting
pca.channels[10].duty_cycle = 0x0000 # Front Dirction
pca.channels[11].duty_cycle = 0xFFFF

# Start Left Moving
pca.channels[4].duty_cycle = 0xFFFF #assign 12V to Motor0 (FL)
pca.channels[5].duty_cycle = 0xFFFF #assign 12V to Motor1 (FR)
pca.channels[6].duty_cycle = 0xFFFF #assign 12V to Motor2 (BL)
pca.channels[7].duty_cycle = 0xFFFF #assign 12V to Motor3 (BR)
time.sleep(5)

# Stop Moving
pca.channels[4].duty_cycle = 0x0000 #assign 0V to Motor0 (FL)
pca.channels[5].duty_cycle = 0x0000 #assign 0V to Motor1 (FR)
pca.channels[6].duty_cycle = 0x0000 #assign 0V to Motor2 (BL)
pca.channels[7].duty_cycle = 0x0000 #assign 0V to Motor3 (BR)
time.sleep(5)

# Car's Right Wheel Moving Direction Setting
# Front Left Wheel Rotation Direction Setting
pca.channels[0].duty_cycle = 0x0000 # Back Dirction
pca.channels[1].duty_cycle = 0xFFFF
# Front Right Wheel Rotation Direction Setting
pca.channels[2].duty_cycle = 0xFFFF # Back Dirction
pca.channels[3].duty_cycle = 0x0000
# Back Left Wheel Rotation Direction Setting
pca.channels[8].duty_cycle = 0x0000 # Back Dirction
pca.channels[9].duty_cycle = 0xFFFF
# Back Right Wheel Rotation Direction Setting
pca.channels[10].duty_cycle = 0xFFFF # Back Dirction
pca.channels[11].duty_cycle = 0x0000

# Start Right Moving
pca.channels[4].duty_cycle = 0xFFFF #assign 12V to Motor0 (FL)
pca.channels[5].duty_cycle = 0xFFFF #assign 12V to Motor1 (FR)
pca.channels[6].duty_cycle = 0xFFFF #assign 12V to Motor2 (BL)
pca.channels[7].duty_cycle = 0xFFFF #assign 12V to Motor3 (BR)
time.sleep(5)

# Stop Moving
pca.channels[4].duty_cycle = 0x0000 #assign 0V to Motor0 (FL)
pca.channels[5].duty_cycle = 0x0000 #assign 0V to Motor1 (FR)
pca.channels[6].duty_cycle = 0x0000 #assign 0V to Motor2 (BL)
pca.channels[7].duty_cycle = 0x0000 #assign 0V to Motor3 (BR)
time.sleep(5)

pca.deinit()