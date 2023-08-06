"""
win10系统专用，用于在windows操作系统中获取窗口、进程等应用程序操作
"""

import win32com.client
import win32gui
import win32ui
import win32con
import win32process
import win32api
from PIL import Image


def get_user32():
    """
    通过该方法返回的对象可以调用user32.dll中的函数

    :return:
    """
    # user32.dll是stdcall
    from ctypes import windll
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


def find_child_windows(hwnd_parent, hwnd_child=0, window_cls=None, title=''):
    """

    :param hwnd_parent: 父窗口的句柄
    :param hwnd_child: 子窗口的句柄，若不为0，则按照z-index的顺序从hwndChildAfter向后开始搜索子窗体，否则从第一个子窗体开始搜索
    :param window_cls: 字符型，是窗体的类名
    :param title: 字符型，是窗体的类名
    :return:
    """
    window_cls = window_cls or 0
    win32gui.FindWindowEx(hwnd_parent, hwnd_child, window_cls, title)


def get_pid_by_hwnd(hwnd):
    """
    根据窗口句柄获取进程ID
    """
    thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
    return thread_id, pid


def capture_pic(hwnd, x1=0, y1=0, x2=0, y2=0, save_to: str = "img.bmp"):
    """
    截取给定句柄对应的窗口中指定位置的图像，可以处理后台画面，默认截取整个窗口画面

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

    im_PIL.save('im_PIL.png')
    im_PIL.show()

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_DC)


def 注入dll(目标进程ID, dll_path):
    """
    将dll_path指定的dll文件注入到目标进程中

    :param 目标进程ID:
    :param dll_path:
    :return:
    """
    win32process.CreateRemoteThread()


if __name__ == "__main__":
    hwnd_title = find_window('计算器', exact=False)
    hwnd1, title = hwnd_title.popitem()
    capture_pic(hwnd1)
