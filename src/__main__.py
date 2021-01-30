
from time import sleep
import sys
import csv
import raspydj
import RPi.GPIO as GPIO
from configparser import ConfigParser


def main():

    '''GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO21
    GPIO.setup(21, GPIO.OUT)  #LED to GPIO20'''

    config = ConfigParser()
    config.read("config/settings.ini")

    playlists = {}
    with open('config/playlists.csv') as csvfile:
        mapping = csv.reader(csvfile)
        for row in mapping:
            playlists[row[0]]=row[1]
    
    rfid_reader = raspydj.RFID().reader
    jukebox = raspydj.jukebox.JukeBox(config=config,controller=raspydj.Controller(config))

    try:
        while True:
            print("Hold a tag near the reader")
            id, text = rfid_reader.read()
            print("ID: %s\nText: %s" % (id,text))
            if str(id) in playlists:
                jukebox.set_playlist(playlists[str(id)])
            sleep(5)
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()

if __name__ == "__main__":
    # execute only if run as a script
    main()