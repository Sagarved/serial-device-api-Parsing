"""
This code will accept com port and connect with panic button serially.
It will trigger scan report every 60 seconds
"""

import serial



def open_com(port):
    global ser
    ser = serial.Serial(port,115200, timeout=20)

def close_com():
    ser.close()

def ser_read():
    #with serial.Serial(port, 115200, timeout=20) as ser:
    for _ in range(1):
            w = ser.write(b'start_scan_test 1' + b'\n')
            for _ in range(1):
                line = ser.readlines()  # read a '\n' terminated line
                print(line)

if __name__=='__main__':
    open_com('COM7')
    ser_read()
    close_com()
