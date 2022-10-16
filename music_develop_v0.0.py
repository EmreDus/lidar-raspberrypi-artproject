'''
from playsound import playsound

playsound('/home/lidar/project/Platform1.wav', block=False)
'''
'''
import pygame
file = '/home/lidar/project/Platform1.wav'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
'''


#sudo apt install python3-gst-1.0
#sudo apt-get install libsdl-ttf2.0-0

from audioplayer import AudioPlayer
AudioPlayer("/home/lidar/project/Platform1.wav").play(loop=True)
while True:
    print("merhaban")