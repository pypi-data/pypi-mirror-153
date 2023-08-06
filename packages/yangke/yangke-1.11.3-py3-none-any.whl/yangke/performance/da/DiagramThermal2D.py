# pygame没有层的概念，每一帧背景都要重新生成
# pygame中的Sprite透明，只有在同一个Group里的Sprite才有透明效果，不同Group在不同层中，层不是透明的

import sys, pygame
from pygame.sprite import Group
import numpy as np

from yangke.performance.da.Diagram2DComponents import BoilerDiagram, TurbineHigh, YkPygameSprite, TurbineMiddle, \
    Heater, GridSprite
from yangke.common.dijstra import find_connect_line, generate_obstacle_map

available_grid = {}
obstacles_grid = {}
need_grid = True
# Noinspection All
screen: pygame.Surface = None


# ========================= 添加热力系统组件 ==================================
def get_target_component(position, group):
    for sprite in group.sprites():
        rect = sprite.rect
        if (rect[0] < position[0] < (rect[0] + rect[2])) and (rect[1] < position[1] < (rect[1] + rect[3])):
            return sprite

    return None


def update_connect_lines(sprite_new: YkPygameSprite, group):
    """
    当某个组件更新时，同时更新与之相关的连接线

    :param group:
    :param sprite_new:
    :return:
    """
    for conn_name, pos in sprite_new.get_absolute_connect_points().items():
        # find_connect_line()
        sprite_new.connect_points_lines.update({conn_name: ""})

    pass


# noinspection All
def connect(pos1, dir1, pos2, dir2, obstacles=None, bound=None, available_grid=None, obstacles_grid=None):
    """
    用线连接图中两点，避开所有部件
    :param pos1:
    :param dir1:
    :param pos2:
    :param dir2:
    :param obstacles: 障碍物所在的矩形区域，给定参数时，(obstacles, bound)可以生成(obstacles_grid,available_grid)，因此是二选一给定即可
    :param bound: 场景边界
    :param obstacles_grid: 障碍物所在的格子区域，格子区域是有障碍物划分生成的行列数量对其的子区域，给定grid的运行速度比给定障碍物和边界快
    :param available_grid: 可用的格子区域
    :return:
    """
    if pos1 is None or pos2 is None:
        return False
    # print("查询最小路径")
    # 判断pos2相对pos1的方向

    points_list = find_connect_line(pos1, dir1, pos2, dir2, obstacles, bound, available_grid, obstacles_grid)

    return True


def generate_connect_lines(group, bound):
    """
    生成所有组件的连接线

    :return:
    """
    obstacles = [sp.rect for sp in group.sprites()]
    global available_grid, obstacles_grid
    available_grid, obstacles_grid = generate_obstacle_map(bound, obstacles)

    for sprite in group.sprites():  # 遍历每一个部件
        sprite: YkPygameSprite = sprite
        for conn_name, pos in sprite.get_absolute_connect_points().items():  # 遍历部件上的所有可能的连接点
            if pos is not None and not isinstance(pos, list):  # 说明该点有连接且尚未添加连接线
                for des_sp in group.sprites():
                    if des_sp != sprite:
                        for temp_name, pos1 in des_sp.get_absolute_connect_points().items():
                            if temp_name == conn_name:
                                if connect(pos, sprite.connect_points_dir.get(temp_name),
                                           pos1, des_sp.connect_points_dir.get(temp_name),
                                           available_grid=available_grid, obstacles_grid=obstacles_grid):  # 如果连接成功
                                    des_sp.connect_points[temp_name] = list(pos1)
                                    sprite.connect_points[conn_name] = list(pos)


def bounce_component(group):
    """
    弹开组中的各个组件，是各组件不重叠

    :param group:
    :return:
    """
    for sp1 in group.sprites():
        sp1: YkPygameSprite = sp1
        for sp2 in group.sprites():
            sp2: YkPygameSprite = sp2
            if sp2 != sp1:
                if sp1.rect.colliderect(sp2.rect):  # 如果两组间重叠
                    if sp1.position == sp2.position:
                        pass


def get_main_group():
    """
    将热力系统图中的所有组件放入一个组中

    :return: 返回组对象，对象类型为pygame.sprite.Group
    """
    # ========================= 添加热力系统组件 ==================================
    boiler = BoilerDiagram(position=(100, 300), line_width=2, color=(255, 0, 0, 255))
    boiler.scale_by(1)
    hp = TurbineHigh(position=(300, 260), line_width=2, color=(0, 0, 0, 255))
    ip = TurbineMiddle(position=(600, 260), line_width=2, color=(0, 0, 0, 255))
    heater1 = Heater(position=(200, 700), line_width=2, color=(0, 0, 0, 255))
    heater2 = Heater(position=(350, 700), line_width=2, color=(0, 0, 0, 255))
    heater3 = Heater(position=(500, 700), line_width=2, color=(0, 0, 0))
    heater4 = Heater(position=(800, 700), line_width=2, color=(0, 0, 0))
    heater5 = Heater(position=(950, 700), line_width=2, color=(0, 0, 0))
    heater6 = Heater(position=(1100, 700), line_width=2, color=(0, 0, 0))
    heater7 = Heater(position=(1250, 700), line_width=2, color=(0, 0, 0))
    main_group = Group()
    main_group.add(boiler)
    main_group.add(hp)
    main_group.add(ip)
    main_group.add(heater1)
    main_group.add(heater2)
    main_group.add(heater3)
    main_group.add(heater4)
    main_group.add(heater5)
    main_group.add(heater6)
    main_group.add(heater7)
    return main_group


def main():
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 1400, 800
    global screen, need_grid
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("机组热力系统图")

    grid = GridSprite(x_list=None, y_list=None, width=width, height=height, color=(0, 255, 255))

    main_group = get_main_group()
    assist_group = Group()  # 用于在画布上显示辅助部件
    assist_group.add(grid)

    target_component = None
    moving = False
    generate_connect_lines(main_group, bound=[0, 0, width, height])
    if need_grid:  # 如果需要绘制格子图
        all_grid = available_grid
        all_grid.update(obstacles_grid)
        x_list = []
        y_list = []
        for rect in all_grid.values():
            x_list.append(rect[0])
            y_list.append(rect[1])
        x_list = list(set(x_list))
        y_list = list(set(y_list))
        grid.update(x_list, y_list)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    target_component = get_target_component(pygame.mouse.get_pos(), main_group)
                    print(target_component)
                    moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    moving = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    need_grid = not need_grid

        screen.fill((255, 255, 255, 200))

        x, y = pygame.mouse.get_pos()
        if isinstance(target_component, YkPygameSprite):
            if moving:
                target_component.move_to(x, y)
                update_connect_lines(target_component, main_group)
        # bounce_component(group)

        # 绘制网格线
        if need_grid:
            assist_group.draw(screen)  # 把sprite的image绘制到rect中
        # 绘制组件
        main_group.draw(screen)

        # 绘制连接线
        # connect.draw(screen)

        pygame.display.flip()
        clock.tick(50)
        # print(clock.get_fps())


if __name__ == "__main__":
    main()
