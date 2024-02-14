import pygame
from Button_class import Button
import sys


# Define constants
WIDTH = 1000
HEIGHT = 600
current_difficulty_index = 1


# Initialize pygame
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

def get_difficulty_fps(index):
    """
    Get the frames per second (FPS) based on the difficulty index.
    Args:
    - index: Integer representing the difficulty level index
    Returns:
    - Integer representing the FPS for the corresponding difficulty level
    """
    # Dictionary mapping difficulty index to FPS
    difficulty_fps = {
        0: 10,  # Easy
        1: 15,  # Normal
        2: 20   # Hard
    }
    # Default to Normal difficulty if index is out of range
    return difficulty_fps.get(index, 15)

# Main menu
# Load and scale the background image
BG = pygame.image.load("images/menu_background.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

# Function to load font with the specified size
def get_font(size):
    """
    Returns the 'Press-Start-2P' font with the desired size.

    Args:
    - size: Integer representing the font size
    """
    return pygame.font.Font("Fonts/Ninja.otf", size)

# Function to handle the fade-in effect
def fade_in(background):
    """
    Apply fade-in effect to the screen.

    Args:
    - background: Surface object representing the background image
    """
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    for alpha in range(255, 0, -10):  # Decrease alpha gradually
        fade_surface.set_alpha(alpha)
        SCREEN.blit(background, (0, 0))  # Draw background
        SCREEN.blit(fade_surface, (0, 0))  # Draw fade surface
        pygame.display.flip()
        pygame.time.delay(15)  # Adjust delay for smoothness

# Function to handle the options menu
def options(play_game_func):
    """
    Display the options menu and handle user interactions.
    """
    global FPS, current_difficulty_index
    difficulty_levels = ["Easy", "Normal", "Hard"]
    
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))  # Display background image
        
        # Display "OPTIONS" text
        OPTIONS_TEXT = get_font(100).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(530, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Display "Difficulty" text
        DIFFICULTY_TEXT = get_font(60).render("Difficulty", True, "black")
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(395, 300))
        SCREEN.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)

        # Initialize buttons for back, left arrow, right arrow, and difficulty level
        OPTIONS_BACK = Button(image=None, pos=(525, 400), 
                                text_input="BACK", font=get_font(75), base_color="black", hovering_color="#b68f40")
        OPTIONS_LEFT_ARROW = Button(image=None, pos=(555, 300), 
                                text_input="<", font=get_font(60), base_color="black", hovering_color="#b68f40")
        OPTIONS_RIGHT_ARROW = Button(image=None, pos=(810, 300), 
                                text_input=">", font=get_font(60), base_color="black", hovering_color="#b68f40")
        OPTIONS_DIFFICULTY = Button(image=None, pos=(685, 300), 
                                text_input=difficulty_levels[current_difficulty_index], font=get_font(65), base_color="black", hovering_color="black")

        # Update button appearance and check for mouse input
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS, transparency=False)
        OPTIONS_LEFT_ARROW.changeColor(OPTIONS_MOUSE_POS, transparency=False)
        OPTIONS_RIGHT_ARROW.changeColor(OPTIONS_MOUSE_POS, transparency=False)
        OPTIONS_DIFFICULTY.changeColor(OPTIONS_MOUSE_POS, transparency=False)

        # Update buttons on the screen
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_LEFT_ARROW.update(SCREEN)
        OPTIONS_RIGHT_ARROW.update(SCREEN)
        OPTIONS_DIFFICULTY.update(SCREEN)

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(play_game_func)
                elif OPTIONS_LEFT_ARROW.checkForInput(OPTIONS_MOUSE_POS):
                    current_difficulty_index = (current_difficulty_index - 1) % len(difficulty_levels)
                    FPS = get_difficulty_fps(current_difficulty_index)
                elif OPTIONS_RIGHT_ARROW.checkForInput(OPTIONS_MOUSE_POS):
                    current_difficulty_index = (current_difficulty_index + 1) % len(difficulty_levels)
                    FPS = get_difficulty_fps(current_difficulty_index)
        pygame.display.update()
        print(current_difficulty_index)
def main_menu(play_game_func):
    """
    Display the main menu and handle user interactions.
    """
    while True:
        # Display background image
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))

        # Define buttons for Play, Options, and Quit
        PLAY_BUTTON = Button(None, pos=(500, 225), 
                            text_input="PLAY", font=get_font(75), base_color="Black", hovering_color="#b68f40")
        OPTIONS_BUTTON = Button(None, pos=(500, 350), 
                            text_input="OPTIONS", font=get_font(75), base_color="Black", hovering_color="#b68f40")
        QUIT_BUTTON = Button(None, pos=(500, 475), 
                            text_input="QUIT", font=get_font(75), base_color="Black", hovering_color="#b68f40")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Update button colors and appearance
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS, transparency=False)
            button.update(SCREEN)
        
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle mouse click events for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_game_func(SCREEN)              
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(play_game_func)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        # Update and draw the main menu screen
        pygame.display.update()