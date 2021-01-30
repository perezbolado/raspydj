import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO21
GPIO.setup(21, GPIO.OUT)  #LED to GPIO20

try:
    while True:
         button_state = GPIO.input(23)
         if button_state == False:
             GPIO.output(21, True)
             print('Button Pressed...')
             time.sleep(0.2)
         else:
             GPIO.output(21, False)
except:
    GPIO.cleanup()