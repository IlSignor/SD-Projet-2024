#################################       This file defines the classes used to do anmiations in the game         #############################################

#importations of the modulus
import pygame
from pygame.locals import *


# Class to manage the fire animation beneath the player's character and the comets
class FireAnimation:
    def __init__(self):
        self.sprite_sheet = pygame.image.load('animations/rocket_fire.png').convert_alpha()      # Load the sprite sheet image for the fire effect
        self.frame_width = 23                                                          # Set the width of each frame
        self.frame_height = 70                                                         # Set the height of each frame
        self.num_columns = 5                                                           # Set the number of frames per row
        self.num_rows = 1                                                              # Set the number of rows in the sprite sheet
        self.frames = self.extract_frames(self.sprite_sheet, self.frame_width,         # Extract frames from the sprite sheet
                                          self.frame_height, self.num_columns,         # based on the specified dimensions
                                          self.num_rows)
        self.index = 0                                                                 # Initialize the frame index for animation control
        self.animation_speed = 5                                                       # Set the animation speed
        self.rect = self.frames[self.index].get_rect()                                 # Initialize the rect object for positioning


    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_columns, num_rows):
        frames = []
        for row in range(num_rows):                                                    # Loop through each row and column
            for col in range(num_columns):                                             # to slice out individual frames
                frame = sprite_sheet.subsurface((col * frame_width, row * frame_height, frame_width, frame_height))
                frames.append(frame)                                                   # Add each frame to the list
        return frames

    def update(self):
        self.index += 1                                                                # Increment the frame index
        if self.index >= len(self.frames):                                             # Reset to 0 if the index exceeds available frames
            self.index = 0                                                             # Loop back to the first frame for continuous animation

    def draw(self, surface, player_rect):
        self.rect.center = (player_rect.centerx, player_rect.bottom + 5)               # Position the fire animation below the player
        surface.blit(self.frames[self.index], self.rect)                               # Draw the current frame on the given surface
  
  
# Class to manage explosion animations
class Explosion:
    def __init__(self, position):
        self.sprite_sheet = pygame.image.load('animations/explosions.png').convert_alpha()        # Load the sprite sheet for explosions
        self.frames = self.extract_frames(self.sprite_sheet, frame_width=30,           # Extract explosion frames using frame dimensions
                                          frame_height=30, num_columns=5,              # and sprite sheet layout
                                          num_rows=4)
        self.index = 0                                                                 # Initialize frame index
        self.rect = self.frames[self.index].get_rect(center=position)                  # Set rect to position the explosion
        self.finished = False                                                          # Flag to indicate if the animation is complete


    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_columns, num_rows):
        frames = []
        for row in range(num_rows):                                                    # Loop through the sprite sheet based on rows
            for col in range(num_columns):                                             # and columns to get each frame
                frame = sprite_sheet.subsurface((col * frame_width, row * frame_height, frame_width, frame_height))
                frames.append(frame)                                                   # Append each frame to the frames list
        return frames

    def update(self):
        self.index += 1                                                                # Move to the next frame in the animation
        if self.index >= len(self.frames):                                             # Check if all frames have been displayed
            self.finished = True                                                       # Mark animation as finished when all frames are shown
        else:
            self.rect = self.frames[self.index].get_rect(center=self.rect.center)      # Update rect to keep the explosion centered

    def draw(self, surface):
        if not self.finished:
            surface.blit(self.frames[self.index], self.rect)                           # Draw the current frame on the given surface


# Class to manage the healing animation displayed above the player's character
class HealAnimation:
    def __init__(self, position):
        self.sprite_sheet = pygame.image.load('animations/heal_animation.png').convert_alpha()    # Load the sprite sheet image for healing effect
        self.frames = self.extract_frames(self.sprite_sheet, frame_width=96,           # Extract frames using specified dimensions
                                          frame_height=96, num_columns=5,              # for each frame and sprite sheet layout
                                          num_rows=3)
        self.index = 0                                                                 # Initialize frame index for animation
        self.rect = self.frames[self.index].get_rect(center=position)                  # Set initial position
        self.finished = False                                                          # Flag to indicate if the animation is complete
        self.animation_speed = 100                                                     # Duration (in milliseconds) between frames
        self.last_update_time = pygame.time.get_ticks()                                # Record the time of the last update


    def extract_frames(self, sprite_sheet, frame_width, frame_height, num_columns, num_rows):
        frames = []
        for row in range(num_rows):                                                    # Loop through each row and column
            for col in range(num_columns):                                             # to slice out individual frames
                frame = sprite_sheet.subsurface((col * frame_width, row * frame_height, frame_width, frame_height))
                frames.append(frame)                                                   # Add each frame to the frames list
        return frames

    def update(self):
        current_time = pygame.time.get_ticks()                                         # Get the current time
        if current_time - self.last_update_time > self.animation_speed:                # Check if enough time has elapsed since last update
            self.index += 1                                                            # Move to the next frame in the animation
            if self.index >= len(self.frames):                                         # Check if all frames have been displayed
                self.finished = True                                                   # Mark animation as finished when all frames are shown
            else:
                self.rect = self.frames[self.index].get_rect(center=self.rect.center)  # Update rect to maintain the animation's position
            self.last_update_time = current_time                                       # Reset the last update time

    def draw(self, surface, player_rect):
        self.rect.center = (player_rect.centerx, player_rect.centery)                  # Position the healing animation centered above player
        if not self.finished:
            surface.blit(self.frames[self.index], self.rect)                           # Draw the current frame on the given surface
