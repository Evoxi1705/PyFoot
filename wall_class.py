import pygame

class Wall:
    def __init__(self,x,y,width,height,color=(255,255,255), radius=20):
        self.rect = pygame.Rect(x, y, width, height) #door dit te gebruiken zal de botsing functie in ball_class makkelijker zijn
        self.color = color
        self.radius = radius #pas op deze moet kleiner zijn dan de helft van de korste zijde van de muur
        
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius = self.radius)
        


