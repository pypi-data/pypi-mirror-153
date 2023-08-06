import time

import win32con
import win32gui
import win32api
from ctypes import windll, byref
from ctypes.wintypes import HWND, POINT
import string

VkCode = {
    "back"     : 0x08,
    "tab"      : 0x09,
    "return"   : 0x0D,
    "shift"    : 0x10,
    "control"  : 0x11,
    "menu"     : 0x12,
    "pause"    : 0x13,
    "capital"  : 0x14,
    "escape"   : 0x1B,
    "space"    : 0x20,
    "end"      : 0x23,
    "home"     : 0x24,
    "left"     : 0x25,
    "up"       : 0x26,
    "right"    : 0x27,
    "down"     : 0x28,
    "print"    : 0x2A,
    "snapshot" : 0x2C,
    "insert"   : 0x2D,
    "delete"   : 0x2E,
    "lwin"     : 0x5B,
    "rwin"     : 0x5C,
    "numpad0"  : 0x60,
    "numpad1"  : 0x61,
    "numpad2"  : 0x62,
    "numpad3"  : 0x63,
    "numpad4"  : 0x64,
    "numpad5"  : 0x65,
    "numpad6"  : 0x66,
    "numpad7"  : 0x67,
    "numpad8"  : 0x68,
    "numpad9"  : 0x69,
    "multiply" : 0x6A,
    "add"      : 0x6B,
    "separator": 0x6C,
    "subtract" : 0x6D,
    "decimal"  : 0x6E,
    "divide"   : 0x6F,
    "f1"       : 0x70,
    "f2"       : 0x71,
    "f3"       : 0x72,
    "f4"       : 0x73,
    "f5"       : 0x74,
    "f6"       : 0x75,
    "f7"       : 0x76,
    "f8"       : 0x77,
    "f9"       : 0x78,
    "f10"      : 0x79,
    "f11"      : 0x7A,
    "f12"      : 0x7B,
    "numlock"  : 0x90,
    "scroll"   : 0x91,
    "lshift"   : 0xA0,
    "rshift"   : 0xA1,
    "lcontrol" : 0xA2,
    "rcontrol" : 0xA3,
    "lmenu"    : 0xA4,
    "rmenu"    : 0XA5
}
PostMessageW = windll.user32.PostMessageW
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA
ClientToScreen = windll.user32.ClientToScreen
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x202
WM_MOUSEWHEEL = 0x020A
WHEEL_DELTA = 120
WM_KEYDOWN = 0x100
WM_KEYUP = 0x101


def click_key(handle: HWND, key: str):
    """
    按下指定按键，测试成功

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
    wparam = vk_code
    lparam = (scan_code << 16) | 1
    PostMessageW(handle, WM_KEYDOWN, wparam, lparam)
    time.sleep(0.5)
    lparam = (scan_code << 16) | 0XC0000001
    PostMessageW(handle, WM_KEYUP, wparam, lparam)


def get_virtual_keycode(key: str):
    """根据按键名获取虚拟按键码

    Args:
        key (str): 按键名

    Returns:
        int: 虚拟按键码
    """
    if len(key) == 1 and key in string.printable:
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
        return VkKeyScanA(ord(key)) & 0xff
    else:
        return VkCode[key]


import sys

if not windll.shell32.IsUserAnAdmin():
    # 不是管理员就提权
    windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1)
