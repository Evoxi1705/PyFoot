import pygame
from abc import ABC, abstractmethod
from constants import *
from class_tools import Vector2
from base_classes import *


class PowerUps(StaticObject):
    """
    Abstract base class for collectible items that modify character attributes.

    Provides a foundation for temporary or permanent stat modifiers, tracking
    spawn time for potential expiration logic.

    Attributes:
        spawn_time (int): The timestamp (in ms) when the object was created.
    """
    def __init__(self, pos: Vector2, height, width):
        super().__init__(pos, height, width)
        self.spawn_time = pygame.time.get_ticks()

    @abstractmethod
    def draw(self, screen):
        """
        Renders the power-up icon to the provided Pygame surface.

        Args:
            screen (pygame.Surface): The destination surface for drawing.
        """
        pass

    def check_collected(self, character):
        cx = self.pos.x
        cy = self.pos.y
    
        closest_x = max(character.pos.x, min(cx, character.pos.x + character.width))
        closest_y = max(character.pos.y, min(cy, character.pos.y + character.height))
    
        dx = cx - closest_x
        dy = cy - closest_y
        distance = (dx**2 + dy**2) ** 0.5
        
        if distance <= POWERUP_HEIGHT:
            self.apply(character)
            return True
        return False
    
    @abstractmethod
    def apply(self, character):
        """
        Modifies the state or attributes of the target character.

        Args:
            charachter (BaseCharacter): The character instance to receive the buff.
        """
        pass

class FasterPowerUp(PowerUps):
    """A speed-enhancing collectible that increases movement velocity."""
    def __init__(self, pos, height, width):
        super().__init__(pos, height, width)
        self.image = pygame.image.load("jump powerup.png")
        self.image = pygame.transform.scale(self.image, (POWERUP_HEIGHT*2, POWERUP_HEIGHT*2))

    def apply(self, character):
        """Increases the character's max_speed by a 1.5x multiplier."""
        character.speed_base = character.max_speed
        character.max_speed *= 1.5
        character.faster_collected = pygame.time.get_ticks()

    def draw(self, screen):
        """Draws the powerup as a circle"""
        screen.blit(self.image, (self.pos.x - POWERUP_HEIGHT, self.pos.y - POWERUP_HEIGHT))

class HighJumpPowerUp(PowerUps):
    """A verticality collectible that enhances jumping capability."""
    def __init__(self, pos, height, width):
        super().__init__(pos, height, width)
        self.image = pygame.image.load("jump powerup.png")
        self.image = pygame.transform.scale(self.image, (POWERUP_HEIGHT*2, POWERUP_HEIGHT*2))

    def apply(self, character):
        """Increases the character's jump_force by a 1.5x multiplier."""
        character.jump_base = character.jump_force
        character.jump_force *= 1.5
        character.highjump_collected = pygame.time.get_ticks()

    def draw(self, screen):
        """Draws the powerup as a circle"""
        screen.blit(self.image, (self.pos.x - POWERUP_HEIGHT, self.pos.y - POWERUP_HEIGHT))
        
class LongerBoostPowerUp(PowerUps):
    """An endurance collectible that extends the duration of the boost state."""
    def __init__(self, pos, height, width):
        super().__init__(pos, height, width)
        self.image = pygame.image.load("jump powerup.png")
        self.image = pygame.transform.scale(self.image, (POWERUP_HEIGHT*2, POWERUP_HEIGHT*2))

    def apply(self, character):
        """Increases the character's boost_time duration by a 1.5x multiplier."""
        character.boost_base = character.boost_time
        character.boost_time *= 1.5
        character.longerboost_collected = pygame.time.get_ticks()

    def draw(self, screen):
        """Draws the powerup as a circle"""
        screen.blit(self.image, (self.pos.x - POWERUP_HEIGHT, self.pos.y - POWERUP_HEIGHT))