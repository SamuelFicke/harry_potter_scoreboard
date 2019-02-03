import os
import random
import wave
import time
#import pyaudio
import serial
import sys
import collections


house_files = ["gryffindor.wav", "slytherin.wav", "hufflepuff.wav", "ravenclaw.wav"]

BASE_AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")

WAIT_TIME = .25


def list_all_sound_files(subdir):
    """
    Get all the sound files from a subdir in the audio
    folder
    :param subdir:
        Subdir to list
    :return:
        all sound files in subdir
    """
    return [f for f in os.listdir(
        os.path.join(BASE_AUDIO_DIR, subdir)
    ) if f[-4:] == '.wav']


def get_full_path(subdir, audio_filename):
    """
    given an audio file and the subdir give a full path
    from the base sound dir
    :param audio_filename:
        string, filename
    :return:
        full path from audio dir
    """
    return os.path.join(
        BASE_AUDIO_DIR,
        subdir,
        audio_filename
    )


def get_random_wav_file(subdir):
    """
    Used to play a sound matching a category
    :param subdir:
        Which subdir to pull the file out of. Base dir is audio
    :return:
        A full path to the sound file chosen.
    """
    return get_full_path(
        subdir,
        random.choice(
            list_all_sound_files(subdir)
        )
    )


def play_sound(sound_file_path):
    """
    Play the sound at a given path
    :param sound_file_path:
        string path
    """
    system_str = "aplay " + sound_file_path
    os.system(system_str)

def generate_script(house):
    # Consider some stalling lines
    script = list_all_sound_files('stalling')
    random.shuffle(script)
    script = [get_full_path('stalling', f)
              for f in script
              if random.random() < .3]

    # Shout I know!
    script.append(get_random_wav_file('know'))

    # Pick a house
    script.append(BASE_AUDIO_DIR + '/houses/' + house_files[house])
    return script    


def play_script(script):
    for sound in script:
        play_sound(sound)
        time.sleep(WAIT_TIME)    


def monitor_serial():
    running = False
    ser = serial.Serial(sys.argv[1], 115200)
    readings = collections.deque(maxlen=3)
    while True:
        reading = ser.readline().strip()
        if reading:
            readings.appendleft(int(reading))
            if any(readings):
                print(readings)
            else:
                running = False
            trigger = all(readings)
            if(all(readings)) and not running:
                running = True
                play_script(generate_script())

def sort(house_num):
   play_script(generate_script(house_num))

if __name__ == '__main__':
    # If a port was passed in we must be using a external device to trigger the
    # script. Read from the device serial port
    if len(sys.argv) > 1:
        monitor_serial()
    else:
        sort(0)
