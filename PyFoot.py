import pygame
from base_classes import *
from ball_class import *
from constants import *
from wall_class import *
from PyFoot_UI import show_menu

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class TempField:
    def get_top(self): return 0
    def get_bottom(self): return SCREEN_HEIGHT
    def get_left(self): return 0 + BW
    def get_right(self): return SCREEN_WIDTH - BW

field = TempField()

pygame.display.set_caption("Main Menu")

player = Player(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT), Vector2(0,0), 50, 100)
ball = Ball(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), Vector2(200,-300), 30)

difficulty = show_menu()

if difficulty == "Easy":
    level = EasyBot(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT), Vector2(0,0), 50, 100, player, ball)
if difficulty == "Medium":
    level = MediumBot(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT), Vector2(0,0), 50, 100, player, ball)
if difficulty == "Hard":
    level = HardBot(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT), Vector2(0,0), 50, 100, player, ball)

run = True
while run:
    dt = clock.tick(60) / 1000  # dt is roughly 0.016 at 60fps
    
    window.fill((0,0,0))
    level.draw(window)
    level.update(dt, field)
    level._handle_action(dt, field)

    ball.draw(window)
    ball.update(dt, field, triangles)
    #ball.bounce_player(player, field)


    player.draw(window)    
    player.update(dt, field)
    player._handle_inputs(dt, field)

    
    block_top_left.draw(window)
    block_bottom_left.draw(window)
    block_top_right.draw(window)
    block_bottom_right.draw(window)
    block_top.draw(window)
    block_bottom.draw(window)

    triangle_top_left.draw(window)
    triangle_bottom_left.draw(window)
    triangle_top_right.draw(window)
    triangle_bottom_right.draw(window)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()