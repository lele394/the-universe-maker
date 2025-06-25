
import numpy as np
import matplotlib.pyplot as plt

class Planet:
    def __init__(self, name="Unnamed", r_min=1, r_max=1, phi=0, theta=0, alpha=0, bound_objects=None, start_phase=0.0):
        
        r_max = r_max if r_max > 1e-10 else 1e-10 # To avoid div/0
        r_min = r_min if r_min > 1e-10 else 1e-10 # To avoid div/0
        
        self.name = name
        self.r_min = r_min 
        self.r_max = r_max 
        self.a = (r_min + r_max) / 2
        self.e = (r_max - r_min) / (r_max + r_min)
        self.b = self.a * np.sqrt(1 - self.e**2)

        self.phi = np.radians(phi)
        self.theta = np.radians(theta)
        self.alpha = np.radians(alpha)

        self.orbit = None
        self.bound_objects = bound_objects or []

        self.start_phase = start_phase % 1.0  # Fraction along orbit (0=start, 1=full cycle)


    def _generate_orbit(self, num_points=500):
        # Parametric ellipse in 2D (x = a cos, y = b sin), centered at one focus
        t = np.linspace(0, 2 * np.pi, num_points)
        x = self.a * np.cos(t) - self.a * self.e
        y = self.b * np.sin(t)
        z = np.zeros_like(t)
        orbit = np.stack([x, y, z], axis=0)

        # Apply composite rotation: Rx(phi) -> Ry(theta) -> Rz(alpha)
        R = self._rotation_matrix_z(self.alpha) @ self._rotation_matrix_y(self.theta) @ self._rotation_matrix_x(self.phi)
        orbit = R @ orbit
        return orbit

    def _rotation_matrix_x(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[1, 0, 0],
                         [0, c, -s],
                         [0, s, c]])

    def _rotation_matrix_y(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[c, 0, s],
                         [0, 1, 0],
                         [-s, 0, c]])

    def _rotation_matrix_z(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[c, -s, 0],
                         [s, c, 0],
                         [0, 0, 1]])



    def get_position(self, age):
        t = 2 * np.pi * ((age + self.start_phase) % 1.0)
        x = self.a * np.cos(t) - self.a * self.e
        y = self.b * np.sin(t)
        z = 0.0
        pos = np.array([x, y, z])

        # Same rotation order
        R = self._rotation_matrix_z(self.alpha) @ self._rotation_matrix_y(self.theta) @ self._rotation_matrix_x(self.phi)
        return R @ pos



    def plot_orbit(self, ax=None, show=True, color='blue', label=None, center=(0, 0, 0)):
        self.orbit = self._generate_orbit()
        
        # Translate orbit to new center
        center = np.asarray(center).reshape(3, 1)
        translated_orbit = self.orbit + center

        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        
        ax.plot(translated_orbit[0], translated_orbit[1], translated_orbit[2], color=color, label=label)
        # ax.scatter(*center, color='orange', label='Orbit Center')  # central object
        
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Planet Orbit in 3D")
        ax.set_box_aspect([1,1,1])
        
        if label or show:
            ax.legend()
        if show:
            plt.show()
