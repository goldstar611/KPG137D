#!/usr/bin/python3

import serial
import time


class KenwoodRadio:
    def __init__(self, port=None):
        print("__init__()")
        self.port = port
        self._connection = None
        
    def __enter__(self):
        print("__enter__()")
        if self.port:
            self._connect()
            self._enter_programming_mode()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__()")
        self._exit_programming_mode()
        
    def _connect(self):
        if not self.port:
            raise ValueError("Could not connect because no port is specif")
            
        self._connection = serial.Serial(port=self.port, 
                                         baudrate=9600, 
                                         bytesize=serial.EIGHTBITS, 
                                         parity=serial.PARITY_NONE, 
                                         stopbits=serial.STOPBITS_ONE,
                                         timeout=10)
        self._connection.flush()
    
    def _enter_programming_mode(self):
        self._connection.baudrate = 9600
        time.sleep(0.1)

        self.write(b"PROGRAM")
        self._expect_response(b"\x16")

        self._connection.baudrate = 9600 * 2
        self._expect_response(b"\x06")

        self.write(b"\x02")
        self._expect_response(b"PTK-U100")
        self.read(size=40)
        
        self.write(b"\x0b\x06")
        self._expect_response(b"\x06")
    
    def _exit_programming_mode(self):
        pre_close_bytes = self.read(self._connection.in_waiting)

        self.write(b"\xBA")
        #self._expect_response(b"\xFE")  # TODO FIXME
        a = self.read(size=1)

        self._connection.baudrate = 9600
        time.sleep(0.1)

        self.write(b"\xBA")
        #self._expect_response(b"\xF0")  # TODO FIXME
        b = self.read(size=1)

        post_close_bytes = self.read(self._connection.in_waiting)
        pass
    
    def _expect_response(self, expected_data):
        actual_data = self.read(len(expected_data))
        if actual_data != expected_data:
            raise ValueError("Radio did not return expected response!\nExpected: {}\nActual: {}".format(expected_data, actual_data))
    
    def read(self, size=1):
        if not self._connection:
            self._connect() 
        return self._connection.read(size)
    
    def write(self, data):
        if not self._connection:
            self._connect()
        self._connection.write(data)


if __name__ == "__main__":
    with KenwoodRadio(port="/dev/ttyUSB0") as r:
        pass
