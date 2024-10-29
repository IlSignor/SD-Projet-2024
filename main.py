import pygame, sys
from pygame.locals import *
from definition import*

# Set up pygame, the window, and the mouse cursor.
pygame.init()

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

pygame.display.set_caption('Dodger')

# Set up the fonts.
pygame.font.init()
font = pygame.font.SysFont(None, 48)
smallFont = pygame.font.SysFont(None, 30)

bullets = [] 
healthItems = [] 
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




def start():
    # Show the "Start" screen.
    windowSurface.blit(backgroundImage, (0, 0))  # Affiche l'image de fond à partir du coin supérieur gauche

    pygame.display.update()

    topScore = 0

    # Show character selection menu
    selectedCharacterIndex = showCharacterSelectionMenu(windowSurface, characterImages, font)
    playerImage = characterImages[selectedCharacterIndex]  # Set player image based on selection
    playerRect = playerImage.get_rect()  # Get the rectangle for the player

    smallPlayerImage = pygame.transform.scale(playerImage, (30, 30)) 
    smallPlayerImageGray = pygame.Surface((30, 30))
    smallPlayerImageGray.blit(smallPlayerImage, (0, 0))
    smallPlayerImageGray.set_alpha(100)

    windowSurface.blit(backgroundImage, (0, 0))  # Affiche l'image de fond à partir du coin supérieur gauche

    heal_animation = HealAnimation(playerRect.center)
    fire_animation = FireAnimation()

    difficulty = showDifficultyMenu(windowSurface)
    if difficulty == 'easy':
        BADDIEMINSPEED = 1
        BADDIEMAXSPEED = 4
        ADDNEWBADDIERATE = 12
        HEALTHHAPPEND = 100
    elif difficulty == 'medium':
        BADDIEMINSPEED = 2
        BADDIEMAXSPEED = 6
        ADDNEWBADDIERATE = 8
        HEALTHHAPPEND = 1000
    elif difficulty == 'hard':
        BADDIEMINSPEED = 4
        BADDIEMAXSPEED = 8
        ADDNEWBADDIERATE = 6
        HEALTHHAPPEND = 1000

    windowSurface.blit(backgroundImage, (0, 0))  # Affiche l'image de fond à partir du coin supérieur gauche

    from game import game
    game(HEALTHHAPPEND, heal_animation, fire_animation, playerRect, bullets, windowSurface, ADDNEWBADDIERATE,BADDIEMINSPEED,BADDIEMAXSPEED,baddieImage,healthItems,healthItemImage,backgroundImage,font, smallPlayerImage, smallPlayerImageGray, playerImage, explosions, gameOverSound, topScore)



rules_button = smallFont.render("?", True, (0, 0, 0), (255, 255, 255))
rules_button_rect = rules_button.get_rect(topright=(windowSurface.get_width() - 20, 20))

# Texte des règles du jeu
rules_text = [
    "Règles du jeu Dodger :",
    "1. Évitez les ennemis en vous déplaçant.",
    "2. Ramassez les objets de soin pour regagner de la vie.",
    "3. Utilisez les flèches pour contrôler le personnage.",
    "4. Essayez de survivre aussi longtemps que possible!"
]

# Surface des règles
rule_window = pygame.Surface((600, 400))
rule_window.fill((50, 50, 50))  # Couleur de fond pour les règles
y_offset = 50
for line in rules_text:
    drawText(line, smallFont, rule_window, 20, y_offset)  # Utilisation de drawText pour les règles
    y_offset += 40

# Variables de contrôle
showing_rules = False
waiting = True

# Boucle principale du menu de démarrage
while waiting:
    windowSurface.blit(backgroundImage, (0, 0))
    drawText("Pressez ENTER pour lancer le jeu", font, windowSurface, windowSurface.get_width() // 2 - 200, windowSurface.get_height() // 2)
    windowSurface.blit(rules_button, rules_button_rect)

    if showing_rules:
        windowSurface.blit(rule_window, (100, 100))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RETURN or event.key == K_KP_ENTER:
                waiting = False  # Quitter le menu pour lancer le jeu
            elif event.key == K_ESCAPE and showing_rules:
                showing_rules = False
        elif event.type == MOUSEBUTTONDOWN:
            if rules_button_rect.collidepoint(event.pos):  # Si le bouton "?" est cliqué
                showing_rules = not showing_rules


start()