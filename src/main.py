from lib.board.unique_id import get_unique_id
from lib.circuit_element.led import LedPico
import process_led

led_pico = LedPico()

print('pico init.')
led_pico.on()
print(f'Unique ID: {get_unique_id()}\n')

try:
    process_led.process()
except BaseException as e:
    print(e)
finally:
    print('pico end.')
    led_pico.off()
