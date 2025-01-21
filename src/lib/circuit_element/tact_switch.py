from machine import Pin
from utime import ticks_ms

from board.pin_layout import to_gpio_number

class TactSwitch:
    OFF = 0
    ON = 1
    BOUNCE_TIME_MS = 5000#[ms]#サーバーが国内ならもうちょっと短くても大丈夫そう

    def __init__(self, name, pinNumber):
        self.lastInterruptTime = 0
        self.name = name
        self.pin = Pin(to_gpio_number(pinNumber), Pin.IN, Pin.PULL_UP)

    def status(self):
        return TactSwitch.ON if self.pin.value() == 0 else TactSwitch.OFF

    def on_click(self, callback):
        def handler(_):
            # debouncing
            currentTime = ticks_ms()
            print(f'bounce: {self.name} {str(currentTime - self.lastInterruptTime)}')
            if currentTime - self.lastInterruptTime > TactSwitch.BOUNCE_TIME_MS:
                print(f'{self.name} tact switch clicked.')
                callback()
                self.lastInterruptTime = currentTime
        self.pin.irq(trigger = Pin.IRQ_FALLING, handler = handler)
