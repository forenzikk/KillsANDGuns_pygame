import math
from drawings import *
from play_map import *
from numba import njit


@njit(fastmath=True, cache=True)  # декоратор
def mapping(a, b):  # вычисление координат верхнего леового угла - квадрат, где мы генерируемся
    return int(a // tile) * tile, int(b // tile) * tile


@njit(fastmath=True, cache=True)
def ray_casting(player_position, angle_of_player, world_map):
    casted_walls = []
    xo, yo = player_position
    texture_vertical, texture_horisontal = 1, 1
    xn, yn = mapping(xo, yo)
    current_angle = angle_of_player - ((math.pi / 3) / 2)
    for ray in range(count_of_rays):
        sin_a = math.sin(current_angle)
        if sin_a:
            sin_a = sin_a
        else:
            sin_a = 0.000001

        cos_a = math.cos(current_angle)

        if cos_a:
            cos_a = cos_a
        else:
            cos_a = 0.000001

        # Пересечение с вертикалями
        if cos_a >= 0:
            # x - текущая вертикаль; dx - вспомогат. переменная для получения
            # очередной вертикали
            x, dx = xn + tile, 1
        else:
            x, dx = xn, -1

        for i in range(0, width_of_world, tile):  # пройдемся по ширине карты
            depth_vertical = (x - xo) / cos_a  # расстояние до вертикали
            yv = yo + depth_vertical * sin_a
            tile_vertical = mapping(x + dx, yv)
            if tile_vertical in world_map:
                texture_vertical = world_map[tile_vertical]
                break
            x += dx * tile

        # Пересечение с горизонталями
        if sin_a >= 0:
            y, dy = yn + tile, 1
        else:
            y, dy = yn, -1

        for i in range(0, height_of_world, tile):
            depth_horisontal = (y - yo) / sin_a
            xh = xo + depth_horisontal * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_horisontal = world_map[tile_h]
                break
            y += dy * tile

        # Проекция препятствия
        if depth_vertical < depth_horisontal:
            depth, offset, texture = depth_vertical, yv, texture_vertical
        else:
            depth, offset, texture = depth_horisontal, xh, texture_horisontal

        offset = int(offset) % tile  # смещение
        depth *= math.cos(angle_of_player - current_angle)
        # недоступность падения игры из-за деления на 0
        depth = max(depth, 0.00001)
        proj_height = int(proj_coeff / depth)

        # для каждого луча: дальность до стены;сдвиг по текстуре;проекционная
        # высота стены;№текстуры
        casted_walls.append((depth, offset, proj_height, texture))
        current_angle += delta_angle
    return casted_walls


def ray_casting_walls(player, textures):
    casted_walls = ray_casting(player.get_position, player.angle, world_map)
    # размер проекции на центральном луче
    wall_shot = casted_walls[center_of_ray][0], casted_walls[center_of_ray][2]
    walls = []
    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values
        wall_column = textures[texture].subsurface(
            offset * scale_texture,
            0,
            scale_texture,
            height_of_textures)  # выделение подповерхности
        wall_column = pygame.transform.scale(
            wall_column, (scale, proj_height))  # масштабирование
        wall_position = (ray * scale, 400 - proj_height // 2)

        walls.append((depth, wall_column, wall_position))
    return walls, wall_shot
