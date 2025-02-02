from machine import Pin, ADC

from lib.board.pin_layout import to_gpio_number

class PotentionMeter:

    def __init__(self, name: str, pinNumber: int, min_value: int = 0):
        self.name = name
        self.adc = ADC(Pin(to_gpio_number(pinNumber)))
        self.min_value = min_value

    def read(self):
        value = self.adc.read_u16()
        return value if self.min_value <= value else 0
