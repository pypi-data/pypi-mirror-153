"""
寻路算法
"""
import pygame
import math
from enum import Enum
import random


def point_index_rectangles(x, y, grid: dict):
    """
    判断点所在的区域的行索引和列索引
    :param grid:
    :return: row_index, col_index
    """
    for pos, rect in grid.items():
        if x == rect[0] or x == rect[0] + rect[2]:
            return x, -1  # 说明点在平行于y轴的横线上
        if y == rect[1] or y == rect[1] + rect[3]:
            return -1, y  # 说明点在平行于x轴的横线上
        if pygame.rect.Rect(rect).collidepoint(x, y):
            return pos  # 点所在的矩形的索引

    return -1, -1  # 说明点不在任何grids中的区域中


def search_until_obstacle(pos=(0, 0), direction="up", obstacle_grid=None, available_grid=None):
    """
    从某个位置向上搜索，直到遇到障碍物，返回起始位置和结束位置的地图区域索引

    :param pos:
    :param direction:
    :param obstacle_grid:
    :param available_grid:
    :return: row1, col1, row2, col2
    """
    start_x, start_y = pos
    row, col = point_index_rectangles(pos[0], pos[1], obstacle_grid)
    available_row = 0
    if direction == "up":
        if row == -1 or col == -1:  # 说明起点不在障碍物区域外部或边界上
            row, col = point_index_rectangles(start_x, start_y - 1, available_grid)
            row1 = row
            col1 = col
            while row != -1 or col != -1:
                # 不是障碍物
                temp_up_bound = available_grid.get((row, col))
                if temp_up_bound is not None:
                    temp_up_bound = temp_up_bound[1]
                if row != -1:
                    available_row = row
                row, col = point_index_rectangles(start_x, temp_up_bound - 1, available_grid)
            return row1, col1, available_row, col
        else:
            print("搜索起始点位于障碍物区域内")
            return -1, -1, -1, -1


def generate_a_star_map(available_grid, obstacle_grid):
    """
    根据可通行区域和障碍物区域的索引及绝对坐标，计算a_star_map的大小和障碍物列表

    :param available_grid:  索引+坐标，例如{(0, 0): [0, 0, 59, 190], (1, 0): [0, 190, 59, 49], ...}
    :param obstacle_grid: 障碍物的索引+坐标，行列的索引+索引对应区域的矩形位置及大小。
    :return: 地图的大小和障碍物区域
    """
    all_keys = []
    all_keys.extend(list(available_grid.keys()))
    all_keys.extend(list(obstacle_grid.keys()))
    row, col = -1, -1  # 地图划分的行数和列数
    for k in all_keys:
        x, y = k
        row = max(x, row)
        col = max(y, col)
    return (row, col), list(obstacle_grid.values())


def coor_2_index(start_x, start_y, grid) -> tuple:
    """
    根据点在画布上的绝对坐标判断其属于画布上的那个区域，返回区域的索引

    :param start_x:
    :param start_y:
    :param grid:
    :return:
    """
    for k, v in grid.items():
        left, right, top, bottom = v[0], v[0] + v[2], v[1], v[1] + v[3]
        if left <= start_x <= right and top <= start_y <= bottom:
            return k
    return -1, -1


def find_connect_line(start_position, start_direction, end_position, end_direction, obstacles=None, bound=None,
                      available_grid=None, obstacle_grid=None):
    """
    查找最优的连接路径

    :param obstacle_grid:
    :param available_grid:
    :param start_position: 路径起点坐标
    :param start_direction: 路径起点的方向，即起点朝哪个方向是正向，一般部件上的锚点有上下左右四个方向，假如是上方锚点，则连接线朝上时少一个拐点，连接线朝其他方向时多一个锚点
    :param end_position: 路径终点坐标
    :param end_direction: 路径终点的方向
    :param obstacles: 障碍物的rectangle列表
    :param bound: 边界
    :return:
    """
    result = []
    if available_grid is None or obstacle_grid is None:
        available_grid, obstacle_grid = generate_obstacle_map(bound, obstacles)

    if start_position[0] > end_position[0]:  # 如果起点在右侧，则交换起点和终点位置
        start_position, end_position = end_position, start_position
        start_direction, end_direction = end_direction, start_direction
    start_x, start_y = start_position
    end_x, end_y = end_position

    map_size, block_list = generate_a_star_map(available_grid, obstacle_grid)
    pos_s_node = coor_2_index(start_x, start_y, obstacle_grid)  # 点必然在障碍物区域上，因此第三个参数无需传入可通行区域的信息
    pos_e_node = coor_2_index(end_x, end_y, obstacle_grid)
    a_map = Map(map_size)  # Map只需要地图大小即可
    my_a_star = AStar(map_size, pos_s_node, pos_e_node)
    my_a_star.set_block(block_list)
    if my_a_star.run() == 0:
        route_list = my_a_star.get_route()
        return route_list
    else:
        print('路径规划失败！')


def generate_obstacle_map(bound: list, obstacles: list):
    """
    生成障碍物地图，必须保证bound包含所有的obstacles，即obstacles不能超出边界的范围

    :param bound: 地图边界，[x,y,w,h]
    :param obstacles: 障碍物列表，每一个障碍物是一个pygame.Rect对象
    :return: 返回两个字典，第一个为路径可通过的格子，第二个为障碍物的格子，字典item项格式为 {(格子行号, 格子列号): [x,y,w,h]}
    """
    bound_x, bound_y, bound_w, bound_h = bound
    rectangles = {}  # {[x,y,w,h]}
    x_list = []
    y_list = []
    for ob in obstacles:
        x, y, w, h = ob
        x_list.extend([x, x + w])
        y_list.extend([y, y + h])
    x_list = list(set(x_list))  # 去重
    x_list.sort()
    y_list = list(set(y_list))
    y_list.sort()
    x_list.append(bound_x + bound_w)
    y_list.append(bound_y + bound_h)
    temp_x_start = bound_x
    for i, x in enumerate(x_list):
        temp_y_start = bound_y
        for j, y in enumerate(y_list):
            rectangles.update({(j, i): [temp_x_start, temp_y_start, x - temp_x_start, y - temp_y_start]})
            temp_y_start = y
        temp_x_start = x

    # 从rectangles中标记出障碍物所在的格子
    available_rectangles = {}
    obstacles_rectangles = {}
    for pos, rect in rectangles.items():
        x, y, w, h = rect
        if pygame.rect.Rect(x, y, w, h).collidelist(obstacles) != -1:  # collidelist返回碰撞的索引
            obstacles_rectangles.update({pos: rect})
        else:
            available_rectangles.update({pos: rect})

    return available_rectangles, obstacles_rectangles


class Map(object):
    def __init__(self, map_size):
        self.map_size = map_size

    def generate_cell(self, cell_width, cell_height):
        x_cell = -cell_width
        for num_x in range(self.map_size[0] // cell_width):
            y_cell = -cell_height
            x_cell += cell_width
            for num_y in range(self.map_size[1] // cell_height):
                y_cell += cell_height
                yield (x_cell, y_cell)


class Node:
    def __init__(self, pos):
        self.pos = pos
        self.father = None
        self.g = 0
        self.f = 0

    def compute_fx(self, encode, father):
        """
        节点的目标函数值f，其值为 f=g+h。g(x)是指起点到当前节点的实际最小距离，h(x)是指从当前节点到目标节点的估计最小值

        :param encode:
        :param father:
        :return:
        """
        if father is None:
            print("未设置当前节点的父节点")

        gx_father = father.g
        # 采用欧式距离计算当前节点与父节点的距离
        # gx_f2n = math.sqrt((father.pos[0] - self.pos[0]) ** 2 + (father.pos[1] - self.pos[1]) ** 2)
        gx_f2n = abs(father.pos[0] - self.pos[0]) + abs(father.pos[1] - self.pos[1])
        g = gx_f2n + gx_father  # 当前节点到起点的距离=父节点到起点的距离+当前节点到父节点的距离

        # hx_n2encode = math.sqrt((self.pos[0] - encode.pos[0]) ** 2 + (self.pos[1] - encode.pos[1]) ** 2)
        hx_n2encode = abs(self.pos[0] - encode.pos[0]) + abs(self.pos[1] - encode.pos[1])
        f = g + hx_n2encode
        return g, f

    def set_fx(self, end_code, father):
        self.g, self.f = self.compute_fx(end_code, father)
        self.father = father

    def update_fx(self, encode, father):
        g, f = self.compute_fx(encode, father)
        if f < self.f:
            self.g, self.f = g, f
            self.father = father


class AStar:
    def __init__(self, map_size, pos_sn, pos_en):
        self.map_size = map_size
        self.open_list = []  # open_list中储存待考察的节点
        self.close_list = []  # 已经考察过的节点
        self.block_list = []
        self.s_node = Node(pos_sn)
        self.e_node = Node(pos_en)
        self.c_node = self.s_node  # 当前搜索到的节点

    def run(self):
        self.open_list.append(self.s_node)
        while len(self.open_list) > 0:
            # 查找open_list中f最小的点
            self.open_list.sort(key=lambda x: x.f)
            self.c_node = self.open_list[0]
            del self.open_list[0]
            self.close_list.append(self.c_node)

            # 扩展当前f最小的节点，并进入下一次循环搜索
            self.extend(self.c_node)
            # 如果open_list列表为空，或者当前搜索节点为目标节点，则跳出循环
            if len(self.open_list) == 0 or self.c_node.pos == self.e_node.pos:
                break

        if self.c_node.pos == self.e_node.pos:
            self.e_node.father = self.c_node.father
            return 0
        else:
            return -1

    def extend(self, c_node):
        """
        计算当前节点的相邻节点的距离，如果其相邻接点已经计算过了，则更新相邻节点的距离信息

        :param c_node:
        :return:
        """
        nodes_neighbor = self.get_neighbor(c_node)
        for node in nodes_neighbor:
            # 判断节点node是否在close_list和block_list中
            if node.pos in list(map(lambda x: x.pos, self.close_list)) or node.pos in self.block_list:
                continue
            else:
                if node.pos in list(map(lambda x: x.pos, self.open_list)):  # 如果节点在open中，则更新该节点的距离信息
                    node.update_fx(self.e_node, c_node)
                else:
                    node.set_fx(self.e_node, c_node)  # 否则，计算节点的距离，并将节点加入open_list中
                    self.open_list.append(node)

    def set_block(self, block_list):
        self.block_list.extend(block_list)

    def get_neighbor(self, node):
        """
        拿到节点node的相邻节点，会剔除超出地图边界的节点索引

        :param node:
        :return:
        """
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        nodes_neighbor = []
        x, y = node.pos[0], node.pos[1]
        for os in offsets:
            x_new, y_new = x + os[0], y + os[1]
            pos_new = (x_new, y_new)
            # 判断是否在地图范围内，超出范围则跳过
            if x_new < 0 or x_new > self.map_size[0] - 1 or y_new < 0 or y_new > self.map_size[1] - 1:
                continue
            nodes_neighbor.append(Node(pos_new))
        return nodes_neighbor

    def get_route(self):
        route = []
        current_node = self.e_node

        while True:
            route.append(current_node.pos)
            current_node = current_node.father
            if current_node.pos == self.s_node.pos:
                break

        route.append(self.s_node.pos)
        route.reverse()
        return route


CELL_WIDTH = 16  # 单元格宽度
CELL_HEIGHT = 16  # 单元格长度
BORDER_WIDTH = 1  # 边框宽度
BLOCK_NUM = 50  # 地图中的障碍物数量
from random import randint


class Color(Enum):
    ''' 颜色 '''
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    @staticmethod
    def random_color():
        '''设置随机颜色'''
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)


def main(map_size=(80, 40), start_node=(1, 1), end_node=(30, 20), block_list=None):
    if block_list is None:
        block_list = [(3, 1)]
    map_size = map_size
    pos_s_node = start_node
    pos_e_node = end_node
    my_a_star = AStar(map_size, pos_s_node, pos_e_node)
    my_a_star.set_block(block_list)
    if my_a_star.run() == 0:
        route_list = my_a_star.get_route()
        print(route_list)
        show_result(map_size, pos_s_node, pos_e_node, block_list, route_list)
    else:
        print('路径规划失败！')


def gen_blocks(width, height):
    """
    随机生成障碍物
    :param width: 地图宽度
    :param height: 地图高度
    :return:返回障碍物坐标集合
    """
    i, block_list = 0, []
    random.seed(100)
    while i < BLOCK_NUM:
        block = (randint(0, width - 1), randint(0, height - 1))
        if block not in block_list:
            block_list.append(block)
            i += 1

    return block_list


def show_result(map_size, pos_sn, pos_en, block_list, route_list):
    # 初始化导入的Pygame模块
    pygame.init()
    # 此处要将地图投影大小转换为像素大小，此处设地图中每个单元格的大小为CELL_WIDTH*CELL_HEIGHT像素
    mymap = Map((map_size[0] * CELL_WIDTH, map_size[1] * CELL_HEIGHT))
    pix_sn = (pos_sn[0] * CELL_WIDTH, pos_sn[1] * CELL_HEIGHT)
    pix_en = (pos_en[0] * CELL_WIDTH, pos_en[1] * CELL_HEIGHT)
    # 对block_list和route_list中的坐标同样要转换为像素值
    bl_pix = list(map(transform, block_list))
    rl_pix = list(map(transform, route_list))
    # 初始化显示的窗口并设置尺寸
    screen = pygame.display.set_mode(mymap.map_size)
    # 设置窗口标题
    pygame.display.set_caption('A*算法路径搜索演示：')
    # 用白色填充屏幕
    screen.fill(Color.WHITE.value)  # 为什么用参数Color.WHITE不行？

    # 绘制屏幕中的所有单元格
    for (x, y) in mymap.generate_cell(CELL_WIDTH, CELL_HEIGHT):
        if (x, y) in bl_pix:
            # 绘制黑色的障碍物单元格，并留出2个像素的边框
            pygame.draw.rect(screen, Color.BLACK.value, (
                (x + BORDER_WIDTH, y + BORDER_WIDTH), (CELL_WIDTH - 2 * BORDER_WIDTH, CELL_HEIGHT - 2 * BORDER_WIDTH)))
        else:
            # 绘制绿色的可通行单元格，并留出2个像素的边框
            pygame.draw.rect(screen, Color.GREEN.value, (
                (x + BORDER_WIDTH, y + BORDER_WIDTH), (CELL_WIDTH - 2 * BORDER_WIDTH, CELL_HEIGHT - 2 * BORDER_WIDTH)))
    # 绘制起点和终点
    pygame.draw.circle(screen, Color.BLUE.value, (pix_sn[0] + CELL_WIDTH // 2, pix_sn[1] + CELL_HEIGHT // 2),
                       CELL_WIDTH // 2 - 1)
    pygame.draw.circle(screen, Color.RED.value, (pix_en[0] + CELL_WIDTH // 2, pix_en[1] + CELL_HEIGHT // 2),
                       CELL_WIDTH // 2 - 1)

    # 绘制搜索得到的最优路径
    rl_pix = [(pos[0] + CELL_WIDTH // 2, pos[1] + CELL_HEIGHT // 2) for pos in rl_pix]
    pygame.draw.aalines(screen, Color.RED.value, False, rl_pix)
    keep_going = True
    while keep_going:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
        pygame.display.flip()


def transform(pos):
    x_new, y_new = pos[0] * CELL_WIDTH, pos[1] * CELL_HEIGHT
    return x_new, y_new


if __name__ == '__main__':
    main()
