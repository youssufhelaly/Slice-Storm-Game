import pygame
import sys
import os
import random
import pygame.math

# Define constants
WIDTH = 1000
HEIGHT = 600

# Initialize pygame
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

# Menu
# Define button class
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        Initialize a button object.

        Args:
        - image: Surface object for button background (can be None)
        - pos: Tuple (x, y) for button position
        - text_input: Text to be displayed on the button
        - font: Font object for the button text
        - base_color: Base color of the button text
        - hovering_color: Color of the button text when hovering over it
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Update the appearance of the button on the screen.

        Args:
        - screen: Surface object representing the game screen
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """
        Check if the button is clicked.

        Args:
        - position: Tuple (x, y) representing the mouse position
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position, transparency):
        """
        Change the color of the button when hovering over it.

        Args:
        - position: Tuple (x, y) representing the mouse position
        - transparency: Boolean indicating whether to apply transparency to the button background
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            if transparency:
                self.image.set_alpha(175)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.image.set_alpha(255)
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
def options():
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
                    main_menu()
                elif OPTIONS_LEFT_ARROW.checkForInput(OPTIONS_MOUSE_POS):
                    current_difficulty_index = (current_difficulty_index - 1) % len(difficulty_levels)
                    FPS = get_difficulty_fps(current_difficulty_index)
                elif OPTIONS_RIGHT_ARROW.checkForInput(OPTIONS_MOUSE_POS):
                    current_difficulty_index = (current_difficulty_index + 1) % len(difficulty_levels)
                    FPS = get_difficulty_fps(current_difficulty_index)

        pygame.display.update()

# Global variable for the current difficulty index
current_difficulty_index = 1  

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

def main_menu():
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
                    play_game(SCREEN)              
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        # Update and draw the main menu screen
        pygame.display.update()

#The main part of the game 
def play_game(SCREEN): 
    """
    Main game loop where the actual gameplay takes place.

    Parameters:
    - SCREEN (pygame.Surface): The main surface for displaying game elements.

    Returns:
    - None
    """
    #initializing useful variables
    global player_lives,game_over,score
    player_lives=3
    score = 0
    fruits = ["pear", "orange", "apple", "strawberry","passionfruit", "lemon", "guava", "kiwi", "peach", "bomb"]  
    background = pygame.image.load("images/Wood_backgroud.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT)) 

    #Smoothing the transition between the main menu and the game
    fade_in(background) 

    # Name of the game
    pygame.display.set_caption("SLICE STORM")
    clock = pygame.time.Clock()

    BLACK = (0,0,0)

    #Define the pause icon
    Pause_Icon = pygame.image.load("images/Pause_Icon.png")
    Pause_Icon = pygame.transform.scale(Pause_Icon, (150, 110)) 

    #Define the knife when clicking
    Cut_Icon = pygame.image.load("images/Knife.png")
    Cut_Icon = pygame.transform.scale(Cut_Icon, (55, 55))

    #Define the Fruit Logo beside the score
    Fruits_logo = pygame.image.load("images/Fruit_logo.png")
    Fruits_logo = pygame.transform.scale(Fruits_logo, (85, 85))

    #Define the score
    font = pygame.font.Font(os.path.join(os.getcwd(), ("Fonts/Normal.ttf")), 25)
    score_text = font.render( str(score), True, (BLACK))
    score_text = pygame.transform.scale(score_text, (50, 50))

    #Define the Heart Lives
    Heart_Icon = pygame.image.load("images/Lives_Icon.png")
    Heart_Icon = pygame.transform.scale(Heart_Icon, (80, 80))
     
    def draw_lives(display, x, y, lives, image) :
        """
        Draw player lives on the screen.

        Args:
        - display: Pygame screen object to display the lives
        - x: x-coordinate for the lives display
        - y: y-coordinate for the lives display
        - lives: Number of lives to display
        - image: Image object for the lives
        """
        for i in range(lives) :
            img_rect = image.get_rect()      
            img_rect.x = int(x + 55 * i)   
            img_rect.y = y                 
            display.blit(image, img_rect)

    def hide_lives(x, y):
        """
        Hide player lives on the screen.

        Args:
        - x: x-coordinate for the lives display
        - y: y-coordinate for the lives display
        """
        SCREEN.blit(Heart_Icon, (x, y))


    # Define function for loading an image
    def load_image(filename):
        """
        Load an image file.

        Args:
        - filename: Name of the image file to load

        Returns:
        - Image object loaded from the file
        """
        image = pygame.image.load(filename)
        return image
    
    # Define function for scaling an image
    def scale_image(image, size):
        return pygame.transform.scale(image, size)
    
    #Initializing a dictionnary called data that will store the different details about fruits
    data = {}
    def generate_random_fruits(fruits):
        """
        Generate a random fruit object.

        Args:
        - fruits: List of fruit names

        Returns:
        - Dictionary containing the fruit data
        """
        random.shuffle(fruits)  # Shuffle the list of fruits 
        fruit_type = random.choice(fruits)
        fruit_name = fruit_type + str(random.randint(0, 10000000000)) # To make every fruit unique
        fruit = ""
        for char in fruit_name:
            if char.isalpha():
                fruit += char
        img = load_image("images/" + fruit + ".png")
        img = scale_image(img, (130, 130))
        #Different details about the fruit
        fruit_data = {
            "image": img,
            "x": random.randint(200, WIDTH - 200),
            "y": HEIGHT - 75,
            "speed_x": random.randint(-15, 15),
            "speed_y": random.randint(-40, -20),
            "hit": False,
        }
        data[fruit_name] = fruit_data

    def update_fruit_positions(data, height):
        """
        Update the positions of fruits and handle collisions.

        Args:
        - data: Dictionary containing fruit data
        - height: Height of the game screen

        Returns:
        - None
        """
        global player_lives, game_over
        fruits_to_remove = []  # Create a list to store fruits to remove
        
        for fruit in list(data.keys()):
            # Handle horizontal movement
            fruit_data = data[fruit]
            fruit_data["x"] += fruit_data["speed_x"]

            # Handle vertical movement
            # When hit and going up this statement ensures that the fruit immediately starts going down to avoid chaos  
            if fruit_data["speed_y"] < 0 and fruit_data["hit"] == True:
                fruit_data["y"] -= fruit_data["speed_y"]
                fruit_data["speed_y"] -= 1.50 

            # When hit and going down this elif statement ensures the fruit continues going down   
            elif fruit_data["speed_y"] >= 0 and fruit_data["hit"] == True:
                fruit_data["y"] += fruit_data["speed_y"]
                fruit_data["speed_y"] += 1.50 
            
            #When ghoing up add a small value to continue to go up until the treshhold or the speed changes signs
            elif fruit_data["speed_y"] < 800 and fruit_data["hit"] != True:
                fruit_data["y"] += fruit_data["speed_y"]
                fruit_data["speed_y"] += 1.5  # Add a small positive value to reverse direction

            # Because fruit is not only the name of the fruit but also the random number in front of it
            fruit_name = "".join(char for char in fruit if char.isalpha())

            # Check if fruit has gone off the screen
            if (fruit_data["y"] > height + 50 or WIDTH + 100 < fruit_data["x"] or -100 > fruit_data["x"]) and fruit_name != "bomb":
                if fruit_data["hit"] != True:
                    player_lives -= 1
                    hide_lives(800, 0)

                if player_lives <= 0:
                    game_over = True  # Set game over flag if no lives left
                    return  
                generate_random_fruits(fruits)

                fruits_to_remove.append(fruit)

        # Remove fruits that have gone off the screen to avoid memory overflow and to not reuse them 
        for fruit in fruits_to_remove:
            del data[fruit]

    def check_collisions(data, x, y, Cut_Icon, range):
        """
        Check for collisions between the knife and fruits.

        Parameters:
        - data (dict): Dictionary containing information about each fruit.
        - x (int): X-coordinate of the knife.
        - y (int): Y-coordinate of the knife.
        - Cut_Icon (Surface): Surface representing the knife image.
        - range (int): Range within which collisions are detected.

        Returns:
        - bool: True if a bomb explosion occurs, False otherwise.
        """

        global player_lives, score

        for fruit_name, fruit_data in data.items():
            if not fruit_data["hit"]:
                # Create a mask for the Cut_Icon surface
                Cut_Icon_mask = pygame.mask.from_surface(Cut_Icon)

                # Calculate the distance between the knife and the fruit
                fruit_mask = pygame.mask.from_surface(fruit_data["image"])
                distance = pygame.math.Vector2(x - fruit_data["x"], y - fruit_data["y"]).length()

                # Check if the distance is within the specified range
                if distance <= range:
                    # Use masks for collision detection
                    collision = fruit_mask.overlap(Cut_Icon_mask, (x - fruit_data["x"], y - fruit_data["y"]))
                    
                    # If collision occurs
                    if collision:
                        fruit_name = "".join(char for char in fruit_name if char.isalpha())
                        
                        # Check if the collided fruit is a bomb
                        if fruit_name == "bomb":
                            # Trigger an explosion animation
                            explosion = load_image("images/explosion.png")
                            explosion = scale_image(explosion, (900, 700))
                            hide_lives(5000, 0)  # Hide the player lives indicator
                            SCREEN.blit(explosion, (50, 0))  # Blit explosion image
                            pygame.display.flip()  # Update display to show explosion
                            pygame.time.delay(1500)  # Delay to make explosion visible
                            return True
                        else:
                            # Increment score and mark the fruit as hit
                            score += 1
                            fruit_data["hit"] = True
                            
        return False

    def render_game_state(SCREEN, data):
        """
        Render the game state including fruits and their sliced halves.

        Parameters:
        - screen (Surface): The screen surface to render on.
        - data (dict): Dictionary containing information about each fruit.
        - width (int): Width of the game window.
        - score (int): Player's current score.
        - height (int): Height of the game window.
        - lives (int): Number of lives remaining.

        Returns:
        - None
        """

        # Iterate over each fruit in the data dictionary
        for fruit in data:
            fruit_data = data[fruit]
            
            # Check if the fruit is not hit
            if not fruit_data["hit"]:
                # Render the original fruit image
                SCREEN.blit(fruit_data["image"], (fruit_data["x"], fruit_data["y"]))
            else:
                # Extract the alphabetic characters from the fruit name
                fruit_name = "".join(char for char in fruit if char.isalpha())
                
                # Check if the fruit is not a bomb
                if fruit_name != "bomb":
                    # Load the left and right halves of the sliced fruit image
                    sliced_fruits_left = load_image("images/half_" + fruit_name + ".png")
                    sliced_fruits_right = pygame.transform.flip(sliced_fruits_left, True, False)  # Flip the left half image horizontally

                    # Calculate positions for left and right halves to avoid chaos
                    left_half_x = fruit_data["x"] - sliced_fruits_left.get_width() / 2
                    right_half_x = fruit_data["x"] + 50  # Adjust as needed

                    # Scale the sliced fruit images to a smaller size
                    sliced_fruits_left = scale_image(sliced_fruits_left, (75, 75))
                    sliced_fruits_right = scale_image(sliced_fruits_right, (75, 75))

                    # Calculate the y-coordinate for the sliced halves
                    sliced_y = fruit_data["y"]  # Adjust as needed

                    # Render the left and right halves of the sliced fruit
                    SCREEN.blit(sliced_fruits_left, (left_half_x, sliced_y))
                    SCREEN.blit(sliced_fruits_right, (right_half_x, sliced_y))

        # Render the score text on the screen
        SCREEN.blit(score_text, (100, 19))

    def game_over_screen(score):
        """
        Display the game over screen with the final score and options to restart or return to the main menu.

        Parameters:
        - score (int): The player's final score.

        Returns:
        - None
        """

        while True:
            SCREEN.fill("black")

            # Render "Game Over" text
            GAME_OVER_TEXT = get_font(125).render("Game Over", True, "#b68f40")
            GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 5))
            SCREEN.blit(GAME_OVER_TEXT, GAME_OVER_RECT)

            # Display the player's score on the game over screen
            SCORE_TEXT = get_font(70).render(f"Score: {score}", True, "white")
            SCORE_RECT = SCORE_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 2.65))
            SCREEN.blit(SCORE_TEXT, SCORE_RECT)

            # Create restart and back buttons
            RESTART_BUTTON = Button(image=None, pos=(WIDTH // 2, HEIGHT // 1.75), 
                                    text_input="Restart", font=get_font(70), base_color="White", hovering_color="#b68f40")
            BACK_BUTTON = Button(None, pos=(WIDTH // 2, HEIGHT // 1.35), 
                                    text_input="BACK", font=get_font(70), base_color="White", hovering_color="#b68f40")

            # Change button color when hovering
            RESTART_BUTTON.changeColor(pygame.mouse.get_pos(), transparency=False)
            RESTART_BUTTON.update(SCREEN)

            BACK_BUTTON.changeColor(pygame.mouse.get_pos(), transparency=False)
            BACK_BUTTON.update(SCREEN)            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Restart the game if the restart button is clicked
                    if RESTART_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        play_game(SCREEN)  # Return from the function to restart the game
                    # Return to the main menu if the back button is clicked
                    if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        main_menu()

            pygame.display.update()

# Initialize fruit data
    generate_random_fruits(fruits)

    # Initialize buttons for pause menu
    RESUME_BUTTON = Button(None, pos=(WIDTH // 2, HEIGHT // 2 - 50), 
                    text_input="RESUME", font=get_font(50), base_color="White", hovering_color="#b68f40")
    QUIT_BUTTON = Button(None, pos=(WIDTH // 2, HEIGHT // 2 + 50), 
                    text_input="QUIT", font=get_font(50), base_color="White", hovering_color="#b68f40")
    
    SCORE_THRESHOLD = 5  # Score threshold to increase difficulty
    
    # Initializing Important variables
    is_paused = False   
    game_over = False        
    game_running = True
    mouse_held = False   

    while game_running and not game_over:

        #Position the different elements    
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(Fruits_logo, (20, 0))

        draw_lives(SCREEN, 800, 0, player_lives, Heart_Icon)

        score_text = font.render(str(score), True, (BLACK))
        score_text = pygame.transform.smoothscale(score_text, (35, 55))

        # Pause button
        PAUSE_BUTTON = Button(Pause_Icon, pos=( WIDTH - 35, HEIGHT - 35 ), 
                text_input= None, font=get_font(120), base_color= "Black", hovering_color="#b68f40")
        PAUSE_BUTTON.changeColor(pygame.mouse.get_pos(), transparency=True)
        PAUSE_BUTTON.update(SCREEN)

        # Handle game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_held = True
                if PAUSE_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    is_paused = True  # Pause the game
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_held = False

        # Check if the game is paused
        while is_paused:

            # Replacing the different elements otherwise black screen
            SCREEN.blit(background, (0, 0))
            SCREEN.blit(Fruits_logo, (20, 0))
            SCREEN.blit(score_text, (100, 19))
            draw_lives(SCREEN, 800, 0, player_lives, Heart_Icon)

            #Make sure the fruits are still there
            render_game_state(SCREEN, data)

            # Create semi-transparent overlay surface
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Fill with black and set alpha to 128 for semi-transparency
            SCREEN.blit(overlay, (0, 0))  # Blit the overlay onto the screen

            # Create the resume and quit buttons once when the game is paused
            RESUME_BUTTON.changeColor(pygame.mouse.get_pos(), transparency=False)
            QUIT_BUTTON.changeColor(pygame.mouse.get_pos(), transparency=False)
            RESUME_BUTTON.update(SCREEN)
            QUIT_BUTTON.update(SCREEN)
            pygame.display.update()   

            for pause_event in pygame.event.get():
                if pause_event.type == pygame.MOUSEBUTTONDOWN and pause_event.button == 1:
                    # Handle pause menu button clicks
                    if RESUME_BUTTON.checkForInput(pause_event.pos):
                        is_paused = False  # Resume the game
                    elif QUIT_BUTTON.checkForInput(pause_event.pos):
                        main_menu()

        # Check for slicing only if the game is not paused
        if mouse_held and not is_paused:
            mouse_position = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_position  
            SCREEN.blit(Cut_Icon, mouse_position) # Putting knife image when clicking     
            collision_detected = check_collisions(data, mouse_x, mouse_y, Cut_Icon, 100)
            if collision_detected:
                game_running = False
                game_over = True

        global current_difficulty_index
        FPS = get_difficulty_fps(current_difficulty_index)
        NEW_FRUIT_PROBABILITY = 1 

        # Increase difficulty based on score
        if score >= SCORE_THRESHOLD:
            FPS += 0.25
            NEW_FRUIT_PROBABILITY += 0.30
            SCORE_THRESHOLD += 5  # Increase the score threshold for the next difficulty level
            if score % 25 == 0:
                fruits.append("bomb")

        # Generate new fruits randomly
        if random.randint(0, 70) < NEW_FRUIT_PROBABILITY:
            generate_random_fruits(fruits)


        # Update fruit positions
        update_fruit_positions(data, HEIGHT)

        # Render game state
        render_game_state(SCREEN, data)

        if game_over:
            game_over_screen(score)
        pygame.display.flip()
        clock.tick(FPS)


# Main function
def main():
    """
    Main function that starts the game.
    It runs the main menu and then starts the game loop.

    Parameters:
    - None

    Returns:
    - None
    """

    # Run the main menu
    main_menu()

    # After the main menu, start the game loop
    play_game(SCREEN)

    pygame.quit()


if __name__ == "__main__":
    main()