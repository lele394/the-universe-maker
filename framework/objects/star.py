import random

from ..utils_class import *
from .object import Object


class Star(Object):
    # Mapping of spectral classes to their temperature ranges (in Kelvin)
    SPECTRAL_TEMPERATURE_RANGES = {
        'O': (30000, 50000),
        'B': (10000, 30000),
        'A': (7500, 10000),
        'F': (6000, 7500),
        'G': (5200, 6000),
        'K': (3700, 5200),
        'M': (2400, 3700),
    }

    # Mapping of spectral classes to their mass ranges (in solar masses)
    SPECTRAL_MASS_RANGES = {
        'O': (16, 90),
        'B': (2.1, 16),
        'A': (1.4, 2.1),
        'F': (1.04, 1.4),
        'G': (0.8, 1.04),
        'K': (0.45, 0.8),
        'M': (0.08, 0.45),
    }

    # Mapping of spectral classes to their radius ranges (in solar radii)
    SPECTRAL_RADIUS_RANGES = {
        'O': (6.6, 15),
        'B': (1.8, 6.6),
        'A': (1.4, 1.8),
        'F': (1.15, 1.4),
        'G': (0.96, 1.15),
        'K': (0.7, 0.96),
        'M': (0.1, 0.7),
    }

    # Mapping of spectral classes to their luminosity ranges (in solar luminosities)
    SPECTRAL_LUMINOSITY_RANGES = {
        'O': (30000, 800000),
        'B': (25, 30000),
        'A': (5, 25),
        'F': (1.5, 5),
        'G': (0.6, 1.5),
        'K': (0.08, 0.6),
        'M': (0.001, 0.08),
    }

    # Mapping of spectral classes to ANSI color codes
    SPECTRAL_COLOR_CODES = {
        'O': '\033[38;5;21m',    # Bright Blue
        'B': '\033[38;5;27m',    # Deep Blue
        'A': '\033[38;5;45m',    # Light Blue
        'F': '\033[38;5;226m',   # Yellow
        'G': '\033[38;5;220m',   # Golden Yellow
        'K': '\033[38;5;208m',   # Orange
        'M': '\033[38;5;196m',   # Red
    }



    def __init__(self, id: int, spectral_class: str, position: Vec3 = None, orbit: list = None, name: str = "default"):
        if orbit is None:
            orbit = []
        super().__init__(id, position, orbit)
        self.name = name

        self.spectral_class = spectral_class.upper()
        self.temperature = self.assign_property(self.SPECTRAL_TEMPERATURE_RANGES)
        self.mass = self.assign_property(self.SPECTRAL_MASS_RANGES)
        self.radius = self.assign_property(self.SPECTRAL_RADIUS_RANGES)
        self.luminosity = self.assign_property(self.SPECTRAL_LUMINOSITY_RANGES)
        self.color_code = self.SPECTRAL_COLOR_CODES.get(self.spectral_class, self.RESET_CODE)

    def assign_property(self, property_ranges):
        if self.spectral_class in property_ranges:
            min_val, max_val = property_ranges[self.spectral_class]
            return round(random.uniform(min_val, max_val), 2)
        else:
            raise ValueError(f"Unknown spectral class: {self.spectral_class}")

    def __str__(self):
        color_block = f"{self.color_code}███{self.RESET_CODE}"
        return (
            f"{self.BOLD}{self.CYAN}======== {self.YELLOW}{self.name} {self.CYAN}========{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Spectral Class:{self.RESET_CODE} {self.YELLOW}{self.spectral_class}{self.RESET_CODE} {color_block}\n"
            f"{self.BOLD}{self.CYAN}Temperature:{self.RESET_CODE} {self.YELLOW}{self.temperature} K{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Mass:{self.RESET_CODE} {self.YELLOW}{self.mass} solar masses{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Radius:{self.RESET_CODE} {self.YELLOW}{self.radius} solar radii{self.RESET_CODE}\n"
            f"{self.BOLD}{self.CYAN}Luminosity:{self.RESET_CODE} {self.YELLOW}{self.luminosity} solar luminosities{self.RESET_CODE}"
        )



