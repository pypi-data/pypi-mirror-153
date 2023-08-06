# encoding=utf-8
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, TextNode, load_prc_file_data, ConfigVariableString
from direct.gui.DirectGui import *

"""
panda3d中的CamelCase和camel_case格式的函数名是同样功能的，只是一个是C++命名规则，一个是python命名规则
"""

# text-encoding
load_prc_file_data("", "text-default-font /c/Windows/Fonts/simsun.ttc")  # 使panda3D支持中文


class Game(ShowBase):
    def __init__(self):
        super(Game, self).__init__()
        self.text1, self.text2, self.game_over_screen, self.final_score_label = None, None, None, None
        self.init2d()
        # self.scene = self.loader.loadModel("models/environment")
        self.scene = self.loader.loadModel("models/海马/haima")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        # self.disable_mouse()

    def init2d(self):
        properties = WindowProperties()
        properties.setSize(1400, 750)
        properties.setTitle("性能监测及运行优化系统")
        self.win.requestProperties(properties)
        bk_text = "DirectOptionMenu Demo"
        self.text1 = OnscreenText(text=bk_text, pos=(0.85, 0.85), scale=0.07,
                                  fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                                  mayChange=1)
        output = "item "
        self.text2 = OnscreenText(text=output, pos=(0.95, -0.95), scale=0.07,
                                  fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                                  mayChange=1)
        # menu = DirectOptionMenu(text="options", scale=0.1, command=self.item_sel,
        #                         items=["item1", "item2", "item3"], initialitem=2,
        #                         highlightColor=(0.0, 0.65, 0.65, 1), pos=(0, 0, 0))

        self.game_over_screen = DirectDialog(frameSize=(-0.7, 0.7, -0.7, 0.7), fadeScreen=0.4, relief=DGG.FLAT,
                                             frameTexture="UI/stoneFrame.jpg")
        label = DirectLabel(text="Game Over!", parent=self.game_over_screen, scale=0.1, pos=(0, 0, 0.2))

        self.final_score_label = DirectLabel(text="", parent=self.game_over_screen, scale=0.07, pos=(0, 0, 0))
        btn = DirectButton(text="重新开始", command=self.start_game, pos=(-0.3, 0, -0.2), parent=self.game_over_screen,
                           scale=0.07)
        DirectButton(text="退出", command=self.quit, pos=(0.3, 0, -0.2), parent=self.game_over_screen, scale=0.07)
        self.game_over_screen.hide()

    def item_sel(self, arg):
        output = "选择了选项：" + arg
        self.text2.setText(output)

    def start_game(self):
        ...

    def quit(self):
        ...


game = Game()
game.run()
