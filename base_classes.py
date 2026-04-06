from abc import ABC, abstractmethod
from constants import SCREEN_HEIGHT, JUMP_FORCE, BOOST_FORCE, BOOST_TIME, MAX_SPEED, GRAVITY
from class_tools import Vector2


class Entity(ABC):
    """
    Abstract base class for all objects that exist in the game world.
    
    Attributes:
        pos: position of the object
    """
    pos: Vector2 # Attribute hint: helps the editor remember what type it was
    height: int
    width: int

    def __init__(self, pos: Vector2, height: int, width: int):
        self.pos = pos
        self.height = height
        self.width = width

    @abstractmethod
    def draw(self, screen):
        """Drawing the objects."""
        pass

class DynamicObject(Entity):
    """
    Class for all dynamic objects in the game world.
    """
    velocity: Vector2

    def __init__(self, pos: Vector2, height, width, velocity: Vector2):
        super().__init__(pos, height, width)
        self.velocity = velocity

    def update(self):
        """Updating the position of the object."""
        self.apply_gravity()
        self.pos += self.velocity

        # Preventing the object to go "through" the floor or to be "stuck" to it 
        if self.pos.y + self.height > SCREEN_HEIGHT:
            self.pos.y = SCREEN_HEIGHT - self.height 
            self.velocity.y = 0 

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
    def __init__(self, pos: Vector2, height, width):
        super().__init__(pos, height, width)
    
    @abstractmethod
    def draw(self, screen):
        """Drawing the objects."""
        pass

class Character(DynamicObject):
    """ 
    Base class for all characters in the game world.
    
    Attributes:
        jump_force: the power of the jump of a character
        boost_force: the power of the boost of a character
        boost_remaining: the boost a character has left (in seconds)
        max_speed: the maximum speed a character can attain (in pixel per second)
    """
    def __init__(self, 
                 pos: Vector2, 
                 velocity: Vector2,
                 height, 
                 width, 
                 jump_force=JUMP_FORCE, 
                 boost_force=BOOST_FORCE, 
                 boost_time=BOOST_TIME, 
                 max_speed=MAX_SPEED):
        
        super().__init__(pos, velocity, height, width)
        self.jump_force = jump_force
        self.boost_force = boost_force
        self.boost_time = boost_time
        self.max_speed = max_speed

    def boost(self):
        # need to create a part where you decelerate 
        # think about the time boosted
        # think about the cooldown
        while time_boosted < self.boost_time:
            while self.velocity.x < self.max_speed:
                self.velocity.x += self.boost_force
            self.velocity.x = self.max_speed


    def jump(self):
        """Ability for a character to jump."""
        if self.pos.y + self.height >= SCREEN_HEIGHT:
            self.velocity.y = -self.jump_force
