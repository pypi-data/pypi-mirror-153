# 需要画面分辨率为1280*720，该区域指客户区大小，整个窗口的大小更大一些，一般为（1296, 759）
import time

from yangke.common.win.win_x64 import capture_pic_undecorated, post_key, do_click, win32con, get_nsh_window, find_pic, \
    logger, os, get_size_of_window
from yangke.objDetect.ocr import ocr
from yangke.core import strInList
from yangke.panda.flow import State, ActionNode, Action

file_temp = "temp.png"
image_folder = r"D:\Users\YangKe\PycharmProjects\lib4python\yangke\panda\nsh\image"
width, height = 1280, 720
display_set_xy = (12, 11)
character_xy = (958, 687)
bag_xy = (994, 689)
task_xy = (1035, 689)
skill_xy = (1073, 688)
manor_xy = (1108, 691)  # 庄园
dress_xy = (1150, 691)  # 时装
team_xy = (1189, 690)
friend_xy = (1224, 695)
union_xy = (1262, 691)  # 帮会
task_section = (1013, 349, 1265, 431)
task_button = (1030, 332)
coor_section = (1187, 34, 1256, 51)
skill_list_xy = [
    (412, 689),
    (464, 688),
    (511, 691),
    (557, 685),
    (608, 690),
    (655, 693),
    (704, 686),
    (756, 690),
    (799, 687),
    (851, 688),
]

skill_F4_xy = (524, 643)
direction_front_xy = (645, 316)


def 快捷点击任务(hwnd):
    post_key(hwnd, ord('F'), [win32con.VK_CONTROL])


def 初始化():
    hwnd = get_nsh_window()
    return hwnd


def 点击角色(hwnd):
    do_click(character_xy[0], character_xy[1], hwnd)


def 获取第一个任务(hwnd):
    """
    已测试完成

    :param hwnd:
    :return:
    """
    关闭子窗口(hwnd)
    do_click(task_button[0], task_button[1], hwnd)  # 点击任务按钮，防止任务面板现实的不是主任务区
    time.sleep(0.5)
    capture_pic_undecorated(hwnd, task_section[0], task_section[1], task_section[2], task_section[3], save_to=file_temp)
    text = ocr(file_temp, method="paddleocr", paragraph=True)
    return text


def respawn(hwnd):
    """
    如果角色死亡，则复活角色

    :param hwnd:
    :return:
    """
    capture_pic_undecorated(hwnd, save_to=file_temp)
    exists, (x, y) = find_pic(os.path.join(image_folder, "复活.png"))
    if exists:
        logger.debug("角色死亡，免费复活")
        do_click(x, y, hwnd)


def close_child_window(hwnd):
    """
    关闭子窗口

    :param hwnd:
    :return:
    """
    capture_pic_undecorated(hwnd, save_to=file_temp)
    exist, _ = find_pic(os.path.join(image_folder, "close.png"))
    if exist:
        do_click(_[0] + 5, _[1] + 5, hwnd)
        time.sleep(1)
        capture_pic_undecorated(hwnd, save_to=file_temp)

    exist, _ = find_pic(os.path.join(image_folder, "close1.png"))
    if exist:
        do_click(_[0] + 5, _[1] + 5, hwnd)
        time.sleep(1)
        capture_pic_undecorated(hwnd, save_to=file_temp)

    exist, _ = find_pic(os.path.join(image_folder, "close2.png"))
    if exist:
        do_click(_[0] + 5, _[1] + 5, hwnd)
        time.sleep(1)
        capture_pic_undecorated(hwnd, save_to=file_temp)

    exist, _ = find_pic(os.path.join(image_folder, "close3.png"))
    if exist:
        do_click(_[0] + 5, _[1] + 5, hwnd)
        time.sleep(1)


def get_coordinate(hwnd):
    """
    获取当前角色所在的坐标

    :param hwnd:
    :return:
    """
    _ = coor_section
    while not is_main_screen(hwnd):  # 等待进入主界面在开始获取坐标
        close_child_window(hwnd)
        time.sleep(1)
    capture_pic_undecorated(hwnd, _[0], _[1], _[2], _[3], save_to=file_temp)
    text: str = ocr(file_temp, paragraph=True, method="paddleocr")
    return text


def is_moving(hwnd):
    """
    判断角色是否移动，如果为False，表示角色不在移动。但不移动也可能误判为移动。

    :param hwnd:
    :return:
    """
    last = get_coordinate(hwnd)
    time.sleep(1)
    this = get_coordinate(hwnd)
    if this == last:
        return False
    else:
        return True


def is_chatting(hwnd):
    """
    判断是否在对话

    :param hwnd:
    :return:
    """
    _ = (1180, 674, 1250, 700)
    capture_pic_undecorated(hwnd, _[0], _[1], _[2], _[3], save_to=file_temp)
    text: str = ocr(file_temp, paragraph=True, method="paddleocr")
    if text == "Esc离开":
        return True


def is_main_screen(state):
    """
    判断是否在主画面

    :param hwnd:
    :return:
    """
    return get_state_main_screen(state).is_state()


def get_state_main_screen(state: State):
    return state.set_state("section.png", section=(925, 670, 1280, 710))


def do_task(hwnd):
    flag = True
    task = 获取第一个任务(hwnd)  # 太耗时，不要放在循环量
    while flag:
        close_child_window(hwnd)
        post_key(hwnd, ord("F"), [win32con.VK_CONTROL])
        logger.debug(f"正在做任务【{task}】...")
        while is_moving(hwnd):  # 如果在移动，说明正在寻路，则等待
            logger.debug("移动中...")
            time.sleep(1)
        capture_pic_undecorated(hwnd, task_section[0], task_section[1], task_section[2], task_section[3],
                                save_to=file_temp)
        text: str = ocr(file_temp, paragraph=True, method="paddleocr")
        task = text.strip().split(" ")[0]
        if strInList(text, ["杀", "击", "剿灭", "战胜"], revert=True):
            自动战斗(hwnd)
        capture_pic_undecorated(hwnd, save_to=file_temp)
        respawn(hwnd)  # 如果角色死亡，则复活
        exists, (x, y) = find_pic(os.path.join(image_folder, "提交.png"))
        if exists:
            logger.debug("提交物品")
            do_click(x, y, hwnd)
        close_child_window(hwnd)
        exist, _ = find_pic(os.path.join(image_folder, "F.png"))
        if exist:
            post_key(hwnd, ord("F"), [])
            post_key(hwnd, ord("F"), [])
            post_key(hwnd, ord("F"), [])
        exist, _ = find_pic(os.path.join(image_folder, "chose1.png"))
        if exist:
            do_click(_[0] + 20, _[1] + 10, hwnd)
        exist, _ = find_pic(os.path.join(image_folder, "分支剧情.png"))
        if exist:
            do_click(_[0] + 20, _[1] + 10, hwnd)


def 关闭子窗口(hwnd):
    capture_pic_undecorated(hwnd, save_to=file_temp)
    exist, _ = find_pic(os.path.join(image_folder, "close.png"))
    if exist:
        do_click(_[0] + 5, _[1] + 5, hwnd)
    for i in range(2):
        post_key(hwnd, win32con.VK_ESCAPE, None)
        time.sleep(1)
    time.sleep(1)
    exist, _ = find_pic(os.path.join(image_folder, "系统设置_返回游戏.png"))
    if exist:
        do_click(_[0], _[1], hwnd)


def 是否有目标(hwnd):
    target_bar = (596, 68, 724, 78)
    capture_pic_undecorated(hwnd, target_bar[0], target_bar[1], target_bar[2], target_bar[3],
                            save_to=file_temp)
    text = ocr(file_temp, paragraph=True, method="paddleocr")
    import re
    m = re.match(r'\d+/\d+\({0,1}\d+%', text)
    if m:
        return True
    else:
        return False


def 自动战斗(hwnd):
    no_target_ = (575, 393, 701, 418)  # 无目标提示区域
    logger.debug("自动战斗...")
    while True:
        post_key(hwnd, ord("M"), None)  # M切换敌人，设置快捷键
        post_key(hwnd, ord("F"), [win32con.VK_CONTROL])
        # post_key(hwnd, ord("V"), None)  # 技能按键都被屏蔽了，需要找新方法发送战斗按键
        # for i in range(10):
        #     skill_i = skill_list_xy[i]
        #     do_click(skill_i[0], skill_i[1], hwnd)
        #     time.sleep(0.8)
        # 召唤宝宝
        do_click(skill_F4_xy[0], skill_F4_xy[1], hwnd)
        do_click(direction_front_xy[0], direction_front_xy[1], hwnd)
        # 使用灵犀三现
        do_click(skill_list_xy[0][0], skill_list_xy[0][1], hwnd)
        do_click(direction_front_xy[0], direction_front_xy[1], hwnd)
        time.sleep(0.5)
        capture_pic_undecorated(hwnd, no_target_[0], no_target_[1], no_target_[2], no_target_[3],
                                save_to=file_temp)  # 灵犀三现没有目标会有提示
        text = ocr(file_temp, paragraph=True, method="paddleocr")
        logger.debug(text)
        respawn(hwnd)
        if text == "没有合适的目标":
            logger.debug("战斗结束")
            break
        capture_pic_undecorated(hwnd, save_to=file_temp)
        exist, _ = find_pic(os.path.join(image_folder, "F.png"))
        if exist:
            post_key(hwnd, ord("F"), [])
            break
    return None


def 开始匹配战场(hwnd):
    capture_pic_undecorated(hwnd, save_to=file_temp)
    min_value, _ = find_pic(os.path.join(image_folder, "zhan.png"))
    do_click(_[0], _[1], hwnd)
    min_value, _ = find_pic(os.path.join(image_folder, "match.png"))
    do_click(_[0], _[1], hwnd)


def 寻路任务一(hwnd):
    post_key(hwnd, ord("F"), [win32con.VK_CONTROL])
    while is_moving(hwnd1):
        time.sleep(1)
        logger.debug("寻路中...")
    return True


def 帮会快意恩仇(hwnd):
    # ------------------- pre -------------------------
    ActionNode(get_state_main_screen(state), action.set_action(pos=(union_xy[0], union_xy[1])),
               state.set_state("修炼.png"), else_action=action.set_action(key="Esc")).do()
    ActionNode(state.set_state("修炼.png")).do()
    close_child_window(hwnd)
    ActionNode(state.set_state(section=coor_section, target=2, state="unchanging"),
               action.set_action(key="F"),
               state.set_state("快意恩仇.png")).do()
    ActionNode(state.set_state("快意恩仇.png"),
               out_node=state.set_state("接受", section=(1117, 591, 1170, 613))).do()  # 找到图片则点击
    ActionNode(state.set_state("接受", section=(1117, 591, 1170, 613)),
               action.set_action(pos=(1117, 591)))  # 找到文字则点击

    post_key(hwnd, ord("F"), [win32con.VK_CONTROL])
    while is_moving(hwnd):
        time.sleep(1)
    post_key(hwnd, ord("F"), None)
    time.sleep(1)
    do_click(task_button[0], task_button[1], hwnd)  # 点击任务按钮，防止任务面板现实的不是主任务区
    close_child_window(hwnd)
    寻路任务一(hwnd)
    do_click(582, 404, hwnd)
    time.sleep(0.8)
    do_click(1125, 596, hwnd)


def run():
    hwnd = 初始化()
    w_, height_ = get_size_of_window(hwnd, client=True)
    if (w_, height_) != (1280, 720):
        logger.warning(f"客户端分辨率不是（1280, 720），可能出现错误！")
    return hwnd


if __name__ == "__main__":
    hwnd1 = run()
    state = State(hwnd1, image_folder=image_folder)
    action = Action(hwnd1, image_folder=image_folder)
    # get_coordinate(hwnd1)
    帮会快意恩仇(hwnd1)

    # do_task(hwnd1)
    # 自动战斗(hwnd)
