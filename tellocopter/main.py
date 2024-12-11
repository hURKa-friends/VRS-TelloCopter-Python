import time
from djitellopy import Tello
import serial

from keyboard_control import KeyboardController2

# constants defines
C_OFF = ''
C_SENSOR = 'control'


class USART_Reader:
    def __init__(self, tello: Tello, port='COM1'):
        self.tello = tello
        
        self.port = port

        self.command = 0
        self.command_val = ''
        self.vel_roll = 0
        self.vel_pitch = 0
        self.vel_yaw = 0

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
        if self.usart.in_waiting > 0:

            if self.command == C_OFF:
                pass
            elif self.command == C_SENSOR:    # default state, send commands from sensor
                self.tello.send_rc_control(self.vel_roll, self.vel_pitch, self.vel_throttle, self.vel_yaw)
            else:
                pass
        else:
            print("No data from USART to process")
        

    def read_data(self):
        if self.usart.in_waiting > 0 :
            csv_data = self.usart.readline().decode('utf-8').strip()

            split_data = csv_data.split(',')
            print(split_data[0], split_data[1], split_data[2], split_data[3])

            self.command_val = csv_data[0]
            self.vel_roll = csv_data[1]
            self.vel_pitch = csv_data[2]
            self.vel_yaw = csv_data[3]


def main(args=None):

    tello = Tello()
    controller = KeyboardController2(tello)
    reader = USART_Reader(tello, port='COM6')

    print("Press 'c' to connect")

    while 1:
        reader.read_data()
        if controller.in_sensor_control:
            reader.process_and_send_command()

        time.sleep(1/50)
        pass


if __name__ == '__main__':
    main()