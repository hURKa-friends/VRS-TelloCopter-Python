from djitellopy import Tello
# from pynput import keyboard
# from pynput.keyboard import Key
import keyboard

import os

gain = 100

class KeyboardController2:
    def __init__(self, tello: Tello):
        self.tello = tello

        # flags
        self.c_pressed = False
        self.t_pressed = False
        self.l_pressed = False
        self.p_pressed = False

        # velocity command values for roll, pitch, yaw
        # value interval <-100, 100>
        self.vel_roll = 0
        self.vel_pitch = 0
        self.vel_yaw = 0
        self.vel_throttle = 0

        self.bat = -1

        # Tello roll/pitch/yaw flying control
        keyboard.on_press_key('w', lambda e: self.set_pitch(gain))
        keyboard.on_press_key('s', lambda e: self.set_pitch(-gain))
        keyboard.on_press_key('d', lambda e: self.set_roll(gain))
        keyboard.on_press_key('a', lambda e: self.set_roll(-gain))
        keyboard.on_press_key('e', lambda e: self.set_yaw(gain))
        keyboard.on_press_key('q', lambda e: self.set_yaw(-gain))
        keyboard.on_press_key('space', lambda e: self.set_throttle(gain))
        keyboard.on_press_key('ctrl', lambda e: self.set_throttle(-gain))

        keyboard.on_release_key('w', lambda e: self.set_pitch(0))
        keyboard.on_release_key('s', lambda e: self.set_pitch(0))
        keyboard.on_release_key('d', lambda e: self.set_roll(0))
        keyboard.on_release_key('a', lambda e: self.set_roll(0))
        keyboard.on_release_key('e', lambda e: self.set_yaw(0))
        keyboard.on_release_key('q', lambda e: self.set_yaw(0))
        keyboard.on_release_key('space', lambda e: self.set_throttle(0))
        keyboard.on_release_key('ctrl', lambda e: self.set_throttle(0))

        # Tello other control
        keyboard.on_press_key('c', lambda e: self.tello_connect())
        keyboard.on_press_key('t', lambda e: self.tello_takeoff())
        keyboard.on_press_key('l', lambda e: self.tello_land())
        keyboard.on_press_key('p', lambda e: self.tello_emergency())


        keyboard.on_release_key('c', lambda e: self.tello_connect_release())
        keyboard.on_release_key('t', lambda e: self.tello_takeoff_release())
        keyboard.on_release_key('l', lambda e: self.tello_land_release())
        keyboard.on_release_key('p', lambda e: self.tello_emergency_release())



    def set_roll(self, value):
        self.vel_roll = value
        self.tello.send_rc_control(self.vel_roll, self.vel_pitch, self.vel_throttle, self.vel_yaw)

    def set_pitch(self, value):
        self.vel_pitch = value
        self.tello.send_rc_control(self.vel_roll, self.vel_pitch, self.vel_throttle, self.vel_yaw)

    def set_yaw(self, value):
        self.vel_yaw = value
        self.tello.send_rc_control(self.vel_roll, self.vel_pitch, self.vel_throttle, self.vel_yaw)

    def set_throttle(self, value):
        self.vel_throttle = value
        self.tello.send_rc_control(self.vel_roll, self.vel_pitch, self.vel_throttle, self.vel_yaw)

    def tello_connect(self):
        if not self.c_pressed:
            self.c_pressed = True
            self.tello.connect()
            
    def tello_connect_release(self):
        self.c_pressed = False

    def tello_takeoff(self):
        if not self.t_pressed:
            self.t_pressed = True
            self.tello.takeoff()

    def tello_takeoff_release(self):
        self.t_pressed = False

    def tello_land(self):
        if not self.l_pressed:
            self.l_pressed = True
            self.tello.land()

    def tello_land_release(self):
        self.l_pressed = False

    def tello_emergency(self):
        if not self.p_pressed:
            self.p_pressed = True
            self.tello.emergency()

    def tello_emergency_release(self):
        self.p_pressed = False

