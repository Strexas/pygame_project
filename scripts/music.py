import pygame as pg

pg.mixer.init()

load_music = pg.mixer.Sound

path = 'data/Sounds/'

Menu_music1 = load_music(path + 'music/Menu/MM1.mp3')
Menu_music2 = load_music(path + 'music/Menu/MM2.mp3')
menu_music = (Menu_music1, Menu_music2)
Game_music1 = load_music(path + 'music/Game/GM1.mp3')
Game_music2 = load_music(path + 'music/Game/GM2.mp3')
game_music = (Game_music1, Game_music2)

moving = load_music(path + 'SFX/moving.mp3')
pressing = load_music(path + 'SFX/pressing.mp3')
channel = pg.mixer.Channel(1)
