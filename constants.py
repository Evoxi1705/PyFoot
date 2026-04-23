import pygame

GRAVITY = 2000
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
JUMP_FORCE = 1000
BOOST_FORCE = 300
MAX_SPEED = 500
MAX_BOOST_SPEED = 3000
BOOST_TIME = 3000
WALL_COLOR = (255, 255, 255)
COOLDOWN = 5000
FRICTION = 0.95
ACCELERATION = 3000
PLAYER1_CONTROLS = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP, "boost": pygame.K_DOWN}
PLAYER2_CONTROLS = {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_s, "boost": pygame.K_w}
DELAY_EASYBOT = 10
BOT_SIDE = 1 # -1 for left, 1 for right
BOUNCE_FACTOR = 3