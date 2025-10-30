import RPi.GPIO as GPIO
import time

switches = {
    'SW1': 5,  
    'SW2': 6,  
    'SW3': 13, 
    'SW4': 19  
}

PWMA = 18 
AIN1 = 22 
AIN2 = 27 

PWMB = 23 
BIN1 = 25 
BIN2 = 24 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(list(switches.values()), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup([PWMA, AIN1, AIN2, PWMB, BIN1, BIN2], GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)
L_Motor.start(0)
R_Motor.start(0)

def motor_control(left_speed, left_dir, right_speed, right_dir):
    L_Motor.ChangeDutyCycle(left_speed)
    GPIO.output(AIN1, left_dir[0])
    GPIO.output(AIN2, left_dir[1])
    
    R_Motor.ChangeDutyCycle(right_speed)
    GPIO.output(BIN1, right_dir[0])
    GPIO.output(BIN2, right_dir[1])

FORWARD = (0, 1)
BACKWARD = (1, 0)
STOP = (0, 0) 

try:
    last_pressed = None 
    while True:
        pressed = None
        
        if GPIO.input(switches['SW1']) == GPIO.HIGH:
            pressed = 'SW1'
        elif GPIO.input(switches['SW2']) == GPIO.HIGH:
            pressed = 'SW2'
        elif GPIO.input(switches['SW3']) == GPIO.HIGH:
            pressed = 'SW3'
        elif GPIO.input(switches['SW4']) == GPIO.HIGH:
            pressed = 'SW4'

        if pressed != last_pressed:
            if pressed == 'SW1':
                print("SW1 pressed - Forward")
                motor_control(50, FORWARD, 50, FORWARD) 
            elif pressed == 'SW2':
                print("SW2 pressed - Right")
                motor_control(50, FORWARD, 0, STOP)      
            elif pressed == 'SW3':
                print("SW3 pressed - Left")
                motor_control(0, STOP, 50, FORWARD)      
            elif pressed == 'SW4':
                print("SW4 pressed - Backward")
                motor_control(50, BACKWARD, 50, BACKWARD) 
            else: 
                print("Stopped")
                motor_control(0, STOP, 0, STOP)          

            last_pressed = pressed 

        time.sleep(0.1) 

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()