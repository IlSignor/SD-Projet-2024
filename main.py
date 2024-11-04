#importations of the modulus and files
import pygame, sys
from pygame.locals import *
from definition import*

#################################       Start function defintions         #############################################

def start():                                      # Function to start the game.
    # Show the "Start" screen.
    windowSurface.blit(backgroundImage, (0, 0))  # Display background image at the top left.

    pygame.display.update()                       # Update the display.

    topScore = 0                                  # Initialize top score.

    # Show character selection menu.
    playerFirstRect = characterImages[1].get_rect()  # Get rectangle for first character image.
    
    selectedCharacterIndex = showCharacterSelectionMenu(windowSurface, characterImages, font, playerFirstRect)  # Display character selection.
    playerImage = characterImages[selectedCharacterIndex]  # Set player image based on selection.
    playerRect = playerImage.get_rect()            # Get the rectangle for the player.

    smallPlayerImage = pygame.transform.scale(playerImage, (30, 30))  # Scale down player image for display.
    smallPlayerImageGray = pygame.Surface((30, 30))  # Create a surface for the gray version.
    smallPlayerImageGray.blit(smallPlayerImage, (0, 0))  # Copy small player image to gray surface.
    smallPlayerImageGray.set_alpha(100)              # Set transparency for gray image.

    windowSurface.blit(backgroundImage, (0, 0))  # Display background image at the top left.

    heal_animation = HealAnimation(playerRect.center)  # Create healing animation object.
    fire_animation = FireAnimation()                    # Create fire animation object.

    difficulty = showDifficultyMenu(windowSurface)  # Show difficulty menu.
    if difficulty == 'easy':                          # If difficulty is easy:
        BADDIEMINSPEED = 1                            # Set minimum baddie speed.
        BADDIEMAXSPEED = 4                            # Set maximum baddie speed.
        ADDNEWBADDIERATE = 12                         # Set rate of adding new baddies.
        HEALTHHAPPEND = 100                           # Set health item appearance rate.
    elif difficulty == 'medium':                      # If difficulty is medium:
        BADDIEMINSPEED = 2                            # Set minimum baddie speed.
        BADDIEMAXSPEED = 6                            # Set maximum baddie speed.
        ADDNEWBADDIERATE = 8                          # Set rate of adding new baddies.
        HEALTHHAPPEND = 1000                          # Set health item appearance rate.
    elif difficulty == 'hard':                        # If difficulty is hard:
        BADDIEMINSPEED = 4                            # Set minimum baddie speed.
        BADDIEMAXSPEED = 8                            # Set maximum baddie speed.
        ADDNEWBADDIERATE = 6                          # Set rate of adding new baddies.
        HEALTHHAPPEND = 10000                         # Set health item appearance rate.

    windowSurface.blit(backgroundImage, (0, 0))  # Display background image at the top left.

    from game import game                            # Import game function.
    game(HEALTHHAPPEND, heal_animation, fire_animation, playerRect, bullets, windowSurface, ADDNEWBADDIERATE, BADDIEMINSPEED, BADDIEMAXSPEED, baddieImage, healthItems, healthItemImage, backgroundImage, font, smallPlayerImage, smallPlayerImageGray, playerImage, explosions, gameOverSound, topScore)  # Start the game.


#################################       Initialization and starting of the game         #############################################

pygame.init()                                   # Initialize Pygame.

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))  # Set up the window size.

pygame.display.set_caption('Dodger')            # Set the window title.

# Set up the fonts.
pygame.font.init()
# Initialize font module.
font_path = "SpaceAge.ttf"                       # Load the font path.
font = pygame.font.Font(font_path, 40)           # Load the main font.
smallFont = pygame.font.Font(font_path, 30)      # Load a smaller font.

bullets = []                                    # List to hold bullets.
healthItems = []                                # List to hold health items.
explosions = []                                 # List to hold explosions.

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')  # Load game over sound.
pygame.mixer.music.load('background.mid')      # Load background music.

# Set up images.
characterImages = [                             # List of character images.
    pygame.image.load('players/player1.png'),
    pygame.image.load('players/player2.png'),
    pygame.image.load('players/player3.png'),
    pygame.image.load('players/player4.png'),
    pygame.image.load('players/player5.png'),
    pygame.image.load('players/player6.png')
]

baddieImage = pygame.image.load('baddie.png')                      # Load baddie image.
healthItemImage = pygame.image.load('cherry.png')                  # Load health item image.

backgroundImage = pygame.image.load('background.jpg').convert()    # Load background image.

RulesRect = pygame.Rect(0, 0, 50, 50)                               # Create a rectangle for the help button with width and height of 50
RulesRect.topright = (windowSurface.get_width() - 20, 20)           # Position the button in the top-right corner with a 20-pixel margin

# Game rules text
rules_text = [                                              # List of rules for the game
    "Règles du jeu Dodger :",
    "1. Évitez les ennemis en vous déplaçant.",
    "2. Ramassez les objets de soin pour regagner de la vie.",
    "3. Utilisez les flèches pour contrôler le personnage.",
    "4. Essayez de survivre aussi longtemps que possible!"
]

# Surface for the rules window
rule_window = pygame.Surface((600, 400))                    # Create a surface with 600x400 pixels for the rules window
rule_window.fill((50, 50, 50))                              # Fill the rules window with a background color (dark gray)
y_offset = 50                                               # Set initial vertical offset for displaying text within the rules window
for line in rules_text:                                     # Loop through each rule in the rules list
    drawText(line, smallFont, rule_window, 20, y_offset)    # Use drawText function to render each rule line
    y_offset += 40                                          # Increment vertical offset for the next line of text

# Control variables
showing_rules = False                                       # Boolean flag to track if the rules window is currently being displayed
waiting = True                                              # Flag to keep the start menu running until the player starts the game

# Main loop for the start menu
while waiting:                                              # Loop until the player decides to start the game
    windowSurface.blit(backgroundImage, (0, 0))             # Display the background image

    # Display start game message
    drawText("Pressez ENTER pour lancer le jeu", font, windowSurface, windowSurface.get_width() // 2  - (font.size("Pressez ENTER pour lancer le jeu")[0] // 2), windowSurface.get_height() // 2)  # Render the start message in the center of the screen

    # Display the rules button
    drawButton(windowSurface, RulesRect, '?', (0, 0, 0), (100, 100, 100))  # Draw the "?" button to access the rules

    # If the rules should be shown, display the rules window
    if showing_rules:                                                       # Check if the rules window is active
        windowSurface.blit(rule_window, (100, 100))                         # Display the rules window at position (100, 100)

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


start()                                                             # Start the game.
