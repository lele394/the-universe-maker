
from ..utils_class import *
from .object import Object
from .star import Star
from .planet import Planet
from .ship import Ship

import random
import numpy as np


def int_to_roman(n):
    numerals = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"),  (90, "XC"),  (50, "L"),  (40, "XL"),
        (10, "X"),   (9, "IX"),   (5, "V"),   (4, "IV"),
        (1, "I")
    ]
    result = ""
    for value, numeral in numerals:
        while n >= value:
            result += numeral
            n -= value
    return result

class StarSystem(Object):
    def __init__(self, id: int, position: Vec3= Vec3(0.0, 0.0, 0.0), name="Unnamed System"):
        super().__init__(id, position, orbit=[])
        self.name = name
        self.star = None


    def generate(self, n_planets=5):
        # ==== Configuration Parameters ====
        spectral_classes = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
        inner_types = ['Rock', 'Metal']
        outer_types = ['Gas', 'Ice', 'Rock']
        inner_weights = [0.8, 0.2]
        outer_weights = [0.5, 0.3, 0.2]
        orbit_threshold = 2.0  # in AU, separates inner and outer planet types

        # Poisson distribution for number of moons
        moon_lambdas = {
            'Gas': 3.0,
            'Ice': 2.0,
            'Rock': 0.5,
            'Metal': 0.3,
        }

        max_satellite_depth = 5
        max_subplanets = 3
        subplanet_mass_threshold = 100  # mass threshold for subplanet generation

        orbit_radius = 0.3  # initial planet orbit radius in AU
        orbit_gap_range = (0.2, 1.5)  # AU, gaps between planet orbits

        # Convert all moon/subplanet/submoon orbits from Earth radii to AU:
        EARTH_RADII_IN_AU = 1 / 215  # ≈0.00465 AU per Earth radius

        moon_orbit_range = (5 * EARTH_RADII_IN_AU, 60 * EARTH_RADII_IN_AU)  # ≈ (0.023, 0.28) AU
        subplanet_orbit_range = (1.5 * EARTH_RADII_IN_AU, 5 * EARTH_RADII_IN_AU)  # ≈ (0.007, 0.023) AU
        # submoon_orbit_range = (3 * EARTH_RADII_IN_AU, 20 * EARTH_RADII_IN_AU)  # ≈ (0.014, 0.093) AU


        # ==== Create Star ====
        spectral_class = random.choice(spectral_classes)
        self.star = Star(self.id * 10, spectral_class)
        self.star.name = f"{spectral_class}-{self.name}"
        self.orbit.append(self.star)

        # ==== Recursive Satellite Function ====
        def add_satellites(parent, depth):
            if depth > max_satellite_depth:
                return

            # Determine number of moons
            lam = moon_lambdas.get(parent.planet_type, 0.0)
            n_satellites = np.random.poisson(lam)

            for i in range(n_satellites):
                moon_orbit = random.uniform(*moon_orbit_range)
                moon_id = parent.id * 10 + i + 1
                moon_name = f"{parent.name}-{int_to_roman(i + 1)}"
                moon = Planet(moon_id, moon_orbit, name=moon_name, is_moon=True, parent_planet=parent)
                parent.orbit.append(moon)
                add_satellites(moon, depth + 1)

        # ==== Create Planets ====
        planets = []
        for i in range(n_planets):
            orbit_radius += random.uniform(*orbit_gap_range)
            planet_id = self.id * 100 + i + 1
            roman_index = int_to_roman(i + 1)
            planet_name = f"{self.name}-{roman_index}"

            if orbit_radius < orbit_threshold:
                planet_type = random.choices(inner_types, weights=inner_weights)[0]
            else:
                planet_type = random.choices(outer_types, weights=outer_weights)[0]

            planet = Planet(planet_id, orbit_radius, name=planet_name, planet_type=planet_type)
            add_satellites(planet, depth=1)

            # ==== Add Subplanets for Massive Gas Giants ====
            if planet_type == 'Gas' and planet.mass > subplanet_mass_threshold:
                n_subplanets = random.randint(1, max_subplanets)
                for j in range(n_subplanets):
                    sp_orbit = random.uniform(*subplanet_orbit_range)
                    sp_id = planet_id * 100 + j + 1
                    sp_name = f"{planet.name}-{int_to_roman(j + 1)}"
                    subplanet = Planet(sp_id, sp_orbit, name=sp_name, planet_type='Rock')
                    add_satellites(subplanet, depth=2)
                    planet.orbit.append(subplanet)

            planets.append(planet)

        self.star.orbit.extend(planets)

    def __str__(self):
        out = f"Star System: {self.name}\n"
        out += f"Star:\n{self.star}\n\n"
        out += f"Planets and Moons:\n"
        for p in self.star.orbit:
            out += f"{p}\n"
            if p.orbit:
                for m in p.orbit:
                    out += f"  Moon/Subplanet:\n    {m}\n"
                    if m.orbit:
                        for sm in m.orbit:
                            out += f"    Moon:\n      {sm}\n"
            out += "\n"
        return out
    
    def display(self):
        # ANSI color codes
        RESET = "\033[0m"
        BOLD = "\033[1m"

        PLANET_ICON_COLOR = "\033[38;5;209m"     
        STAR_ICON_COLOR = "\033[38;5;226m"     
        MOON_ICON_COLOR = "\033[38;5;47m"     
        SHIP_ICON_COLOR = "\033[38;5;199m"     


        NAME_COLOR = "\033[38;5;221m"     # Soft gold
        LABEL_COLOR = "\033[38;5;244m"    # Grayish for labels
        VALUE_COLOR = "\033[38;5;39m"     # Bright blue for values

        type_color = {
            'Rock': "\033[38;5;220m",     # Yellow-orange
            'Metal': "\033[38;5;250m",    # Light gray
            'Gas': "\033[38;5;81m",       # Cyan
            'Ice': "\033[38;5;111m",      # Light blue
        }

        def print_body(body, prefix="", is_last=True, ancestors_last=[]):
            connector = " └──>" if is_last else " ├──>"

            # Build prefix
            spacer = ""
            for is_ancestor_last in ancestors_last:
                spacer += "     " if is_ancestor_last else " │   "
            spacer += connector

            if isinstance(body, Star):
                print(
                    f"{spacer}{BOLD}{STAR_ICON_COLOR} * {NAME_COLOR}{body.name}{RESET} "
                    f"{LABEL_COLOR}(Spectral Class:{RESET} {VALUE_COLOR}{body.spectral_class}{RESET}{LABEL_COLOR}){RESET} "
                    f"Perceived color : {body.color_code}███{self.RESET_CODE}"
                )
            elif isinstance(body, Planet):
                symbol = f"{BOLD}{MOON_ICON_COLOR} •" if body.is_moon else f"{BOLD}{PLANET_ICON_COLOR} ⬤"
                type_col = type_color.get(body.planet_type, "")
                print(
                    f"{spacer}{symbol} {BOLD}{NAME_COLOR}{body.name}{RESET} "
                    f"{type_col}{body.planet_type}{RESET}   \t"
                    f"{LABEL_COLOR}Orbit:{RESET} {VALUE_COLOR}{body.orbit_radius:3.3f} au{RESET} \t"
                    f"{LABEL_COLOR}Radius:{RESET} {VALUE_COLOR}{body.radius} R⊕{RESET}    \t"
                    f"{LABEL_COLOR}Density:{RESET} {VALUE_COLOR}{body.density} g/cm³{RESET} \t"
                )
            elif isinstance(body, Ship):
                symbol = f"{BOLD}{SHIP_ICON_COLOR} ➤"
                print(
                    f"{spacer}{symbol} {BOLD}{NAME_COLOR}{body.name}{RESET}   "
                    f"{body.owner_color} {body.owner}    {LABEL_COLOR} {body.type} {RESET}"
                )

            last_index = len(body.orbit) - 1
            for i, child in enumerate(body.orbit):
                is_last_child = (i == last_index)
                print_body(child, prefix + "   ", is_last_child, ancestors_last + [is_last])

        print(f"{BOLD}\033[92m ¤ Star System: {self.name}{RESET}")
        print_body(self.star, is_last=True)



    def get_object(self, name):
        def search(orbiting_bodies):
            for obj in orbiting_bodies:
                if obj.name == name:
                    return obj
                # Recursively search moons or sub-planets
                if hasattr(obj, 'orbit'):
                    found = search(obj.orbit)
                    if found:
                        return found
            return None

        if self.star:
            return search(self.star.orbit)
        return None
