from machine import Pin
from utime import ticks_ms

from board.pin_layout import to_gpio_number

class TactSwitch:
    OFF = 0
    ON = 1
    BOUNCE_TIME_MS = 1000#[ms]#サーバーが国内ならもうちょっと短くても大丈夫そう

    def __init__(self, name: str, pinNumber: int, bounce_time_ms = BOUNCE_TIME_MS):
        self.lastInterruptTime = 0
        self.name = name
        self.pin = Pin(to_gpio_number(pinNumber), Pin.IN, Pin.PULL_UP)
        self.bounce_time_ms = bounce_time_ms

    def status(self):
        return TactSwitch.ON if self.pin.value() == 0 else TactSwitch.OFF

    def on_click(self, callback):
        def handler(_):
            # debouncing
            currentTime = ticks_ms()
            print(f'bounce: {self.name} {str(currentTime - self.lastInterruptTime)}')
            if currentTime - self.lastInterruptTime > self.bounce_time_ms:
                print(f'{self.name} tact switch clicked.')
                self.lastInterruptTime = currentTime
                callback()
        self.pin.irq(trigger = Pin.IRQ_FALLING, handler = handler)
