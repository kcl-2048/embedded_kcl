import RPi.GPIO as GPIO
import time

switches = [5, 6, 19, 13] 
buzzer_pin = 12          

notes = {
    5: 262, 
    6: 294,  
    19: 330, 
    13: 392  
}

note_duration = 0.3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzer_pin, GPIO.OUT)

p = GPIO.PWM(buzzer_pin, 100) 
prev_states = [0] * 4         

try:
    while True:
        for i in range(4): 
            pin = switches[i]
            current_state = GPIO.input(pin) 
            
            if current_state == 1 and prev_states[i] == 0:
                freq = notes.get(pin) 
                if freq:
                    p.ChangeFrequency(freq)
                    p.start(50)       
                    time.sleep(note_duration)    
                    p.stop()          
            
            prev_states[i] = current_state 
            
        time.sleep(0.05) 

except KeyboardInterrupt: 
    pass

finally: 
    p.stop() 
    GPIO.cleanup()