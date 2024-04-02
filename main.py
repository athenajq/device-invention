from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import time

# set up servos
kit = ServoKit(channels=16)
stop_values = [-0.05, -0.02, 0.06, 0.01, 0,0]
motor_values = ["123", "456", "789", "987", "654", "321"]
str_input = ""
global turn_motor
turn_motor = False

C1 = 25
C2 = 23
C3 = 16

R1 = 24
R2 = 21 
R3 = 20
R4 = 12


# Initialize the GPIO pins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# The readLine function implements the procedure discussed in the article
# It sends out a single pulse to one of the rows of the keypad
# and then checks each column for changes
# If it detects a change, the user pressed the button that connects the given line
# to the detected column

def readLine(line, characters):
    val = ""
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        val = characters[0]
    if(GPIO.input(C2) == 1):
        val =  characters[1]
    if(GPIO.input(C3) == 1):
        val =  characters[2]
    GPIO.output(line, GPIO.LOW)
    return val

try:
    while True:
        # call the readLine function for each row of the keypad
        new_val = ''
        new_val += readLine(R1, ["1","2","3"])
        new_val += readLine(R2, ["4","5","6"])
        new_val += readLine(R3, ["7","8","9"])
        new_val += readLine(R4, ["*","0","#"])
        
        # prevents spamming that happens but also prevents a repeated number to be valid
        if len(str_input) < 1 or new_val != str_input[-1]:
            str_input += new_val
        time.sleep(0.1)
        
        if len(str_input) > 0 and str_input[-1] == "#":
            str_input= str_input[:-1]
            turn_motor = True
        if turn_motor:
            found_string = False
            print(str_input)
            for i in range(len(motor_values)):
                if str_input == motor_values[i]:
                    fount_string = True
                    print(i)
                    kit.continuous_servo[i].throttle = 1
                    time.sleep(1)
                    kit.continuous_servo[i].throttle = stop_values[i]
                    time.sleep(0.5)
                    kit.continuous_servo[i].throttle = -1
                    time.sleep(1)
                    turn_motor = False
                    str_input = ""
                    break
            if found_string == False:
                str_input = ""
                turn_motor = False
        # stop servos
        for i in range(6):
            if not turn_motor:
                kit.continuous_servo[i].throttle = stop_values[i]
except KeyboardInterrupt:
    print("\nApplication stopped!")
    

