import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Create a Rect object: (x, y, width, height)
player = pygame.Rect(50, 50, 64, 64)
velocity = 20

run = True
while run:
    pygame.time.delay(30) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()