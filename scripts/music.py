import pygame as pg
from random import randint


pg.mixer.init()

load_music = pg.mixer.Sound

path = 'data/Sounds/'

Menu_music1 = load_music(path + 'music/Menu/MM1.mp3')
Menu_music2 = load_music(path + 'music/Menu/MM2.mp3')
menu_music = [Menu_music2, Menu_music1]
Game_music1 = load_music(path + 'music/Game/GM1.mp3')
Game_music2 = load_music(path + 'music/Game/GM2.mp3')
game_music = [Game_music1, Game_music2]
if randint(0, 1):
    game_music = game_music[::-1]
if randint(0, 1):
    menu_music = menu_music[::-1]


moving = load_music(path + 'SFX/moving.mp3')
pressing = load_music(path + 'SFX/pressing.mp3')
channel = pg.mixer.Channel(1)
