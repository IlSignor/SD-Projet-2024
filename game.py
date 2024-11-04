#importations of the modulus and files
import pygame, random
from pygame.locals import *
from definition import*

#################################       Game defintion         #############################################

def game(HEALTHHAPPEND, heal_animation, fire_animation, playerRect, bullets, windowSurface, ADDNEWBADDIERATE, BADDIEMINSPEED, BADDIEMAXSPEED, baddieImage, healthItems, healthItemImage, backgroundImage, font, smallFont, smallPlayerImage, smallPlayerImageGray, playerImage, explosions, gameOverSound, topScore):
    while True:                            # Main game loop
        # Initialize game variables.
        baddies = []                       # List to hold baddie objects.
        score = 0                          # Player's score.
        lives = 3                          # Player's lives.
        heal_animation = None               # Healing animation.

        # Set player position at the bottom center of the window.
        playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 120)
        moveLeft = moveRight = False       # Movement flags for player.
        baddieAddCounter = 0                # Counter to control baddie spawning.
        pygame.mixer.music.play(-1, 0.0)   # Play background music in a loop.

        while True:                        # The game loop runs while the game is active.
            score += 1                     # Increment score.

            for event in pygame.event.get():  # Event handling.
                if event.type == QUIT:
                    terminate()              # Close the game.

                if event.type == KEYDOWN:  # Key pressed event.
                    if event.key == K_LEFT or event.key == K_a:  # Move left.
                        moveRight = False
                        moveLeft = True
                    if event.key == K_RIGHT or event.key == K_d:  # Move right.
                        moveLeft = False
                        moveRight = True
                    if event.key == K_SPACE:  # Shoot when space is pressed.
                        shoot(playerRect, bullets) 
                    if event.key == K_ESCAPE:  # Open pause menu.
                        pause_menu(windowSurface, font)

                if event.type == KEYUP:     # Key released event.
                    if event.key == K_LEFT or event.key == K_a:
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == K_d:
                        moveRight = False

            # Add new baddies at the top of the screen, if needed.
            baddieAddCounter += 1              # Increment counter for baddie spawning.
            if baddieAddCounter == ADDNEWBADDIERATE:  # Check if it's time to add a new baddie.
                baddieAddCounter = 0            # Reset the counter.
                baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)  # Randomize baddie size.
                # Create a new baddie object.
                newBaddie = {
                    'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 100 - baddieSize, baddieSize, baddieSize),
                    'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                    'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                }
                baddies.append(newBaddie)      # Add the new baddie to the list.

            # Randomly spawn health items.
            if random.randint(1, HEALTHHAPPEND) <= 1:  # 5% chance to spawn health item.
                itemRect = pygame.Rect(random.randint(0, WINDOWWIDTH - 30), 0, 30, 30)  # Create item rectangle.
                healthItems.append({'rect': itemRect, 'speed': random.randint(2, 5)})  # Add to health items list.

            # Move the player around based on input.
            if moveLeft and playerRect.left > 0:  # Move left if within bounds.
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)  # Move player left.
            if moveRight and playerRect.right < WINDOWWIDTH:  # Move right if within bounds.
                playerRect.move_ip(PLAYERMOVERATE, 0)  # Move player right.

            # Move the baddies down the screen.
            for b in baddies:
                b['rect'].move_ip(0, b['speed'])  # Move each baddie down based on its speed.
                
            # Move health items down the screen.
            move_health_items(healthItems)

            # Display each health item.
            for item in healthItems:
                windowSurface.blit(healthItemImage, item['rect'])  # Draw health item.

            # Delete baddies that have fallen past the bottom.
            for b in baddies[:]:
                if b['rect'].top > WINDOWHEIGHT:  # If baddie is off screen.
                    baddies.remove(b)              # Remove it from the list.

            # Draw the game world on the window.
            windowSurface.blit(backgroundImage, (0, 0))  # Draw background image at the top left.

            # Draw the score and top score.
            drawText('Score: %s' % (score), smallFont, windowSurface, 750, 0)  # Draw current score.
            drawText('Top Score: %s' % (topScore), smallFont, windowSurface, 10, 0)  # Draw top score.
            draw_lives(windowSurface, lives, smallPlayerImage, smallPlayerImageGray, isGameOver=False)  # Display lives.
            windowSurface.blit(playerImage, playerRect)  # Draw the player's rectangle.

            # Draw each baddie.
            for b in baddies:
                windowSurface.blit(b['surface'], b['rect'])  # Draw baddie.

            move_bullets(bullets)  # Move the bullets.
            score = check_bullet_hits(baddies, explosions, score, bullets)  # Check for bullet hits.

            fire_animation.update()  # Update fire animation.
            fire_animation.draw(windowSurface, playerRect)  # Draw fire animation on player.

            # Manage explosions.
            for explosion in explosions[:]:
                explosion.update()  # Update each explosion.
                if explosion.finished:  # Check if explosion is finished.
                    explosions.remove(explosion)  # Remove it if done.

            for explosion in explosions:
                explosion.draw(windowSurface)  # Draw each explosion.
                
            move_health_items(healthItems)  # Move health items down.
            lives, heal_animation = check_health_item_collision(playerRect, healthItems, lives, heal_animation)  # Check for collisions with health items.

            if heal_animation is not None:  # If there is an active heal animation.
                heal_animation.update()  # Update the healing animation.
                heal_animation.draw(windowSurface, playerRect)  # Draw healing animation on player.
            
            for item in healthItems:
                windowSurface.blit(healthItemImage, item['rect'])  # Draw health items.

            # Draw the shots.
            for bullet in bullets:
                pygame.draw.rect(windowSurface, (255, 0, 0), bullet)  # Draw red bullets.
            
            pygame.display.update()  # Update the display.

            hitBaddie = playerHasHitBaddie(playerRect, baddies)  # Check for collision with baddies.

            if playerRect.topleft < (0, 0):  # Check if player is off screen.
                break  # End the game loop.
            
            if hitBaddie:  # If a collision has occurred.
                lives -= 1  # Decrease lives.
                trigger_explosion(explosions, hitBaddie['rect'].center)  # Trigger explosion at collision point.
                baddies.remove(hitBaddie)  # Remove the hit baddie.
                if lives <= 0:  # If no lives left.
                    playerRect.topleft = (-10000, -10000)  # Move player off-screen.
                    if score > topScore:  # If the score beats the top score.
                        topScore = score  # Update the top score.

            mainClock.tick(FPS)  # Control the frame rate.

        # Stop the game and show the "Game Over" screen.
        pygame.mixer.music.stop()  # Stop the background music.
        gameOverSound.play()  # Play game over sound.
        clear_lives_area(windowSurface, backgroundImage)  # Clear the area showing lives.

        # Draw game over information.
        draw_lives(windowSurface, lives, smallPlayerImage, smallPlayerImageGray, isGameOver=True)  # Show lives.

        pygame.display.update()  # Update display after drawing.

        show_game_over_menu(windowSurface, score, font, smallFont, topScore)  # Show game over menu.

