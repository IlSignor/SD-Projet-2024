import pygame, random
from pygame.locals import *
from definition import*


def game(HEALTHHAPPEND, heal_animation, fire_animation, playerRect, bullets, windowSurface, ADDNEWBADDIERATE,BADDIEMINSPEED,BADDIEMAXSPEED,baddieImage,healthItems,healthItemImage,backgroundImage,font, smallPlayerImage, smallPlayerImageGray, playerImage, explosions, gameOverSound, topScore):
    while True:
        # Set up the start of the game.
        baddies = []
        score = 0
        lives = 3
        heal_animation = None
        
        playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 120)
        moveLeft = moveRight = False
        baddieAddCounter = 0
        pygame.mixer.music.play(-1, 0.0)

        while True: # The game loop runs while the game part is playing.
            score += 1 # Increase score.
            
            for event in pygame.event.get():

                if event.type == QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    if event.key == K_LEFT or event.key == K_a:
                        moveRight = False
                        moveLeft = True
                    if event.key == K_RIGHT or event.key == K_d:
                        moveLeft = False
                        moveRight = True
                    if event.key == K_SPACE:
                        shoot(playerRect, bullets) #shoot if the player click space                  
                    if event.key == K_ESCAPE:  # Check for "escape" key to pause the game
                        pause_menu(windowSurface, font)
                        
                if event.type == KEYUP:                  
                    if event.key == K_LEFT or event.key == K_a:
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == K_d:
                        moveRight = False

            # Add new baddies at the top of the screen, if needed.
            baddieAddCounter += 1
            if baddieAddCounter == ADDNEWBADDIERATE:
                baddieAddCounter = 0
                baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
                newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 100 - baddieSize, baddieSize, baddieSize),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                            }

                baddies.append(newBaddie)
            
            if random.randint(1, HEALTHHAPPEND) <= 1:  # 5% de chance de spawn
                itemRect = pygame.Rect(random.randint(0, WINDOWWIDTH - 30), 0, 30, 30)
                healthItems.append({'rect': itemRect, 'speed': random.randint(2, 5)})

            # Move the player around.
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if moveRight and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)

            # Move the baddies down.
            for b in baddies:
                b['rect'].move_ip(0, b['speed'])
                
            # Déplacer les items de soin vers le bas
            move_health_items(healthItems)

            # Afficher chaque item de soin
            for item in healthItems:
                windowSurface.blit(healthItemImage, item['rect'])


            # Delete baddies that have fallen past the bottom.
            for b in baddies[:]:
                if b['rect'].top > WINDOWHEIGHT:
                    baddies.remove(b)




            # Draw the game world on the window.
            windowSurface.blit(backgroundImage, (0, 0))  # Affiche l'image de fond à partir du coin supérieur gauche


            # Draw the score and top score.
            drawText('Score: %s' % (score), font, windowSurface, 800, 0)
            drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 0)
            draw_lives(windowSurface, lives, smallPlayerImage, smallPlayerImageGray, isGameOver=False)
            # Draw the player's rectangle.
            windowSurface.blit(playerImage, playerRect)

            # Draw each baddie.
            for b in baddies:
                windowSurface.blit(b['surface'], b['rect'])
            
                
            move_bullets(bullets)  # Displace the shots
            score = check_bullet_hits(baddies, explosions, score, bullets)

            fire_animation.update()
            fire_animation.draw(windowSurface, playerRect)
            
            for explosion in explosions[:]:
                explosion.update()
                if explosion.finished:
                    explosions.remove(explosion)

            for explosion in explosions:
                explosion.draw(windowSurface)
                
            move_health_items(healthItems)
            lives, heal_animation = check_health_item_collision(playerRect, healthItems, lives, heal_animation, windowSurface)

            if heal_animation is not None:
                heal_animation.update()
                heal_animation.draw(windowSurface, playerRect)
            
            for item in healthItems:
                windowSurface.blit(healthItemImage, item['rect'])

            # Draw the shots
            for bullet in bullets:
                pygame.draw.rect(windowSurface, (255, 0, 0), bullet)  # Red shots
            

            pygame.display.update()


            hitBaddie = playerHasHitBaddie(playerRect, baddies)  # Vérifie la collision

            if playerRect.topleft < (0, 0):
                break  # Termine la boucle de jeu
            
            if hitBaddie:  # Si une collision a eu lieu
                lives -= 1
                trigger_explosion(explosions, hitBaddie['rect'].center)
                baddies.remove(hitBaddie)  # Supprime uniquement le baddie en collision
                if lives <= 0:
                    playerRect.topleft = (-10000, -10000)
                    if score > topScore:
                        topScore = score  # Met à jour le meilleur score

            mainClock.tick(FPS)

        # Stop the game and show the "Game Over" screen.
        pygame.mixer.music.stop()
        gameOverSound.play()
        clear_lives_area(windowSurface, backgroundImage)


        draw_lives(windowSurface, lives, smallPlayerImage, smallPlayerImageGray, isGameOver=True)
        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)

        pygame.display.update()

        
        show_game_over_menu(windowSurface,score, font)        