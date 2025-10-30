import RPi.GPIO as GPIO
import time

buzzer = 12
scale = [262, 294, 330, 349, 392, 440, 494, 523]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)

p = GPIO.PWM(buzzer, 100)

try:
    p.start(50)
    for freq in scale:
        p.ChangeFrequency(freq)
        time.sleep(0.5)
    p.stop()

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()