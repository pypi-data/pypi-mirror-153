import ctypes
from ctypes import *


def load_dll(dll_path):
    # dll = windll.LoadLibrary(dll_path)  # 按stdcall调用协议调用其中的函数
    # dll = cdll.LoadLibrary(dll_path)
    # dll = WinDLL(dll_path)
    dll = CDLL(dll_path)  # 按cdecl调用协议调用其中的函数
    return dll


def connect_server(ip, port, user, passwd, use_group=False):
    """
    连接SIS系统数据库系统

    :param ip:
    :param port:
    :param user:
    :param passwd:
    :param use_group:
    :return:
    """
    dll = load_dll(r"D:\PycharmProjects\lib4python\yangke\sis\dbpapi_x64.dll")
    dll.DBP_Open.restype = ctypes.c_void_p
    dbp = dll.DBP_Open(ip, ctypes.c_uint16(port), user, passwd, ctypes.c_bool(use_group))  # 该方法返回一个指针
    dbp = hex(dbp)
    print(dbp)
    err_code = dll.DBP_Connect(dbp)


connect_server(ip="172.22.191.211", port=12085, user="admin", passwd="admin")
