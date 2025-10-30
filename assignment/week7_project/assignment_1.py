import RPi.GPIO as GPIO
import time

switches = [5, 6, 13, 19]
sw_names = ['SW1', 'SW2', 'SW3', 'SW4']

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prev_states = [0] * 4
click_counts = [0] * 4

try:
    while True:
        for i in range(4):
            current_state = GPIO.input(switches[i])
            
            if current_state == 1 and prev_states[i] == 0:
                click_counts[i] += 1
                output_tuple = (f'{sw_names[i]} click', click_counts[i])
                print(output_tuple)
            
            prev_states[i] = current_state
        
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

GPIO.cleanup()