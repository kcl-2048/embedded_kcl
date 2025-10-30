import RPi.GPIO as GPIO
import time

switches = [5, 6, 13, 19] 
buzzer_pin = 12          

melody_1 = [262, 294, 330, 349, 392, 440, 494, 523] 
melody_2 = [392, 392, 440, 440, 392, 392, 330]       
melody_3 = [523, 523, 587, 587, 523, 523, 440]       
melody_4 = [262, 330, 392, 523, 392, 330, 262]       

duration_1 = [0.4] * 8                              
duration_2 = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.8]    
duration_3 = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.8]
duration_4 = [0.3] * 7                              

melodies = [melody_1, melody_2, melody_3, melody_4]
durations = [duration_1, duration_2, duration_3, duration_4]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzer_pin, GPIO.OUT)

p = GPIO.PWM(buzzer_pin, 100) 
prev_states = [0] * 4         
is_playing = False            

def play_melody(melody_notes, melody_durations):
    global is_playing
    if is_playing: 
        return
    is_playing = True 
    p.start(50)       
    for i in range(len(melody_notes)):
        p.ChangeFrequency(melody_notes[i]) 
        time.sleep(melody_durations[i])    
    p.stop()          
    is_playing = False 

try:
    while True:
        for i in range(4): 
            current_state = GPIO.input(switches[i]) 
            if current_state == 1 and prev_states[i] == 0 and not is_playing:
                play_melody(melodies[i], durations[i]) 
            prev_states[i] = current_state 
        time.sleep(0.05) 

except KeyboardInterrupt: 
    pass

finally: 
    p.stop() 
    GPIO.cleanup()