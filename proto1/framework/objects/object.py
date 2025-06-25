from ..utils_class import *


class Object():

    RESET_CODE = '\033[0m'
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"

    def __init__(self, id, position: Vec3 = None, orbit: list = None):
        self.id = id
        self.position = position if position else Vec3(0.0, 0.0, 0.0)
        self.orbit = orbit if orbit is not None else []
