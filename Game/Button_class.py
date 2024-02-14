import pygame
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