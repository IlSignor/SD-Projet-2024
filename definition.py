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

def waitForPlayerToPressKey():                    # Function to wait for player key press
    while True:                                   # Infinite loop
        for event in pygame.event.get():         # Process events
            if event.type == QUIT:                # Check for quit event
                terminate()                        # Terminate if quit
            if event.type == KEYDOWN:             # Check for key down event
                return                             # Return when a key is pressed

def drawText(text, font, surface, x, y):         # Function to draw text on the surface
    textobj = font.render(text, 1, TEXTCOLOR)    # Render the text
    textrect = textobj.get_rect()                 # Get the rectangular area of the text
    textrect.topleft = (x, y)                     # Set the position of the text
    surface.blit(textobj, textrect)               # Blit the text onto the surface

def drawButton(windowSurface, buttonRect, text, color, hoverColor): # Function to draw a button
    mousePos = pygame.mouse.get_pos()             # Get the position of the mouse
    # Change button color if mouse is over it
    if buttonRect.collidepoint(mousePos):          # Check if mouse is over button
        pygame.draw.rect(windowSurface, hoverColor, buttonRect) # Draw hover color
    else:
        pygame.draw.rect(windowSurface, color, buttonRect) # Draw normal color

    buttonFont = pygame.font.SysFont(None, 40)     # Define button font
    textSurf = buttonFont.render(text, True, BUTTONTEXTCOLOR) # Render button text
    textRect = textSurf.get_rect(center=buttonRect.center) # Get text rect centered in button
    windowSurface.blit(textSurf, textRect)          # Blit the text onto the button

#################################       Explosions and bullets defintions         #############################################

def trigger_explosion(explosions, position):     # Function to trigger an explosion
    explosions.append(Explosion(position))        # Add explosion at the specified position

def shoot(playerRect, bullets):                    # Function to shoot a bullet
    bullet = pygame.Rect(playerRect.centerx - 2, playerRect.top - 10, 5, 10) # Create a bullet
    bullets.append(bullet)                         # Add bullet to the list

def move_bullets(bullets):                         # Function to move bullets
    for bullet in bullets[:]:                      # Iterate through bullets
        bullet.y -= 10                             # Move bullet up
        if bullet.bottom < 0:                      # Check if bullet is out of screen
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
            surface.blit(smallPlayerImageGray, (500 + i * 45, 10)) # Draw gray image
        else:                                      # If the game is not over
            if i < lives:                          # If player has life
                surface.blit(smallPlayerImage, (500 + i * 45, 10)) # Draw normal image
            else:                                  # If player is out of life
                surface.blit(smallPlayerImageGray, (500 + i * 45, 10)) # Draw gray image

def clear_lives_area(surface, backgroundImage):   # Function to clear the lives area
    lives_area = pygame.Rect(500, 10, 3 * 45, 30) # Define the lives area
    surface.blit(backgroundImage, (500, 10), lives_area) # Clear the lives area

def move_health_items(healthItems):              # Function to move health items
    for item in healthItems[:]:                   # Iterate through health items
        item['rect'].y += item['speed']           # Move health item down
        if item['rect'].top > WINDOWHEIGHT:       # Check if health item is out of window
            healthItems.remove(item)               # Remove health item if it goes out

def check_health_item_collision(playerRect, healthItems, lives, heal_animation):    #  Function if a player grab a health item
    for item in healthItems[:]:                                    # Iterate through health items
        if playerRect.colliderect(item['rect']):                  # Check for collision with player
            if lives < 3:                                          # Check if player has less than maximum lives
                lives += 1                                         # Increase lives by 1
                heal_animation = HealAnimation(playerRect.center)  # Create a new heal animation at player's center
            healthItems.remove(item)                               # Remove the health item after collision
  
    return lives, heal_animation                                    # Return updated lives and heal animation

def playerHasHitBaddie(playerRect, baddies):     # Function to check if player has hit a baddie
    for b in baddies:                             # Iterate through baddies
        if playerRect.colliderect(b['rect']):    # Check for collision
            return b                              # Return the baddie if hit
    return None                                   # Return None if no hit

#################################       Menu defintions         #############################################

def showCharacterSelectionMenu(windowSurface, characterImage, font, playerRect):    # Function to show the character selection menu
    numCharacters = len(characterImage)                                   # Get the number of characters

    quitButtonRect = pygame.Rect(400, 500, 200, 50)                    # Define the Quit button rectangle

    while True:
        backgroundImage = pygame.image.load('background.jpg').convert()  # Load background image
        windowSurface.blit(backgroundImage, (0, 0))                     # Blit background to window surface
        borderOffset = 15                                                  # Offset for centering the border around the image

        mouseX, mouseY = pygame.mouse.get_pos()                          # Get mouse position

        for i in range(numCharacters):                                   # Display each character
            playerX = 100 + i * 150                                      # Position for each character
            playerY = 200                                                 # Fixed Y position for characters

            playerRect.topleft = (playerX, playerY)                     # Update playerRect position

            isMouseOver = playerRect.collidepoint(mouseX, mouseY)       # Check if mouse is over character

            if isMouseOver:                                              # If mouse is over character
                borderColor = (255, 255, 0)                             # Set border color to yellow
                
                borderRect = playerRect.inflate(2 * borderOffset, 2 * borderOffset) # Center border around image
                
                pygame.draw.rect(windowSurface, borderColor, borderRect, 5) # Draw border

            windowSurface.blit(characterImage[i], (100 + i * 150, 200)) # Blit character image

        drawText('Click on a character to select', font, windowSurface, 100, 400) # Display instructions

        drawButton(windowSurface, quitButtonRect, 'Quitter', (255, 100, 100), (255, 150, 150)) # Draw Quit button

        pygame.display.update()                                         # Update display

        for event in pygame.event.get():
            if event.type == QUIT:                                      # Check for quit event
                terminate()                                             # Terminate if quit
            if event.type == MOUSEBUTTONDOWN:                          # Check for mouse button down
                for i in range(numCharacters):                         # Check for character clicks
                    if (
                        100 + i * 150 <= mouseX <= 100 + i * 150 + 130 and # Check if mouse is over character
                        200 <= mouseY <= 200 + 130
                    ):
                        return i                                         # Return index of selected character

                if quitButtonRect.collidepoint(mouseX, mouseY):       # Check if Quit button is clicked
                    terminate()                                         # Terminate

def showDifficultyMenu(windowSurface):             # Function to show the difficulty menu
    BUTTONCOLOR = (100, 200, 255)                 # Color for buttons
    BUTTONHOVERCOLOR = (150, 220, 255)            # Hover color for buttons
    QUITBUTTONCOLOR = (255, 100, 100)             # Color for quit button
    QUITBUTTONHOVERCOLOR = (255, 150, 150)        # Hover color for quit button

    easyButton = pygame.Rect(300, 200, 200, 50)   # Define easy button
    mediumButton = pygame.Rect(300, 300, 200, 50)  # Define medium button
    hardButton = pygame.Rect(300, 400, 200, 50)    # Define hard button
    quitButton = pygame.Rect(300, 500, 200, 50)    # Define quit button
    returnMenuButtonRect = pygame.Rect(300, 600, 200, 50) # Define return to menu button
    
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
        drawButton(windowSurface, easyButton, 'Facile', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw easy button
        drawButton(windowSurface, mediumButton, 'Moyen', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw medium button
        drawButton(windowSurface, hardButton, 'Difficile', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw hard button
        drawButton(windowSurface, quitButton, 'Quitter', QUITBUTTONCOLOR, QUITBUTTONHOVERCOLOR) # Draw quit button
        drawButton(windowSurface, returnMenuButtonRect, 'Retour au menu', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw return button

        pygame.display.update()                    # Update display
        mainClock.tick(FPS)                        # Control frame rate

def pause_menu(windowSurface, font):                # Function to show the pause menu
    quitButtonRect = pygame.Rect((WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) + 50, 200, 50)  # Define Quit button rectangle
    returnMenuButtonRect = pygame.Rect((WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) + 110, 200, 50) # Define return menu button

    waitingForUnpause = True
    while waitingForUnpause:                                         # Loop until unpaused
        transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))  # Create a transparent surface
        transparent_surface.set_alpha(10)                           # Set alpha for transparency
        transparent_surface.fill((220, 220, 220))                   # Fill with a color

        windowSurface.blit(transparent_surface, (0, 0))             # Blit the transparent surface
        drawText('Paused', font, windowSurface, (WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) - 100) # Draw pause text
        drawText('Press ESC to resume.', font, windowSurface, (WINDOWWIDTH / 2) - 150, (WINDOWHEIGHT / 2)) # Draw resume instruction

        drawButton(windowSurface, quitButtonRect, 'Quitter', (255, 100, 100), (255, 150, 150)) # Draw Quit button
        drawButton(windowSurface, returnMenuButtonRect, 'Retour au menu', (100, 255, 100), (150, 255, 150)) # Draw return menu button
        
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

def show_game_over_menu(windowSurface, score, font):    # Function to show the game over screen
    BUTTONCOLOR = (100, 200, 255)                                 # Color for buttons
    BUTTONHOVERCOLOR = (150, 220, 255)                            # Hover color for buttons
    QUITBUTTONCOLOR = (255, 100, 100)                             # Color for quit button
    QUITBUTTONHOVERCOLOR = (255, 150, 150)                        # Hover color for quit button

    playAgainButton = pygame.Rect(300, 200, 200, 50)             # Define Play Again button rectangle
    quitButton = pygame.Rect(300, 300, 200, 50)                  # Define Quit button rectangle
    returnMenuButtonRect = pygame.Rect((WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) + 110, 200, 50) # Define return menu button

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

        windowSurface.fill((255, 255, 255))                       # Fill the window with white
        drawText('Game Over', font, windowSurface, 350, 50)       # Draw Game Over text
        drawText(f'Your Score: {score}', font, windowSurface, 350, 100) # Draw score text
        drawButton(windowSurface, playAgainButton, 'Play Again', BUTTONCOLOR, BUTTONHOVERCOLOR) # Draw Play Again button
        drawButton(windowSurface, quitButton, 'Quit', QUITBUTTONCOLOR, QUITBUTTONHOVERCOLOR) # Draw Quit button
        drawButton(windowSurface, returnMenuButtonRect, 'Retour au menu', (100, 255, 100), (150, 255, 150)) # Draw return button

        pygame.display.update()                                    # Update display
        mainClock.tick(FPS)                                        # Control frame rate

    textobj = font.render(text, 1, TEXTCOLOR)                    # Render the text
    textrect = textobj.get_rect()                                 # Get the rectangular area of the text
    textrect.topleft = (x, y)                                     # Set the position of the text
    surface.blit(textobj, textrect)                               # Blit the text onto the surface

    bullet = pygame.Rect(playerRect.centerx - 2, playerRect.top - 10, 5, 10)  # Create bullet at player position
    bullets.append(bullet)                                         # Add bullet to the list