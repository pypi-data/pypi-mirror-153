"""
绘制热力系统图

"""
import cocos
import pyglet
from cocos.actions import *
from cocos.director import director
from cocos.scene import Scene
from cocos.cocosnode import CocosNode
from pyglet.canvas import Canvas

from yangke.performance.da.Components import Boiler


class KeyDisplay(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(KeyDisplay, self).__init__()
        self.text = cocos.text.Label("", x=100, y=280)
        self.key_pressed = set()
        self.update_text()
        self.add(self.text)

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string(k) for k in self.key_pressed]
        text = 'Keys: ' + ','.join(key_names)
        self.text.element.text = text

    def on_key_press(self, key, modifiers):
        self.key_pressed.add(key)
        self.update_text()

    def on_key_release(self, key, modifiers):
        self.key_pressed.remove(key)
        self.update_text()


class MouseDisplay(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(MouseDisplay, self).__init__()
        self.posx = 100
        self.posy = 240
        self.text = cocos.text.Label('No mouse event yet',
                                     font_size=18,
                                     x=self.posx, y=self.posy)
        self.add(self.text)

    def update_text(self, x, y):
        text = f"Mouse @ {x},{y}"
        self.text.element.text = text
        self.text.element.x = self.posx
        self.text.element.y = self.posy

    def on_mouse_motion(self, x, y, dx, dy):
        self.update_text(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.update_text(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.posx, self.posy = director.get_virtual_coordinates(x, y)
        self.update_text(x, y)


class MyApp(cocos.layer.ColorLayer):
    def __init__(self):
        super(MyApp, self).__init__(255, 255, 255, 255)
        # super(MyApp, self).__init__()

        # label = cocos.text.Label('Hello, World!',
        #                          font_name='Times New Roman',
        #                          font_size=32,
        #                          anchor_x='center', anchor_y='center',
        #                          position=(320, 240))
        # self.add(label)
        self.add(Boiler(), z=1)

        # sprite = cocos.sprite.Sprite("grossini.png", position=(320, 240), scale=1)
        # self.add(sprite, z=1)
        # scale = ScaleBy(3, duration=2)  # 两秒内缩放三次
        # label.do(Repeat(scale + Reverse(scale)))  # 将缩放动作添加到label标签上


if __name__ == "__main__":
    director.init(resizable=True, width=1400, height=800)
    # app_layer = MyApp()
    # app_layer.do(RotateBy(360, duration=10))  # 让整个画面旋转
    # director.run(Scene(app_layer))
    director.run(Scene(MyApp()))
