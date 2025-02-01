from machine import Pin, PWM, Timer

from lib.board.pin_layout import to_gpio_number

class DynamicSpeaker:
    MAX_DUTY = 15

    def __init__(self, name: str, pinNumber: int, potentionmeter = None):
        self.name = name
        self.pwm = PWM(Pin(to_gpio_number(pinNumber), Pin.OUT))
        self.potentionmeter = potentionmeter
        self.timer = Timer()

    def __adjust_volume(self, _):
        if self.potentionmeter is not None:
            self.pwm.duty_u16(2 ** (int(self.potentionmeter.read() / 65535 * DynamicSpeaker.MAX_DUTY)))
        else:
            self.pwm.duty_u16(2 ** DynamicSpeaker.MAX_DUTY)

    def on(self, freq):
        print(f'{self.name} speaker {freq}Hz emitted.')
        self.pwm.freq(freq)
        self.timer.init(period = 1, mode = Timer.PERIODIC, callback = self.__adjust_volume)

    def off(self):
        self.pwm.duty_u16(0)
        self.timer.deinit()
