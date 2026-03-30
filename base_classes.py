from abc import ABC, abstractmethod
from constants import GRAVITY
from class_tools import Vector2


class Entity(ABC):
    """
    Abstract base class for all objects that exist in the game world.
    
    Attributes:
        pos: position of the object
    """
    def __init__(self, pos):
        self.pos = pos

    @abstractmethod
    def draw(self, screen):
        """Drawing the objects."""
        pass

class DynamicObject(Entity):
    """
    Class for all dynamic objects in the game world.
    """
    def __init__(self, pos, velocity):
        super().__init__(pos)
        self.velocity = Vector2(velocity)

    def update(self):
        """Updating the position of the object."""
        self.apply_gravity()
        self.pos += self.velocity

    def apply_gravity(self):
        """Applying gravity to the object."""
        self.velocity.y += GRAVITY

    @abstractmethod
    def draw(self, screen):
        """Drawing the objects."""
        pass

class StaticObject(Entity):
    """
    Abstract base class for all static objects in the game world.
    """
    def __init__(self, pos):
        super().__init__(pos)
    
    @abstractmethod
    def draw(self, screen):
        """Drawing the objects."""
        pass

class Character(DynamicObject):
    def __init__(self, pos, velocity, jump_force, boost_force, boost_remaining, max_speed):
        super().__init__(pos, velocity)
        self.jump_force = jump_force
        self.boost_force = boost_force
        self.boost_remaining = boost_remaining
        self.max_speed = max_speed

    def jump(self):
        pass

    def boost(self):
        pass