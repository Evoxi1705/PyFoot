import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# For testing purposes
class TempField:
    def get_top(self): return 0
    def get_bottom(self): return SCREEN_HEIGHT
    def get_left(self): return 0
    def get_right(self): return SCREEN_WIDTH

#field = [block_top_left, block_bottom_left, block_top_right, block_bottom_right]

field = TempField()

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