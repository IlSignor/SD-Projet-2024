import pygame, random, sys
from pygame.locals import *
from definition import*

# Set up pygame, the window, and the mouse cursor.
pygame.init()

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

pygame.display.set_caption('Dodger')

# Set up the fonts.
pygame.font.init()
font = pygame.font.SysFont(None, 48)


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


start()