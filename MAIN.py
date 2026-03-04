import pygame

pygame.init()

window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Main Menu")

#character attributes
x = 50
y = 50
WIDTH, HEIGHT = 40, 30
velocity = 5

#game loop
run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        if x == 0:
            continue
        else:
            x -= velocity

    if keys[pygame.K_RIGHT]:
        if x == 1000:
            continue
        else:
            x += velocity

    if keys[pygame.K_UP]:
        if y == 0:
            continue
        else:
            y -= velocity

    if keys[pygame.K_DOWN]:
        if y == 800:
            continue
        else:
            y += velocity

    window.fill((255, 255, 255))
    pygame.draw.rect(window, (255, 0, 0), (x, y, WIDTH, HEIGHT))
    pygame.display.update()

pygame.quit()

#test change