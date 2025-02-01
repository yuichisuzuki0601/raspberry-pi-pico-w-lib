from machine import Pin, ADC

from lib.board.pin_layout import to_gpio_number

class PotentionMeter:

    def __init__(self, name: str, pinNumber: int):
        self.name = name
        self.adc = ADC(Pin(to_gpio_number(pinNumber)))

    def read(self):
        return self.adc.read_u16()
