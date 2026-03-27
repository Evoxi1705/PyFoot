from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, pos):
        self.pos = pos

    @abstractmethod
    def draw(self, screen):
        pass