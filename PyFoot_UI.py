import pygame_gui
import pygame
from constants import *

pygame.init()

def show_menu():
    """
    Initializes and manages the main menu graphical user interface.

    Handles the rendering of the background image, title text, and interactive 
    difficulty buttons using pygame_gui. The function enters a local event loop 
    and blocks execution until a difficulty selection is made or the window is closed.

    Returns:
        str: The selected difficulty level ("Easy", "Medium", or "Hard").
        None: If the game loop is terminated (e.g., window closed) without a selection.

    Note:
        This function creates its own pygame.display surface and UIManager instance,
        leveraging "UI_theme.json" for widget styling.
    """
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "UI_theme.json")

    # Buttons
    easy_button_rect = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, 2*SCREEN_HEIGHT/6 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)
    medium_button_rect = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, 3*SCREEN_HEIGHT/6 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)
    hard_button_rect = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, 4*SCREEN_HEIGHT/6 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)
    tutorial_button_rect = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, 5*SCREEN_HEIGHT/6 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)

    easy_button = pygame_gui.elements.UIButton(easy_button_rect, "EASY", manager)
    medium_button = pygame_gui.elements.UIButton(medium_button_rect, "MEDIUM", manager)
    hard_button = pygame_gui.elements.UIButton(hard_button_rect, "HARD", manager)
    tutorial_button = pygame_gui.elements.UIButton(tutorial_button_rect, "TUTORIAL", manager)


    # Game loop
    clock = pygame.time.Clock()
    run = True

    while run:

        window.fill((255, 255, 255))
        dt = clock.tick(60) / 1000 
        manager.update(dt)

        font = pygame.font.SysFont("Arial", 80, bold=True)
        title_surface = font.render("PyFoot", True, (255, 0, 0))
        window.blit(title_surface, (SCREEN_WIDTH/2 - title_surface.get_width()/2, SCREEN_HEIGHT/8)) 

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
                if event.ui_element == tutorial_button:
                    return "tutorial"
            
        manager.draw_ui(window)

        pygame.display.flip()
    pygame.quit()


def show_end_screen(player_score, bot_score):
    """
    Displays the end screen with the result and final score.

    Returns:
        str: "menu" if the player clicks Back to Main Menu, "quit" if they click Quit.
    """
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "UI_theme.json")

    # Buttons
    menu_button_rect = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, 3*SCREEN_HEIGHT/5 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_button_rect = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, 4*SCREEN_HEIGHT/5 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)
   

    menu_button = pygame_gui.elements.UIButton(menu_button_rect, "MAIN MENU", manager)
    quit_button = pygame_gui.elements.UIButton(quit_button_rect, "QUIT", manager)
    
    result_text = "You won!" if player_score > bot_score else "You lost!" if bot_score > player_score else "Draw!"

    # Game loop
    clock = pygame.time.Clock()
    run = True

    while run:

        window.fill((255, 255, 255))
        dt = clock.tick(60) / 1000
        manager.update(dt)

        font_big = pygame.font.SysFont("Arial", 80, bold=True)
        font_score = pygame.font.SysFont("Arial", 50)

        result_surface = font_big.render(result_text, True, (255, 0, 0))
        score_surface = font_score.render(f"{player_score}  -  {bot_score}", True, (255, 0, 0))

        window.blit(result_surface, (SCREEN_WIDTH/2 - result_surface.get_width()/2, SCREEN_HEIGHT/5))
        window.blit(score_surface, (SCREEN_WIDTH/2 - score_surface.get_width()/2, SCREEN_HEIGHT/3))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_START_PRESS:
                if event.ui_element == menu_button:
                    return "menu"
                if event.ui_element == quit_button:
                    return "quit"

        manager.draw_ui(window)

        pygame.display.flip()

def show_tutorial():
    """
    Displays the tutorial of the game.

    Returns:
        str: "menu" if the player clicks Back to Main Menu.
    """
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "UI_theme.json")

    # Menu button
    menu_button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) - BUTTON_HEIGHT/2, 1.5*BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
    menu_button = pygame_gui.elements.UIButton(menu_button_rect, "MAIN MENU", manager)

    # Turorial image
    background = pygame.transform.scale(pygame.image.load("media/tutorial.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Game loop
    clock = pygame.time.Clock()
    run = True

    while run:

        window.fill((255, 255, 255))
        dt = clock.tick(60) / 1000 
        manager.update(dt)

        window.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_START_PRESS:
                if event.ui_element == menu_button:
                    return "menu"
            
        manager.draw_ui(window)

        pygame.display.flip()
    pygame.quit()