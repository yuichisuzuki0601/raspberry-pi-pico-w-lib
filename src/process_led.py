from utime import sleep_ms

from lib.circuit_element.led import Led

def process():
    led_red = Led('red', 17)
    led_yellow = Led('yellow', 12)

    # =====

    print('=== Led Process Start ===')

    try:
        while True:
            led_red.on()
            led_yellow.on()
            sleep_ms(500)
            led_red.off()
            led_yellow.off()
            sleep_ms(500)
    except BaseException as e:
        led_red.off()
        led_yellow.off()
        raise e
