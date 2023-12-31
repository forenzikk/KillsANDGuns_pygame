import pygame
import time
from sprites_obj import *
from drawings import *
from cooperation import *
from numba import jit
import asyncio

def write_text(text):  # вывод текста перед игрой
    screen.fill((0, 0, 0))
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (600, 400)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(5)  # Задержка в 5 секунд
    return None

pygame.init()  # инициализация всех необходимых модулей
pygame.mouse.set_visible(False)#видимость курсора
screen_map = pygame.Surface(minimap_res)
screen = pygame.display.set_mode((1200, 800))  # размер экрана
font = pygame.font.Font(None, 36)

pygame.display.set_caption("Kills & Guns")  # title of game
icon = pygame.image.load('images/icon.png')  # icon

# инициализация экземпляров
sprites = Sprites()
clock = pygame.time.Clock()  # желаемое кол-во кадров в сек
player = Player(sprites)
drawing = Drawing(screen, screen_map, player, clock)
interaction = Interaction(player, sprites, drawing)

menu = drawing.menu()
interaction.musical_playing()

write_text("Добро пожаловать в настоящий ад, мой друг! Посмотрим, что ты можешь")
while True:

    player.movement()
    drawing.background(player.angle)
    walls, wall_shot = ray_casting_walls(player, drawing.textures)
    # передаем список параметров стен и список вычисленных параметров спрайтов
    if menu:
        drawing.world(walls + [obj.object_locate(player)
                      for obj in sprites.list_of_objects])
    else:
        sprites.list_of_objects = sprites.list_of_objects_2
        drawing.world(walls + [obj.object_locate(player)
                      for obj in sprites.list_of_objects])

    drawing.mini_map(player)
    drawing.player_weapon([wall_shot, sprites.sprite_shot])
    drawing.draw_score()
    interaction.interaction_objects()
    interaction.npc_action()
    interaction.checking_win()

    pygame.display.flip()  # обновление содержимого на каждой итерации
    clock.tick()
