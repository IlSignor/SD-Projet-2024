#################################       This file defines the main class that runs the game         #############################################

#importations of the modulus and files
import pygame, random
from pygame.locals import *
from definitions import*

#################################       Game defintion         #############################################

class SpaceShooterGame:
    def __init__(self):
        # Initialize pygame and set up the window, fonts, and other necessary elements (images, ...)
        
        self.character_images_selection = [pygame.image.load(f'playersselection/player{i}.png') for i in range(1, 7)]
        self.character_images = [pygame.image.load(f'players/player{i}.png') for i in range(1, 7)]
        self.character_image_right = pygame.image.load('players/playersleft.png')
        self.character_image_left = pygame.image.load('players/playersright.png')
        
        self.comet_image = pygame.image.load('comet.png')
        self.health_item_image = pygame.transform.scale(pygame.image.load('live.png'), (25, 25))
        self.background_image = pygame.transform.scale(pygame.image.load('background.jpg').convert(), (WINDOWWIDTH, WINDOWHEIGHT))
        self.background_start = pygame.transform.scale(pygame.image.load('background_start.jpg').convert(), (WINDOWWIDTH, WINDOWHEIGHT))
        
        self.top_score = 0
        
        self.player_image_right = pygame.transform.scale(self.character_image_right, (60, 120))  # Set player image based on selection.
        self.player_image_left = pygame.transform.scale(self.character_image_left, (60, 120))  # Set player image based on selection.
        self.player_rect = pygame.transform.scale(self.character_images_selection[0], (80, 120)).get_rect()


    def start(self):  # Method to start the game (launcher)
        
        # Show the "Start" screen
        
        window_surface.blit(self.background_image, (0, 0))  # Display background image at the top left
        pygame.display.update()                             # Update the display

        # Show character selection menu

        global selected_character_index                     # Global use of selected_character_index  
        
        selected_character = ShowMenu()                                                                                 # Display character selection
        selected_character_index = selected_character.show_character_selection_menu(self.character_images_selection)    # Give an attribute to selected_character_index  
        
        player_image = pygame.transform.scale(self.character_images[selected_character_index], (80, 120))               # Use the right player image

        # Show difficulty selection
        index_difficulty = ShowMenu()
        difficulty = index_difficulty.show_difficulty_menu()        # Choose the difficulty level
        
        if difficulty == 'easy':  # If difficulty is easy:
            COMETMINSPEED = 1     # Set minimum comet speed
            COMETMAXSPEED = 4     # Set maximum comet speed
            ADDNEWCOMETRATE = 12  # Set rate of adding new comets
            HEALTHHAPPEND = 100   # Set health item appearance rate
            ALIENHAPPEND = 500    # set rate of adding aliens
            
        elif difficulty == 'medium':  # If difficulty is medium:
            COMETMINSPEED = 2         # Set minimum comet speed
            COMETMAXSPEED = 6         # Set maximum comet speed
            ADDNEWCOMETRATE = 8       # Set rate of adding new comets
            HEALTHHAPPEND = 1000      # Set health item appearance rate
            ALIENHAPPEND = 300        # set rate of adding aliens
            
        elif difficulty == 'hard':  # If difficulty is hard:
            COMETMINSPEED = 4       # Set minimum comet speed
            COMETMAXSPEED = 8       # Set maximum comet speed
            ADDNEWCOMETRATE = 6     # Set rate of adding new comets
            HEALTHHAPPEND = 10000   # Set health item appearance rate
            ALIENHAPPEND = 200      # set rate of adding aliens

        window_surface.blit(self.background_image, (0, 0))  # Display background image at the top left

        SpaceShooterGame.game_loop(self, HEALTHHAPPEND, ADDNEWCOMETRATE, COMETMINSPEED, COMETMAXSPEED, ALIENHAPPEND, player_image)    #launch the game loop                                                                         
 
    def game_loop(self, HEALTHHAPPEND, ADDNEWCOMETRATE, COMETMINSPEED, COMETMAXSPEED, ALIENHAPPEND, player_image):      # Main loop of the game (game loop)
            
        pygame.init()
        pygame.display.set_caption('Space Shooter')  # Set the window title
        
        while True:                                  # Main game loop
            # Initialize game variables.
            PLAYERMOVERATE = 5 
            bullets = []                            # List to hold bullets
            comets = []                             # List to hold comets
            aliens = []                             # List to hold aliens
            health_items = []                       # List to hold health items
            explosions = []                         # List to hold explosions
            score = 0                               # Player's score
            lives = 3                               # Player's lives
            heal_animation = None                   # Healing animation
            rotation = "None"                       # The player doesn't rotate
            fire_animation = FireAnimation()        # Create fire animation object
            health_lives = HealthLives()            # Assign the class health_lives to a variable
            explosion_bullets = ExplosionBullets()  # Assign the class explosion_bullets to a variable

            pygame.mixer.music.load('sounds/background.mp3')      # Load background music

            # Set player position at the bottom center of the window.
            self.player_rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 150)
            move_left = move_right = False     # Movement flags for player
            comet_add_counter = 0              # Counter to control comet spawning
            pygame.mixer.music.play(-1, 0.0)   # Play background music in a loop

            while True:                           # The game loop runs while the game is active
                score += 1                        # Increment score
                for event in pygame.event.get():  # Event handling
                    if event.type == QUIT:
                        basic.terminate()               # Close the game

                    if event.type == KEYDOWN:                        # Key pressed event
                        if event.key == K_LEFT or event.key == K_a:  # Move left
                            move_right = False
                            move_left = True
                            
                        if event.key == K_RIGHT or event.key == K_d:  # Move right
                            move_left = False
                            move_right = True

                        if event.key == K_SPACE:  # Shoot when space is pressed
                            explosion_bullets.shoot(self.player_rect, bullets) 
                            
                        if event.key == K_ESCAPE:  # Open pause menu
                            pause = ShowMenu()
                            pause.pause_menu()

                    if event.type == KEYUP:     # Key released event
                        rotation = "None"       # The player doesn't rotate
                        if event.key == K_LEFT or event.key == K_a:
                            move_left = False
                        if event.key == K_RIGHT or event.key == K_d:
                            move_right = False

                # Add new comets at the top of the screen, if needed
                comet_add_counter += 1                    # Increment counter for comet spawning
                if comet_add_counter == ADDNEWCOMETRATE:  # Check if it's time to add a new comet
                    comet_add_counter = 0                 # Reset the counter
                    comet_size = random.randint(20, 60)   # Randomize comet size
                    # Create a new comet object
                    new_comet = {
                        'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - comet_size), 100 - comet_size, comet_size, comet_size),
                        'speed': random.randint(COMETMINSPEED, COMETMAXSPEED),
                        'surface': pygame.transform.scale(self.comet_image, (comet_size, comet_size)),
                    }
                    comets.append(new_comet)      # Add the new comet to the list
                
                # Randomly spawn aliens
                
                if random.randint(1, ALIENHAPPEND) == 1:  # Adjust the spawn rate (1 in 200 chance per frame)
                    alien_size = 50                       # Fixed size for aliens
                    new_alien = {
                        'rect': pygame.Rect(self.player_rect.centerx-40, 100-alien_size, alien_size, alien_size),
                        'speed': 5,  # Alien speed
                        'surface': pygame.transform.scale(pygame.image.load('alien.png'), (alien_size, alien_size)),
                        'lives': 3
                    }
                    aliens.append(new_alien)      # Add the new alien to the list


                # Randomly spawn health items
                if random.randint(1, HEALTHHAPPEND) <= 1:                                     # Chance to spawn health item
                    item_rect = pygame.Rect(random.randint(0, WINDOWWIDTH - 30), 30, 30, 30)  # Create item rectangle
                    health_items.append({'rect': item_rect, 'speed': random.randint(2, 5)})   # Add to health items list

                # Move the player around based on input
                if move_left and self.player_rect.left > 0:           # Move left if within bounds
                    self.player_rect.move_ip(-1 * PLAYERMOVERATE, 0)  # Move player left
                    rotation = "Left"                                 # The player rotate left
                if move_right and self.player_rect.right < WINDOWWIDTH:  # Move right if within bounds
                    self.player_rect.move_ip(PLAYERMOVERATE, 0)          # Move player right.
                    rotation = "Right"                                   # The player rotate right

                # Move the comets down the screen
                for b in comets:
                    b['rect'].move_ip(0, b['speed'])  # Move each comet down based on its speed
                    
                # Move health items down the screen
                health_lives.move_health_items(health_items)

                # Display each health item
                for item in health_items:
                    window_surface.blit(self.health_item_image, item['rect'])  # Draw health item

                # Delete comets that have fallen past the bottom
                for b in comets[:]:
                    if b['rect'].top > WINDOWHEIGHT:  # If comet is off screen
                        comets.remove(b)              # Remove it from the list

                # Delete aliens that have fallen past the bottom
                for alien in aliens[:]:
                    if alien['rect'].top > WINDOWHEIGHT:    # If alien is off screen
                        aliens.remove(alien)                # Remove it from the list
                        
                # Draw the game world on the window
                window_surface.blit(self.background_image, (0, 0))  # Draw background image at the top left.

                # Draw the score and top score
                banner = pygame.Surface((1000, 50))                      # Create a surface with 1000X50 pixels for the banner
                banner.fill((0, 0, 0))                                   # Fill the banner
                window_surface.blit(banner, (0, 0))                      # Draw the banner
                basic.draw_text('Score: %s' % (score), small_font, window_surface, 750, 10)              # Draw current score
                basic.draw_text('Top Score: %s' % (self.top_score), small_font, window_surface, 10, 10)  # Draw top score
                
                health_lives.draw_lives(lives, is_game_over=False)  # Display lives
                
                if rotation == "None":                                                # If the player doesn't rotate
                    window_surface.blit(player_image, self.player_rect)               # Print the player normal image
                elif rotation == "Right":                                             # If the player rotate right
                    window_surface.blit(self.player_image_right, self.player_rect)    # Print the player right image
                if rotation == "Left":                                                # If the player rotate left
                    window_surface.blit(self.player_image_left, self.player_rect)     # Print the player left image

                # Draw each comet
                for b in comets:
                    window_surface.blit(b['surface'], b['rect'])  # Draw comet

                explosion_bullets.move_bullets(bullets)  # Move the bullets
                score = explosion_bullets.check_bullet_hits(comets,self.comet_image, explosions, score, bullets)  # Check for bullet hits comets
                explosion_bullets.check_alien_hits(aliens,explosions, bullets)  # Check for bullet hits aliens

                fire_animation.update()                                # Update fire animation
                fire_animation.draw(window_surface, self.player_rect)  # Draw fire animation on player

                # Move aliens down the screen
                explosion_bullets.move_aliens(aliens, self.player_rect)
                for alien in aliens:
                    window_surface.blit(alien['surface'], alien['rect'])

                # Manage explosions
                for explosion in explosions[:]:
                    explosion.update()                # Update each explosion
                    if explosion.finished:            # Check if explosion is finished
                        explosions.remove(explosion)  # Remove it if done

                for explosion in explosions:
                    explosion.draw(window_surface)  # Draw each explosion
                    
                health_lives.move_health_items(health_items)                                                                             # Move health items down
                lives, heal_animation = health_lives.check_health_item_collision(health_items, self.player_rect, lives, heal_animation)  # Check for collisions with health items

                if heal_animation is not None:                             # If there is an active heal animation
                    heal_animation.update()                                # Update the healing animation
                    heal_animation.draw(window_surface, self.player_rect)  # Draw healing animation on player
                
                for item in health_items:
                    window_surface.blit(self.health_item_image, item['rect'])  # Draw health items

                # Draw the shots
                for bullet in bullets:
                    pygame.draw.rect(window_surface, (255, 0, 0), bullet)  # Draw red bullets
                
                pygame.display.update()  # Update the display
                
                hit_comet = health_lives.player_hit_comet(self.player_rect, comets)  # Check for collision with comets
                hit_alien = health_lives.player_hit_comet(self.player_rect, aliens)  # Check for collision with aliens

                if self.player_rect.topleft < (0, 0):  # Check if player is off screen
                    break                              # End the game loop (game-over)
                
                if hit_comet:                                                                  # If a collision has occurred
                    lives -= 1                                                                 # Decrease lives
                    explosion_bullets.trigger_explosion(explosions, hit_comet['rect'].center)  # Trigger explosion at collision point
                    comets.remove(hit_comet)                                                   # Remove the hit comet
                    if lives <= 0:                                                             # If no lives left
                        self.player_rect.topleft = (-10000, -10000)                            # Move player off-screen
                        if score > self.top_score:                                             # If the score beats the top score
                            self.top_score = score+1                                           # Update the top score
                
                if hit_alien:                                                                  # If a collision has occurred
                    lives -= 1                                                                 # Decrease lives
                    explosion_bullets.trigger_explosion(explosions, hit_alien['rect'].center)  # Trigger explosion at collision point
                    aliens.remove(hit_alien)                                                   # Remove the hit comet
                    if lives <= 0:                                                             # If no lives left
                        self.player_rect.topleft = (-10000, -10000)                            # Move player off-screen
                        if score > self.top_score:                                             # If the score beats the top score
                            self.top_score = score+1                                           # Update the top score

                main_clock.tick(60)  # Control the frame rate.

            # Stop the game and show the "Game Over" screen
            pygame.mixer.music.stop()  # Stop the background music

            # Draw game over information
            health_lives.draw_lives(lives, is_game_over=True)  # Show lives

            pygame.display.update()                              # Update display after drawing

            gameover = ShowMenu()
            gameover.show_game_over_menu(score, self.top_score)  # Show game over menu