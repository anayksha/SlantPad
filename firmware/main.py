'''
this is supposed to have functionality that allows the user to
swap between profiles and have more complex lighting effects
and a proper screen thing but i honestly dont want to code this rn
cause i then I have to learn kmk
'''
import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB, AnimationModes # remember to install NeoPixel library
from kmk.extensions.display import Display, TextEntry, ImageEntry # remember to install adafruit_display_text
from kmk.extensions.display.ssd1306 import SSD1306 # remember to install adafruit_displayio_ssd1306

keyboard = KMKKeyboard()
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)

keyboard.col_pins(board.D10, board.D2, board.D1)
keyboard.row_pins(board.D3, board.D9, board.D8)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

encoder_handler.pins = (board.D6, board.D7, None)

keyboard.keymap = [
    [KC.A, KC.B, KC.C],
    [KC.D, KC.E, KC.F],
    [KC.G, KC.H, KC.I]
]
encoder_handler.map = [((KC.DOWN, KC.UP, KC.NO))]

rgb = RGB(pixel_pin=board.D0, num_pixels=12, rgb_order=(1,0,2))
rgb.animation_mode = AnimationModes.BREATHING_RAINBOW
keyboard.extensions.append(rgb)

i2c_bus = busio.I2C(board.GP_SCL, board.GP_SDA)
display_driver = SSD1306(i2c=i2c_bus)


display = Display(display=display_driver, width=128, height=32)
display.entries = [TextEntry(text="Hello There", x=64, y=16, x_anchor="M", y_anchor="M")]
keyboard.extensions.append(display)

if __name__ == "__main__":
    keyboard.go()