import pygame
import time
import platform
import os


def play_sound(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(2)


def main():
    os_name = platform.system()
    path = "audio.mp3"
    if os_name == "Linux":
        print("your system is going to poweroff in 10s")
        time.sleep(10)
        play_sound(path)
        os.system("systemctl poweroff")
    elif os_name != "Windows":
        print("your system is going to shutdown in 10s")
        time.sleep(10)
        play_sound(path)
        os.system("shutdown -s")
    else:
        print("your system is going to shutdown in 10s")
        time.sleep(10)
        play_sound(path)
        os.system("shutdown -s")

if __name__ == "__main__":
    main()
