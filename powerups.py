import pygame
from abc import ABC, abstractmethod
from constants import *
from class_tools import Vector2
from base_classes import *


class PowerUps(StaticObject):
    def __init__(self, pos: Vector2, height, width):
        super().__init__(pos, height, width)
        self.spawn_time = pygame.time.get_ticks()

    @abstractmethod
    def draw(self, screen):
        pass
    
    @abstractmethod
    def apply(self, charachter):
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

class FasterPowerUp(PowerUps):
    def __init__(self, pos, height, width):
        super().__init__(pos, height, width)

    def apply(self, charachter):
        charachter.max_speed *= 1.5

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 50, 50), (int(self.pos.x), int(self.pos.y)), POWERUP_HEIGHT)
        font = pygame.font.SysFont(None, 36)
        text = font.render("S", True, (255, 255, 255))
        rect = text.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(text, rect)

class HighJumpPowerUp(PowerUps):
    def __init__(self, pos, height, width):
        super().__init__(pos, height, width)

    def apply(self, charachter):
        charachter.jump_force *= 1.5

    def draw(self, screen):
        pygame.draw.circle(screen, (50, 50, 255), (int(self.pos.x), int(self.pos.y)), POWERUP_HEIGHT)
        font = pygame.font.SysFont(None, 36)
        text = font.render("J", True, (255, 255, 255))
        rect = text.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(text, rect)

class LongerBoostPowerUp(PowerUps):
    def __init__(self, pos, height, width):
        super().__init__(pos, height, width)

    def apply(self, charachter):
        charachter.boost_time *= 1.5

    def draw(self, screen):
        pygame.draw.circle(screen, (50, 200, 50), (int(self.pos.x), int(self.pos.y)), POWERUP_HEIGHT)
        font = pygame.font.SysFont(None, 36)
        text = font.render("B", True, (255, 255, 255))
        rect = text.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(text, rect)
