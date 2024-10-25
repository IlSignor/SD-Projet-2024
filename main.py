import pygame, random, sys
from pygame.locals import *
from definition import*
from game import*

WINDOWWIDTH = 1000
WINDOWHEIGHT = 800

TEXTCOLOR = (0, 0, 0)
BUTTONTEXTCOLOR = (255, 255, 255)

FPS = 60

BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
PLAYERMOVERATE = 5

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
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


# Show the "Start" screen.
windowSurface.blit(backgroundImage, (0, 0))  # Affiche l'image de fond à partir du coin supérieur gauche

pygame.display.update()

topScore = 0
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)

# Show character selection menu
selectedCharacterIndex = showCharacterSelectionMenu(windowSurface, characterImages, font)
playerImage = characterImages[selectedCharacterIndex]  # Set player image based on selection
playerRect = playerImage.get_rect()  # Get the rectangle for the player

smallPlayerImage = pygame.transform.scale(playerImage, (30, 30)) 
smallPlayerImageGray = pygame.Surface((30, 30))
smallPlayerImageGray.blit(smallPlayerImage, (0, 0))
smallPlayerImageGray.set_alpha(100)

windowSurface.blit(backgroundImage, (0, 0))  # Affiche l'image de fond à partir du coin supérieur gauche

difficulty = showDifficultyMenu(windowSurface,mainClock,FPS)
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


game(FPS, PLAYERMOVERATE, BADDIEMINSIZE, BADDIEMAXSIZE, mainClock, playerRect, bullets, windowSurface, ADDNEWBADDIERATE,BADDIEMINSPEED,BADDIEMAXSPEED,baddieImage,healthItems,healthItemImage,backgroundImage,font, smallPlayerImage, smallPlayerImageGray, playerImage, explosions, gameOverSound, topScore)