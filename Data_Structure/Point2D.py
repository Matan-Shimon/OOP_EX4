class Point2D:

    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def setPoint(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z

    def __str__(self) -> str:
        return f"X = {self.x} Y={self.y} Z = {self.z}"

    def __repr__(self) -> str:
        return f"X = {self.x} Y={self.y} Z = {self.z}"