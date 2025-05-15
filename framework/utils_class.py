import math

class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def to_list(self):
        return [self.x, self.y, self.z]

    def norm(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def cos_angle_with(self, other):
        dot = self.dot(other)
        norms = self.norm() * other.norm()
        if norms == 0:
            raise ValueError("Cannot compute angle with zero-length vector")
        return max(-1.0, min(1.0, dot / norms))  # clip to avoid domain errors

    def angle_with(self, other, degrees=False):
        cos_theta = self.cos_angle_with(other)
        angle = math.acos(cos_theta)
        return math.degrees(angle) if degrees else angle
