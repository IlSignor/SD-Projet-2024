#################################       This file defines the classes and constants used to the main mechanics of the game         #############################################

#importations of the modulus and files
import pygame, sys, random
from pygame.locals import *
from animations import*

# Constants of the configuration of the window size
WINDOWWIDTH = 1000
WINDOWHEIGHT = 800
window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Constants of the button colors
BUTTONCOLOR = (0, 120, 200) 
BUTTONOVERCOLOR = (150, 220, 255)
QUITBUTTONCOLOR = (215, 0, 0)
QUITBUTTONOVERCOLOR = (255, 150, 150)

# Fonts used
pygame.font.init()
font = pygame.font.Font("SpaceAge.ttf", 40)
small_font = pygame.font.Font("SpaceAge.ttf", 30)

# Definition of the main clock of the game
main_clock = pygame.time.Clock()


#################################       Basic elements class         #############################################

class Basic:
    pygame.font.init()                             # Use the font module
    def __init__(self):
        self.TEXTCOLOR = (255,255,255)             # Define the color of the text
        self.BUTTONTEXTCOLOR = (0, 0, 0)           # Define the text color of the buttons
        
    
    def terminate(self):                                  # Function to terminate the game
        pygame.quit()                                     # Quit Pygame
        sys.exit()                                        # Exit the program

    def draw_text(self, text, font, surface, x, y):         # Function to draw text on the surface
        text_obj = font.render(text, 1, self.TEXTCOLOR)     # Render the text
        text_rect = text_obj.get_rect()                     # Get the rectangular area of the text
        text_rect.topleft = (x, y)                          # Set the position of the text
        surface.blit(text_obj, text_rect)                   # Blit the text onto the surface

    def draw_button(self, button_rect, text, color, over_color): # Function to draw a button
        mouse_pos = pygame.mouse.get_pos()                       # Get the position of the mouse
        
        # Change button color if mouse is over it
        if button_rect.collidepoint(mouse_pos):                                         # Check if mouse is over button
            pygame.draw.rect(window_surface, over_color, button_rect, border_radius=20) # Draw hover color
        else:
            pygame.draw.rect(window_surface, color, button_rect, border_radius=20) # Draw normal color
        
        textSurf = font.render(text, True, self.BUTTONTEXTCOLOR)                   # Render button text
        text_rect = textSurf.get_rect(center=button_rect.center)                   # Get text rect centered in button
        window_surface.blit(textSurf, text_rect)                                   # Blit the text onto the button

basic = Basic()                         # Put the basic class in a variable to use it in an easier way   

#################################       Explosions and bullets class         #############################################

class ExplosionBullets:
    def __init__(self):
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.mp3')            # Add explosion sound
        self.shots_sound = pygame.mixer.Sound('sounds/laser_shot.mp3')               # Add explosion sound
        
    def trigger_explosion(self,explosions, position):        # Function to trigger an explosion
        self.explosion_sound.play()                          # Play the explosion sound 
        explosions.append(Explosion(position))               # Add explosion at the specified position
        
    def shoot(self,player_rect, bullets):                                          # Function to shoot a bullet
        self.shots_sound.play()                                                    # Play the shoot sound
        bullet = pygame.Rect(player_rect.centerx - 2, player_rect.top - 10, 5, 10) # Create a bullet
        bullets.append(bullet)                                                     # Add bullet to the list
                
    def move_bullets(self, bullets):                         # Function to move bullets
        for bullet in bullets[:]:                            # Iterate through bullets
            bullet.y -= 10                                   # Move bullet up
            if bullet.bottom < 100:                          # Check if bullet is out of screen
                bullets.remove(bullet)                       # Remove bullet if it goes out
    
    def move_aliens(self, aliens, player_rect):              # Function to move aliens
        for alien in aliens:                                   # Loop through each alien in the list
            alien['rect'].move_ip(0, alien['speed'])           # Move the alien vertically by its speed
            if alien['rect'].centerx < player_rect.centerx:    # If the alien is left of the player
                alien['rect'].move_ip(5, 0)                    # Move the alien 5 units to the right
            elif alien['rect'].centerx > player_rect.centerx:  # If the alien is right of the player
                alien['rect'].move_ip(-5, 0)                   # Move the alien 5 units to the left

    def check_bullet_hits(self, comets,comet_image, explosions, score, bullets): # Function to check bullet hits
        for comet in comets[:]:                                                  # Iterate through comets
            for bullet in bullets[:]:                                            # Iterate through bullets
                if bullet.colliderect(comet['rect']):                            # Check for collision
                    ExplosionBullets.trigger_explosion(self, explosions, comet['rect'].center) # Trigger explosion
                    if 45 < comet['rect'].width <= 60:                                         # If the comet is "size 3"
                        comet_new_size = random.randint(31, 45)                                # Creates a new smaller size for the comet
                        comet['rect'].width = comet_new_size                                   # Makes the comet smaller
                        comet['rect'].height = comet_new_size                                  # Makes the comet smaller
                        comet['surface'] = pygame.transform.scale(comet_image, (comet_new_size, comet_new_size))  # Makes the comet smaller
                        
                    elif 30 < comet['rect'].width <= 45:                 # If the comet is "size 2"
                        comet_new_size = random.randint(20, 30)          # Creates a new smaller size for the comet
                        comet['rect'].width = comet_new_size             # Makes the comet smaller
                        comet['rect'].height = comet_new_size            # Makes the comet smaller
                        comet['surface'] = pygame.transform.scale(comet_image, (comet_new_size, comet_new_size))  # Makes the comet smaller
                        
                    else:                              # Else
                        comets.remove(comet)           # Remove comet if hit
                        score += 250                   # Update score
                    bullets.remove(bullet)             # Remove bullet
                    break                              # Break out of bullet loop
        return score                                   # Return updated score
    
    def check_alien_hits(self, aliens, explosions, bullets):    # Function to check aliens hits
        for alien in aliens:                           # Loop through each alien in the list
            for bullet in bullets:                     # Loop through each bullet in the list
                if bullet.colliderect(alien['rect']):  # Check if the bullet collides with the alien's rectangle
                    # Trigger an explosion at the alien's position (adjusted slightly vertically)
                    ExplosionBullets.trigger_explosion(self, explosions, (alien['rect'].centerx, alien['rect'].centery + 20)) 
                    
                    alien['lives'] -= 1           # Reduce the alien's life count by 1

                    if alien['lives'] == 0:      # If the alien's lives reach 0
                        aliens.remove(alien)     # Remove the alien from the list

                    bullets.remove(bullet)  # Remove the bullet from the list after collision
                    break                   # Exit the bullet loop to avoid checking the removed bullet

#################################       Health and lives class         #############################################

class HealthLives:
    def __init__(self):
        self.small_live_image = pygame.transform.scale(pygame.image.load(f'live.png'), (30, 30))  # Scale down player image for display
        self.small_live_image_gray = pygame.Surface((30, 30))                                     # Create a surface for the gray version
     
     
    def draw_lives(self, lives, is_game_over):           # Function to draw lives
        for i in range(3):                               # Loop for 3 lives
            if is_game_over:                             # If the game is over
                window_surface.blit(self.small_live_image_gray, (455 + i * 45, 10)) # Draw gray image
            else:                                                                   # If the game is not over
                if i < lives:                                                       # If player has life
                    window_surface.blit(self.small_live_image, (455 + i * 45, 10))  # Draw normal image
                else:                                                               # If player is out of life
                    window_surface.blit(self.small_live_image_gray, (455 + i * 45, 10)) # Draw gray image

    def move_health_items(self, health_items):              # Function to move health items
        for item in health_items[:]:                        # Iterate through health items
            item['rect'].y += item['speed']                 # Move health item down
            if item['rect'].top > WINDOWHEIGHT:             # Check if health item is out of window
                health_items.remove(item)                   # Remove health item if it goes out

    def check_health_item_collision(self,health_items, player_rect, lives, heal_animation):    #  Function if a player grab a health item
        heal_sound = pygame.mixer.Sound("sounds/heal.mp3")                    # Load heal sound
        for item in health_items[:]:                                          # Iterate through health items
            if player_rect.colliderect(item['rect']):                         # Check for collision with player
                if lives < 3:                                                 # Check if player has less than maximum lives
                    lives += 1                                                # Increase lives by 1
                    heal_sound.play()                                         # Play heal sound
                    heal_animation = HealAnimation(player_rect.center)        # Create a new heal animation at player's center
                health_items.remove(item)                                     # Remove the health item after collision
    
        return lives, heal_animation                                          # Return updated lives and heal animation

    def player_hit_comet(self, player_rect, comets):     # Function to check if player has hit a comet
        for b in comets:                                 # Iterate through comets
            if player_rect.colliderect(b['rect']):       # Check for collision
                return b                                 # Return the comet if hit
        return None                                      # Return None if no hit

#################################       Menu class         #############################################

class ShowMenu:
    def __init__(self):
        pygame.font.init()                                                # Load the font module
        
        self.game_over_sound = pygame.mixer.Sound('sounds/gameover.mp3')  # Load game over sound
        self.player_selection_rect = pygame.Rect(0, 0, 130, 220)          # Set player_rect to the size of each character image (130x220 pixels)


    def show_character_selection_menu(self,character_image):    # Function to show the character selection menu
        num_characters = len(character_image)                # Get the number of characters in the character_image list
        quit_buttonRect = pygame.Rect(400, 680, 200, 50)     # Define the quit button rectangle

        while True:                                                                                                                # Start a loop to display the character selection menu
            background_image = pygame.transform.scale(pygame.image.load('background.jpg').convert(), (WINDOWWIDTH, WINDOWHEIGHT))  # Load the background image and scale it to match the window size
            window_surface.blit(background_image, (0, 0))                                                                          # Draw the background image on the window surface
            
            borderOffset = 15                         # Set the border offset for selection border around characters

            mouseX, mouseY = pygame.mouse.get_pos()   # Get the current position of the mouse cursor


            for i in range(num_characters):      # Loop through each character to display it
                player_x = 80 + (i // 2) * 350   # Calculate X position for each character, arranging them in two rows
                player_y = 50 + (i % 2) * 300    # Calculate Y position for each character, alternating between rows

                self.player_selection_rect.topleft = (player_x, player_y)  # Update player_rect position for current character

                isMouseOver = self.player_selection_rect.collidepoint(mouseX, mouseY)  # Check if the mouse is over the current character's area

                if isMouseOver:                                         # If mouse is over the character, change the border color to yellow
                    borderColor = (0, 120, 200)                         # Blue border color
                    borderRect = self.player_selection_rect.inflate(2 * borderOffset, 2 * borderOffset)  # Inflate the player_rect to create a border around the character
                    pygame.draw.rect(window_surface, borderColor, borderRect, 5, 10)                     # Draw the border around the character

                window_surface.blit(pygame.transform.scale(character_image[i], (130, 220)), (player_x, player_y))  # Blit the character image at the calculated position

            basic.draw_text('Click on a player to select', font, window_surface, window_surface.get_width() // 2 - (font.size("Click on a player to select")[0] // 2), 600)  # Display instruction text at the top center
            basic.draw_button(quit_buttonRect, 'Quit', QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR)  # Draw the Quit button

            pygame.display.update()           # Update the window surface to reflect the changes

            for event in pygame.event.get():            # Check for user input events
                if event.type == QUIT:                  # If the window is closed
                    basic.terminate()                   # Exit the program
                if event.type == MOUSEBUTTONDOWN:       # If the mouse button is pressed
                    for i in range(num_characters):     # Loop through characters to check if one was clicked
                        player_x = 40 + (i // 2) * 350  # Calculate X position for the character
                        player_y = 40 + (i % 2) * 300   # Calculate Y position for the character

                        if player_x <= mouseX <= player_x + 220 and player_y <= mouseY <= player_y + 220:  # Check if mouse is within the bounds of the character
                            return int(i)                                                                  # Return the index of the selected character

                    if quit_buttonRect.collidepoint(mouseX, mouseY):       # Check if Quit button is clicked
                        basic.terminate()                                  # Exit the program
                                        
    def show_difficulty_menu(self):    # Function to show the difficulty menu
        background_image = pygame.transform.scale(pygame.image.load('background.jpg').convert(), (WINDOWWIDTH, WINDOWHEIGHT))   # Background image used
        window_surface.blit(background_image, (0, 0))
        easy_button = pygame.Rect(100, 200, 200, 50)             # Define easy button
        medium_button = pygame.Rect(400, 200, 200, 50)           # Define medium button
        hard_button = pygame.Rect(700, 200, 200, 50)             # Define hard button
        return_menu_button_rect = pygame.Rect(400, 500, 200, 50) # Define return to menu button
        quit_button = pygame.Rect(400, 600, 200, 50)             # Define quit button

        
        while True:                                    # Infinite loop
            for event in pygame.event.get():           # Process events
                if event.type == QUIT:                 # Check for quit event
                    basic.terminate()                  # basic.terminate if quit
                if event.type == MOUSEBUTTONDOWN:      # Check for mouse button down
                    if easy_button.collidepoint(event.pos): # Check if easy button is clicked
                        return 'easy'                       # Return easy
                    elif medium_button.collidepoint(event.pos): # Check if medium button is clicked
                        return 'medium'                         # Return medium
                    elif hard_button.collidepoint(event.pos):   # Check if hard button is clicked
                        return 'hard'                            # Return hard
                    elif quit_button.collidepoint(event.pos):    # Check if quit button is clicked
                        basic.terminate()                        # basic.terminate
                    elif return_menu_button_rect.collidepoint(event.pos): # Check if return button is clicked
                        from main import SpaceShooterGame                 # Import start function from main
                        game_instance = SpaceShooterGame()                # Créer une instance de la classe
                        game_instance.start()                             # Start the game

            # Draw buttons
            basic.draw_button(easy_button, 'Easy', BUTTONCOLOR, BUTTONOVERCOLOR)             # Draw easy button
            basic.draw_button(medium_button, 'Normal', BUTTONCOLOR, BUTTONOVERCOLOR)         # Draw medium button
            basic.draw_button(hard_button, 'Difficult', BUTTONCOLOR, BUTTONOVERCOLOR)        # Draw hard button
            basic.draw_button(return_menu_button_rect, 'Menu', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw return button
            basic.draw_button(quit_button, 'Quit', QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR)     # Draw quit button
            

            basic.draw_text('Choose the difficulty level', font, window_surface, window_surface.get_width() // 2  - (font.size("Choose the difficulty level")[0] // 2), 400) # Draw the text of the menu
            
            pygame.display.update()                    # Update display
            main_clock.tick(60)                        # Control frame rate

    def pause_menu(self):                                        # Function to show the pause menu
        return_menu_button_rect = pygame.Rect(400, 500, 200, 50) # Define return menu button
        quit_buttonRect = pygame.Rect(400, 600, 200, 50)         # Define Quit button rectangle
        pygame.mixer.music.stop()                                # Stop the background music
        
        waitingForUnpause = True                                 # Wait for the player to unpause the game
        while waitingForUnpause:                                               # Loop until unpaused
            transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))  # Create a transparent surface
            transparent_surface.set_alpha(10)                           # Set alpha for transparency
            transparent_surface.fill((220, 220, 220))                   # Fill with a color

            window_surface.blit(transparent_surface, (0, 0))                                                                       # Blit the transparent surface
            basic.draw_text('Paused', font, window_surface, window_surface.get_width() // 2  - (font.size("Paused")[0] // 2), 300) # Draw pause text
            basic.draw_text('Press ESC to resume', font, window_surface, window_surface.get_width() // 2  - (font.size("Press ESC to resume")[0] // 2), 400) # Draw resume instruction

            basic.draw_button(return_menu_button_rect, 'Menu', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw return menu button
            basic.draw_button(quit_buttonRect, 'Quit', QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR) # Draw Quit button

            
            pygame.display.update()                                     # Update display

            for event in pygame.event.get():                            # Handle events
                if event.type == QUIT:                                  # Check for quit event
                    basic.terminate()                                   # basic.terminate if quit
                if event.type == KEYDOWN:                               # Check for key down event
                    if event.key == K_ESCAPE:                           # Check if ESC key is pressed
                        waitingForUnpause = False                       # Unpause if ESC is pressed
                        pygame.mixer.music.play()                       # Play the background music.
                if event.type == MOUSEBUTTONDOWN:                       # Check for mouse button down
                    if quit_buttonRect.collidepoint(event.pos):         # Check if Quit button is clicked
                        basic.terminate()                               # basic.terminate
                    if return_menu_button_rect.collidepoint(event.pos):   # Check if return button is clicked
                        from main import SpaceShooterGame                 # Import start function from main
                        game_instance = SpaceShooterGame()  # Create a class instance
                        game_instance.start()               # Start the game

    def show_game_over_menu(self, score, top_score):        # Function to show the game over screen
        play_again_button = pygame.Rect(350, 400, 300, 50)              # Define Play Again button rectangle
        return_menu_button_rect = pygame.Rect(400, 500, 200, 50)        # Define return menu button
        quit_button = pygame.Rect(400, 600, 200, 50)                    # Define Quit button rectangle
        self.game_over_sound.play()                                     # Play the game over sound

        while True:
            for event in pygame.event.get():                            # Handle events
                if event.type == QUIT:                                  # Check for quit event
                    basic.terminate()                                   # basic.terminate if quit

                if event.type == MOUSEBUTTONDOWN:                       # Check for mouse button down
                    if play_again_button.collidepoint(event.pos):       # Check if Play Again button is clicked
                        self.game_over_sound.stop()
                        return True                                     # Return True to play again
                    elif quit_button.collidepoint(event.pos):           # Check if Quit button is clicked
                        basic.terminate()                               # basic.terminate
                    elif return_menu_button_rect.collidepoint(event.pos): # Check if return button is clicked
                        self.game_over_sound.stop()
                        from main import SpaceShooterGame          # Import start function from main
                        game_instance = SpaceShooterGame()         # Create a class instance
                        game_instance.start()                      # Start the game
            transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))  # Create a transparent surface
            transparent_surface.set_alpha(10)                                  # Set alpha for transparency
            transparent_surface.fill((220, 220, 220))                         # Fill with a color

            window_surface.blit(transparent_surface, (0, 0))                                                                                                       # Blit the transparent surface
            basic.draw_text('Game Over!', font, window_surface, window_surface.get_width() // 2  - (font.size("Game Over!")[0] // 2), 150)                         # Draw Game Over text
            basic.draw_text(f'Your Score: {score}', small_font, window_surface, window_surface.get_width() // 2  - (font.size("Game Over!")[0] // 2), 200)         # Draw score text
            basic.draw_text('Top Score: %s' % (top_score), small_font, window_surface, window_surface.get_width() // 2  - (font.size("Game Over!")[0] // 2), 250)  # Draw top score.
            basic.draw_button(play_again_button, 'Play Again', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw Play Again button
            basic.draw_button(return_menu_button_rect, 'Menu', BUTTONCOLOR, BUTTONOVERCOLOR) # Draw return button
            basic.draw_button(quit_button, 'Quit', QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR)     # Draw Quit button

            pygame.display.update()                                    # Update display
            main_clock.tick(60)                                        # Control frame rate