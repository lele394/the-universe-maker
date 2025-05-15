import numpy as np
import random

from ..utils_class import *
from .object import Object


class Planet(Object):
    # Common properties per planet type
    type_properties = {
        "Gas": {
            "mass_range": (50, 300),  # Earth masses
            "radius_range": (3.5, 14),  # Earth radii
            "density_range": (0.3, 1.3),
            "core_composition": "Hydrogen-Helium",
            "atmosphere_options": ["Hydrogen-Helium", "Methane", "Ammonia"]
        },
        "Ice": {
            "mass_range": (1, 50),
            "radius_range": (1.5, 3.5),
            "density_range": (0.9, 2.0),
            "core_composition": "Water-Ice",
            "atmosphere_options": ["Methane", "Nitrogen", "None"]
        },
        "Rock": {
            "mass_range": (0.1, 10),
            "radius_range": (0.5, 2),
            "density_range": (3.0, 5.5),
            "core_composition": "Iron-Nickel",
            "atmosphere_options": ["Thin CO₂", "Nitrogen-Oxygen", "None"]
        },
        "Metal": {
            "mass_range": (0.5, 5),
            "radius_range": (0.3, 1.2),
            "density_range": (5.0, 8.0),
            "core_composition": "Iron-Nickel",
            "atmosphere_options": ["None"]
        },
        "Moon": {
            "mass_range": (0.001, 0.1),
            "radius_range": (0.1, 0.5),
            "density_range": (2.5, 4.0),
            "core_composition": "Rocky-Iron",
            "atmosphere_options": ["None", "Trace Gases"]
        }
    }

    def __init__(self, id: int, orbit_radius: float, position=None, orbit=None, 
                name="Unnamed Planet", planet_type=None, is_moon=False, parent_planet=None):
        super().__init__(id, position, orbit if orbit else [])

        self.name = name
        self.orbit_radius = orbit_radius  # AU for planets, planetary radii or similar for moons
        self.is_moon = is_moon
        self.parent_planet = parent_planet  # Planet this moon orbits, None if planet

        # If type not specified, randomly pick based on body type
        if planet_type is None:
            planet_type = "Moon" if is_moon else random.choice(["Gas", "Ice", "Rock", "Metal"])
        self.planet_type = planet_type

        props = self.type_properties[planet_type]

        # Mass & radius within type ranges
        self.mass = round(random.uniform(*props["mass_range"]), 3)
        self.radius = round(random.uniform(*props["radius_range"]), 3)

        # Density consistent with type
        self.density = round(random.uniform(*props["density_range"]), 3)

        # Surface gravity (g = M / R^2), normalized to Earth units
        self.surface_gravity = round(self.mass / self.radius**2, 3)

        # Escape velocity (approx sqrt(2 * g * R))
        self.escape_velocity = round(math.sqrt(2 * self.surface_gravity * self.radius), 3)

        # Orbital period:
        # Planets orbit stars: T^2 = r^3 (years and AU)
        # Moons orbit planets: use simplified approximation (in days), assuming circular orbits
        if not is_moon:
            self.orbital_period = round(math.sqrt(self.orbit_radius**3), 3)  # Earth years
        else:
            # Assuming orbit_radius in planetary radii, convert to AU assuming Earth's radius as baseline (~0.00000465 AU)
            # This is a simplification
            orbital_radius_AU = self.orbit_radius * 0.00000465 * (parent_planet.radius if parent_planet else 1)
            self.orbital_period = round(math.sqrt(orbital_radius_AU**3), 5) * 365.25  # days

        # Rotation period random
        self.rotation_period = round(random.uniform(10, 1000), 1)  # hours

        # Atmosphere from options
        self.atmosphere = random.choice(props["atmosphere_options"])

        # Temperature (simplified)
        if not is_moon:
            # Based on star distance
            self.temperature = round(288 / math.sqrt(self.orbit_radius), 1)
        else:
            # Moons cooler, assume lower temperature (arbitrary)
            self.temperature = round(random.uniform(50, 250), 1)

        # Core composition
        self.core_composition = props["core_composition"]

    def __str__(self):
        header = f"{self.BOLD}{self.CYAN}======== {self.YELLOW}{self.name} ({'Moon' if self.is_moon else 'Planet'}) {self.CYAN}========{self.RESET_CODE}\n"
        return (
            header +
            f"{self.BOLD}{self.CYAN}Type:{self.RESET_CODE} {self.YELLOW}{self.planet_type}{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Orbit Radius:{self.RESET_CODE} {self.YELLOW}{self.orbit_radius}{' planetary radii' if self.is_moon else ' AU'}{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Temperature:{self.RESET_CODE} {self.YELLOW}{self.temperature} K{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Mass:{self.RESET_CODE} {self.YELLOW}{self.mass} {'Earth masses' if not self.is_moon else 'Earth masses (moon scale)'}{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Radius:{self.RESET_CODE} {self.YELLOW}{self.radius} {'Earth radii' if not self.is_moon else 'Earth radii (moon scale)'}{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Density:{self.RESET_CODE} {self.YELLOW}{self.density} g/cm³{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Surface Gravity:{self.RESET_CODE} {self.YELLOW}{self.surface_gravity} g{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Escape Velocity:{self.RESET_CODE} {self.YELLOW}{self.escape_velocity} × Earth's{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Rotation Period:{self.RESET_CODE} {self.YELLOW}{self.rotation_period} hours{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Orbital Period:{self.RESET_CODE} {self.YELLOW}{self.orbital_period} {'days' if self.is_moon else 'Earth years'}{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Core Composition:{self.RESET_CODE} {self.YELLOW}{self.core_composition}{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Atmosphere:{self.RESET_CODE} {self.YELLOW}{self.atmosphere}{self.RESET_CODE}"
        )
