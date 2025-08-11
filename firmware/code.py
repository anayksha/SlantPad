'''
TODO: explain that this allows u to swap between diff keybinds for diff onshape modes
'''
import board # type: ignore
import busio # type: ignore

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.macros import Macros
from kmk.extensions.display import Display, TextEntry, ImageEntry # remember to install adafruit_display_text
from kmk.extensions.display.ssd1306 import SSD1306 # remember to install adafruit_displayio_ssd1306
from kmk.extensions.media_keys import MediaKeys

from pad_profiles import Profile, ProfileSwitcher


keyboard = KMKKeyboard()
encoder_handler = EncoderHandler()
i2c_bus = busio.I2C(board.D5, board.D4)
display_driver = SSD1306(i2c=i2c_bus)
display = Display(display=display_driver, width=128, height=32)

keyboard.col_pins = (board.D10, board.D2, board.D1)
keyboard.row_pins = (board.D3, board.D9, board.D8)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
encoder_handler.pins = ((board.D6, board.D7, None))

keyboard.modules.extend([encoder_handler, Macros()])
keyboard.extensions.extend([display, MediaKeys()])


# idk abt the specific keybinds ill figure them out later
# idk why i chose microsoft colors but they're good placeholder ig
MEDIA_PROFILE = Profile(
    [[
        KC.MPRV, KC.MPLY, KC.MNXT,
        KC.VOLD, KC.MUTE, KC.VOLU,
        KC.MRWD, KC.MSTP, KC.MFFD
    ]],
    [
        TextEntry("Samvididdy", 64, 16, x_anchor="M", y_anchor="B"),
        TextEntry("ik where u live", 64, 16, x_anchor="M", y_anchor="T")
    ]
)
PS_PROFILE = Profile(
    [[
        KC.N1, KC.N1, KC.N1,
        KC.N1, KC.N1, KC.N1,
        KC.N1, KC.N1, KC.N1
    ]],
    [
        TextEntry("part studio be like", 64, 16, x_anchor="M", y_anchor="M"),
    ]
)
SKETCH_PROFILE = Profile(
    [[
        KC.N2, KC.N2, KC.N2,
        KC.N2, KC.N2, KC.N2,
        KC.N2, KC.N2, KC.N2
    ]],
    [
        TextEntry("sketch be like", 64, 16, x_anchor="M", y_anchor="M")
    ]
)
CONSTRAINT_PROFILE = Profile(
    [[
        KC.N3, KC.N3, KC.N3,
        KC.N3, KC.N3, KC.N3,
        KC.N3, KC.N3, KC.N3
    ]],
    [
        TextEntry("constraint be like", 64, 16, x_anchor="M", y_anchor="M")
    ]
)
ASM_PROFILE = Profile(
    [[
        KC.N4, KC.N4, KC.N4,
        KC.N4, KC.N4, KC.N4,
        KC.N4, KC.N4, KC.N4
    ]],
    [
        TextEntry("assembly be like", 64, 16, x_anchor="M", y_anchor="M")
    ]
)
STEP_SIZE = 2

profile_switcher = ProfileSwitcher([MEDIA_PROFILE, PS_PROFILE, SKETCH_PROFILE, CONSTRAINT_PROFILE, ASM_PROFILE], STEP_SIZE)


def switch_left_profile():
    switch_profile = profile_switcher.step_left()

    if switch_profile:
        profile = profile_switcher.curr_profile
        keyboard.keymap = profile.keymap
        display.entries = profile.scrn_elements


def switch_right_profile():
    switch_profile = profile_switcher.step_right()

    if switch_profile:
        profile = profile_switcher.curr_profile
        keyboard.keymap = profile.keymap
        display.entries = profile.scrn_elements

init_profile = profile_switcher.curr_profile
keyboard.keymap = init_profile.keymap
display.entries = init_profile.scrn_elements

ENC_LEFT = KC.MACRO(switch_left_profile)
ENC_RIGHT = KC.MACRO(switch_right_profile)

encoder_handler.map = [((ENC_LEFT, ENC_RIGHT, KC.NO))]

if __name__ == "__main__":
    keyboard.go()