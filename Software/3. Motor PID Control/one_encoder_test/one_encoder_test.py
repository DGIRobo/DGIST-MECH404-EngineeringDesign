'''
Motor Parameters

No load current: 120mA
Rated torque: 3.5KG.CM
No load speed: 330rpm
Rated speed: 250rpm
Rated Current: 1A
Maximum torque: 5KG.CM
Stop current: 2.3A
Reduction Ratio: 29
'''

'''
Encoder Parameters

Type: AB phase incremental
Wire speed: 360
Supply power: 5V
Interface type: PH2.0
Function: control speed
Encoder pulses: 11 pulses for one rotation
'''

# 4체배 카운트
# 11 pulses * 4 folds = 44 pulses on one motor rotation
# 29 gear ratio * 44 pulses = 1276 pulses on one load rotation
import RPi.GPIO as IO
import time

encPinA = 10
encPinB = 24

IO.setmode(IO.BCM)
IO.setwarnings(False)
IO.setup(encPinA, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(encPinB, IO.IN, pull_up_down=IO.PUD_UP)

encoderPos = 0

def encoderA(channel):
    global encoderPos
    if IO.input(encPinA) == IO.input(encPinB):
        encoderPos += 1
    else:
        encoderPos -= 1
    print('PinA : %d, encoder : %d' %(channel, encoderPos))

def encoderB(channel):
    global encoderPos
    if IO.input(encPinA) == IO.input(encPinB):
        encoderPos -= 1
    else:
        encoderPos += 1
    print('PinB : %d, encoder : %d' %(channel, encoderPos))

IO.add_event_detect(encPinA, IO.BOTH, callback=encoderA)
IO.add_event_detect(encPinB, IO.BOTH, callback=encoderB)

while True:
    time.sleep(0.5)