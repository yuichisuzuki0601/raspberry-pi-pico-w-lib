from machine import Pin, PWM

from board.pin_layout import to_gpio_number

class Tb67h45:
    DEFAULT_SPEED = int(65536 * (50 / 100))

    def __init__(self, name: str, pin1Number: int, pin2Number: int):
        self.name = name
        self.pin1 = PWM(Pin(to_gpio_number(pin1Number), Pin.OUT), 60000)
        self.pin2 = PWM(Pin(to_gpio_number(pin2Number), Pin.OUT), 60000)

    def rotate(self, reverse = False, speed = DEFAULT_SPEED):
        fix = self.pin1 if reverse else self.pin2
        pwm = self.pin2 if reverse else self.pin1
        fix.duty_u16(65536)
        pwm.duty_u16(65536 - speed)

    def stop(self):
        self.pin1.duty_u16(65536)
        self.pin2.duty_u16(65536)
