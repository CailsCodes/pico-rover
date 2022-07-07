from math import atan, atan2, degrees, sqrt
from time import sleep

import board
import digitalio
import pwmio


class Driver():

    def __init__(self, a, b):
        self.pwm_a = pwmio.PWMOut(a)
        self.pwm_b = pwmio.PWMOut(b)

    def calc_speed(self, speed):
        return (speed * 65535) // 100
    
    def drive(self, forward=0, backward=0):
        assert backward == 0 or forward == 0
        speed = self.calc_speed(forward if forward else backward)

        if forward:
            self.pwm_a.duty_cycle = speed
            self.pwm_b.duty_cycle = 0
        else:
            self.pwm_a.duty_cycle = 0
            self.pwm_b.duty_cycle = speed


class Rover():

    def __init__(self):
        
        self.left_motor = Driver(board.GP21, board.GP20)
        self.right_motor = Driver(board.GP19, board.GP18)

        self.motor_1 = digitalio.DigitalInOut(board.GP17)
        self.motor_1.direction = digitalio.Direction.OUTPUT

        self.motor_2 = digitalio.DigitalInOut(board.GP16)
        self.motor_2.direction = digitalio.Direction.OUTPUT

        self.motor_status(True)
        
    def motor_status(self, status=True):
        self.motor_1.value = status
        self.motor_2.value = status

    def detect_spin(self, x, y, in_sector=15):
        "Determine whether robot should spin on the spot."
        point_angle = degrees(atan(y/x))
        if -in_sector < point_angle < in_sector:
            return True

    def calc_speed(self, x, y):
        return min(sqrt(x**2 + y**2), 1)

    def calc_angle(self, x, y):
        return degrees(atan2(y, x))

    def get_differential_speeds(self, angle, speed):
        differential = angle / 90
        left = right = speed
        if differential > 1: # left
            left /= differential
        elif differential < 1: # right
            right *= differential
        return left, right
