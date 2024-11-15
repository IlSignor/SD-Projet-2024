#importations of the modulus and files
import pygame, sys
from pygame.locals import *
from classes import*

# Configuration of the window size
WINDOWWIDTH = 1000
WINDOWHEIGHT = 800

# Configuration of the colors
TEXTCOLOR = (255, 255, 255)
BUTTONTEXTCOLOR = (0, 0, 0)
BUTTONCOLOR = (0, 120, 200) 
BUTTONOVERCOLOR = (150, 220, 255)
QUITBUTTONCOLOR = (215, 0, 0)
QUITBUTTONOVERCOLOR = (255, 150, 150)

# Configuration of the baddies size, player movement speed, FPS and clock to control the frame rate

PLAYERMOVERATE = 5 
FPS = 60
main_clock = pygame.time.Clock()
top_score = 0

#################################       Basic defintions         #############################################

def terminate():                                  # Function to terminate the game
    pygame.quit()                                 # Quit Pygame
    sys.exit()                                    # Exit the program

def draw_text(text, font, surface, x, y):         # Function to draw text on the surface
    text_obj = font.render(text, 1, TEXTCOLOR)    # Render the text
    text_rect = text_obj.get_rect()                 # Get the rectangular area of the text
    text_rect.topleft = (x, y)                     # Set the position of the text
    surface.blit(text_obj, text_rect)               # Blit the text onto the surface

def draw_button(window_surface, button_rect, text, color, over_color): # Function to draw a button
    mouse_pos = pygame.mouse.get_pos()             # Get the position of the mouse
    # Change button color if mouse is over it
    if button_rect.collidepoint(mouse_pos):          # Check if mouse is over button
        pygame.draw.rect(window_surface, over_color, button_rect, border_radius=20) # Draw hover color
    else:
        pygame.draw.rect(window_surface, color, button_rect, border_radius=20) # Draw normal color
    font_path = "SpaceAge.ttf"
    buttonFont = pygame.font.Font(font_path, 40)     # Define button font
    textSurf = buttonFont.render(text, True, BUTTONTEXTCOLOR) # Render button text
    text_rect = textSurf.get_rect(center=button_rect.center) # Get text rect centered in button
    window_surface.blit(textSurf, text_rect)          # Blit the text onto the button

#################################       Explosions and bullets defintions         #############################################

def trigger_explosion(explosions, position):       # Function to trigger an explosion
    explosion_sound = pygame.mixer.Sound('sounds/explosion.mp3')            # Add explosion sound
    explosion_sound.play()
    explosions.append(Explosion(position))         # Add explosion at the specified position

def shoot(player_rect, bullets):                    # Function to shoot a bullet
    bullet = pygame.Rect(player_rect.centerx - 2, player_rect.top - 10, 5, 10) # Create a bullet
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

def draw_lives(surface, lives, small_player_image, small_player_image_gray, is_game_over): # Function to draw lives
    for i in range(3):                             # Loop for 3 lives
        if is_game_over:                             # If the game is over
            surface.blit(small_player_image_gray, (455 + i * 45, 10)) # Draw gray image
        else:                                      # If the game is not over
            if i < lives:                          # If player has life
                surface.blit(small_player_image, (455 + i * 45, 10)) # Draw normal image
            else:                                  # If player is out of life
                surface.blit(small_player_image_gray, (455 + i * 45, 10)) # Draw gray image

def move_health_items(health_items):              # Function to move health items
    for item in health_items[:]:                   # Iterate through health items
        item['rect'].y += item['speed']           # Move health item down
        if item['rect'].top > WINDOWHEIGHT:       # Check if health item is out of window
            health_items.remove(item)               # Remove health item if it goes out

def check_health_item_collision(player_rect, health_items, lives, heal_animation):    #  Function if a player grab a health item
    heal_sound = pygame.mixer.Sound("sounds/heal.mp3")                    # Load heal sound
    for item in health_items[:]:                                    # Iterate through health items
        if player_rect.colliderect(item['rect']):                  # Check for collision with player
            if lives < 3:                                          # Check if player has less than maximum lives
                lives += 1                                         # Increase lives by 1
                heal_sound.play()                                              # Play heal sound
                heal_animation = HealAnimation(player_rect.center)  # Create a new heal animation at player's center
            health_items.remove(item)                               # Remove the health item after collision
  
    return lives, heal_animation                                    # Return updated lives and heal animation

def playerHashit_baddie(player_rect, baddies):     # Function to check if player has hit a baddie
    for b in baddies:                             # Iterate through baddies
        if player_rect.colliderect(b['rect']):    # Check for collision
            return b                              # Return the baddie if hit
    return None                                   # Return None if no hit

#################################       Menu defintions         #############################################

def show_character_selection_menu(window_surface, character_image, font, player_rect, QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR):    
    num_characters = len(character_image)                # Get the number of characters in the character_image list
    quit_buttonRect = pygame.Rect(400, 680, 200, 50)  # Define the quit button rectangle

    while True:                                                                                                               # Start a loop to display the character selection menu
        background_image = pygame.transform.scale(pygame.image.load('background.jpg').convert(), (WINDOWWIDTH, WINDOWHEIGHT))  # Load the background image and scale it to match the window size
        window_surface.blit(background_image, (0, 0))                                                                           # Draw the background image on the window surface
        
        borderOffset = 15                         # Set the border offset for selection border around characters

        mouseX, mouseY = pygame.mouse.get_pos()  # Get the current position of the mouse cursor
        
        player_rect = pygame.Rect(0, 0, 220, 220)  # Set player_rect to the size of each character image (220x220 pixels)

        for i in range(num_characters):      # Loop through each character to display it
            player_x = 40 + (i // 2) * 350   # Calculate X position for each character, arranging them in two rows
            player_y = 40 + (i % 2) * 300    # Calculate Y position for each character, alternating between rows

            player_rect.topleft = (player_x, player_y)  # Update player_rect position for current character

            isMouseOver = player_rect.collidepoint(mouseX, mouseY)  # Check if the mouse is over the current character's area

            if isMouseOver:                                         # If mouse is over the character, change the border color to yellow
                borderColor = (255, 255, 0)                         # Yellow border color
                borderRect = player_rect.inflate(2 * borderOffset, 2 * borderOffset)  # Inflate the player_rect to create a border around the character
                pygame.draw.rect(window_surface, borderColor, borderRect, 5)          # Draw the border around the character

            window_surface.blit(pygame.transform.scale(character_image[i], (220, 220)), (player_x, player_y))  # Blit the character image at the calculated position

        draw_text('Click on a player to select', font, window_surface, window_surface.get_width() // 2 - (font.size("Click on a player to select")[0] // 2), 600)  # Display instruction text at the top center
        draw_button(window_surface, quit_buttonRect, 'Quit', QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR)  # Draw the Quit button

        pygame.display.update()           # Update the window surface to reflect the changes

        for event in pygame.event.get():  # Check for user input events
            if event.type == QUIT:        # If the window is closed
                terminate()               # Exit the program
            if event.type == MOUSEBUTTONDOWN:   # If the mouse button is pressed
                for i in range(num_characters):  # Loop through characters to check if one was clicked
                    player_x = 40 + (i // 2) * 350  # Calculate X position for the character
                    player_y = 40 + (i % 2) * 300   # Calculate Y position for the character

                    if player_x <= mouseX <= player_x + 220 and player_y <= mouseY <= player_y + 220:  # Check if mouse is within the bounds of the character
                        return i                                                                   # Return the index of the selected character

                if quit_buttonRect.collidepoint(mouseX, mouseY):  # Check if Quit button is clicked
                    terminate()                                  # Exit the program
                                       
                                  

def show_difficulty_menu(window_surface, font, BUTTONCOLOR, BUTTONOVERCOLOR, QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR):    # Function to show the difficulty menu

    easy_button = pygame.Rect(100, 200, 200, 50)   # Define easy button
    medium_button = pygame.Rect(400, 200, 200, 50)  # Define medium button
    hard_button = pygame.Rect(700, 200, 200, 50)    # Define hard button
    return_menu_button_rect = pygame.Rect(400, 500, 200, 50) # Define return to menu button
    quit_button = pygame.Rect(400, 600, 200, 50)    # Define quit button

    
    while True:                                   # Infinite loop
        for event in pygame.event.get():          # Process events
            if event.type == QUIT:                 # Check for quit event
                terminate()                        # Terminate if quit
            if event.type == MOUSEBUTTONDOWN:      # Check for mouse button down
                if easy_button.collidepoint(event.pos): # Check if easy button is clicked
                    return 'easy'                   # Return easy
                elif medium_button.collidepoint(event.pos): # Check if medium button is clicked
                    return 'medium'                 # Return medium
                elif hard_button.collidepoint(event.pos):   # Check if hard button is clicked
                    return 'hard'                   # Return hard
                elif quit_button.collidepoint(event.pos):    # Check if quit button is clicked
                    terminate()                     # Terminate
                elif return_menu_button_rect.collidepoint(event.pos): # Check if return button is clicked
                    from main import start          # Import start function from main
                    start()                        # Go back to main menu

        # Draw buttons
        draw_button(window_surface, easy_button, 'Easy', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw easy button
        draw_button(window_surface, medium_button, 'Normal', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw medium button
        draw_button(window_surface, hard_button, 'Difficult', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw hard button
        draw_button(window_surface, return_menu_button_rect, 'Menu', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw return button
        draw_button(window_surface, quit_button, 'Quit', QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR) # Draw quit button
        

        draw_text('Choose the difficulty level', font, window_surface, window_surface.get_width() // 2  - (font.size("Choose the difficulty level")[0] // 2), 400) #   Draw the text of the menu
        
        pygame.display.update()                    # Update display
        main_clock.tick(FPS)                        # Control frame rate

def pause_menu(window_surface, font, BUTTONCOLOR, BUTTONOVERCOLOR, QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR):                      # Function to show the pause menu
    return_menu_button_rect = pygame.Rect(400, 500, 200, 50) # Define return menu button
    quit_buttonRect = pygame.Rect(400, 600, 200, 50)       # Define Quit button rectangle

    waitingForUnpause = True
    while waitingForUnpause:                                         # Loop until unpaused
        transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))  # Create a transparent surface
        transparent_surface.set_alpha(10)                           # Set alpha for transparency
        transparent_surface.fill((220, 220, 220))                   # Fill with a color

        window_surface.blit(transparent_surface, (0, 0))             # Blit the transparent surface
        draw_text('Paused', font, window_surface, window_surface.get_width() // 2  - (font.size("Paused")[0] // 2), 300) # Draw pause text
        draw_text('Press ESC to resume', font, window_surface, window_surface.get_width() // 2  - (font.size("Press ESC to resume")[0] // 2), 400) # Draw resume instruction

        draw_button(window_surface, return_menu_button_rect, 'Menu', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw return menu button
        draw_button(window_surface, quit_buttonRect, 'Quit', QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR) # Draw Quit button

        
        pygame.display.update()                                     # Update display

        for event in pygame.event.get():                            # Handle events
            if event.type == QUIT:                                   # Check for quit event
                terminate()                                         # Terminate if quit
            if event.type == KEYDOWN:                               # Check for key down event
                if event.key == K_ESCAPE:                           # Check if ESC key is pressed
                    waitingForUnpause = False                       # Unpause if ESC is pressed
            if event.type == MOUSEBUTTONDOWN:                      # Check for mouse button down
                if quit_buttonRect.collidepoint(event.pos):         # Check if Quit button is clicked
                    terminate()                                     # Terminate
                if return_menu_button_rect.collidepoint(event.pos):   # Check if return button is clicked
                    from main import start                            # Import start function from main
                    start()                                         # Go back to main menu

def show_game_over_menu(window_surface, score, font, small_font, top_score, BUTTONCOLOR, BUTTONOVERCOLOR, QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR):    # Function to show the game over screen

    play_again_button = pygame.Rect(350, 400, 300, 50)             # Define Play Again button rectangle
    return_menu_button_rect = pygame.Rect(400, 500, 200, 50)        # Define return menu button
    quit_button = pygame.Rect(400, 600, 200, 50)                  # Define Quit button rectangle

    while True:
        for event in pygame.event.get():                          # Handle events
            if event.type == QUIT:                                 # Check for quit event
                terminate()                                        # Terminate if quit

            if event.type == MOUSEBUTTONDOWN:                     # Check for mouse button down
                if play_again_button.collidepoint(event.pos):       # Check if Play Again button is clicked
                    return True                                     # Return True to play again
                elif quit_button.collidepoint(event.pos):          # Check if Quit button is clicked
                    terminate()                                     # Terminate
                elif return_menu_button_rect.collidepoint(event.pos): # Check if return button is clicked
                    from main import start                           # Import start function from main
                    start()                                        # Go back to main menu

        transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))  # Create a transparent surface
        transparent_surface.set_alpha(10)                           # Set alpha for transparency
        transparent_surface.fill((220, 220, 220))                   # Fill with a color

        window_surface.blit(transparent_surface, (0, 0))             # Blit the transparent surface
        draw_text('Game Over!', font, window_surface, window_surface.get_width() // 2  - (font.size("Game Over!")[0] // 2), 150)       # Draw Game Over text
        draw_text(f'Your Score: {score}', small_font, window_surface, window_surface.get_width() // 2  - (font.size("Game Over!")[0] // 2), 200) # Draw score text
        draw_text('Top Score: %s' % (top_score), small_font, window_surface, window_surface.get_width() // 2  - (font.size("Game Over!")[0] // 2), 250)  # Draw top score.
        draw_button(window_surface, play_again_button, 'Play Again', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw Play Again button
        draw_button(window_surface, return_menu_button_rect, 'Menu', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw return button
        draw_button(window_surface, quit_button, 'Quit', QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR) # Draw Quit button

        pygame.display.update()                                    # Update display
        main_clock.tick(FPS)                                        # Control frame rate