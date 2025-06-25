#!/usr/bin/env python3
"""
generate_solar_system_json.py

Fetches orbital elements for the major Solar System bodies and some moons
from JPL Horizons, then writes out a nested JSON file.
"""

import json
import numpy as np
from astroquery.jplhorizons import Horizons

# --- Configuration ----------------------------------------------------------

# Epoch for which to pull the elements (J2000.0)
EPOCH = 2451545.0
KM_PER_AU = 149597870.7  # kilometers in one AU
# Horizons location code for the Sun
LOCATION = "@sun"

# Bodies: Horizons ID : (name, [list of moon IDs])
BODIES = {
    1:  ("Mercury",  []),
    2:  ("Venus",    []),
    3:  ("Earth",    [(301,   "Moon")]),
    4:  ("Mars",     [(401,   "Phobos"),
                      (402,   "Deimos")]),
    5:  ("Jupiter",  [(501,   "Io"),
                      (502,   "Europa"),
                      (503,   "Ganymede"),
                      (504,   "Callisto"),
                      (505,   "Amalthea"),
                      (506,   "Himalia"),
                      (507,   "Elara")]),
    6:  ("Saturn",   [(601,   "Titan"),
                      (602,   "Rhea"),
                      (603,   "Iapetus"),
                      (604,   "Dione"),
                      (605,   "Tethys"),
                      (606,   "Enceladus"),
                      (607,   "Mimas"),
                      (608,   "Hyperion"),
                      (609,   "Phoebe")]),
    7:  ("Uranus",   [(701,   "Titania"),
                      (702,   "Oberon"),
                      (703,   "Umbriel"),
                      (704,   "Ariel"),
                      (705,   "Miranda")]),
    8:  ("Neptune",  [(801,   "Triton"),
                      (802,   "Nereid")]),
    9:  ("Pluto",    [(901,   "Charon"),
                      (902,   "Nix"),
                      (903,   "Hydra"),
                      (904,   "Kerberos"),
                      (905,   "Styx")])
}


# Output path
OUTPUT_FILE = "solar_system.json"


# --- Helper functions -------------------------------------------------------

def fetch_elements(horizons_id):
    """Query JPL Horizons for one body and return the first elements row."""
    obj = Horizons(id=horizons_id, location=LOCATION, epochs=EPOCH)
    el = obj.elements()[0]  # astropy.table.Row
    return {
        "a":      float(el["a"]),      # semi-major axis (AU)
        "e":      float(el["e"]),      # eccentricity
        "inc":    float(el["incl"]),   # inclination (deg)
        "Omega":  float(el["Omega"]),  # longitude of ascending node (deg)
        "omega":  float(el["w"]),      # argument of perihelion (deg)
        "M":      float(el["M"])       # mean anomaly at epoch (deg)
    }

def make_planet_dict(horizons_id, name, moon_ids):
    """Build the dict for one planet, including its moons."""
    el = fetch_elements(horizons_id)
    # perihelion/aphelion
    r_min = el["a"] * (1 - el["e"])
    r_max = el["a"] * (1 + el["e"])
    # normalized start_phase
    start_phase = (el["M"] % 360) / 360.0

    # build children
    moons = []
    for mid, moon_name in moon_ids:
        mev = fetch_elements(mid)
        # convert satellite semi-major axis from km → AU:
        a_au = mev["a"] / KM_PER_AU
        r_min_m = a_au * (1 - mev["e"])
        r_max_m = a_au * (1 + mev["e"])
        moons.append({
            "name":        moon_name,
            "r_min":       r_min_m,
            "r_max":       r_max_m,
            "phi":         mev["inc"],
            "theta":       mev["Omega"],
            "alpha":       mev["omega"],
            "start_phase": (mev["M"] % 360) / 360.0,
            "bound_objects": []
        })

    return {
        "name":         name,
        "r_min":        r_min,
        "r_max":        r_max,
        "phi":          el["inc"],
        "theta":        el["Omega"],
        "alpha":        el["omega"],
        "start_phase":  start_phase,
        "bound_objects": moons
    }


# --- Main -------------------------------------------------------------------

def main():
    # Build root (Sun)
    system = {
        "name":           "Solar System",
        "creation_date":  EPOCH,
        "root": {
            "name":          "Sun",
            "r_min":         0.0,
            "r_max":         0.0,
            "phi":           0.0,
            "theta":         0.0,
            "alpha":         0.0,
            "start_phase":   0.0,
            "bound_objects": []
        }
    }

    # Fetch each planet and append
    for pid, (pname, moons) in BODIES.items():
        print(f"Fetching {pname} ({pid})…")
        planet_dict = make_planet_dict(pid, pname, moons)
        system["root"]["bound_objects"].append(planet_dict)

    # Write JSON
    with open(OUTPUT_FILE, "w") as fp:
        json.dump(system, fp, indent=2)
    print(f"Written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
