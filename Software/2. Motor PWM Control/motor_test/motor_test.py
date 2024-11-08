import time
import busio

from board import SCL, SDA
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c, address=0x40)
pca.frequency = 100

# Front Left Wheel(0th Motor) Test Start
print("Motor0 Test Start")
# Front Left Wheel Rotation Direction Setting
print("Motor0 Enable to Front")
pca.channels[0].duty_cycle = 0xFFFF
pca.channels[1].duty_cycle = 0x0000
# Front Left Wheel PWM Control
pca.channels[4].duty_cycle = 0xFFFF #assign 12V to Motor0
time.sleep(5)
pca.channels[4].duty_cycle = 0x0000 #assign 0V to Motor0
time.sleep(5)

# Front Right Wheel(1st Motor) Test Start
print("Motor1 Test Start")
# Front Right Wheel Rotation Direction Setting
print("Motor1 Enable to Front")
pca.channels[2].duty_cycle = 0x0000
pca.channels[3].duty_cycle = 0xFFFF
# Front Right Wheel PWM Control
pca.channels[5].duty_cycle = 0xFFFF #assign 12V to Motor1
time.sleep(5)
pca.channels[5].duty_cycle = 0x0000 #assign 0V to Motor1
time.sleep(5)

# Back Left Wheel(2nd Motor) Test Start
print("Motor2 Test Start")
# Back Left Wheel Rotation Direction Setting
print("Motor2 Enable to Front")
pca.channels[8].duty_cycle = 0xFFFF
pca.channels[9].duty_cycle = 0x0000
# Back Left Wheel PWM Control
pca.channels[6].duty_cycle = 0xFFFF #assign 12V to Motor2
time.sleep(5)
pca.channels[6].duty_cycle = 0x0000 #assign 0V to Motor2
time.sleep(5)

# Back Right Wheel(3rd Motor) Test Start
print("Motor3 Test Start")
# Back Right Wheel Rotation Direction Setting
print("Motor3 Enable to Front")
pca.channels[10].duty_cycle = 0x0000
pca.channels[11].duty_cycle = 0xFFFF
# Back Left Wheel PWM Control
pca.channels[7].duty_cycle = 0xFFFF #assign 12V to Motor3
time.sleep(5)
pca.channels[7].duty_cycle = 0x0000 #assign 0V to Motor3
time.sleep(5)

pca.deinit()