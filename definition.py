import pygame, random, sys
from pygame.locals import *

# Configuration de la fenêtre
WINDOWWIDTH = 1000
WINDOWHEIGHT = 800

# Couleurs
TEXTCOLOR = (0, 0, 0)
BUTTONTEXTCOLOR = (255, 255, 255)

BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
PLAYERMOVERATE=5

FPS = 60
mainClock = pygame.time.Clock()

class FireAnimation:
    def __init__(self):
        # Charger la sprite sheet et définir les paramètres
        self.sprite_sheet = pygame.image.load('rocket_fire.png').convert_alpha()
        self.frame_width = 23
        self.frame_height = 70
        self.num_columns = 5
        self.num_rows = 1
        self.frames = self.extract_frames(self.sprite_sheet, self.frame_width, self.frame_height, self.num_columns, self.num_rows)
        self.index = 0
        self.animation_speed = 5  # Vitesse de l'animation
        self.rect = self.frames[self.index].get_rect()  # Initialiser le rect

    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_columns, num_rows):
        frames = []
        for row in range(num_rows):
            for col in range(num_columns):
                frame = sprite_sheet.subsurface((col * frame_width, row * frame_height, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self):
        # Met à jour l'index de l'animation
        self.index += 1
        if self.index >= len(self.frames):
            self.index = 0  # Remet à zéro pour boucler l'animation

    def draw(self, surface, player_rect):
        # Dessine l'animation de feu sous le joueur
        self.rect.center = (player_rect.centerx, player_rect.bottom + 35)  # Positionner sous le joueur
        surface.blit(self.frames[self.index], self.rect)
  
class Explosion:
    def __init__(self, position):
        self.sprite_sheet = pygame.image.load('explosions.png').convert_alpha()
        self.frames = self.extract_frames(self.sprite_sheet, frame_width=30, frame_height=30, num_columns=5, num_rows=4)
        self.index = 0
        self.rect = self.frames[self.index].get_rect(center=position)
        self.finished = False

    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_columns, num_rows):
        frames = []
        for row in range(num_rows):
            for col in range(num_columns):
                frame = sprite_sheet.subsurface((col * frame_width, row * frame_height, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self):
        self.index += 1
        if self.index >= len(self.frames):
            self.finished = True
        else:
            self.rect = self.frames[self.index].get_rect(center=self.rect.center)

    def draw(self, surface):
        if not self.finished:
            surface.blit(self.frames[self.index], self.rect)

class HealAnimation:
    def __init__(self, position):
        self.sprite_sheet = pygame.image.load('heal_animation.png').convert_alpha()
        self.frames = self.extract_frames(self.sprite_sheet, frame_width=96, frame_height=96, num_columns=5, num_rows=3)
        self.index = 0
        self.rect = self.frames[self.index].get_rect(center=position)
        self.finished = False
        self.animation_speed = 100  # Durée en millisecondes entre les images
        self.last_update_time = pygame.time.get_ticks()  # Temps de la dernière mise à jour

    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_columns, num_rows):
        frames = []
        for row in range(num_rows):
            for col in range(num_columns):
                frame = sprite_sheet.subsurface((col * frame_width, row * frame_height, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self):
        current_time = pygame.time.get_ticks()  # Obtenez le temps actuel
        if current_time - self.last_update_time > self.animation_speed:  # Vérifiez si le temps écoulé est suffisant
            self.index += 1  # Passez à la frame suivante
            if self.index >= len(self.frames):
                self.finished = True  # Terminez l'animation si toutes les frames ont été affichées
            else:
                self.rect = self.frames[self.index].get_rect(center=self.rect.center)  # Mettre à jour la position de l'animation
            self.last_update_time = current_time  # Réinitialisez le temps de la dernière mise à jour

    def draw(self, surface, player_rect):
        # Positionner l'animation de soin au-dessus du joueur
        self.rect.center = (player_rect.centerx, player_rect.centery)
        if not self.finished:
            surface.blit(self.frames[self.index], self.rect)


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
            return b
    return None

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def shoot(playerRect, bullets):
    bullet = pygame.Rect(playerRect.centerx - 2, playerRect.top - 10, 5, 10)
    bullets.append(bullet)

def move_bullets(bullets):
    for bullet in bullets[:]:
        bullet.y -= 10
        if bullet.bottom < 0:
            bullets.remove(bullet)

def check_bullet_hits(baddies, bullets, explosions, score):
    for baddie in baddies[:]:
        for bullet in bullets[:]:
            if bullet.colliderect(baddie['rect']):
                trigger_explosion(explosions, baddie['rect'].center)
                if baddie['rect'].width <= 30 and baddie['rect'].height <= 30:
                    baddies.remove(baddie)
                    score += 250
                bullets.remove(bullet)
                break
    return score

def draw_lives(surface, lives, smallPlayerImage, smallPlayerImageGray, isGameOver):
    for i in range(3):
        if isGameOver:
            surface.blit(smallPlayerImageGray, (500 + i * 45, 10))
        else:
            if i < lives:
                surface.blit(smallPlayerImage, (500 + i * 45, 10))
            else:
                surface.blit(smallPlayerImageGray, (500 + i * 45, 10))

def clear_lives_area(surface, backgroundImage):
    lives_area = pygame.Rect(500, 10, 3 * 45, 30)
    surface.blit(backgroundImage, (500, 10), lives_area)

def drawButton(windowSurface, buttonRect, text, color, hoverColor):
    mousePos = pygame.mouse.get_pos()
    # Changer la couleur du bouton si la souris est dessus
    if buttonRect.collidepoint(mousePos):
        pygame.draw.rect(windowSurface, hoverColor, buttonRect)
    else:
        pygame.draw.rect(windowSurface, color, buttonRect)

    buttonFont = pygame.font.SysFont(None, 40)
    textSurf = buttonFont.render(text, True, BUTTONTEXTCOLOR)
    textRect = textSurf.get_rect(center=buttonRect.center)
    windowSurface.blit(textSurf, textRect)

def showDifficultyMenu(windowSurface):
    BUTTONCOLOR = (100, 200, 255)
    BUTTONHOVERCOLOR = (150, 220, 255)
    QUITBUTTONCOLOR = (255, 100, 100)
    QUITBUTTONHOVERCOLOR = (255, 150, 150)

    easyButton = pygame.Rect(300, 200, 200, 50)
    mediumButton = pygame.Rect(300, 300, 200, 50)
    hardButton = pygame.Rect(300, 400, 200, 50)
    quitButton = pygame.Rect(300, 500, 200, 50)
    returnMenuButtonRect = pygame.Rect(300, 600, 200, 50)
    
    while True:
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
                elif quitButton.collidepoint(event.pos):
                    terminate()
                elif returnMenuButtonRect.collidepoint(event.pos):
                    from main import start
                    start()

        # Dessiner les boutons
        drawButton(windowSurface, easyButton, 'Facile', BUTTONCOLOR, BUTTONHOVERCOLOR)
        drawButton(windowSurface, mediumButton, 'Moyen', BUTTONCOLOR, BUTTONHOVERCOLOR)
        drawButton(windowSurface, hardButton, 'Difficile', BUTTONCOLOR, BUTTONHOVERCOLOR)
        drawButton(windowSurface, quitButton, 'Quitter', QUITBUTTONCOLOR, QUITBUTTONHOVERCOLOR)
        drawButton(windowSurface, returnMenuButtonRect, 'Retour au menu', BUTTONCOLOR, BUTTONHOVERCOLOR)

        pygame.display.update()
        mainClock.tick(FPS)

def move_health_items(healthItems):
    for item in healthItems[:]:
        item['rect'].y += item['speed']
        if item['rect'].top > WINDOWHEIGHT:
            healthItems.remove(item)


def showCharacterSelectionMenu(windowSurface, characterImage, font):
    numCharacters = len(characterImage)

    # Définir le bouton Quitter
    quitButtonRect = pygame.Rect(400, 500, 200, 50)

    while True:
        # Chargement de l'image de fond
        backgroundImage = pygame.image.load('background.jpg').convert()
        windowSurface.blit(backgroundImage, (0, 0))

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
                borderColor = (255, 255, 0)
                pygame.draw.rect(windowSurface, borderColor, (100 + i * 150, 200, 130, 130), 5)

            # Afficher l'image du personnage
            windowSurface.blit(characterImage[i], (100 + i * 150, 200))

        # Afficher les instructions
        drawText('Click on a character to select', font, windowSurface, 100, 400)

        # Dessiner le bouton Quitter
        drawButton(windowSurface, quitButtonRect, 'Quitter', (255, 100, 100), (255, 150, 150))

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
                    terminate()

def pause_menu(windowSurface, font):
    quitButtonRect = pygame.Rect((WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) + 50, 200, 50)
    returnMenuButtonRect = pygame.Rect((WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) + 110, 200, 50)

    waitingForUnpause = True
    while waitingForUnpause:
        transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
        transparent_surface.set_alpha(10)
        transparent_surface.fill((220, 220, 220))

        windowSurface.blit(transparent_surface, (0, 0))
        drawText('Paused', font, windowSurface, (WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) - 100)
        drawText('Press ESC to resume.', font, windowSurface, (WINDOWWIDTH / 2) - 150, (WINDOWHEIGHT / 2))

        drawButton(windowSurface, quitButtonRect, 'Quitter', (255, 100, 100), (255, 150, 150))
        drawButton(windowSurface, returnMenuButtonRect, 'Retour au menu', (100, 255, 100), (150, 255, 150))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    waitingForUnpause = False
            if event.type == MOUSEBUTTONDOWN:
                if quitButtonRect.collidepoint(event.pos):
                    terminate()
                if returnMenuButtonRect.collidepoint(event.pos):
                    from main import start
                    start()

def show_game_over_menu(windowSurface, score, font):
    BUTTONCOLOR = (100, 200, 255)
    BUTTONHOVERCOLOR = (150, 220, 255)
    QUITBUTTONCOLOR = (255, 100, 100)
    QUITBUTTONHOVERCOLOR = (255, 150, 150)

    playAgainButton = pygame.Rect(300, 200, 200, 50)
    quitButton = pygame.Rect(300, 300, 200, 50)
    returnMenuButtonRect = pygame.Rect((WINDOWWIDTH / 2) - 100, (WINDOWHEIGHT / 2) + 110, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == MOUSEBUTTONDOWN:
                if playAgainButton.collidepoint(event.pos):
                    return True
                elif quitButton.collidepoint(event.pos):
                    terminate()
                elif returnMenuButtonRect.collidepoint(event.pos):
                    from main import start
                    start()

        windowSurface.fill((255, 255, 255))
        drawText('Game Over', font, windowSurface, 350, 50)
        drawText(f'Your Score: {score}', font, windowSurface, 350, 100)
        drawButton(windowSurface, playAgainButton, 'Play Again', BUTTONCOLOR, BUTTONHOVERCOLOR)
        drawButton(windowSurface, quitButton, 'Quit', QUITBUTTONCOLOR, QUITBUTTONHOVERCOLOR)
        drawButton(windowSurface, returnMenuButtonRect, 'Retour au menu', (100, 255, 100), (150, 255, 150))

        pygame.display.update()
        mainClock.tick(FPS)

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def shoot(playerRect, bullets):
    # create a new shot in the center of the player
    bullet = pygame.Rect(playerRect.centerx - 2, playerRect.top - 10, 5, 10)  # Tir étroit
    bullets.append(bullet)

def move_bullets(bullets):
    for bullet in bullets[:]:
        bullet.y -= 10  # Goes up by 10 pixels per frame
        if bullet.bottom < 0:
            bullets.remove(bullet)  # Remove of bullet is out of the screen

def check_bullet_hits(baddies, explosions, score, bullets):
    for baddie in baddies[:]:
        for bullet in bullets[:]:
            if bullet.colliderect(baddie['rect']):
                # Ajout d'une explosion
                trigger_explosion(explosions, baddie['rect'].center)  

                if baddie['rect'].width <= 30 and baddie['rect'].height <= 30:
                    baddies.remove(baddie)  # Supprimer le baddie si de taille acceptable
                    score += 250  # Ajouter 250 points si le baddie est détruit
                
                bullets.remove(bullet)  # Supprimer la balle
                break  # Sortir de la boucle des balles pour éviter la modification de la liste pendant l'itération
    return score  # Retourner le score mis à jour

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

def move_health_items(healthItems):
    for item in healthItems[:]:
        item['rect'].y += item['speed']
        if item['rect'].top > WINDOWHEIGHT:
            healthItems.remove(item)

def check_health_item_collision(playerRect, healthItems, lives, heal_animation, windowSurface):
    for item in healthItems[:]:
        if playerRect.colliderect(item['rect']):
            if lives < 3:
                lives += 1
                heal_animation = HealAnimation(playerRect.center)  # Créez une nouvelle animation au centre du joueur
            healthItems.remove(item)

            # Initialiser l'animation de soin
            
            
            
    return lives, heal_animation  # Retournez également l'animation pour mise à jour
