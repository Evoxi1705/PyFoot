import pygame_gui
import pygame
from constants import *

pygame.init()

def show_menu():
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "UI_theme.json")

    # Background
    bg = pygame.image.load("Rocket League Sideswipe Season 24.webp")
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Title
    # title_rect = pygame.Rect(SCREEN_WIDTH/2 - TEXT_WIDTH/2, SCREEN_HEIGHT/5 - BUTTON_HEIGHT/2, TEXT_WIDTH, TEXT_HEIGHT)
    # title = pygame_gui.elements.UILabel(title_rect, "PyFoot", manager, object_id="#main_title")

    # Buttons
    easy_button_rect = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, 2*SCREEN_HEIGHT/5 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)
    medium_button_rect = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, 3*SCREEN_HEIGHT/5 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)
    hard_button_rect = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, 4*SCREEN_HEIGHT/5 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)

    easy_button = pygame_gui.elements.UIButton(easy_button_rect, "EASY", manager)
    medium_button = pygame_gui.elements.UIButton(medium_button_rect, "MEDIUM", manager)
    hard_button = pygame_gui.elements.UIButton(hard_button_rect, "HARD", manager)

    # Game loop
    clock = pygame.time.Clock()
    run = True

    while run:

        window.fill((250,250,250))
        window.blit(bg, (0,0))
        dt = clock.tick(60) / 1000 
        manager.update(dt)

        font = pygame.font.SysFont("Arial", 80, bold=True)
        title_surface = font.render("PyFoot", True, (0, 71, 255))
        window.blit(title_surface, (SCREEN_WIDTH/2 - title_surface.get_width()/2, SCREEN_HEIGHT/7)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_START_PRESS:
                if event.ui_element == easy_button:
                    return "Easy"
                if event.ui_element == medium_button:
                    return "Medium"
                if event.ui_element == hard_button:
                    return "Hard"
            
        manager.draw_ui(window)

        pygame.display.flip()
    pygame.quit()

show_menu()
