import numpy as np
import random
from scipy.signal import convolve2d

from ..utils_class import *
from .object import Object

from ..config import planet as planet_config
from ..config import colors









def height_to_color(value):
    """Interpolates color from color_scheme based on value in [0,1]."""

    color_scheme = planet_config.color_scheme_dic["earth"]

    for i in range(len(color_scheme) - 1):
        v0, c0 = color_scheme[i]
        v1, c1 = color_scheme[i + 1]
        if value <= v1:
            t = (value - v0) / (v1 - v0)
            return c0 if t < 0.5 else c1
    return color_scheme[-1][1]

def render_heightmap(map_data):
    rows, cols = map_data.shape
    for y in range(0, rows, 2):
        top = map_data[y]
        bottom = map_data[y+1] if y+1 < rows else np.zeros(cols)
        line = ""
        for t, b in zip(top, bottom):
            color_top = height_to_color(t)
            color_bottom = height_to_color(b)
            line += f"\x1b[48;5;{color_bottom}m\x1b[38;5;{color_top}m▀"
        print(line + "\x1b[0m")  # Reset


def generate_heightmap(rows, cols, surface_seed):
    rng = np.random.default_rng(surface_seed)
    lat = np.linspace(-np.pi / 2, np.pi / 2, rows)
    lon = np.linspace(0, 2 * np.pi, cols)
    lat_grid, _ = np.meshgrid(lat, lon, indexing='ij')

    noise = rng.random((rows, cols))
    lat_weight = np.cos(lat_grid)

    terrain = noise * lat_weight

    terrain += np.ones((rows, cols)) *( 5.0 - np.exp(- (lat_grid*0.6)**8))

    kernels = {
        3: np.array([
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]
        ]) / 16,
        4: np.array([
            [1, 3, 3, 1],
            [3, 9, 9, 3],
            [3, 9, 9, 3],
            [1, 3, 3, 1]
        ]) / 64,
        5: np.array([
            [1, 4, 6, 4, 1],
            [4,16,24,16, 4],
            [6,24,36,24, 6],
            [4,16,24,16, 4],
            [1, 4, 6, 4, 1]
        ]) / 256,
        6: np.array([
            [1, 5, 10, 10, 5, 1],
            [5,25, 50, 50,25, 5],
            [10,50,100,100,50,10],
            [10,50,100,100,50,10],
            [5,25, 50, 50,25, 5],
            [1, 5, 10, 10, 5, 1]
        ]) / 676
    }

    kernel_size = random.choice(list(kernels.keys()))
    kernel = kernels[kernel_size]

    terrain = convolve2d(terrain, kernel, mode='same', boundary='wrap')
    terrain = (terrain - terrain.min()) / (terrain.max() - terrain.min())  # Normalize
    return terrain



class Planet(Object):
    # Common properties per planet type


    def __init__(self, id: int, orbit_radius: float, position=None, orbit=None, 
                name="Unnamed Planet", planet_type=None, is_moon=False, parent_planet=None):
        super().__init__(id, position, orbit if orbit else [])

        self.name = name
        self.orbit_radius = orbit_radius  # AU for planets, planetary radii or similar for moons
        self.is_moon = is_moon
        self.parent_planet = parent_planet  # Planet this moon orbits, None if planet
        
        
        self.has_been_scanned = False
        self.surface_seed = None
        self.heightmap = None
        self.anomalies = {
            "athmosphere" : {},
            "terrain" : {},
            "underground" : {}
        }

        # If type not specified, randomly pick based on body type
        if planet_type is None:
            planet_type = "Moon" if is_moon else random.choice(["Gas", "Ice", "Rock", "Metal"])
        self.planet_type = planet_type

        props = planet_config.type_properties[planet_type]

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
        header = f"{colors.BOLD}{colors.CYAN}======== {colors.YELLOW}{self.name} ({'Moon' if self.is_moon else 'Planet'}) {colors.CYAN}========{colors.RESET}\n"
        return (
            header +
            f"{colors.BOLD}{colors.CYAN}Type:{colors.RESET} {colors.YELLOW}{self.planet_type}{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Orbit Radius:{colors.RESET} {colors.YELLOW}{self.orbit_radius}{' planetary radii' if self.is_moon else ' AU'}{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Temperature:{colors.RESET} {colors.YELLOW}{self.temperature} K{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Mass:{colors.RESET} {colors.YELLOW}{self.mass} {'Earth masses' if not self.is_moon else 'Earth masses (moon scale)'}{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Radius:{colors.RESET} {colors.YELLOW}{self.radius} {'Earth radii' if not self.is_moon else 'Earth radii (moon scale)'}{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Density:{colors.RESET} {colors.YELLOW}{self.density} g/cm³{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Surface Gravity:{colors.RESET} {colors.YELLOW}{self.surface_gravity} g{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Escape Velocity:{colors.RESET} {colors.YELLOW}{self.escape_velocity} × Earth's{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Rotation Period:{colors.RESET} {colors.YELLOW}{self.rotation_period} hours{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Orbital Period:{colors.RESET} {colors.YELLOW}{self.orbital_period} {'days' if self.is_moon else 'Earth years'}{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Core Composition:{colors.RESET} {colors.YELLOW}{self.core_composition}{colors.RESET}\n"
            f"{colors.BOLD}{colors.CYAN}Atmosphere:{colors.RESET} {colors.YELLOW}{self.atmosphere}{colors.RESET}"
        )

    def scan(self):


        if not self.has_been_scanned:
            self.has_been_scanned = True
            self.surface_seed = random.randint(0, 99999999)

            # Random anomalies
            self.anomalies["athmosphere"] = random.sample(planet_config.ATMOSPHERIC_ANOMALIES, k=random.randint(1, 3))
            self.anomalies["terrain"] = random.sample(planet_config.TERRAIN_ANOMALIES, k=random.randint(1, 3))
            self.anomalies["underground"] = random.sample(planet_config.UNDERGROUND_ANOMALIES, k=random.randint(1, 3))

            self.heightmap = generate_heightmap(32, 64, self.surface_seed)

            
        print(f"\n{colors.BOLD}{colors.CYAN} ======================= Terrain  Scanner ====================={colors.RESET}")
        render_heightmap(self.heightmap)


        print(f"\n{colors.BOLD}{colors.CYAN}== Atmospheric Anomalies =={colors.RESET}")
        for anomaly in self.anomalies["athmosphere"]:
            print(f"  {colors.YELLOW}- {anomaly}{colors.RESET}")

        print(f"\n{colors.BOLD}{colors.CYAN}== Terrain Anomalies =={colors.RESET}")
        for anomaly in self.anomalies["terrain"]:
            print(f"  {colors.YELLOW}- {anomaly}{colors.RESET}")

        print(f"\n{colors.BOLD}{colors.CYAN}== Underground Anomalies =={colors.RESET}")
        for anomaly in self.anomalies["underground"]:
            print(f"  {colors.YELLOW}- {anomaly}{colors.RESET}")



