import time
from djitellopy import Tello
import serial

from keyboard_control import KeyboardController2

# Tello custom command constants
C_DEFAULT = 'NONE'
C_CALIB = 'CALIB'
C_FRONTFLIP = 'FRONTFLIP'
C_BACKFLIP = 'BACKFLIP'
C_RIGHTFLIP = 'RIGHTFLIP'
C_LEFTFLIP = 'LEFTFLIP'

# This class reads data from USART and sends commands to Tello
class USART_Reader:
    def __init__(self, tello: Tello, port='COM1'):
        self.tello = tello
        self.port = port    # USART port

        self.doing_flip = False

        # Tello control variables
        self.command_val = ''
        self.vel_roll = 0
        self.vel_pitch = 0
        self.vel_yaw = 0
        self.vel_throttle = 0

        # USART communication setup
        self.usart = serial.Serial(
            port=self.port,
            baudrate=115200,
            timeout=1,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        
        print("Using COM port:", self.usart.name)


    def process_and_send_command(self):
        if self.command_val == C_DEFAULT:    # default state, send commands from sensor
            self.tello.send_rc_control(self.vel_roll, self.vel_pitch, self.vel_throttle, self.vel_yaw)

        # if self.command_val == C_FRONTFLIP or self.command_val == C_BACKFLIP or self.command_val == C_RIGHTFLIP or self.command_val == C_LEFTFLIP:
        #     if self.command_val == C_FRONTFLIP and not self.doing_flip == True:
        #         self.doing_flip = True
        #         response = self.tello.send_command_with_return("flip f", int(self.tello.RESPONSE_TIMEOUT))
        #         if 'ok' in response.lower():
        #             self.doing_flip = False     
        #         self.tello.flip_forward()
        #     elif self.command_val == C_BACKFLIP and not self.doing_flip == True:
        #         self.doing_flip = True
        #         response = self.tello.send_command_with_return("flip b", int(self.tello.RESPONSE_TIMEOUT))
        #         if 'ok' in response.lower():
        #             self.doing_flip = False
        #     elif self.command_val == C_RIGHTFLIP and not self.doing_flip == True:
        #         self.doing_flip = True
        #         response = self.tello.send_command_with_return("flip r", int(self.tello.RESPONSE_TIMEOUT))
        #         if 'ok' in response.lower():
        #             self.doing_flip = False
        #     elif self.command_val == C_LEFTFLIP and not self.doing_flip == True:
        #         self.doing_flip = True
        #         response = self.tello.send_command_with_return("flip l", int(self.tello.RESPONSE_TIMEOUT))
        #         if 'ok' in response.lower():
        #             self.doing_flip = False
        #     else:
        #         pass
        else:
            pass


    def read_data(self):
        if self.usart.in_waiting > 0 :
            csv_data = self.usart.readline().decode('utf-8').strip()

            split_data = csv_data.split(',')
            # print(split_data[0], split_data[1], split_data[2], split_data[3], split_data[4])

            if len(split_data) >= 5:
                self.command_val = split_data[0]
                self.vel_roll = int(split_data[1])
                self.vel_pitch = int(split_data[2])
                self.vel_yaw = int(split_data[3])
                self.vel_throttle = int(split_data[4])
                # self.vel_yaw = 0
                # self.vel_throttle = int(self.vel_throttle*0.75)
                # self.vel_yaw = -self.vel_yaw


def main(args=None):

    tello = Tello()
    controller = KeyboardController2(tello)
    reader = USART_Reader(tello, port='COM5')

    print("Press 'c' to connect")

    while 1:
        reader.read_data()
        if controller.in_sensor_control:
            reader.process_and_send_command()

        time.sleep(1/50)
        pass


if __name__ == '__main__':
    main()