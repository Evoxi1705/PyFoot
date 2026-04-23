import pygame

GRAVITY = 2000
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
JUMP_FORCE = 400
BOOST_FORCE = 300
MAX_SPEED = 500
MAX_BOOST_SPEED = 20
BOOST_TIME = 1000
WALL_COLOR = (255, 255, 255)
COOLDOWN = 4000
FRICTION = 0.95
ACCELERATION = 3000
PLAYER1_CONTROLS = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP, "boost": pygame.K_DOWN}
PLAYER2_CONTROLS = {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_s, "boost": pygame.K_w}