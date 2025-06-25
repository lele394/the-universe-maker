import framework as fr

from framework.common import Colors 


# Red text green BG
print(Colors.RED +Colors.BG_BRIGHT_GREEN+ "Hi" + Colors.RESET)










from framework.objects import Planet, SolarSystem

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import json

def load_planet(data):
    return Planet(
        name=data.get("name", "Unnamed"),
        r_min=data.get("r_min", 1),
        r_max=data.get("r_max", 1),
        phi=data.get("phi", 0),
        theta=data.get("theta", 0),
        alpha=data.get("alpha", 0),
        start_phase=data.get("start_phase", 0.0),
        bound_objects=[load_planet(obj) for obj in data.get("bound_objects", [])]
    )

def load_solar_system_from_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    root = load_planet(data["root"])
    return SolarSystem(root=root, name=data.get("name", "Unnamed System"), creation_date=data.get("creation_date", 0.0))


# moon.plot_orbit()

solar_system = load_solar_system_from_json("solar_system.json")
solar_system.display(age=0.0)