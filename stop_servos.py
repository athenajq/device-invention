import time
from adafruit_servokit import ServoKit
 
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
stop_values = [-0.05, -0.02, 0.06, 0.01, 0,0]
while True: 
    kit.continuous_servo[6].throttle = 1