from machine import Pin
from utime import sleep_ms

from board.pin_layout import to_gpio_number

class Led:
    FLASH_TIME_MS = 100#[ms]

    def __init__(self, name: str, pinNumber):
        self.name = name
        id = 'LED' if pinNumber == 'LED' else to_gpio_number(pinNumber)
        self.pin = Pin(id, Pin.OUT)

    def on(self):
        print(self.name + ' led emitted.')
        self.pin.on()

    def off(self):
        self.pin.off()

    def flash(self, ms: int = FLASH_TIME_MS):
        self.on()
        sleep_ms(ms)
        self.off()

class LedPico(Led):
    def __init__(self):
        super().__init__('pico', 'LED')

class LedGroup:
    SEQUENCIAL_FLASH_TIME_MS = 50#[ms]
    ALL_FLASH_TIME_MS = 500#[ms]

    def __init__(self, *leds):
        self.leds = leds

    def all_on(self):
        for led in self.leds:
            led.on()

    def all_off(self):
        for led in self.leds:
            led.off()

    def sequencal_flash(self):
        for led in self.leds:
            led.on()
            sleep_ms(LedGroup.SEQUENCIAL_FLASH_TIME_MS)
            led.off()

    def all_flash(self):
        self.all_on()
        sleep_ms(LedGroup.ALL_FLASH_TIME_MS)
        self.all_off()
