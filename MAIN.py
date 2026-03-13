import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Create a Rect object: (x, y, width, height)
player = pygame.Rect(50, 50, 64, 64)
velocity = 20

#Character Animation 
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

# Jumping variables
isJump = False
jumpCount = 10

left = False
right = False
walkCount = 0

# Defining a drawing function
def redrawgamewindow():
    global walkCount
    window.blit(bg, (0,0))
    pygame.draw.rect(window, (255, 0, 0), player)
    pygame.display.update()

run = True
while run:
    pygame.time.delay(30) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawgamewindow()
    
    keys = pygame.key.get_pressed()
    
    # Horizontal Movement with Boundary Checks
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= velocity
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
        player.x += velocity
        left = False
        right = True
    else:
        left = False
        right = False
        walkCount = 0

    # Vertical Movement and Jumping
    if not isJump:
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= velocity
        if keys[pygame.K_DOWN] and player.bottom < SCREEN_HEIGHT:
            player.y += velocity
        
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        # Jump Logic
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            player.y -= (jumpCount ** 2) / 2 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    # This ensures the player never stays outside the screen
    if player.left < 0: 
        player.left = 0
    if player.right > SCREEN_WIDTH: 
        player.right = SCREEN_WIDTH
    if player.top < 0: 
        player.top = 0
    if player.bottom > SCREEN_HEIGHT: 
        player.bottom = SCREEN_HEIGHT



pygame.quit()