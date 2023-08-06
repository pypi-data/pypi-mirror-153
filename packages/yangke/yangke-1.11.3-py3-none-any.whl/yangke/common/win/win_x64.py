"""
win10系统专用，用于在windows操作系统中获取窗口、进程等应用程序操作
"""
import ctypes
import time

import cv2
import win32gui
import win32ui
import win32con
import win32process
from PIL import Image
import os
import win32api
from yangke.base import pic2ndarray, crop_pic
from yangke.common.config import logger

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def get_user32():
    """
    通过该方法返回的对象可以调用user32.dll中的函数

    :return:
    """
    # user32.dll是stdcall
    from ctypes import windll
    # import ctypes
    # _user32 = ctypes.WinDLL("user32")
    return windll.user32


def get_Ws2_32():
    """
    通过该方法返回的对象可以调用Ws2_32.dll中的函数，例如send发包函数

    :return:
    """
    from ctypes import windll
    # Ws2_32.send()  # 发包函数
    return windll.Ws2_32


def get_kernel32():
    """
    通过该方法返回的对象可以调用kernel32.dll中的函数，例如LoadLibraryA，OpenProcess等
    参见https://docs.microsoft.com/zh-cn/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess

    :return:
    """
    # kernel32.dll是stdcall
    from ctypes import windll
    return windll.kernel32


def get_msvcrt():
    # msvcrt是微软C标准库，包含了大部分C标准函数，这些函数都是以cdecl调用协议进行调用的
    # 例如 msvcrt.printf()  msvcrt.strchr()
    from ctypes import cdll
    return cdll.msvcrt


def get_all_window():
    """
    获取windows系统中当前所有的窗口句柄及标题
    :return: 返回格式为{hwnd, title}的字典
    """
    hwnd_title = {}

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible((hwnd)):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    return hwnd_title


def find_window(title, window_cls=None, exact=True):
    """
    查找窗口句柄，可以精确查找指定标题的窗口，也可模糊查找标题包含指定字符串的窗口。
    如果精确查找，则只返回一个窗口句柄值，返回类型为int，在存在多个同名窗口时，也只返回找到的第一个。
    如果模糊查找，会返回包含指定字符串的所有窗口的句柄信息，返回格式为{hwnd:title}的字典。

    :param title: 查找的窗口名称
    :param window_cls: 窗口的类名，例如："GxWindowClass"、"Windows.UI.Core.CoreWindow"等，不指定则匹配所有类型的窗口
    :param exact: 是否精确查找，默认为True，为False是则匹配包含title的所有窗口
    :return: exact为True是返回窗口的句柄，exact为False时返回{hwnd:title}
    """
    # 获取句柄
    window_cls = window_cls or 0
    if exact:
        hwnd = win32gui.FindWindow(window_cls, title)
        return hwnd
    else:
        hwnd_title = get_all_window()
        hwnd_title_filter = {}
        for hwnd1, title1 in hwnd_title.items():
            title1 = str(title1)
            if title1.find(title) != -1:
                hwnd_title_filter[hwnd1] = title1
        return hwnd_title_filter


def filter_windows_by_cls(hwnd_list, cls_name=0):
    """
    按类名筛选窗口，返回类名为cls_name的窗口

    :param hwnd_list:
    :param cls_name:
    :return:
    """
    if not isinstance(cls_name, list):
        cls_name = [cls_name]
    result = []
    for hwnd in hwnd_list:
        _name = win32gui.GetClassName(hwnd)
        if _name in cls_name:
            result.append(hwnd)
    return result


def filter_windows_by_title(hwnd_list, title=None):
    if not isinstance(title, list):
        title = [title]
    result = []
    for hwnd in hwnd_list:
        _t = win32gui.GetWindowText(hwnd)
        if _t in title:
            result.append(hwnd)
    return result


def find_child_windows(hwnd_parent, window_cls=None, title=None):
    """
    获取父窗口下的子窗口

    :param hwnd_parent: 父窗口的句柄
    :param window_cls: 字符型或字符型的列表，是窗体的类名，如果需要保留多种类的窗口，则以列表形式传入多个类名
    :param title: 字符型，是窗体的类名
    :return:
    """
    if not hwnd_parent:
        return []
    window_cls = window_cls or 0
    # win32gui.FindWindowEx(hwnd_parent, hwnd_child, window_cls, title) # 该方法获取子窗口有时候获取不到，不要使用，例如不知道类名时，无法使用
    hwndChildList = []
    win32gui.EnumChildWindows(hwnd_parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
    # 按类名筛选窗口
    if window_cls != 0:
        hwndChildList = filter_windows_by_cls(hwndChildList, cls_name=window_cls)
    if title is not None:
        hwndChildList = filter_windows_by_title(hwndChildList, title=title)

    return hwndChildList


def get_pid_by_hwnd(hwnd):
    """
    根据窗口句柄获取进程ID
    """
    thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
    return thread_id, pid


def get_size_of_window(hwnd, client=False):
    """
    获取窗口大小

    :param hwnd: 窗口句柄
    :param client: 是否获取客户区大小，即不包括标题框的窗口大小，默认为否，即返回总大小
    :return:
    """
    if client:
        left, top, right, bot = win32gui.GetClientRect(hwnd)
    else:
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    return width, height


def capture_pic_undecorated(hwnd, x1=0, y1=0, x2=0, y2=0, save_to="temp.png"):
    """
    截取窗口不包括标题框的区域的画面

    :param hwnd:
    :param x1: 截图区域的左上角x坐标，
    :param y1: 截图区域的左上角y坐标
    :param x2: 截图区域的右下角x坐标
    :param y2: 截图区域的右下角y坐标
    :param save_to:
    :return:
    """
    capture_pic(hwnd, save_to=save_to)
    w_, h_ = get_size_of_window(hwnd)  # 窗口总大小
    w, h = get_size_of_window(hwnd, client=True)  # 客户去大小，即不包括标题框的区域的大小
    pad_x = int((w_ - w) / 2)
    pad_y_t = int(h_ - h - pad_x)
    pad_y_b = int(h_ - h - pad_y_t)
    crop_pic(save_to, pad_x, pad_y_t, w_ - pad_x, h_ - pad_y_b, save_to=save_to)  # 裁掉图片中窗口的修饰框
    if (x1, y1, x2, y2) != (0, 0, 0, 0):  # 如果需要传入了截图区域，则对图片进行裁剪
        crop_pic(save_to, x1, y1, x2, y2, save_to)  # 对窗口客户区中的区域进行裁剪
    return save_to


def capture_pic(hwnd, x1=0, y1=0, x2=0, y2=0, save_to: str = "temp.png", show=False):
    """
    截取给定句柄对应的窗口中指定位置的图像，可以处理后台画面，默认截取整个窗口画面。
    测试游戏画面可以截取成功，如逆水寒，但Windows的记事本、计算器截取不成功

    :param hwnd: 要截图的窗口句柄
    :param x1: 截图区域的左上角x坐标，
    :param y1: 截图区域的左上角y坐标
    :param x2: 截图区域的右下角x坐标
    :param y2: 截图区域的右下角y坐标
    :param save_to: 保存截图到文件时，通过该参数指定文件名
    :return:
    """
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    # 获取句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hwnd_DC = win32gui.GetWindowDC(hwnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hwnd_DC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    # 保存图像
    # 方法一：windows api保存
    # saveBitMap.SaveBitmapFile(saveDC, save_to)

    # 方法二：PIL保存
    bmp_info = saveBitMap.GetInfo()
    bmp_str = saveBitMap.GetBitmapBits(True)
    im_PIL = Image.frombuffer('RGB', (bmp_info['bmWidth'], bmp_info['bmHeight']), bmp_str, 'raw', 'BGRX', 0, 1)

    im_PIL.save(save_to)
    if show:
        im_PIL.show()

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_DC)
    if (x1, y1, x2, y2) != (0, 0, 0, 0):  # 如果需要传入了截图区域，则对图片进行裁剪
        crop_pic(save_to, x1, y1, x2, y2, save_to)


def 注入dll(目标进程ID, dll_path):
    """
    将dll_path指定的dll文件注入到目标进程中

    :param 目标进程ID:
    :param dll_path:
    :return:
    """
    win32process.CreateRemoteThread()


def find_pic(template: str, screen: str = "temp.png", threshold: float = 0.8):
    """
    从图片中查找另一张图片的位置

    :param screen: 大图片，即在该图片中查找
    :param template: 小图片，即在大图片中查找该图片的相对位置
    :param threshold: 阈值，越大则要求越相似
    :return: exists, (x,y)
    """
    threshold = 1 - threshold
    try:
        # scr = cv2.imread(screen)
        scr = pic2ndarray(screen)
        tp = pic2ndarray(template)
        result = cv2.matchTemplate(scr, tp, cv2.TM_SQDIFF_NORMED)
    except cv2.error:
        print('文件错误：', screen, template)
        time.sleep(1)
        try:
            scr = cv2.imread(screen)
            tp = cv2.imread(template)
            result = cv2.matchTemplate(scr, tp, cv2.TM_SQDIFF_NORMED)
        except cv2.error:
            return False, None
    h, w = scr.shape[:2]
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # logger.debug(f"{min_val=}, {max_val=}")
    # min_val越小，表示可信度越高
    exist = True
    if min_val < threshold:
        logger.debug(f"找图可信度较高:{os.path.basename(template)}")
    else:
        logger.warning(f"找图可信度较低:{os.path.basename(template)}")
        exist = False
    coordinate = (min_loc[0], min_loc[1])
    return exist, coordinate


def do_click(cx, cy, hwnd, right=False):
    """
    在窗口上点击鼠标，测试hwnd为桌面句柄时成功。
    逆水寒游戏窗口测试失败。

    :param right: 是否右键点击，默认否
    :param cx: 点击位置在窗口的相对x坐标
    :param cy: 点击位置在窗口的相对y坐标
    :param hwnd: 需要点击的窗口句柄
    :return:
    """
    logger.debug(f"左键点击({cx, cy})")
    long_position = win32api.MAKELONG(cx, cy)
    if right:
        win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, long_position)
        time.sleep(0.1)
        win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, long_position)
    else:
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        time.sleep(0.1)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)


def key_press(hwnd, key):
    ...


def post_key(hwnd, key, shift, specialkey=False, last_time=0.01):
    """
    向指定窗口发送按键事件，记事本已测试成功，逆水寒测试成功。但部分按键的功能与实际按键功能不一致，原因未知。
    某些应用可能无法使用，测试失败的有：斗鱼客户端(客户端会激活，但功能无效)

    示例：
    hwnd = 记事本编辑框的窗口句柄 # 需要注意的是，如果是Ctrl+S这类功能按键，窗口句柄是记事本的根句柄还是下面的字句并都无所谓，但如果是编辑内容的输入，如输入A字母，则必须是编辑子窗口的句柄
    PostKeyEx(hwnd, ord('A'), [win32con.VK_CONTROL], False)  # 全选记事本内容，相当于发送Ctrl+A按键事件
    PostKeyEx(hwnd, ord('S'), [win32con.VK_MENU], False)  # 打开记事本设置面板，相当于发送Alt+S按键事件
    PostKeyEx(hwnd, ord('A'), None, False)  # 在编辑区输入字母a，相当于在编辑区按“A"键
    :param hwnd: 窗口句柄。
    :param key: 需要点击的普通键，如ord('A')等
    :param shift:
    :param specialkey:
    :param last_time: 按键持续时间，即键位按下的时间，单位为s
    :return:
    """
    _user32 = get_user32()
    PBYTE256 = ctypes.c_ubyte * 256
    if win32gui.IsWindow(hwnd):
        ThreadId = _user32.GetWindowThreadProcessId(hwnd, None)  # win32process.GetWindowThreadProcessId给出了错误的值

        lparam = win32api.MAKELONG(0, _user32.MapVirtualKeyA(key, 0))
        msg_down = win32con.WM_KEYDOWN
        msg_up = win32con.WM_KEYUP

        if specialkey:
            lparam = lparam | 0x1000000

        # 如果有修改-使用PostMessage和AttachThreadInput
        pKeyBuffers = PBYTE256()
        pKeyBuffers_old = PBYTE256()

        win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        _user32.AttachThreadInput(win32api.GetCurrentThreadId(), ThreadId, True)
        # 记录当前按下的组合键，如ctrl、shift、alt的状态，状态记录在pKeyBuffers_old中
        _user32.GetKeyboardState(ctypes.byref(pKeyBuffers_old))

        # ------------------------- 如果是组合按键，才需要设置键盘状态 --------------------------------
        if shift is not None and len(shift) > 0:
            # 记录需要按下的组合键，如ctrl、shift、alt的状态，状态记录在pKeyBuffers中
            for mod_key in shift:
                if mod_key == win32con.VK_MENU:  # Alt键需要单独处理，VK_MENU就是ALT键
                    lparam = lparam | 0x20000000
                    msg_down = win32con.WM_SYSKEYDOWN
                    msg_up = win32con.WM_SYSKEYUP
                pKeyBuffers[mod_key] |= 128
            _user32.SetKeyboardState(ctypes.byref(pKeyBuffers))  # 将当前的键盘状态设置为记录的pKeyBuffers
            time.sleep(0.1)
        # win32api.PostThreadMessage(ThreadId, msg_down, key, lparam)
        win32api.PostMessage(hwnd, msg_down, key, lparam)
        time.sleep(0.1)
        # win32api.PostThreadMessage(ThreadId, msg_up, key, lparam | 0xC0000000)
        win32api.PostMessage(hwnd, msg_up, key, lparam | 0xC0000000)
        time.sleep(0.1)
        # ------------------------- 如果是组合按键，恢复设置键盘状态 --------------------------------
        if shift is not None and len(shift) > 0:
            _user32.SetKeyboardState(ctypes.byref(pKeyBuffers_old))
            time.sleep(0.01)
        _user32.AttachThreadInput(win32api.GetCurrentThreadId(), ThreadId, False)


def send_message(hwnd, str):
    """
    想窗口发送字符串，窗口必须是可以接受字符串的，例如记事本的编辑区。测试成功。
    需要注意的是，该方法不是发送按键事件的方法。

    :param hwnd:
    :param str:
    :return:
    """
    str2int = [ord(c) for c in str]
    for x in str2int:
        win32api.SendMessage(hwnd, win32con.WM_CHAR, x, 0)


def get_nsh_window():
    """
    获取逆水寒的游戏窗口
    :return:
    """
    hwnd_title = find_window('逆水寒 角色ID', exact=False)
    hwnd, title = hwnd_title.popitem()
    return hwnd


if __name__ == "__main__":
    hwnd = get_nsh_window()
    # capture_pic(hwnd, show=False, save_to="temp.png")
    # post_key(hwnd, ord('F'), [win32con.VK_CONTROL])
    from yangke.common.win.keyboard import *

    while True:
        click_key(hwnd, "V")
