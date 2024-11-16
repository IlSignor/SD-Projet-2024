#importations of the modulus and files
import pygame, random
from pygame.locals import *
from definition import*

#################################       Game defintion         #############################################


def game(BUTTONCOLOR, BUTTONOVERCOLOR, QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR,                                                    # Button color constants
        HEALTHHAPPEND, ADDNEWcometRATE, cometMINSPEED, cometMAXSPEED,                                                        # comet and health constants
        comet_image, health_item_image, background_image,                                                                      # comet, health and background images
        small_player_image, small_player_image_gray, player_image, player_image_left, player_image_right,                       # Player images management
        player_rect, window_surface,                                                                                            # Surfaces management
        font, small_font, top_score):                                                                                           # font management
           
    
    game_over_sound = pygame.mixer.Sound('sounds/gameover.mp3')  # Load game over sound.
    pygame.mixer.music.load('sounds/background.mid')      # Load background music.

    while True:                            # Main game loop
        # Initialize game variables.
        comets = []                       # List to hold comet objects.
        bullets = []                       # List to hold bullets.
        health_items = []                  # List to hold health items.
        explosions = []                    # List to hold explosions.
        score = 0                          # Player's score.
        lives = 3                          # Player's lives.
        heal_animation = None              # Healing animation.
        rotation = "None"                  # The player doesn't rotate
        fire_animation = FireAnimation()   # Create fire animation object.

        # Set player position at the bottom center of the window.
        player_rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 150)
        move_left = move_right = False     # Movement flags for player.
        comet_add_counter = 0             # Counter to control comet spawning.
        pygame.mixer.music.play(-1, 0.0)   # Play background music in a loop.

        while True:                           # The game loop runs while the game is active.
            score += 1                        # Increment score.
            for event in pygame.event.get():  # Event handling.
                if event.type == QUIT:
                    terminate()               # Close the game.

                if event.type == KEYDOWN:     # Key pressed event.
                    if event.key == K_LEFT or event.key == K_a:  # Move left.
                        move_right = False
                        move_left = True
                        
                    if event.key == K_RIGHT or event.key == K_d:  # Move right.
                        move_left = False
                        move_right = True

                    if event.key == K_SPACE:  # Shoot when space is pressed.
                        shoot(player_rect, bullets) 
                    if event.key == K_ESCAPE:  # Open pause menu.
                        pause_menu(window_surface, font, BUTTONCOLOR, BUTTONOVERCOLOR, QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR)

                if event.type == KEYUP:     # Key released event.
                    rotation = "None"  # The player doesn't rotate
                    if event.key == K_LEFT or event.key == K_a:
                        move_left = False
                    if event.key == K_RIGHT or event.key == K_d:
                        move_right = False

            # Add new comets at the top of the screen, if needed.
            comet_add_counter += 1              # Increment counter for comet spawning.
            if comet_add_counter == ADDNEWcometRATE:  # Check if it's time to add a new comet.
                comet_add_counter = 0            # Reset the counter.
                comet_size = random.randint(20, 60)  # Randomize comet size.
                # Create a new comet object.
                new_comet = {
                    'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - comet_size), 100 - comet_size, comet_size, comet_size),
                    'speed': random.randint(cometMINSPEED, cometMAXSPEED),
                    'surface': pygame.transform.scale(comet_image, (comet_size, comet_size)),
                }
                comets.append(new_comet)      # Add the new comet to the list.

            # Randomly spawn health items.
            if random.randint(1, HEALTHHAPPEND) <= 1:  # 5% chance to spawn health item.
                item_rect = pygame.Rect(random.randint(0, WINDOWWIDTH - 30), 30, 30, 30)  # Create item rectangle.
                health_items.append({'rect': item_rect, 'speed': random.randint(2, 5)})  # Add to health items list.

            # Move the player around based on input.
            if move_left and player_rect.left > 0:  # Move left if within bounds.
                player_rect.move_ip(-1 * PLAYERMOVERATE, 0)  # Move player left.
                rotation = "Left"                         # The player rotate left
            if move_right and player_rect.right < WINDOWWIDTH:  # Move right if within bounds.
                player_rect.move_ip(PLAYERMOVERATE, 0)  # Move player right.
                rotation = "Right"                         # The player rotate right

            # Move the comets down the screen.
            for b in comets:
                b['rect'].move_ip(0, b['speed'])  # Move each comet down based on its speed.
                
            # Move health items down the screen.
            move_health_items(health_items)

            # Display each health item.
            for item in health_items:
                window_surface.blit(health_item_image, item['rect'])  # Draw health item.

            # Delete comets that have fallen past the bottom.
            for b in comets[:]:
                if b['rect'].top > WINDOWHEIGHT:  # If comet is off screen.
                    comets.remove(b)              # Remove it from the list.

            # Draw the game world on the window.
            window_surface.blit(background_image, (0, 0))  # Draw background image at the top left.

            # Draw the score and top score.
            banner = pygame.Surface((1000, 50))                     # Create a surface with 1000X50 pixels for the banner
            banner.fill((0, 0, 0))                            # Fill the banner
            window_surface.blit(banner, (0, 0))                      # Draw the banner
            draw_text('Score: %s' % (score), small_font, window_surface, 750, 10)  # Draw current score.
            draw_text('Top Score: %s' % (top_score), small_font, window_surface, 10, 10)  # Draw top score.
            draw_lives(window_surface, lives, small_player_image, small_player_image_gray, is_game_over=False)  # Display lives.
            
            if rotation == "None":                                  # If the player doesn't rotate
                window_surface.blit(player_image, player_rect)         # Print the player normal image
            elif rotation == "Right":                               # If the player rotate right
                window_surface.blit(player_image_right, player_rect)    # Print the player right image
            if rotation == "Left":                                  # If the player rotate left
                window_surface.blit(player_image_left, player_rect)     # Print the player left image

            # Draw each comet.
            for b in comets:
                window_surface.blit(b['surface'], b['rect'])  # Draw comet.

            move_bullets(bullets)  # Move the bullets.
            score = check_bullet_hits(comets,comet_image, explosions, score, bullets)  # Check for bullet hits.

            fire_animation.update()  # Update fire animation.
            fire_animation.draw(window_surface, player_rect)  # Draw fire animation on player.

            # Manage explosions.
            for explosion in explosions[:]:
                explosion.update()  # Update each explosion.
                if explosion.finished:  # Check if explosion is finished.
                    explosions.remove(explosion)  # Remove it if done.

            for explosion in explosions:
                explosion.draw(window_surface)  # Draw each explosion.
                
            move_health_items(health_items)  # Move health items down.
            lives, heal_animation = check_health_item_collision(player_rect, health_items, lives, heal_animation)  # Check for collisions with health items.

            if heal_animation is not None:  # If there is an active heal animation.
                heal_animation.update()  # Update the healing animation.
                heal_animation.draw(window_surface, player_rect)  # Draw healing animation on player.
            
            for item in health_items:
                window_surface.blit(health_item_image, item['rect'])  # Draw health items.

            # Draw the shots.
            for bullet in bullets:
                pygame.draw.rect(window_surface, (255, 0, 0), bullet)  # Draw red bullets.
            
            pygame.display.update()  # Update the display.

            hit_comet = playerHashit_comet(player_rect, comets)  # Check for collision with comets.

            if player_rect.topleft < (0, 0):  # Check if player is off screen.
                break  # End the game loop.
            
            if hit_comet:  # If a collision has occurred.
                lives -= 1  # Decrease lives.
                trigger_explosion(explosions, hit_comet['rect'].center)  # Trigger explosion at collision point.
                comets.remove(hit_comet)  # Remove the hit comet.
                if lives <= 0:  # If no lives left.
                    player_rect.topleft = (-10000, -10000)  # Move player off-screen.
                    if score > top_score:  # If the score beats the top score.
                        top_score = score+1  # Update the top score.

            main_clock.tick(FPS)  # Control the frame rate.

        # Stop the game and show the "Game Over" screen.
        pygame.mixer.music.stop()  # Stop the background music.
        game_over_sound.play()  # Play game over sound.

        # Draw game over information.
        draw_lives(window_surface, lives, small_player_image, small_player_image_gray, is_game_over=True)  # Show lives.

        pygame.display.update()  # Update display after drawing.

        show_game_over_menu(window_surface, score, font, small_font, top_score, BUTTONCOLOR, BUTTONOVERCOLOR, QUITBUTTONCOLOR, QUITBUTTONOVERCOLOR, game_over_sound)  # Show game over menu.