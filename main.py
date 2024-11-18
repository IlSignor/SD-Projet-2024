#importations of the modulus and files
import pygame, sys
from pygame.locals import *
from definitions import*
from game import SpaceShooterGame

#################################       starting of the game         #############################################

pygame.init()                                   # Initialize Pygame.

pygame.display.set_caption('Space Shooter')            # Set the window title.

# Set up images.                            
character_images_selection = [                    # List of character images for the selection menu
    pygame.image.load('playersselection/player1.png'),
    pygame.image.load('playersselection/player2.png'),
    pygame.image.load('playersselection/player3.png'),
    pygame.image.load('playersselection/player4.png'),
    pygame.image.load('playersselection/player5.png'),
    pygame.image.load('playersselection/player6.png') 
]
character_images = [                             # List of character images.
    pygame.image.load('players/player1.png'),
    pygame.image.load('players/player2.png'),
    pygame.image.load('players/player3.png'),
    pygame.image.load('players/player4.png'),
    pygame.image.load('players/player5.png'),
    pygame.image.load('players/player6.png')
]

character_image_right = pygame.image.load('players/playersleft.png')                            # Character image for right rotations.

character_image_left = pygame.image.load('players/playersright.png')                             # Character image for left rotations.

comet_image = pygame.image.load('comet.png')                      # Load comet image.
health_item_image = pygame.transform.scale(pygame.image.load('live.png'),(25,25))    # Load heal image.

background_image = pygame.transform.scale(pygame.image.load('background.jpg').convert(),(WINDOWWIDTH, WINDOWHEIGHT))    # Load background image.

background_start = pygame.transform.scale(pygame.image.load('background_start.jpg').convert(),(WINDOWWIDTH, WINDOWHEIGHT))    # Load background start image.

RulesRect = pygame.Rect(0, 0, 50, 50)                               # Create a rectangle for the help button with width and height of 50
RulesRect.topright = (window_surface.get_width() - 20, 20)           # Position the button in the top-right corner with a 20-pixel margin

# Game rules text
rules_text = [                                              # List of rules for the game
    "Rules of the game :",
    "1   Avoid objects by moving",
    "2  Collect healing items to regain health",
    "3  Use the  arrows to control the player",
    "4  Use the spacebar to shoot bullets",
    "5  Press ESC to pause the game",
    "6  Try to survive as long as possible!"
]

# Surface for the rules window
rule_window = pygame.Surface((800, 360))                    # Create a surface with 800X360 pixels for the rules window
rule_window.fill((0, 0, 0))                           # Fill the rules window with a background color (white)
y_offset = 40                                               # Set initial vertical offset for displaying text within the rules window
for line in rules_text:                                     # Loop through each rule in the rules list
    basic.draw_text(line, small_font, rule_window, 20, y_offset)    # Use basic.draw_text function to render each rule line
    y_offset += 40                                          # Increment vertical offset for the next line of text

# Control variables
showing_rules = False                                       # Boolean flag to track if the rules window is currently being displayed
waiting = True                                              # Flag to keep the start menu running until the player starts the game

# Main loop for the start menu
while waiting:                                              # Loop until the player decides to start the game
    window_surface.blit(background_start, (0, 0))             # Display the background image

    # Display start game message
    basic.draw_text("Welcome to the Space Shooter", font, window_surface, window_surface.get_width() // 2  - (font.size("Welcome to the Space Shooter")[0] // 2), window_surface.get_height() // 2 + 180) 
    basic.draw_text("Press ENTER to start the game", font, window_surface, window_surface.get_width() // 2  - (font.size("Press ENTER to start the game")[0] // 2), window_surface.get_height() // 2 + 270)  # Render the start message in the center of the screen

    # Display the rules button
    basic.draw_button(RulesRect, '?', BUTTONCOLOR, BUTTONOVERCOLOR)  # Draw the "?" button to access the rules

    # If the rules should be shown, display the rules window
    if showing_rules:                                                       # Check if the rules window is active
        window_surface.blit(rule_window, (100, 220))                         # Display the rules window at position (100, 100)

    pygame.display.update()                                                 # Update the display to show all drawn elements

    # Event handling loop
    for event in pygame.event.get():                                # Loop through each event in the event queue
        if event.type == QUIT:                                      # If the quit event is triggered (user closes the window)
            pygame.quit()                                           # Quit Pygame
            sys.exit()                                              # Exit the program
        elif event.type == KEYDOWN:                                 # If a key is pressed down
            if event.key == K_RETURN or event.key == K_KP_ENTER:    # If the ENTER key is pressed
                waiting = False                                     # Exit the menu and start the game
            elif event.key == K_ESCAPE and showing_rules:           # If ESCAPE key is pressed while rules are showing
                showing_rules = False                               # Hide the rules window
        elif event.type == MOUSEBUTTONDOWN:                         # If a mouse button is clicked
            if RulesRect.collidepoint(event.pos):                   # Check if the click is within the rules button's rectangle
                showing_rules = not showing_rules                   # Toggle the display of the rules window

game_instance = SpaceShooterGame()  # Créer une instance de la classe
game_instance.start()               # Start the game.