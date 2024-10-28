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