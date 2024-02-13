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

#Menu
#Define button class
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        # Initialize button attributes
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        # Update button appearance
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        # Check if the button is clicked
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position, transparency):
        # Check if the button is clicked
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            if transparency:
                self.image.set_alpha(175)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.image.set_alpha(255)

BG = pygame.image.load("images/menu_background.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Fonts/Ninja.otf", size)

# Function to handle the fade-in effect
def fade_in(background):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    for alpha in range(255, 0, -10):  # Decrease alpha gradually
        fade_surface.set_alpha(alpha)
        SCREEN.blit(background, (0, 0))  # Draw background
        SCREEN.blit(fade_surface, (0, 0))  # Draw fade surface
        pygame.display.flip()
        pygame.time.delay(15)  # Adjust delay for smoothness

current_difficulty_index = 1  
def options():
    global FPS,current_difficulty_index
    difficulty_levels = ["Easy", "Normal", "Hard"]
    while True:

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(100).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(550, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)


        DIFFICULTY_TEXT = get_font(60).render( "Difficulty", True, ("black"))
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(395, 300))
        SCREEN.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)

        OPTIONS_BACK = Button(image=None, pos=(525, 400), 
                            text_input="BACK", font=get_font(75), base_color="black", hovering_color="#b68f40")

        OPTIONS_LEFT_ARROW = Button(image=None, pos=(555, 300), 
                            text_input="<", font=get_font(60), base_color="black", hovering_color="#b68f40")

        OPTIONS_RIGHT_ARROW = Button(image=None, pos=(810, 300), 
                            text_input=">", font=get_font(60), base_color="black", hovering_color="#b68f40")

        OPTIONS_DIFFICULTY = Button(image=None, pos=(685, 300), 
                            text_input=difficulty_levels[current_difficulty_index], font=get_font(65), base_color="black", hovering_color="black")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS, transparency=False)
        OPTIONS_LEFT_ARROW.changeColor(OPTIONS_MOUSE_POS, transparency=False)
        OPTIONS_RIGHT_ARROW.changeColor(OPTIONS_MOUSE_POS, transparency=False)
        OPTIONS_DIFFICULTY.changeColor(OPTIONS_MOUSE_POS, transparency=False)

        OPTIONS_BACK.update(SCREEN)
        OPTIONS_LEFT_ARROW.update(SCREEN)
        OPTIONS_RIGHT_ARROW.update(SCREEN)
        OPTIONS_DIFFICULTY.update(SCREEN)

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

def get_difficulty_fps(index):
    difficulty_fps = {
        0: 10,  # Easy
        1: 15,  # Normal
        2: 20   # Hard
    }
    return difficulty_fps.get(index, 15)  # Default to Normal difficulty if index is out of range


# Define functions for menu and gameplay
def main_menu():

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))

        PLAY_BUTTON = Button(None, pos=(500, 225), 
                            text_input="PLAY", font=get_font(75), base_color="Black", hovering_color="#b68f40")
        OPTIONS_BUTTON = Button(None, pos=(500, 350), 
                            text_input="OPTIONS", font=get_font(75), base_color="Black", hovering_color="#b68f40")
        QUIT_BUTTON = Button(None, pos=(500, 475), 
                            text_input="QUIT", font=get_font(75), base_color="Black", hovering_color="#b68f40")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS, transparency=False)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle mouse click events for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_game(SCREEN,current_difficulty_index)              
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        # Update and draw the main menu screen
        pygame.display.update()

#The main part of the game 
def play_game(SCREEN,current_game_difficulty): 

    #initializing useful variables
    global player_lives,game_over,score
    player_lives=3
    score = 0
    fruits = ["pear", "orange", "apple", "strawberry","passionfruit", "lemon", "guava", "kiwi", "peach", "bomb"]  
    background = pygame.image.load("images/Wood_backgroud.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT)) 

    fade_in(background)

    pygame.display.set_caption("SLICE STORM")
    clock = pygame.time.Clock()

    BLACK = (0,0,0)

    Pause_Icon = pygame.image.load("images/Pause_Icon.png")
    Pause_Icon = pygame.transform.scale(Pause_Icon, (150, 110)) 

    Cut_Icon = pygame.image.load("images/Knife.png")
    Cut_Icon = pygame.transform.scale(Cut_Icon, (55, 55))

    Fruits_logo = pygame.image.load("images/Fruit_logo.png")
    Fruits_logo = pygame.transform.scale(Fruits_logo, (85, 85))

    font = pygame.font.Font(os.path.join(os.getcwd(), ("Fonts/Normal.ttf")), 25)
    score_text = font.render( str(score), True, (BLACK))
    score_text = pygame.transform.scale(score_text, (50, 50))

    Heart_Icon = pygame.image.load("images/Lives_Icon.png")
    Heart_Icon = pygame.transform.scale(Heart_Icon, (80, 80))
     

    def draw_lives(display, x, y, lives, image) :
        for i in range(lives) :
            img_rect = image.get_rect()      
            img_rect.x = int(x + 55 * i)   
            img_rect.y = y                 
            display.blit(image, img_rect)

    def hide_lives(x, y):
        SCREEN.blit(Heart_Icon, (x, y))
    data = {}

    # Define function for loading an image
    def load_image(filename):
        image = pygame.image.load(filename)
        return image

    # Define function for scaling an image
    def scale_image(image, size):
        return pygame.transform.scale(image, size)

    # Define function for generating random fruits
    def generate_random_fruits(fruits):
        random.shuffle(fruits)  # Shuffle the list of fruits
        fruit_type = random.choice(fruits)
        fruit_name = fruit_type + str(random.randint(0, 10000000000))
        fruit = ""
        for char in fruit_name :
            if char.isalpha():
                fruit+=char
        img = load_image("images/" + fruit + ".png")
        img = scale_image(img, (130, 130))
        fruit_data = {
            "image": img,
            "x": random.randint(200, WIDTH - 200),
            "y": HEIGHT - 75  ,
            "speed_x": random.randint(-15, 15),
            "speed_y": random.randint(-40, -20),
            "hit": False,
        }
        data[fruit_name] = fruit_data

    # Define function for updating fruit positions
    def update_fruit_positions(data, height):
        global player_lives,game_over
        fruits_to_remove = []  # Create a list to store fruits to remove
        for fruit in list(data.keys()):
            fruit_data = data[fruit]
            fruit_data["x"] += fruit_data["speed_x"]
            if fruit_data["speed_y"] < 0 and fruit_data["hit"]==True :
                fruit_data["y"] -= fruit_data["speed_y"]
                fruit_data["speed_y"] -= 1.50 
            elif fruit_data["speed_y"] >= 0 and fruit_data["hit"]==True :
                fruit_data["y"] += fruit_data["speed_y"]
                fruit_data["speed_y"] += 1.50 
            elif fruit_data["speed_y"] < 800 and fruit_data["hit"]!=True :  # If the fruit is moving up
                fruit_data["y"] += fruit_data["speed_y"]
                fruit_data["speed_y"] += 1.5 # Add a small positive value to reverse direction

                

                 
            fruit_name = ""
            for char in fruit:
                if char.isalpha():
                    fruit_name+=char
            # Check if fruit has gone off the screen
            if (fruit_data["y"] > height + 50 or WIDTH +  100 < fruit_data["x"] or -100 > fruit_data["x"] ) and fruit_name!= "bomb" :
                if fruit_data["hit"] != True:
                    player_lives -=1
                    hide_lives(800,0)

                if player_lives <= 0:
                    game_over = True # Set game over flag if no lives left
                    return  
                generate_random_fruits(fruits)
                fruits_to_remove.append(fruit)
        for fruit in fruits_to_remove:
            del data[fruit]


    # Define function for checking for collisions


    def check_collisions(data, x, y, Cut_Icon, range):
        global player_lives,score
        for fruit_name, fruit_data in data.items():
            if not fruit_data["hit"]:
                # Create a mask for the Cut_Icon surface
                Cut_Icon_mask = pygame.mask.from_surface(Cut_Icon)
                # Calculate the distance between the Cut_Icon and the fruit
                fruit_mask = pygame.mask.from_surface(fruit_data["image"])
                distance = pygame.math.Vector2(x - fruit_data["x"], y - fruit_data["y"]).length()
                if distance <= range:
                    # Use the masks for collision detection
                    collision = fruit_mask.overlap(Cut_Icon_mask, (x - fruit_data["x"], y - fruit_data["y"]))
                    if collision:
                        fruit_name2 = ""
                        for char in fruit_name:
                            if char.isalpha():
                                fruit_name2+=char
                        if fruit_name2 == "bomb":
                            explosion = load_image("images/explosion.png")
                            explosion = scale_image(explosion, (900, 700))
                            hide_lives(5000,0) 
                            # Blit the explosion image onto the screen at the bomb's position
                            SCREEN.blit(explosion, (50, 0))
                            pygame.display.flip()  # Update the display to show the explosion
                            # Introduce a delay to make the explosion visible
                            pygame.time.delay(1500)  # Delay for 1500 milliseconds (1.5 second)
                            return True
                        else:
                            score += 1
                            fruit_data["hit"] = True
        return False
    # Define function for rendering game state
    def render_game_state(screen, data, width,score, height, lives):
        for fruit in data:
            fruit_data = data[fruit]
            if not fruit_data["hit"]:
                screen.blit(fruit_data["image"], (fruit_data["x"], fruit_data["y"]))
            else:
                fruit_name = ""
                for char in fruit:
                    if char.isalpha():
                        fruit_name+=char
                if fruit_name!="bomb":
                    sliced_fruits_left = load_image("images/half_" + fruit_name + ".png")
                    sliced_fruits_right = pygame.transform.flip(sliced_fruits_left, True, False)  # Flip the left half image horizontally

                    # Calculate positions for left and right halves
                    left_half_x = fruit_data["x"] - sliced_fruits_left.get_width() / 2
                    right_half_x = fruit_data["x"] + 50

                    #Scale the to be a little bit smaleler for less chaos
                    sliced_fruits_left = scale_image(sliced_fruits_left, (75, 75))
                    sliced_fruits_right = scale_image(sliced_fruits_right, (75, 75))

                    # Calculate the new y-coordinate for the sliced halves
                    sliced_y = fruit_data["y"]  # Adjust as needed

                    # Render the left and right halves
                    screen.blit(sliced_fruits_left, (left_half_x, sliced_y))
                    screen.blit(sliced_fruits_right, (right_half_x, sliced_y))
        screen.blit(score_text,(100,19))

    def game_over_screen(score):
        while True:
            SCREEN.fill("black")

            GAME_OVER_TEXT = get_font(125).render("Game Over", True, "#b68f40")
            GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 5))
            SCREEN.blit(GAME_OVER_TEXT, GAME_OVER_RECT)

            # Display the score on the game over screen
            SCORE_TEXT = get_font(70).render(f"Score: {score}", True, "white")
            SCORE_RECT = SCORE_TEXT.get_rect(center=(WIDTH // 2, HEIGHT // 2.65))
            SCREEN.blit(SCORE_TEXT, SCORE_RECT)

            RESTART_BUTTON = Button(image=None, pos=(WIDTH // 2, HEIGHT // 1.75), 
                                text_input="Restart", font=get_font(70), base_color="White", hovering_color="#b68f40")
            BACK_BUTTON = Button(None, pos=(WIDTH // 2, HEIGHT // 1.35), 
                                text_input="BACK", font=get_font(70), base_color="White", hovering_color="#b68f40")
            

            RESTART_BUTTON.changeColor(pygame.mouse.get_pos(),transparency= False)
            RESTART_BUTTON.update(SCREEN)

            BACK_BUTTON.changeColor(pygame.mouse.get_pos(),transparency= False)
            BACK_BUTTON.update(SCREEN)            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESTART_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        play_game(SCREEN)  # Return from the function to restart the game
                    if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                         main_menu()

            pygame.display.update()
         


    # Initialize fruit data
    generate_random_fruits(fruits)

    RESUME_BUTTON = Button(None, pos=(WIDTH // 2, HEIGHT // 2 - 50), 
                    text_input="RESUME", font=get_font(50), base_color="White", hovering_color="#b68f40")
    QUIT_BUTTON = Button(None, pos=(WIDTH // 2, HEIGHT // 2 + 50), 
                    text_input="QUIT", font=get_font(50), base_color="White", hovering_color="#b68f40")
    

    SCORE_THRESHOLD = 5  # Score threshold to increase difficulty

    is_paused = False  
    game_over = False        
    game_running = True
    mouse_held = False   
    while game_running and not game_over:
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(Fruits_logo, (20, 0))
        draw_lives(SCREEN, 800, 0, player_lives, Heart_Icon)

        PAUSE_BUTTON = Button(Pause_Icon, pos=( WIDTH - 35, HEIGHT - 35 ), 
                text_input= None, font=get_font(120), base_color= "Black", hovering_color="#b68f40")
        PAUSE_BUTTON.changeColor(pygame.mouse.get_pos(), transparency = True)
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
                mouse_held= False

        # Check if the game is paused
        while is_paused:

                        # Blit the game elements first
            SCREEN.blit(background, (0, 0))
            SCREEN.blit(Fruits_logo, (20, 0))
            draw_lives(SCREEN, 800, 0, player_lives, Heart_Icon)
            # Display pause menu and handle events
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
                        pygame.quit()
                        sys.exit()

        # Check for slicing only if the game is not paused
        if mouse_held and not is_paused:
            mouse_position = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_position  
            SCREEN.blit(Cut_Icon, mouse_position)     
            collision_detected = check_collisions(data, mouse_x, mouse_y, Cut_Icon, 100)
            if collision_detected:
                game_running = False
                game_over = True

        global current_difficulty_index
        FPS = get_difficulty_fps(current_difficulty_index)

        NEW_FRUIT_PROBABILITY = 1 
        if score >= SCORE_THRESHOLD:
            FPS+=0.25
            NEW_FRUIT_PROBABILITY+=0.30
            SCORE_THRESHOLD += 5  # Increase the score threshold for the next difficulty level
            if score % 25 == 0:
                fruits.append("bomb")

        if random.randint(0,70) < NEW_FRUIT_PROBABILITY :
        # Generate a new random fruit
            generate_random_fruits(fruits)

        score_text = font.render(str(score), True, (BLACK))
        score_text = pygame.transform.smoothscale(score_text, (35, 55))

        # Update fruit positions
        update_fruit_positions(data, HEIGHT)

        # Render game state
        render_game_state(SCREEN, data, WIDTH, HEIGHT, score, player_lives)

        if game_over:
            game_over_screen(score)
        pygame.display.flip()
        clock.tick(FPS)


# Main function
def main():


    # Run the main menu
    main_menu()

    # After the main menu, start the game loop
    play_game(SCREEN)

    pygame.quit()

if __name__ == "__main__":
    main()