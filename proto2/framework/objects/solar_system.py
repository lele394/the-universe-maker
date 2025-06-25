import numpy as np
import matplotlib.pyplot as plt

class SolarSystem:
    def __init__(self, root, name="Unnamed System", creation_date=0.0):
        self.root = root
        self.name = name
        self.creation_date = creation_date

    def _display_recursive(self, planet, ax, age, center):
        # Plot orbit around current center
        planet.orbit = planet._generate_orbit()
        orbit = planet.orbit + np.array(center).reshape(3, 1)
        ax.plot(orbit[0], orbit[1], orbit[2], label=planet.name)

        # Plot body at current position
        position = planet.get_position(age) + center
        ax.scatter(*position, label=f"{planet.name}", s=20)

        # Recurse for moons/children
        for child in planet.bound_objects:
            self._display_recursive(child, ax, age, position)

    def display(self, age=0.0):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        self._display_recursive(self.root, ax, age, center=np.zeros(3))

        ax.set_title(f"Solar System: {self.name} (Age = {age:.2f})")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        
        # ======= Remove distortions ======
        # Get all axis limits
        x_limits = ax.get_xlim()
        y_limits = ax.get_ylim()
        z_limits = ax.get_zlim()

        # Find the overall range
        x_range = x_limits[1] - x_limits[0]
        y_range = y_limits[1] - y_limits[0]
        z_range = z_limits[1] - z_limits[0]
        max_range = max(x_range, y_range, z_range)

        # Compute center
        x_middle = np.mean(x_limits)
        y_middle = np.mean(y_limits)
        z_middle = np.mean(z_limits)

        # Set all axis limits to be centered and span the same range
        ax.set_xlim(x_middle - max_range / 2, x_middle + max_range / 2)
        ax.set_ylim(y_middle - max_range / 2, y_middle + max_range / 2)
        ax.set_zlim(z_middle - max_range / 2, z_middle + max_range / 2)

        # Now force equal aspect
        ax.set_box_aspect([1, 1, 1])


        ax.legend()
        plt.show()
