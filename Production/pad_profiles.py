'''
TODO: add module docstring
'''
class Profile:
    '''
    TODO: make docstring
    '''
    def __init__(self, keymap:list, scrn_elements:list):
        self.keymap = keymap
        self.scrn_elements = scrn_elements
        
class ProfileSwitcher:
    '''
    TODO: make docstring
    '''
    def __init__(self, profiles:list, step_size:int):
        self.pos = 0
        self.profiles = profiles
        self.step_size = step_size

    def step_left(self) -> bool:
        '''
        steps the position to the left, and returns True if the current profile changed
        '''
        self.pos = (self.pos - 1) % (len(self.profiles) * self.step_size)
        return self.pos % self.step_size == 0

    def step_right(self) -> bool:
        self.pos = (self.pos + 1) % (len(self.profiles) * self.step_size)
        return self.pos % self.step_size == 0

    @property
    def curr_profile(self) -> Profile:
        return self.profiles[self.pos // self.step_size]
