'''
TODO: explain that this allows u to swap between diff keybinds for diff onshape modes
'''
import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.macros import Macros
from kmk.extensions.rgb import RGB, AnimationModes # remember to install NeoPixel library
from kmk.extensions.display import Display, TextEntry, ImageEntry # remember to install adafruit_display_text
from kmk.extensions.display.ssd1306 import SSD1306 # remember to install adafruit_displayio_ssd1306

from pad_profiles import Profile, ProfileSwitcher

# idk abt the specific keybinds ill figure them out later
PS_PROFILE = Profile(
    [[KC.NO, KC.NO, KC.NO],
     [KC.NO, KC.NO, KC.NO],
     [KC.NO, KC.NO, KC.NO]],
    (30, 247, 50),
    AnimationModes.BREATHING,
    []
)
SKETCH_PROFILE = Profile(
    [[KC.NO, KC.NO, KC.NO],
     [KC.NO, KC.NO, KC.NO],
     [KC.NO, KC.NO, KC.NO]],
    (56, 247, 50),
    AnimationModes.BREATHING,
    []
)
CONSTRAINT_PROFILE = Profile(
    [[KC.NO, KC.NO, KC.NO],
     [KC.NO, KC.NO, KC.NO],
     [KC.NO, KC.NO, KC.NO]],
    (141, 250, 50),
    AnimationModes.BREATHING,
    []
)
ASM_PROFILE = Profile(
    [[KC.NO, KC.NO, KC.NO],
     [KC.NO, KC.NO, KC.NO],
     [KC.NO, KC.NO, KC.NO]],
    (9, 217, 50),
    AnimationModes.BREATHING,
    []
)
STEP_SIZE = 2


profile_switcher = ProfileSwitcher([PS_PROFILE, SKETCH_PROFILE, CONSTRAINT_PROFILE, ASM_PROFILE], STEP_SIZE)

keyboard = KMKKeyboard()
keyboard.col_pins = (board.D10, board.D2, board.D1)
keyboard.row_pins = (board.D3, board.D9, board.D8)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
encoder_handler.pins = (board.D6, board.D7, None)

keyboard.modules.append(Macros())

rgb = RGB(pixel_pin=board.D0, num_pixels=12, val_default=50, val_limit=50, rgb_order=(1,0,2))
rgb.animation_mode = AnimationModes.BREATHING_RAINBOW
keyboard.extensions.append(rgb)

i2c_bus = busio.I2C(board.GP_SCL, board.GP_SDA)
display_driver = SSD1306(i2c=i2c_bus)
display = Display(display=display_driver, width=128, height=32)
display.entries = [TextEntry(text="Hello There", x=64, y=16, x_anchor="M", y_anchor="M")]
keyboard.extensions.append(display)


def switch_left_profile():
    switch_profile = profile_switcher.step_left()

    if switch_profile:
        profile = profile_switcher.curr_profile
        keyboard.keymap = profile.keymap
        rgb.set_hsv_fill(*profile.color)
        rgb.animation_mode = profile.anim_mode
        display.entries = profile.scrn_elements


def switch_right_profile():
    switch_profile = profile_switcher.step_right()

    if switch_profile:
        profile = profile_switcher.curr_profile
        keyboard.keymap = profile.keymap
        rgb.set_hsv_fill(*profile.color)
        rgb.animation_mode = profile.anim_mode
        display.entries = profile.scrn_elements


keyboard.keymap = profile_switcher.curr_profile.keymap

ENC_LEFT = KC.MACRO(switch_left_profile)
ENC_RIGHT = KC.MACRO(switch_right_profile)

encoder_handler.map = [((ENC_LEFT, ENC_RIGHT, KC.NO))]

if __name__ == "__main__":
    keyboard.go()