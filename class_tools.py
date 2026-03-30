import math

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    # Defines how the vector looks when printed: print(v)
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    # Addition: v1 + v2
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    # Subtraction: v1 - v2
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    # Multiplication (Scaling): v1 * 5
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    # Length of the vector (Magnitude)
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    # Normalization (Scaling to a length of 1)
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return self * (1 / mag)
    
    # Makes the vector readable as a sequence for pygame
    # In things like pygame.draw.circle(surface, color, center, radius) pygame will try to iterate over center for example
    # Iter and yield respond with "First, here is the x. Second, here is the y."
    def __iter__(self):
        yield self.x
        yield self.y

    # Makes the += operator work properply
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self  