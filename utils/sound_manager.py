"""
Sound Manager for Dota 2 Timer Alerts

Handles loading and playback of .wav files triggered by rune spawns,
Roshan timers, and day/night transitions. Uses pygame for non-blocking
sound playback and supports PyInstaller bundling.
"""

import os
import pygame

from utils.path_utils import resource_path

# Initialize pygame mixer once globally
pygame.mixer.init()

# Map rune/cycle event names to corresponding sound files
RUNE_SOUNDS = {
    'Bounty_Rune': 'bounty_rune.wav',
    'Power_Rune': 'power_rune.wav',
    'Roshan_Rune': 'roshan_rune.wav',
    'Water_Rune': 'water_rune.wav',
    'Wisdom_Rune': 'wisdom_rune.wav',
    'Day_Cycle': 'day.wav',
    'Night_Cycle': 'night.wav'
}

def play_rune_sounds(rune_list: list) -> None:
    """
    Play sounds associated with a list of rune or cycle events.

    Args:
        rune_list (list): List of rune/cycle event identifiers
    """
    for rune in sorted(rune_list):
        sound_file = RUNE_SOUNDS.get(rune)
        if sound_file:
            full_sound_path = resource_path(f"sounds/{sound_file}")
            play_sound(full_sound_path)

def play_sound(path: str) -> None:
    """
    Play a single .wav file from the given path.

    Args:
        path (str): Absolute path to .wav file
    """
    try:
        sound = pygame.mixer.Sound(path)
        sound.play()
    except pygame.error as e:
        print(f"[ERROR] Failed to play sound: {path} | {e}")
