from djitellopy import Tello
from pynput import keyboard
from pynput.keyboard import Key

import os



class KeyboardController:
    """Class used to control Tello drone using keyboard input.
    Multiple keys pressed simultaneously is supported.
    """

    def __init__(self, tello: Tello):
        self.tello = tello

        self.val = 100

        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.current_pressed = set()

        self.fly_keys = [
            'w',
            'a',
            's',
            'd',
            'q',
            'e',
            Key.space,
            Key.ctrl
        ]

        # velocity command values for roll, pitch, yaw
        # value interval <-100, 100>
        self.vel_roll = 0
        self.vel_pitch = 0
        self.vel_yaw = 0
        self.vel_throttle = 0

        self.bat = -1


    def on_press(self, key):
        """Function handling pressing keys.
        When mapped key is pressed, defined command is executed.
        """

        if key not in self.current_pressed:
            self.current_pressed.add(key)

        for k in self.current_pressed:
            try:
                # connect
                if k.char == 'c':
                    self.tello.connect()

                if k.char == 'p':
                    os.system('cls')

                # # takeoff/land
                # if k.char == 't':
                #     self.tello.takeoff()
                # if k.char == 'l':
                #     self.tello.land()
                #     self.vel_roll = 0
                #     self.vel_pitch = 0
                #     self.vel_yaw = 0
                #     self.vel_throttle = 0

                #     self.tello.send_rc_control(self.vel_roll, self.vel_pitch, self.vel_throttle, self.vel_yaw)
                    

                # roll/pitch/yaw/up/down
                if k.char in self.fly_keys:
                    if k.char == 'w':
                        self.vel_pitch = self.val
                    if k.char == 's':
                        self.vel_pitch = -self.val
                    if k.char == 'a':
                        self.vel_roll = -self.val
                    if k.char == 'd':
                        self.vel_roll = self.val
                    if k.char == 'e':
                        self.vel_yaw = self.val
                    if k.char == 'q':
                        self.vel_yaw = -self.val
                    if k.char == Key.space:
                        self.vel_throttle = self.val
                    if k.char == Key.ctrl:
                        self.vel_throttle = -self.val
                    self.tello.send_rc_control(self.vel_roll, self.vel_pitch, self.vel_throttle, self.vel_yaw)
                    
            except AttributeError:
                pass
                

        


    def on_release(self, key):
        """Function handling releasing keys.
        When mapped key is released, defined command is executed.
        Mainly functions as setting values to their default value, when key is released.
        """

        if key in self.current_pressed:
            self.current_pressed.remove(key)

        
        try:
            # takeoff/land
            if key.char == 'o':
                self.tello.emergency()
            if key.char == 'b':
                self.bat = self.tello.get_battery()
                print(self.bat)
            if key.char == 't':
                self.tello.takeoff()
            if key.char == 'l':
                try:
                    self.tello.land()
                except Exception as e:
                    print(f"Failed to send land command: {e}")

                self.vel_roll = 0
                self.vel_pitch = 0
                self.vel_yaw = 0
                self.vel_throttle = 0

            # roll/pitch/yaw/up/down
            if key.char in self.fly_keys:
                if key.char == 'w':
                    self.vel_pitch = 0
                if key.char == 's':
                    self.vel_pitch = 0
                if key.char == 'a':
                    self.vel_roll = 0
                if key.char == 'd':
                    self.vel_roll = 0
                if key.char == 'e':
                    self.vel_yaw = 0
                if key.char == 'q':
                    self.vel_yaw = 0
                if key.char == Key.space:
                    self.vel_throttle = 0
                if key.char == Key.ctrl:
                    self.vel_throttle = 0
                self.tello.send_rc_control(self.vel_roll, self.vel_pitch, self.vel_throttle, self.vel_yaw)
        except AttributeError:
            pass