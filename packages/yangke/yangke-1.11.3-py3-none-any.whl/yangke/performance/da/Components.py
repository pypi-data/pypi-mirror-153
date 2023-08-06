"""
热力系统图的组件类
"""
from cocos.cocosnode import CocosNode
from pyglet.gl import *


class Boiler(CocosNode):
    def __init__(self, position=(80, 200), scale=1, line_width=2, color=(0, 0, 0)):
        """
        锅炉图标
        """
        super(Boiler, self).__init__()
        self.position = position
        self.scale = scale
        self.line_width = line_width
        self.color = color

        self.in_water_coor = None  # 给水的连接点坐标
        self.main_steam_coor = None  # 主蒸汽的连接点坐标
        self.cold_reheat_steam_coor = None  # 冷再的连接点坐标
        self.heat_reheat_steam_coor = None  # 热再的连接点坐标
        self.draw()

    def move_by(self, dx, dy):
        """
        相对移动

        :param dx:
        :param dy:
        :return:
        """
        self.position = self.position[0] + dx, self.position[1] + dy

    def move_to(self, x, y):
        """
        移动到位置(x,y)

        :param x:
        :param y:
        :return:
        """
        self.position = x, y

    def draw(self):
        # glPushMatrix()
        # self.transform()
        glLineWidth(3)
        glColor4b(0, 0, 0, 100)
        # # glTexCoord2d(0, 0)
        glBegin(GL_LINES)
        glVertex2f(self.position[0] - 40, self.position[1] - 60)
        glVertex2f(self.position[0] + 40, self.position[1] - 60)
        glVertex2f(self.position[0] + 40, self.position[1] - 60)
        glVertex2f(self.position[0] + 40, self.position[1] + 60)
        glVertex2f(self.position[0] + 40, self.position[1] + 60)
        glVertex2f(self.position[0] - 40, self.position[1] + 60)
        glVertex2f(self.position[0] - 40, self.position[1] + 60)
        glVertex2f(self.position[0] - 40, self.position[1] - 60)
        glEnd()
        # #
        # glFlush()
        # glPopMatrix()
        # glRectf(self.position[0]-40, self.position[1]-60, self.position[0]+40, self.position[1]+60)
