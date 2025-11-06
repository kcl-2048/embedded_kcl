import threading
import serial
import time
import RPi.GPIO as GPIO

L_PWM = 18
R_PWM = 23

L_IN1 = 22
L_IN2 = 27

R_IN1 = 24
R_IN2 = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L_PWM, GPIO.OUT)
GPIO.setup(R_PWM, GPIO.OUT)
GPIO.setup(L_IN1, GPIO.OUT)
GPIO.setup(L_IN2, GPIO.OUT)
GPIO.setup(R_IN1, GPIO.OUT)
GPIO.setup(R_IN2, GPIO.OUT)

L_Motor = GPIO.PWM(L_PWM, 100)
R_Motor = GPIO.PWM(R_PWM, 100)
L_Motor.start(0)
R_Motor.start(0)

bt_serial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
bt_cmd = ""

def set_L_motor(speed):
    if speed > 0:
        GPIO.output(L_IN1, GPIO.LOW)
        GPIO.output(L_IN2, GPIO.HIGH)
        L_Motor.ChangeDutyCycle(speed)
    elif speed < 0:
        GPIO.output(L_IN1, GPIO.HIGH)
        GPIO.output(L_IN2, GPIO.LOW)
        L_Motor.ChangeDutyCycle(abs(speed))
    else:
        GPIO.output(L_IN1, GPIO.LOW)
        GPIO.output(L_IN2, GPIO.LOW)
        L_Motor.ChangeDutyCycle(0)

def set_R_motor(speed):
    if speed > 0:
        GPIO.output(R_IN1, GPIO.LOW)
        GPIO.output(R_IN2, GPIO.HIGH)
        R_Motor.ChangeDutyCycle(speed)
    elif speed < 0:
        GPIO.output(R_IN1, GPIO.HIGH)
        GPIO.output(R_IN2, GPIO.LOW)
        R_Motor.ChangeDutyCycle(abs(speed))
    else:
        GPIO.output(R_IN1, GPIO.LOW)
        GPIO.output(R_IN2, GPIO.LOW)
        R_Motor.ChangeDutyCycle(0)

def go(speed=100):
    set_L_motor(speed)
    set_R_motor(-speed)
    print("Go")

def back(speed=100):
    set_L_motor(-speed)
    set_R_motor(speed)
    print("Back")

def left(speed=50):
    set_L_motor(-speed)
    set_R_motor(-speed)
    print("Left")

def right(speed=50):
    set_L_motor(speed)
    set_R_motor(speed)
    print("Right")

def stop():
    set_L_motor(0)
    set_R_motor(0)
    print("Stop")

def serial_thread():
    global bt_cmd
    while True:
        data = bt_serial.readline()
        data = data.decode()
        bt_cmd = data

def main():
    global bt_cmd
    try:
        while True:
            if bt_cmd.find("B1") >= 0:
                bt_cmd = ""
                go()
            elif bt_cmd.find("B2") >= 0:
                bt_cmd = ""
                back()
            elif bt_cmd.find("B0") >= 0:
                bt_cmd = ""
                left()
            elif bt_cmd.find("B4") >= 0:
                bt_cmd = ""
                right()
            elif bt_cmd.find("B3") >= 0:
                bt_cmd = ""
                stop()
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    thread = threading.Thread(target=serial_thread)
    thread.start()
    main()
    bt_serial.close()
    GPIO.cleanup()