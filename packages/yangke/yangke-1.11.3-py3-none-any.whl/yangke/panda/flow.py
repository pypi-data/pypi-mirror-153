"""
定义操作流程
"""
import copy
import os.path
import time

from yangke.base import pic2ndarray
from yangke.common.win.win_x64 import *
from yangke.objDetect.ocr import ocr


class State:
    def __init__(self, hwnd, image_folder):
        self.hwnd = hwnd
        self.target = None
        self.type = "image"
        self.image_folder = image_folder
        self.state = "exist"  # 有"exist","absent","unchanging", "changing"四种取值，分别表示存在，不存在，保持不变，变化中
        self.threshold = 0.8
        self.pos = None
        self.section = None

    def set_state(self, target, state="exist", threshold=0.8, section=None):
        """

        :param target:
        :param state: 有"exist","absent","unchanging", "changing"四种取值，分别表示存在，不存在，保持不变，变化中
        :param threshold:
        :param section:
        :return:
        """
        self.type = "image"  # 状态的类型，是发现什么图片还是找到什么文字
        if isinstance(target, str):
            if os.path.exists(os.path.join(self.image_folder, target)):  # 首先尝试在指定的image_folder目录下查找目标图片
                self.target = os.path.join(self.image_folder, target)
            elif os.path.exists(target):  # 如果上面目录没查到，则在当前程序娙目录中查找
                self.target = os.path.abspath(target)
            try:
                self.target = pic2ndarray(self.target)
            except:
                self.type = "text"  # 如果target转换为图片时发生错误，则类型为text
        if target == 1:  # 当state为unchanging或changing时，target标记目标的类型，1表示图片不变，2表示文字
            self.type = "image"
        elif target == 2:
            self.type = "text"

        self.state = state  # 判断的条件是存在还是不存在，默认target存在则条件满足，返回True
        self.threshold = threshold
        self.section = section
        return copy.deepcopy(self)

    def is_state(self):
        if self.section is not None:
            _ = self.section
        else:
            _ = (0, 0, 0, 0)
        capture_pic_undecorated(self.hwnd, x1=_[0], y1=_[1], x2=_[2], y2=_[3])
        if self.type == "image":
            exists, pos = find_pic("temp.png", self.target, threshold=self.threshold)
            if exists:
                self.pos = pos
                if self.state == "exist":  # 要求存在，并且存在，则返回True
                    return True
                elif self.state == "absent":  # 要求不存在，但是存在，则返回False
                    return False
            else:
                if self.state == "exist":  # 要求存在，但是不存在，则返回False
                    return False
                elif self.state == "absent":  # 要求不存在，并且不存在，则返回True
                    return True
        else:
            text = ocr("temp.png", self.threshold, paragraph=True, method="paddleocr")
            if self.state == "exist":
                if self.target in text:
                    return True
                else:
                    return False
            elif self.state == "absent":
                if self.target in text:
                    return True
                else:
                    return False
            elif self.state == "unchanging":
                time.sleep(1)
                text1 = ocr("temp.png", self.threshold, paragraph=True, method="paddleocr")
                if text1 == text:  # 如果文字未改变，则返回True
                    return True
                else:
                    return False
            elif self.state == "changing":
                time.sleep(1)
                text1 = ocr("temp.png", self.threshold, paragraph=True, method="paddleocr")
                if text1 == text:
                    return False
                else:
                    return True
        return False


class Action:
    def __init__(self, hwnd, image_folder=""):
        self.hwnd = hwnd
        self.image_folder = image_folder
        self.act = "mouse"
        self.pos = None
        self.key = None
        self.right = None

    def set_action(self, pos=None, key=None, right=False):
        """
        设置动作，不支持鼠标键盘同时操作

        :param pos: 位置
        :param key: 按键，可取值：‘ctrl+f’,'shift+1'等
        :param right: 是否鼠标右键
        :return:
        """
        self.pos = pos
        self.key = key
        if self.key is not None:
            self.act = "key"
        else:
            self.act = "mouse"
        self.right = False
        return copy.deepcopy(self)

    def do(self):
        if self.act == "mouse":
            _ = self.pos
            do_click(_[0], _[1], self.hwnd, self.right)
        else:
            keys = self.key.strip().split("+")
            shift = []
            key = 0
            for k in keys:
                if len(k) == 1:
                    key = ord(k)
                elif k.lower() == "ctrl":
                    shift.append(win32con.VK_CONTROL)
                elif k.lower() == "alt":
                    shift.append(win32con.VK_MENU)
                elif k.lower() == "shift":
                    shift.append(win32con.VK_SHIFT)
                elif k.lower() == "esc":
                    key = win32con.VK_ESCAPE
            post_key(hwnd=self.hwnd, key=key, shift=shift)


class ActionNode:
    def __init__(self, in_node, action=None, out_node=None, else_action=None):
        self.condition: State = in_node  # 当前发现什么，即如果该状态满足，才进行相应操作
        self.action: Action = action  # 状态满足后需要执行的操作
        self.else_action = else_action  # 万一第一个状态不满足，需要执行的操作
        self.result: State = out_node  # 操作执行后，应当产生的结果，如果该结果没有发生，则再次执行self.action
        self.pos = self.condition.pos

    def do(self):
        _ = 0
        while not self.condition.is_state():  # 当不满足输入状态时，等待
            time.sleep(1)
            _ += 1
            if _ > 5 and self.else_action is not None:  # 当等待超过10秒时，尝试补救操作
                self.else_action.do()
            if _ > 10:  # 仍然操作无效时，报错
                logger.error("尝试了各种方法，但一直无法满足ActionNode的初始状态!")
                break
        if self.action is None:
            # 如果没有指定动作，则默认点击condition的坐标位置，因为condition一般为查找某个图标，该图标往往是点击目标
            self.action = Action(self.condition.hwnd, self.condition.image_folder)
            self.action.set_action(pos=(self.condition.pos[0], self.condition.pos[1]))
        self.action.do()
        time.sleep(1)
        if self.result is None:
            return True
        while not self.result.is_state():
            self.action.do()
            time.sleep(1)
        return True

# state = State(hwnd, image_folder="")
#
# action1 = ActionNode(state.set_state("*.png"), Action("Mouse", pos=(0, 0)),
#                      state.set_state("接受", section=(0, 0, 200, 200)))
# action1.do()
