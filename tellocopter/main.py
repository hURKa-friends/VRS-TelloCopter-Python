import time

from djitellopy import Tello
from keyboard_control import KeyboardController

def main(args=None):
    tello = Tello()
    controller = KeyboardController(tello)

    print("Press 'c' to connect")

    while 1:
        # tello.send_rc_control(controller.vel_roll, controller.vel_pitch, controller.vel_throttle, controller.vel_yaw)
        # print(controller.bat)
        # time.sleep(0.5)
        # print(f"throttle: {controller.vel_throttle}\n"
        #     f"roll:     {controller.vel_throttle}\n"
        #     f"pitch:    {controller.vel_throttle}\n"
        #     f"yaw:      {controller.vel_throttle}")
        pass

if __name__ == '__main__':
    main()