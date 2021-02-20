import pygame as pg

pg.mixer.init()


load_music = pg.mixer.Sound

path = 'data/Sounds/'

Menu_music = load_music(path + 'music/Menu/Menu_music.mp3')
Game_music1 = load_music(path + 'music/Game/GM1.mp3')
Game_music2 = load_music(path + 'music/Game/GM2.mp3')

moving = load_music(path + 'SFX/moving.mp3')
pressing = load_music(path + 'SFX/pressing.mp3')
channel = pg.mixer.Channel(1)
