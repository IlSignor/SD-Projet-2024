import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 1000
WINDOWHEIGHT = 800

TEXTCOLOR = (0, 0, 0)
BUTTONTEXTCOLOR = (255, 255, 255)

FPS = 60

BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
PLAYERMOVERATE = 5

# Classe pour gérer l'explosion
class Explosion:
    def __init__(self, position):
        self.sprite_sheet = pygame.image.load('explosions.png').convert_alpha()  # Charge la sprite sheet
        self.frames = self.extract_frames(self.sprite_sheet, frame_width=30, frame_height=120, num_frames=5)  # Changez les dimensions et le nombre de frames selon l'image
        self.index = 0
        self.rect = self.frames[self.index].get_rect(center=position)
        self.finished = False

    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            # Découpe chaque image de la sprite sheet
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def update(self):
        self.index += 1
        if self.index >= len(self.frames):
            self.finished = True
        else:
            self.rect = self.frames[self.index].get_rect(center=self.rect.center)  # Mettre à jour la position de l'explosion

    def draw(self, surface):
        if not self.finished:
            surface.blit(self.frames[self.index], self.rect)


# Fonction pour gérer l'explosion
def trigger_explosion(explosions, position):
    explosions.append(Explosion(position))
    
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return b  # Retourne le baddie en collision
    return None  # Aucune collision trouvée


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def shoot(playerRect):
    # create a new shot in the center of the player
    bullet = pygame.Rect(playerRect.centerx - 2, playerRect.top - 10, 5, 10)  # Tir étroit
    bullets.append(bullet)

def move_bullets():
    for bullet in bullets[:]:
        bullet.y -= 10  # Goes up by 10 pixels per frame
        if bullet.bottom < 0:
            bullets.remove(bullet)  # Remove of bullet is out of the screen
            
def check_bullet_hits(baddies, explosions):
    for baddie in baddies[:]:
        for bullet in bullets[:]:
            if bullet.colliderect(baddie['rect']):
                # Ajout d'une explosion quelle que soit la taille
                trigger_explosion(explosions, baddie['rect'].center)  # Ajout de l'explosion
                
                if baddie['rect'].width <= 30 and baddie['rect'].height <= 30:
                    baddies.remove(baddie)  # Supprimer le baddie si de taille acceptable
                
                bullets.remove(bullet)  # Supprimer la balle
                break  # Sortir de la boucle des balles pour éviter de modifier la liste pendant l'itération
                 
   
def draw_lives(surface, lives, smallPlayerImage, smallPlayerImageGray, isGameOver):
    for i in range(3):
        if isGameOver==True:
            surface.blit(smallPlayerImageGray, (500 + i * 45, 10))
        else:
            if i < lives:
                surface.blit(smallPlayerImage, (500 + i * 45, 10))
            else:
                surface.blit(smallPlayerImageGray, (500 + i * 45, 10))

def clear_lives_area(surface, backgroundImage):
    lives_area = pygame.Rect(500, 10, 3 * 45, 30)
    surface.blit(backgroundImage, (500, 10), lives_area)


#choose the difficulty:
def drawButton(buttonRect, text, color, hoverColor):
    mousePos = pygame.mouse.get_pos()
    if buttonRect.collidepoint(mousePos):
        pygame.draw.rect(windowSurface, hoverColor, buttonRect)
    else:
        pygame.draw.rect(windowSurface, color, buttonRect)

    # Add text on the button
    buttonFont = pygame.font.SysFont(None, 40)
    textSurf = buttonFont.render(text, True, BUTTONTEXTCOLOR)
    textRect = textSurf.get_rect(center=buttonRect.center)
    windowSurface.blit(textSurf, textRect)

def showDifficultyMenu():
    # Couleurs des boutons
    BUTTONCOLOR = (100, 200, 255)
    BUTTONHOVERCOLOR = (150, 220, 255)
    QUITBUTTONCOLOR = (255, 100, 100)
    QUITBUTTONHOVERCOLOR = (255, 150, 150)
    
    # Définition des boutons avec leurs coordonnées
    easyButton = pygame.Rect(300, 200, 200, 50)
    mediumButton = pygame.Rect(300, 300, 200, 50)
    hardButton = pygame.Rect(300, 400, 200, 50)
    quitButton = pygame.Rect(300, 500, 200, 50)

    while True:

        # Gère les événements utilisateur
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == MOUSEBUTTONDOWN:
                if easyButton.collidepoint(event.pos):
                    return 'easy'
                elif mediumButton.collidepoint(event.pos):
                    return 'medium'
                elif hardButton.collidepoint(event.pos):
                    return 'hard'
                elif quitButton.collidepoint(event.pos):  # Si le bouton "Quitter" est cliqué
                    terminate()
                    
        # Dessine les boutons
        drawButton(easyButton, 'Facile', BUTTONCOLOR, BUTTONHOVERCOLOR)
        drawButton(mediumButton, 'Moyen', BUTTONCOLOR, BUTTONHOVERCOLOR)
        drawButton(hardButton, 'Difficile', BUTTONCOLOR, BUTTONHOVERCOLOR)
        drawButton(quitButton, 'Quitter', QUITBUTTONCOLOR, QUITBUTTONHOVERCOLOR)
        
        pygame.display.update()
        mainClock.tick(FPS)

def move_health_items():
    for item in healthItems[:]:
        item['rect'].y += item['speed']
        if item['rect'].top > WINDOWHEIGHT:
            healthItems.remove(item)

def check_health_item_collision(playerRect):
    global lives
    for item in healthItems[:]:
        if playerRect.colliderect(item['rect']):
            if lives < 3:
                lives += 1
            healthItems.remove(item)

def showCharacterSelectionMenu():
    selectedCharacterIndex = 0
    numCharacters = len(characterImages)

    # Définir le bouton Quitter
    quitButtonRect = pygame.Rect(400, 500, 200, 50)  # Position du bouton Quitter

    while True:
        # Chargement de l'image de fond
        backgroundImage = pygame.image.load('background.jpg').convert()
        windowSurface.blit(backgroundImage, (0, 0))  # Affiche l'arrière-plan

        # Obtenir la position de la souris
        mouseX, mouseY = pygame.mouse.get_pos()

        # Afficher les personnages
        for i in range(numCharacters):
            # Vérifier si la souris est au-dessus du personnage
            isMouseOver = (
                100 + i * 150 <= mouseX <= 100 + i * 150 + 130 and
                200 <= mouseY <= 200 + 130
            )

            # Dessiner la bordure uniquement si survolé
            if isMouseOver:
                borderColor = (255, 255, 0)  # Jaune si survolé
                pygame.draw.rect(windowSurface, borderColor, (100 + i * 150, 200, 130, 130), 5)

            # Afficher l'image du personnage
            windowSurface.blit(characterImages[i], (100 + i * 150, 200))

        # Afficher les instructions
        drawText('Click on a character to select', font, windowSurface, 100, 400)

        # Dessiner le bouton Quitter
        drawButton(quitButtonRect, 'Quitter', (255, 100, 100), (255, 150, 150))

        # Mettre à jour l'affichage
        pygame.display.update()

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                # Vérifier si un personnage a été cliqué
                for i in range(numCharacters):
                    if (
                        100 + i * 150 <= mouseX <= 100 + i * 150 + 130 and
                        200 <= mouseY <= 200 + 130
                    ):
                        return i  # Retourner l'index du personnage sélectionné

                # Vérifier si le bouton "Quitter" a été cliqué
                if quitButtonRect.collidepoint(mouseX, mouseY):
                    terminate()  # Fermer le jeu si le bouton Quitter est cliqué


def pause_menu():
    # Définir le bouton Quitter
    quitButtonRect = pygame.Rect((WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) + 50, 200, 50)  # Position du bouton Quitter

    waitingForUnpause = True
    while waitingForUnpause:
        # Créer une surface semi-transparente pour le fond
        transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
        transparent_surface.set_alpha(10)  # Opacité de 0 (transparent) à 255 (opaque)
        transparent_surface.fill((220, 220, 220))  # Couleur grise (vous pouvez changer la couleur)

        # Afficher l'image de fond semi-transparente
        windowSurface.blit(transparent_surface, (0, 0))

        # Afficher les textes "Paused" et "Press ESC to resume"
        drawText('Paused', font, windowSurface, (WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) - 100)
        drawText('Press ESC to resume.', font, windowSurface, (WINDOWWIDTH / 2) - 150, (WINDOWHEIGHT / 2))

        # Dessiner le bouton "Quitter"
        drawButton(quitButtonRect, 'Quitter', (255, 100, 100), (255, 150, 150))

        # Mettre à jour l'affichage
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()  # Fermer le jeu
            if event.type == KEYDOWN:
                # Vérifier si la touche pressée est "ESC"
                if event.key == pygame.K_ESCAPE:
                    waitingForUnpause = False  # Reprendre le jeu si ESC est appuyé
            if event.type == MOUSEBUTTONDOWN:
                # Obtenir la position de la souris
                mouseX, mouseY = pygame.mouse.get_pos()

                # Vérifier si le bouton "Quitter" a été cliqué
                if quitButtonRect.collidepoint(mouseX, mouseY):
                    terminate()  # Fermer le jeu si le bouton Quitter est cliqué


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

#set up bullets
bullets = [] #list to store player's shots

# Set up health items
healthItems = []  # Initialize health items list

#set up explosions
explosions = []

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images.
characterImages = [
    pygame.image.load('player1.png'),
    pygame.image.load('player2.png'),
    pygame.image.load('player3.png'),
    pygame.image.load('player4.png'),
    pygame.image.load('player5.png'),
    pygame.image.load('player6.png')
]


baddieImage = pygame.image.load('baddie.png')
healthItemImage = pygame.image.load('cherry.png')

backgroundImage = pygame.image.load('background.jpg').convert()


# Show the "Start" screen.
windowSurface.blit(backgroundImage, (0, 0))  # Affiche l'image de fond à partir du coin supérieur gauche

pygame.display.update()


topScore = 0
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)

# Show character selection menu
selectedCharacterIndex = showCharacterSelectionMenu()
playerImage = characterImages[selectedCharacterIndex]  # Set player image based on selection
playerRect = playerImage.get_rect()  # Get the rectangle for the player

smallPlayerImage = pygame.transform.scale(playerImage, (30, 30)) 
smallPlayerImageGray = pygame.Surface((30, 30))
smallPlayerImageGray.blit(smallPlayerImage, (0, 0))
smallPlayerImageGray.set_alpha(100)

windowSurface.blit(backgroundImage, (0, 0))  # Affiche l'image de fond à partir du coin supérieur gauche

difficulty = showDifficultyMenu()
if difficulty == 'easy':
    BADDIEMINSPEED = 1
    BADDIEMAXSPEED = 4
    ADDNEWBADDIERATE = 12
elif difficulty == 'medium':
    BADDIEMINSPEED = 2
    BADDIEMAXSPEED = 6
    ADDNEWBADDIERATE = 8
elif difficulty == 'hard':
    BADDIEMINSPEED = 4
    BADDIEMAXSPEED = 8
    ADDNEWBADDIERATE = 6

windowSurface.blit(backgroundImage, (0, 0))  # Affiche l'image de fond à partir du coin supérieur gauche


while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    lives = 3

    
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
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
                    shoot(playerRect) #shoot if the player click space                  
                if event.key == K_ESCAPE:  # Check for "P" key to pause the game
                    pause_menu()  # Call the pause menu function

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
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize),  random.randint(50, 150) - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)
        
        if random.randint(1, 1000) <= 1:  # 5% de chance de spawn
            itemRect = pygame.Rect(random.randint(0, WINDOWWIDTH - 30), 0, 30, 30)
            healthItems.append({'rect': itemRect, 'speed': random.randint(2, 5)})

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the baddies down.
        for b in baddies:
            b['rect'].move_ip(0, b['speed'])
            
        # Déplacer les items de soin vers le bas
        move_health_items()

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
        
            
        move_bullets()  # Displace the shots
        check_bullet_hits(baddies, explosions)
        
        for explosion in explosions[:]:
            explosion.update()
            if explosion.finished:
                explosions.remove(explosion)

        for explosion in explosions:
            explosion.draw(windowSurface)
            
        move_health_items()
        check_health_item_collision(playerRect)

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

    
    waitingForKeyPress = True
    while waitingForKeyPress:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                waitingForKeyPress = False
                gameOverSound.stop()