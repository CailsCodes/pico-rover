from busio import UART
import board
import digitalio
from time import sleep, sleep_ms
import _bleio

class Bluedot:

    def __init__(self, tx=board.GP0, rx=board.GP1):
        self.uart = UART(tx=tx, rx=rx, baudrate=115200)
        self.BLE_MODE_PIN = digitalio.DigitalInOut(board.GP15)
        self.BLE_MODE_PIN.direction = digitalio.Direction.INPUT
        
    def wait_for_connection(self):
        if not self.BLE_MODE_PIN.value:
            print("Waiting for connection...")
        while not self.BLE_MODE_PIN.value:
            sleep(5)

    def assert_name(self, BLE_NAME=b"SPP-Rover", _attempt=0):
        self.uart.write(b"AT+TD\r\n")
        sleep_ms(20)
        current_name = uart.read()[3:-4]
        print("Current SPP name is: ", current_name)

        if current_name != BLE_NAME:
            print("Updating name to: ", BLE_NAME)
            uart.write(b"AT+BD"+BLE_NAME+b"\r\n")
            sleep_ms(20)
            if _attempt < 3:
                self.assert_name(BLE_NAME=BLE_NAME, _attempt=_attempt+1)
            else:
                raise AssertionError("Could not change name of SPP")

        
    def read_device(self, message):
        assert message[0] == "3"
        *_, client_name
        return client_name

    
    def BLE_address(self, message):
        addr = message[3:15].decode("utf-8")
        return ":".join([addr[i:i+2] for i in range(0,11,2)][::-1])


    def read_xy(self, message):
        x = y = 0
        assert message[0] == "1" or  message[0] == "2"
        *_, x, y = message.split(",")
        x, y = float(x), float(y.strip())
        return x,y