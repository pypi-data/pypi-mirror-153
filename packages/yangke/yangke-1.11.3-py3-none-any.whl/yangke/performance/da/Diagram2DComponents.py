import pygame
from pygame.sprite import Sprite


class GridSprite(Sprite):
    """
    网格线
    """

    def __init__(self, x_list, y_list, width=10, height=10, color=(0, 0, 0), line_width=1):
        """
        pygame的网格线部件
        :param x_list: 绘制的垂直于x轴的网格线的位置列表
        :param y_list: 绘制的垂直于y轴的网格线的位置列表
        :param width: 绘图界面的宽，也就是画布的宽
        :param height: 绘图界面的高，也就是画布的高
        :param color: 网格线的颜色
        :param line_width: 网格线的宽度
        """
        super(GridSprite, self).__init__()
        self.x_list = x_list
        self.y_list = y_list
        self.color = color
        self.line_width = line_width
        self.image = pygame.Surface([width, height]).convert_alpha()
        self.image.fill((255, 255, 255, 0))
        # self.image.set_alpha(128)  # 0全透明，看不到当前层，255完全不透明，看不到被遮挡的层
        self.rect = self.image.get_rect()
        self.draw()

    def update(self, x_list, y_list):
        self.x_list = x_list
        self.y_list = y_list
        self.draw()

    def draw(self, screen=None):
        """
        精灵的绘制会遮挡self.rect下的其他内容，没找到解决方法

        :param screen
        :return:
        """
        canvas = self.image
        canvas_width = canvas.get_width()
        canvas_height = canvas.get_height()
        if self.x_list is not None:
            for x in self.x_list:
                pygame.draw.line(canvas, color=self.color, start_pos=(x, 0), end_pos=(x, canvas_height), width=1)
        if self.y_list is not None:
            for y in self.y_list:
                pygame.draw.line(canvas, color=self.color, start_pos=(0, y), end_pos=(canvas_width, y), width=1)
        if screen is not None:
            screen.blit(self.image, (0, 0))


class YkPygameSprite(Sprite):
    def __init__(self):
        super(YkPygameSprite, self).__init__()
        self.position = (0, 0)
        self.connect_points = {}  # 记录图标上的锚点
        self.connect_points_dir = {}  # 记录锚点的方向
        self.connect_points_lines = {}  # 记录锚点与其他图标连接的线信息
        self.tag = None

    def move_to(self, x, y):
        """
        移动到位置(x,y)

        :param x:
        :param y:
        :return:
        """
        self.position = x, y
        self.scale_by(1)

    def scale_by(self, scale):
        w, h = self.image.get_width(), self.image.get_height()
        w_new, h_new = int(w * scale), int(h * scale)
        self.image = pygame.transform.scale(self.image, (w_new, h_new))
        self.rect = pygame.rect.Rect(self.position[0] - w_new // 2, self.position[1] - h_new // 2, w_new, h_new)

    def get_absolute_connect_points(self):
        """
        获取图标连接点的绝对坐标
        :return:
        """
        x, y = self.position
        connect_points = {}
        for name, pos in self.connect_points.items():
            if pos is not None:
                connect_points.update({name: (pos[0] + x, pos[1] + y)})
            else:
                connect_points.update({name: None})
        return connect_points


class BoilerDiagram(YkPygameSprite):
    """
    锅炉
    """

    def __init__(self, position=(0, 0), color=(0, 0, 0), line_width=2):
        super(BoilerDiagram, self).__init__()
        self.is_event_handler = False
        self.position = position  # 锅炉位置坐标
        self.line_width = line_width  # 线宽
        self.color = color  # 线条颜色
        # self.rect1 = [0, 0, 80, 100]

        self.image = pygame.Surface([80 + line_width, 120 + line_width]).convert_alpha()
        self.image.fill((255, 255, 255, 0))

        self.draw()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.rect.Rect(position[0] - width // 2, position[1] - height // 2, width, height)

        self.connect_points = {"主给水连接点": (-10, height//2), "主蒸汽连接点": (-10, -height//2),
                               "冷再连接点": None, "热再连接点": None}
        self.connect_points_dir = {"主给水连接点": "down", "主蒸汽连接点": "up",
                                   "冷再连接点": "down", "热再连接点": "up"}

    def draw(self):
        """
        绘制锅炉图标

        :return:
        """
        canvas = self.image
        pygame.draw.rect(canvas, width=self.line_width, color=self.color, rect=[0, 10, 80, 100])
        pygame.draw.lines(canvas, width=self.line_width, color=self.color, closed=False,
                          points=[(30, 0), (30, 20), (30, 100), (30, 120)])
        pygame.draw.lines(canvas, width=self.line_width, color=self.color, closed=False,
                          points=[(50, 0), (50, 20), (50, 100), (50, 120)])


class TurbineHigh(YkPygameSprite):
    def __init__(self, position=(0, 0), line_width=2, color=(0, 0, 0)):
        super(TurbineHigh, self).__init__()
        self.position = position
        self.line_width = line_width
        self.color = color

        self.center_line = (0, 100)
        self.image = pygame.Surface([120, 140]).convert_alpha()
        self.image.fill((0, 0, 255, 50))  # 第四个参数默认是255
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.rect.Rect(position[0] - width // 2, position[1] - height // 2, width, height)
        self.draw()

        self.connect_points = {"主蒸汽连接点": (118, 20), "冷再连接点": (0, 138), "1抽连接点": None}
        self.connect_points_dir = {"主蒸汽连接点": "up", "冷再连接点": "down", "1抽连接点": "down"}

    def draw(self):
        """
        绘制高压缸图标

        :return:
        """
        canvas = self.image
        pygame.draw.lines(canvas, width=self.line_width, color=self.color, closed=True,
                          points=[(0, 0), (118, 20), (118, 118), (0, 138)])


class TurbineMiddle(YkPygameSprite):
    def __init__(self, position=(0, 0), line_width=2, color=(0, 0, 0)):
        super(TurbineMiddle, self).__init__()
        self.position = position
        self.line_width = line_width
        self.color = color

        self.center_line = (0, 100)
        self.image = pygame.Surface([160, 140]).convert_alpha()
        self.image.fill((255, 255, 250, 0))
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.rect.Rect(position[0] - width // 2, position[1] - height // 2, width, height)
        self.draw()

        self.connect_points = {"热再连接点": (118, 20), "3抽连接点": (0, 138), "4抽连接点": None,
                               "中排连接点": (158, 0)}
        self.connect_points_dir = {"热再连接点": "up", "3抽连接点": "down", "4抽连接点": "down",
                                   "中排连接点": "down"}

    def draw(self):
        """
        绘制高压缸图标

        :return:
        """
        canvas = self.image
        pygame.draw.lines(canvas, width=self.line_width, color=self.color, closed=True,
                          points=[(0, 20), (158, 0), (158, 138), (0, 118)])


class Heater(YkPygameSprite):
    def __init__(self, position=(0, 0), line_width=2, color=(0, 0, 0)):
        super(Heater, self).__init__()
        self.position = position
        self.line_width = line_width
        self.color = color

        self.image = pygame.Surface([80, 40]).convert_alpha()
        self.image.fill((255, 255, 255, 0))
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.rect.Rect(position[0] - width // 2, position[1] - height // 2, width, height)
        self.draw()

        self.connect_points = {"进水连接点": (78, 20), "进汽连接点": (20, 0), "出水连接点": (0, 20),
                               "疏水出口连接点": (70, 30), "上级连排疏水连接点": None}
        self.connect_points_dir = {"进水连接点": "down", "进汽连接点": "up", "出水连接点": "left",
                                   "疏水出口连接点": "down", "上级连排疏水连接点": "down"}

    def draw(self):
        """
        绘制高压缸图标

        :return:
        """
        canvas = self.image
        pygame.draw.lines(canvas, width=self.line_width, color=self.color, closed=True,
                          points=[(0, 0), (78, 0), (78, 38), (0, 38)])
        pygame.draw.line(canvas, color=self.color, start_pos=(58, 0), end_pos=(58, 40), width=self.line_width)
