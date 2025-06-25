
class planet:

    ATMOSPHERIC_ANOMALIES = [
        "High altitude winds",
        "Perpetual lightning storms",
        "Toxic cloud layers",
        "Radioactive fog",
        "Aurora storms",
        "Magnetic field inversion",
        "Supercooled jet streams",
        "Acid rain",
        "Invisible atmosphere (light-bending gases)",
        "Supersonic wind tunnels",
        "Atmospheric plasma arcs",
        "Anti-gravity turbulence",
        "Floating ice crystals",
        "Localized firestorms",
        "Cryogenic vapor flows",
        "Volcanic gas haze",
        "Electrical vortexes",
        "Photosensitive dust storms",
        "Organic spore clouds",
        "Methane monsoons",
        "Blackout storms (EM disruption)"
    ]


    TERRAIN_ANOMALIES = [
        "Sand planet",
        "Shifting landmasses",
        "Crystal growth fields",
        "Magnetized rock plains",
        "Lava lakes",
        "Living terrain (biological surface)",
        "Bone deserts (fossil remains)",
        "Active tectonic fault zones",
        "Mirror-smooth rock formations",
        "Ultradense gravity wells",
        "Color-changing soil",
        "Cactus forests with silicon spines",
        "Geothermal geyser fields",
        "Salt flat mirage zones",
        "Frozen lightning scars",
        "Radioactive boulder fields",
        "Metallic dunes",
        "Tectonic breathing zones",
        "Alien monolith ruins",
        "Acoustic canyons (resonant stone)",
        "Hovering rock islands"
    ]


    UNDERGROUND_ANOMALIES = [
        "Underground oceans",
        "Hollow planetary core",
        "Subsurface fungal networks",
        "Thermal crystal caverns",
        "Ancient alien tunnels",
        "Volatile gas pockets",
        "Living cave systems",
        "Superconductive ore veins",
        "Bioluminescent cavern walls",
        "Dark matter sinkholes",
        "Magnetic cave mazes",
        "Sentient crystal formations",
        "Glowing geothermal rivers",
        "Prehistoric DNA vaults",
        "Petrified underground forests",
        "Resonant mineral chambers",
        "Shifting subterranean corridors",
        "Toxic mineral sludge",
        "Time-warp chambers",
        "Corrosive acid springs",
        "Silicon-based fossil beds"
    ]






    color_scheme_dic = {

        "earth" : [
            (0.05, 17),    # Deep water - dark blue
            (0.15, 19),    # Water - blue
            (0.25, 33),    # Shore - cyan-ish
            (0.35, 71),    # Lowland - greenish
            (0.45, 142),   # Plains - light green
            (0.55, 181),   # Hills - yellow-green
            (0.65, 179),   # Foothills - yellow
            (0.75, 214),   # Mountains - orange
            (0.85, 223),   # High peaks - light orange/pink
            (1.00, 231)    # Ice caps - bright white
        ],

        "lava" : [
            (0.05, 52),    # Cold dark - deep red
            (0.15, 88),    # Dark red
            (0.25, 124),   # Red-orange
            (0.35, 160),   # Orange
            (0.45, 166),   # Bright orange
            (0.55, 172),   # Light orange
            (0.65, 178),   # Yellow-orange
            (0.75, 184),   # Yellow
            (0.85, 220),   # Bright yellow
            (1.00, 229)    # White hot
        ],

        "toxic" : [
            (0.05, 54),    # Very dark purple
            (0.15, 55),    # Dark purple
            (0.25, 56),    # Purple
            (0.35, 71),    # Greenish teal
            (0.45, 83),    # Green
            (0.55, 85),    # Bright green
            (0.65, 118),   # Lime green
            (0.75, 154),   # Yellow-green
            (0.85, 190),   # Light green
            (1.00, 229)    # Pale yellow
        ],

        "desert" : [
            (0.05, 94),    # Dark brown
            (0.15, 130),   # Brown
            (0.25, 136),   # Light brown
            (0.35, 172),   # Sandy orange
            (0.45, 178),   # Yellow-orange
            (0.55, 214),   # Orange
            (0.65, 220),   # Light orange
            (0.75, 223),   # Peach
            (0.85, 229),   # Light tan
            (1.00, 231)    # Bright white (hot sun glare)
        ],

        "ice" : [
            (0.05, 17),    # Dark blue
            (0.15, 18),    # Deep blue
            (0.25, 19),    # Blue
            (0.35, 37),    # Light blue
            (0.45, 39),    # Ice blue
            (0.55, 45),    # Pale cyan
            (0.65, 123),   # Pale turquoise
            (0.75, 159),   # Pale aqua
            (0.85, 195),   # Near white blue
            (1.00, 231)    # Bright white (snow/ice cap)
        ]



    }




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