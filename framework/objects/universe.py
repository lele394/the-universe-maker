import random
import numpy as np
import string
import copy

from ..utils_class import *

from .star_system import StarSystem


class Universe:
    def __init__(self):
        self.systems = {}
        self.n_systems = None

    def generate(self, n_systems: int, poisson_lambda: float):
        used_names = set()
        self.n_systems = n_systems

        def random_system_name():
            while True:
                prefix = ''.join(random.choices(string.ascii_uppercase, k=3))
                suffix = ''.join(random.choices(string.digits, k=4))
                name = f"{prefix}-{suffix}"
                if name not in used_names:
                    used_names.add(name)
                    return name

        for i in range(n_systems):
            system_name = random_system_name()
            n_planets = max(1, np.random.poisson(poisson_lambda))

            pos = Vec3(
                random.random(),
                random.random(),
                random.random()
            )
            system = None
            system = StarSystem(id=i, name=system_name, position=pos)
            system.generate(n_planets=n_planets)
            # system.display()
            self.systems[system_name] = copy.deepcopy(system)



    def info(self):
        for name, system in self.systems.items():
            print(name, system.star.spectral_class, system.position)



    def get_system(self, name):
        try: 
            return self.systems[name]
        except KeyError:
            return None