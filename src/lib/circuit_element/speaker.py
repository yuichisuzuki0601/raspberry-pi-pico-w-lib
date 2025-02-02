from machine import Pin, PWM, Timer

from lib.board.pin_layout import to_gpio_number

class DynamicSpeaker:
    MAX_DUTY = 32768

    def __adjust_volume(self, _):
        duty = 0
        if self.is_on:
            if self.potentionmeter is None:
                duty = DynamicSpeaker.MAX_DUTY
            else:
                duty = int((self.potentionmeter.read() / 65535) * DynamicSpeaker.MAX_DUTY)
        self.pwm.duty_u16(duty)

    def __init__(self, name: str, pinNumber: int, potentionmeter = None):
        self.name = name
        self.pwm = PWM(Pin(to_gpio_number(pinNumber), Pin.OUT))
        self.potentionmeter = potentionmeter
        self.is_on = False
        self.timer = Timer()
        self.timer.init(period = 50, mode = Timer.PERIODIC, callback = self.__adjust_volume)

    def on(self, freq):
        print(f'{self.name} speaker {freq}Hz emitted.')
        self.pwm.freq(freq)
        self.is_on = True

    def off(self):
        self.is_on = False
