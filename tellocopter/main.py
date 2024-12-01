import time

from djitellopy import Tello
from keyboard_control import KeyboardController2

def main(args=None):
    tello = Tello()
    controller = KeyboardController2(tello)

    print("Press 'c' to connect")

    while 1:
        time.sleep(0.5)
        pass

if __name__ == '__main__':
    main()