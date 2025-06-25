import numpy as np
import random

from ..utils_class import *
from .object import Object


class Ship(Object):
    def __init__(self, id: int, stats: dict, current_location, position=None, orbit=None):
        super().__init__(id, position, orbit if orbit else [])

        self.name = stats.get("name", "unnamed")
        self.type = stats.get("type", "frigate")
        self.owner = stats.get("owner", "Léo")
        self.owner_color = stats.get("owner_color", "\033[38;5;39m")

        self.current_location = current_location

        self.spawn()


    def __str__(self):
        return (
            f" ======= {self.name} ======= \t"
            f" Type : {self.type} \t"
            f" Owner : {self.owner} \t"
            f" Location : {self.current_location.name} \t"
        )


    def spawn(self):
        """
        takes the new object (Star or Planet) where to spawn.
        """
        self.current_location.orbit.insert(0, self)

    def move(self, new_location):
        """
        takes the new object (Star or Planet) where to go.
        """
        self.current_location.orbit.remove(self)
        self.current_location = new_location
        self.spawn()
