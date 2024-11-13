#importations of the modulus and files
import pygame, sys
from pygame.locals import *
from classes import*

# Configuration of the window size
WINDOWWIDTH = 1000
WINDOWHEIGHT = 800

TEXTCOLOR = (0, 0, 0)                           # Color for text
BUTTONTEXTCOLOR = (255, 255, 255)               # Color for button text

BADDIEMINSIZE = 10                               # Minimum size for baddies
BADDIEMAXSIZE = 40                               # Maximum size for baddies
PLAYERMOVERATE = 5                               # Player movement speed

FPS = 60                                         # Frames per second
mainClock = pygame.time.Clock()                  # Clock for controlling the frame rate

#################################       Basic defintions         #############################################

def terminate():                                  # Function to terminate the game
    pygame.quit()                                 # Quit Pygame
    sys.exit()                                    # Exit the program

def draw_text(text, font, surface, x, y):         # Function to draw text on the surface
    textobj = font.render(text, 1, TEXTCOLOR)    # Render the text
    textrect = textobj.get_rect()                 # Get the rectangular area of the text
    textrect.topleft = (x, y)                     # Set the position of the text
    surface.blit(textobj, textrect)               # Blit the text onto the surface

def draw_button(windowSurface, buttonRect, text, color, hoverColor): # Function to draw a button
    mousePos = pygame.mouse.get_pos()             # Get the position of the mouse
    # Change button color if mouse is over it
    if buttonRect.collidepoint(mousePos):          # Check if mouse is over button
        pygame.draw.rect(windowSurface, hoverColor, buttonRect, border_radius=10) # Draw hover color
    else:
        pygame.draw.rect(windowSurface, color, buttonRect, border_radius=10) # Draw normal color
    font_path = "SpaceAge.ttf"
    buttonFont = pygame.font.Font(font_path, 40)     # Define button font
    textSurf = buttonFont.render(text, True, BUTTONTEXTCOLOR) # Render button text
    textRect = textSurf.get_rect(center=buttonRect.center) # Get text rect centered in button
    windowSurface.blit(textSurf, textRect)          # Blit the text onto the button

#################################       Explosions and bullets defintions         #############################################

def trigger_explosion(explosions, position):       # Function to trigger an explosion
    explosion_sound = pygame.mixer.Sound('sounds/explosion.mp3')            # Add explosion sound
    explosion_sound.play()
    explosions.append(Explosion(position))         # Add explosion at the specified position

def shoot(playerRect, bullets):                    # Function to shoot a bullet
    bullet = pygame.Rect(playerRect.centerx - 2, playerRect.top - 10, 5, 10) # Create a bullet
    shots_sound = pygame.mixer.Sound('sounds/laser_shot.mp3')             # Add explosion sound
    shots_sound.play()
    bullets.append(bullet)                         # Add bullet to the list

def move_bullets(bullets):                         # Function to move bullets
    for bullet in bullets[:]:                      # Iterate through bullets
        bullet.y -= 10                             # Move bullet up
        if bullet.bottom < 100:                      # Check if bullet is out of screen
            bullets.remove(bullet)                 # Remove bullet if it goes out

def check_bullet_hits(baddies, explosions, score, bullets): # Function to check bullet hits
    for baddie in baddies[:]:                     # Iterate through baddies
        for bullet in bullets[:]:                  # Iterate through bullets
            if bullet.colliderect(baddie['rect']): # Check for collision
                trigger_explosion(explosions, baddie['rect'].center) # Trigger explosion
                if baddie['rect'].width <= 30 and baddie['rect'].height <= 30: # Check size
                    baddies.remove(baddie)         # Remove baddie if hit
                    score += 250                   # Update score
                bullets.remove(bullet)             # Remove bullet
                break                              # Break out of bullet loop
    return score                                   # Return updated score

#################################       Health and lives defintions         #############################################

def draw_lives(surface, lives, smallPlayerImage, smallPlayerImageGray, isGameOver): # Function to draw lives
    for i in range(3):                             # Loop for 3 lives
        if isGameOver:                             # If the game is over
            surface.blit(smallPlayerImageGray, (455 + i * 45, 10)) # Draw gray image
        else:                                      # If the game is not over
            if i < lives:                          # If player has life
                surface.blit(smallPlayerImage, (455 + i * 45, 10)) # Draw normal image
            else:                                  # If player is out of life
                surface.blit(smallPlayerImageGray, (455 + i * 45, 10)) # Draw gray image

def clear_lives_area(surface, backgroundImage):   # Function to clear the lives area
    lives_area = pygame.Rect(500, 10, 3 * 45, 30) # Define the lives area
    surface.blit(backgroundImage, (500, 10), lives_area) # Clear the lives area

def move_health_items(healthItems):              # Function to move health items
    for item in healthItems[:]:                   # Iterate through health items
        item['rect'].y += item['speed']           # Move health item down
        if item['rect'].top > WINDOWHEIGHT:       # Check if health item is out of window
            healthItems.remove(item)               # Remove health item if it goes out

def check_health_item_collision(playerRect, healthItems, lives, heal_animation):    #  Function if a player grab a health item
    heal_sound = pygame.mixer.Sound("sounds/heal.mp3")                    # Load heal sound
    for item in healthItems[:]:                                    # Iterate through health items
        if playerRect.colliderect(item['rect']):                  # Check for collision with player
            if lives < 3:                                          # Check if player has less than maximum lives
                lives += 1                                         # Increase lives by 1
                heal_sound.play()                                              # Play heal sound
                heal_animation = HealAnimation(playerRect.center)  # Create a new heal animation at player's center
            healthItems.remove(item)                               # Remove the health item after collision
  
    return lives, heal_animation                                    # Return updated lives and heal animation

def playerHasHitBaddie(playerRect, baddies):     # Function to check if player has hit a baddie
    for b in baddies:                             # Iterate through baddies
        if playerRect.colliderect(b['rect']):    # Check for collision
            return b                              # Return the baddie if hit
    return None                                   # Return None if no hit

#################################       Menu defintions         #############################################

def show_character_selection_menu(windowSurface, characterImage, font, playerRect):    
    numCharacters = len(characterImage)                # Get the number of characters in the characterImage list
    quitButtonRect = pygame.Rect(400, 680, 200, 50)  # Define the quit button rectangle

    while True:                                                                                                               # Start a loop to display the character selection menu
        backgroundImage = pygame.transform.scale(pygame.image.load('background.jpg').convert(), (WINDOWWIDTH, WINDOWHEIGHT))  # Load the background image and scale it to match the window size
        windowSurface.blit(backgroundImage, (0, 0))                                                                           # Draw the background image on the window surface
        
        borderOffset = 15                         # Set the border offset for selection border around characters

        mouseX, mouseY = pygame.mouse.get_pos()  # Get the current position of the mouse cursor
        
        playerRect = pygame.Rect(0, 0, 220, 220)  # Set playerRect to the size of each character image (220x220 pixels)

        for i in range(numCharacters):      # Loop through each character to display it
            playerX = 40 + (i // 2) * 350   # Calculate X position for each character, arranging them in two rows
            playerY = 40 + (i % 2) * 300    # Calculate Y position for each character, alternating between rows

            playerRect.topleft = (playerX, playerY)  # Update playerRect position for current character

            isMouseOver = playerRect.collidepoint(mouseX, mouseY)  # Check if the mouse is over the current character's area

            if isMouseOver:                                         # If mouse is over the character, change the border color to yellow
                borderColor = (255, 255, 0)                         # Yellow border color
                borderRect = playerRect.inflate(2 * borderOffset, 2 * borderOffset)  # Inflate the playerRect to create a border around the character
                pygame.draw.rect(windowSurface, borderColor, borderRect, 5)          # Draw the border around the character

            windowSurface.blit(pygame.transform.scale(characterImage[i], (220, 220)), (playerX, playerY))  # Blit the character image at the calculated position

        draw_text('Click on a player to select', font, windowSurface, windowSurface.get_width() // 2 - (font.size("Click on a player to select")[0] // 2), 600)  # Display instruction text at the top center
        draw_button(windowSurface, quitButtonRect, 'Quit', (255, 100, 100), (255, 150, 150))  # Draw the Quit button

        pygame.display.update()           # Update the window surface to reflect the changes

        for event in pygame.event.get():  # Check for user input events
            if event.type == QUIT:        # If the window is closed
                terminate()               # Exit the program
            if event.type == MOUSEBUTTONDOWN:   # If the mouse button is pressed
                for i in range(numCharacters):  # Loop through characters to check if one was clicked
                    playerX = 40 + (i // 2) * 350  # Calculate X position for the character
                    playerY = 40 + (i % 2) * 300   # Calculate Y position for the character

                    if playerX <= mouseX <= playerX + 220 and playerY <= mouseY <= playerY + 220:  # Check if mouse is within the bounds of the character
                        return i                                                                   # Return the index of the selected character

                if quitButtonRect.collidepoint(mouseX, mouseY):  # Check if Quit button is clicked
                    terminate()                                  # Exit the program
                                       
                                  

def show_difficulty_menu(windowSurface, font):    # Function to show the difficulty menu
    BUTTONCOLOR = (100, 200, 255)                 # Color for buttons
    BUTTONHOVERCOLOR = (150, 220, 255)            # Hover color for buttons
    QUITBUTTONCOLOR = (255, 100, 100)             # Color for quit button
    QUITBUTTONHOVERCOLOR = (255, 150, 150)        # Hover color for quit button

    easyButton = pygame.Rect(100, 200, 200, 50)   # Define easy button
    mediumButton = pygame.Rect(400, 200, 200, 50)  # Define medium button
    hardButton = pygame.Rect(700, 200, 200, 50)    # Define hard button
    returnMenuButtonRect = pygame.Rect(400, 500, 200, 50) # Define return to menu button
    quitButton = pygame.Rect(400, 600, 200, 50)    # Define quit button

    
    while True:                                   # Infinite loop
        for event in pygame.event.get():          # Process events
            if event.type == QUIT:                 # Check for quit event
                terminate()                        # Terminate if quit
            if event.type == MOUSEBUTTONDOWN:      # Check for mouse button down
                if easyButton.collidepoint(event.pos): # Check if easy button is clicked
                    return 'easy'                   # Return easy
                elif mediumButton.collidepoint(event.pos): # Check if medium button is clicked
                    return 'medium'                 # Return medium
                elif hardButton.collidepoint(event.pos):   # Check if hard button is clicked
                    return 'hard'                   # Return hard
                elif quitButton.collidepoint(event.pos):    # Check if quit button is clicked
                    terminate()                     # Terminate
                elif returnMenuButtonRect.collidepoint(event.pos): # Check if return button is clicked
                    from main import start          # Import start function from main
                    start()                        # Go back to main menu

        # Draw buttons
        draw_button(windowSurface, easyButton, 'Easy', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw easy button
        draw_button(windowSurface, mediumButton, 'Normal', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw medium button
        draw_button(windowSurface, hardButton, 'Difficult', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw hard button
        draw_button(windowSurface, returnMenuButtonRect, 'Menu', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw return button
        draw_button(windowSurface, quitButton, 'Quit', QUITBUTTONCOLOR, QUITBUTTONHOVERCOLOR) # Draw quit button
        

        draw_text('Choose the difficulty level', font, windowSurface, windowSurface.get_width() // 2  - (font.size("Choose the difficulty level")[0] // 2), 400) #   Draw the text of the menu
        
        pygame.display.update()                    # Update display
        mainClock.tick(FPS)                        # Control frame rate

def pause_menu(windowSurface, font):                      # Function to show the pause menu
    returnMenuButtonRect = pygame.Rect(400, 500, 200, 50) # Define return menu button
    quitButtonRect = pygame.Rect(400, 600, 200, 50)       # Define Quit button rectangle

    waitingForUnpause = True
    while waitingForUnpause:                                         # Loop until unpaused
        transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))  # Create a transparent surface
        transparent_surface.set_alpha(10)                           # Set alpha for transparency
        transparent_surface.fill((220, 220, 220))                   # Fill with a color

        windowSurface.blit(transparent_surface, (0, 0))             # Blit the transparent surface
        draw_text('Paused', font, windowSurface, windowSurface.get_width() // 2  - (font.size("Paused")[0] // 2), 300) # Draw pause text
        draw_text('Press ESC to resume', font, windowSurface, windowSurface.get_width() // 2  - (font.size("Press ESC to resume")[0] // 2), 400) # Draw resume instruction

        draw_button(windowSurface, returnMenuButtonRect, 'Menu', (100, 200, 255), (150, 220, 255)) # Draw return menu button
        draw_button(windowSurface, quitButtonRect, 'Quit', (255, 100, 100), (255, 150, 150)) # Draw Quit button

        
        pygame.display.update()                                     # Update display

        for event in pygame.event.get():                            # Handle events
            if event.type == QUIT:                                   # Check for quit event
                terminate()                                         # Terminate if quit
            if event.type == KEYDOWN:                               # Check for key down event
                if event.key == K_ESCAPE:                           # Check if ESC key is pressed
                    waitingForUnpause = False                       # Unpause if ESC is pressed
            if event.type == MOUSEBUTTONDOWN:                      # Check for mouse button down
                if quitButtonRect.collidepoint(event.pos):         # Check if Quit button is clicked
                    terminate()                                     # Terminate
                if returnMenuButtonRect.collidepoint(event.pos):   # Check if return button is clicked
                    from main import start                            # Import start function from main
                    start()                                         # Go back to main menu

def show_game_over_menu(windowSurface, score, font, smallFont, topScore):    # Function to show the game over screen
    BUTTONCOLOR = (100, 200, 255)                                 # Color for buttons
    BUTTONHOVERCOLOR = (150, 220, 255)                            # Hover color for buttons
    QUITBUTTONCOLOR = (255, 100, 100)                             # Color for quit button
    QUITBUTTONHOVERCOLOR = (255, 150, 150)                        # Hover color for quit button

    playAgainButton = pygame.Rect(350, 400, 300, 50)             # Define Play Again button rectangle
    returnMenuButtonRect = pygame.Rect(400, 500, 200, 50)        # Define return menu button
    quitButton = pygame.Rect(400, 600, 200, 50)                  # Define Quit button rectangle

    while True:
        for event in pygame.event.get():                          # Handle events
            if event.type == QUIT:                                 # Check for quit event
                terminate()                                        # Terminate if quit

            if event.type == MOUSEBUTTONDOWN:                     # Check for mouse button down
                if playAgainButton.collidepoint(event.pos):       # Check if Play Again button is clicked
                    return True                                     # Return True to play again
                elif quitButton.collidepoint(event.pos):          # Check if Quit button is clicked
                    terminate()                                     # Terminate
                elif returnMenuButtonRect.collidepoint(event.pos): # Check if return button is clicked
                    from main import start                           # Import start function from main
                    start()                                        # Go back to main menu

        transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))  # Create a transparent surface
        transparent_surface.set_alpha(10)                           # Set alpha for transparency
        transparent_surface.fill((220, 220, 220))                   # Fill with a color

        windowSurface.blit(transparent_surface, (0, 0))             # Blit the transparent surface
        draw_text('Game Over!', font, windowSurface, windowSurface.get_width() // 2  - (font.size("Game Over!")[0] // 2), 150)       # Draw Game Over text
        draw_text(f'Your Score: {score}', smallFont, windowSurface, windowSurface.get_width() // 2  - (font.size("Game Over!")[0] // 2), 200) # Draw score text
        draw_text('Top Score: %s' % (topScore), smallFont, windowSurface, windowSurface.get_width() // 2  - (font.size("Game Over!")[0] // 2), 250)  # Draw top score.
        draw_button(windowSurface, playAgainButton, 'Play Again', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw Play Again button
        draw_button(windowSurface, returnMenuButtonRect, 'Menu', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw return button
        draw_button(windowSurface, quitButton, 'Quit', QUITBUTTONCOLOR, QUITBUTTONHOVERCOLOR) # Draw Quit button


        pygame.display.update()                                    # Update display
        mainClock.tick(FPS)                                        # Control frame rate