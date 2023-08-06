# -*- coding: utf-8 -*-
import ctypes
import math
import os.path
import time
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from yangke.base import merge_two_dataframes
from yangke.common.config import logger
from yangke.core import runCMD


def ctypes_str2char_array(string: str):
    """
    python3中的字符串是以utf-8格式编码的，为了将字符串传递给C函数，需要将其解码为byte类型，对应C函数中的char*类型或char[]类型

    :param string:
    :return:
    """
    return string.encode("utf8")


def init_write_sis(ip=None, user=None, passwd_str=None, port=None):
    """
    使用dbp_api.write_snapshot_by_cmd()方法时需要先调用该方法设置相关SIS操作脚本的路径

    :return:
    """
    import sys
    import re
    import yangke.common.fileOperate as fo
    path = sys.executable
    lines = fo.read_lines("write_sis.bat")
    lines_new = []
    for line in lines:
        line = line.replace("%python_exec%", path)
        line = line.replace("%py_file%", os.path.abspath("temp_write_sis.py"))
        lines_new.append(line)
    fo.writeLines("temp_write_sis.bat", lines_new)
    if ip is not None and user is not None and passwd_str is not None and port is not None:
        lines = fo.read_lines("write_sis.py")
        lines_new = []
        for line in lines:
            line = line.replace('@ip@', ip)
            line = line.replace('@user@', user)
            line = line.replace('@passwd@', passwd_str)
            line = line.replace('@port@', str(port))
            lines_new.append(line)

        fo.writeLines("temp_write_sis.py", lines_new)


class DllMode:
    def __init__(self, ip=None, user=None, passwd_str=None, port=None):
        # self.dll = ctypes.cdll.LoadLibrary(r"D:\lengduan\test2\dbpapi_x64.dll")
        path = r"D:\lengduan\lib4python\yangke\sis\dbpapi_x64.dll"
        try:
            self.handle: Optional[ctypes.c_uint64] = None
            self.dll = ctypes.cdll.LoadLibrary(path)
        except OSError:
            logger.warning(f"找不到指定的动态链接库！请检查路径{path}")
            raise OSError(f"找不到指定的动态链接库！请检查路径{path}")
        if ip is not None and user is not None and passwd_str is not None and port is not None:
            self.connect(ip, user, passwd_str, port)

    def __del__(self):
        self.close()

    def connect(self, ip, user, passwd_str, port):
        self.dll.DBPCreate2.restype = ctypes.c_uint64
        ip = ctypes_str2char_array(ip)
        user = ctypes_str2char_array(user)
        passwd = ctypes_str2char_array(passwd_str)
        port = int(port)
        self.handle = ctypes.c_uint64(self.dll.DBPCreate2(ip, user, passwd, port, 0))
        if self.handle is None:
            print("连接创建失败")
            return False
        ret = self.dll.DBP_Connect(self.handle)
        if 0 == ret:
            return True
        else:
            print("服务器连接失败")
            return False

    def close(self):
        if self.handle is not None and self.handle.value > 0:
            self.dll.DBP_Close(self.handle)
            self.handle = None

    def is_connect(self):
        ret = self.dll.DBP_IsConnect(self.handle)
        if 0 == ret:
            return True
        return False

    def dis_connect(self):
        """
        断开连接

        :return:
        """
        ret = self.dll.DBP_DisConnect(self.handle)
        if 0 == ret:
            return True
        return False

    def get_his_value(self, tags: list or str, tags_description=None, start_time: datetime = None,
                      end_time: datetime = None,
                      time_interval=10, use_description=True):
        """
        待验证

        :param tags:
        :param tags_description: 参考get_snapshot中的同名参数
        :param start_time:
        :param end_time:
        :param time_interval: 时间间隔，单位s
        :param use_description: 参考get_snapshot中的同名参数
        :return:
        """
        now = datetime.now()
        start_time = start_time or now - timedelta(days=0, hours=2)  # 默认两小时前的时间为读数起始时间
        end_time = end_time or now - timedelta(days=0, hours=0)  # 默认一小时前的时间为读数结束时间
        start_time_long = int(time.mktime(start_time.timetuple()))  # 将时间转为UNIX时间
        end_time_long = int(time.mktime(end_time.timetuple()))
        start_time_c = ctypes.c_long(start_time_long)  # c_long和c_ulong貌似都可以
        end_time_c = ctypes.c_long(end_time_long)
        insert_time = ctypes.c_long(time_interval)  # 插值时间，只有下方flag为1是才有效
        flag = ctypes.c_long(1)  # 标记，为0时取样本值，插值时间参数无效，为1时使插值时间参数生效
        # 预留的点数，如果读取的时间段内点数超过这个数，结果会被裁剪，如果读取的点数少于这个数，会补零
        data_num = math.ceil((end_time_long - start_time_long) / time_interval)
        a = ctypes.c_int(10)
        b = ctypes.c_int(10)
        value_type = ctypes.pointer(a)  # 指针和数组在python传递时有所区别
        data_size_actual = ctypes.pointer(b)  # 返回实际读到的数据个数
        value_double_arr = (ctypes.c_double * data_num)()
        value2_arr = (ctypes.c_long * data_num)()
        time_long_arr = (ctypes.c_long * data_num)()
        qas_short_arr = (ctypes.c_short * data_num)()
        if isinstance(tags, str):  # 读取单个参数的历史数据，tags为数据库标签名
            tag_name = ctypes_str2char_array(tags)  # 名字
            self.dll.DBPGetHisVal(self.handle, tag_name, start_time_c, end_time_c, insert_time, flag,
                                  value_double_arr, value2_arr, time_long_arr, qas_short_arr,
                                  ctypes.c_int(data_num), value_type, data_size_actual)
            return self._assemble_dataframe(tags, time_long_arr, qas_short_arr, value_double_arr, value2_arr,
                                            value_type, None, False)
        else:  # 读取多个数据的历史数据，tags为数据库标签名组成的列表
            df = None
            if tags_description is not None and use_description:
                kks_des = dict(zip(tags, tags_description))
            else:
                kks_des = dict(zip(tags, tags))
            for tag in tags:
                tag_name = kks_des.get(tag)
                tag_c = ctypes_str2char_array(tag)
                self.dll.DBPGetHisVal(self.handle, tag_c, start_time_c, end_time_c, insert_time, flag,
                                      value_double_arr, value2_arr, time_long_arr, qas_short_arr,
                                      ctypes.c_int(data_num), value_type, data_size_actual)
                _ = self._assemble_dataframe(tag_name, time_long_arr, qas_short_arr, value_double_arr, value2_arr,
                                             value_type, None, False)
                if df is None:
                    df = _
                else:
                    df = merge_two_dataframes(df, _)[0]
            return df

    def get_snapshot(self, tags, tag_description=None, need_detail=False, use_description=True):
        """
        获取给定标签列表的快照数据

        :param tags: 标签名
        :param need_detail:是否需要数据的详细信息，默认不需要，如果为True,则会返回数据质量、错误码等详细信息
        :param tag_description: 标签点的描述
        :param use_description: 当给定点描述时，数据列的标题是否使用点描述代替标签名
        :return:
        """

        n_size = len(tags)
        tag_names = (ctypes.c_char_p * n_size)()  # 名字
        for i in range(n_size):
            tag_names[i] = ctypes_str2char_array(tags[i])

        time_long_arr = (ctypes.c_uint32 * n_size)()  # 时间，系统里的时间应该比当前时间早8小时

        qas_short_arr = (ctypes.c_short * n_size)()  # 质量

        value_double_arr = (ctypes.c_double * n_size)()  # 浮点数类型的值
        value2_arr = (ctypes.c_int32 * n_size)()  # 整形类型的值
        value2_type = (ctypes.c_int32 * n_size)()  # 数据类型
        error_code_arr = (ctypes.c_short * n_size)()  # 数据错误码
        self.dll.DBPGetSnapshot(
            self.handle,  # 句柄
            tag_names,  # char* sTagNames[],  //in,标签名字符串指针数组  //apistring
            time_long_arr,  # long ltimes[],   //in, 时标
            qas_short_arr,  # short snqas[],   //in, 质量
            value_double_arr,  # double  dblvals[],   //in, 存放double值,DT_FLOAT32,DT_FLOAT64存放区
            value2_arr,  # long lvals[],   //in, 存放Long值,DT_DIGITAL,DT_INT32,DT_INT64存放区
            value2_type,  # int  ntypes[],   //in, 数据类型,DT_INT32,DT_FLOAT32等。
            error_code_arr,  # short errs[],    //in/out, 错误码
            n_size  # int  nsize    //in, 个数
        )
        if tag_description is not None and use_description:  # 如果使用描述，且描述不为空
            return self._assemble_dataframe(tag_description, time_long_arr,
                                            qas_short_arr, value_double_arr, value2_arr,
                                            value2_type,
                                            error_code_arr, need_detail=need_detail)
        else:
            return self._assemble_dataframe(tags, time_long_arr, qas_short_arr,
                                            value_double_arr, value2_arr,
                                            value2_type,
                                            error_code_arr, need_detail=need_detail)

    @staticmethod
    def _assemble_dataframe(tags, time_long_arr, qas_short_arr, value_double_arr, value2_arr, value2_type,
                            error_code_arr, need_detail=False):
        """
        将代理服务器返回的数据组装成dataframe格式的对象

        :param tags: 数据标签
        :param time_long_arr:
        :param qas_short_arr:
        :param value_double_arr:
        :param value2_arr:
        :param value2_type:
        :param error_code_arr:
        :param need_detail: 是否需要数据的详细信息，默认不需要，如果为True,则会返回数据质量、错误码等详细信息
        :return:
        """
        n_size = len(time_long_arr)  # 标签个数
        if not need_detail:
            columns = ["DateTime"]
            if isinstance(tags, str):  # 说明是读历史数据，只有一个变量标签，但有多个时间标签
                columns = ["DateTime", tags]
                data_list = []
                for i in range(n_size):
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_long_arr[i]))
                    if value2_type[0] == 3:
                        data_list.append([time_str, value_double_arr[i]])
                    else:
                        data_list.append([time_str, value2_arr[i]])
                result = pd.DataFrame(columns=columns, data=data_list)
            else:
                columns.extend(tags)
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_long_arr[0]))
                data_list = [time_str]
                for i in range(n_size):
                    if value2_type[i] == 3:  # 如果数据类型==3，则说明读到的是double类型数据
                        data_list.append(value_double_arr[i])
                    else:
                        data_list.append(value2_arr[i])
                result = pd.DataFrame(columns=columns, data=[data_list])
        else:
            result = {}
            for i in range(n_size):
                if isinstance(tags, str):
                    ...
                else:
                    tag = tags[i]
                    columns = ["DateTime", "值", "质量", "数据类型", "错误码"]
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_long_arr[i]))
                    qas = qas_short_arr[i]
                    value_type = value2_type[i]
                    if value_type == 3:
                        value = value_double_arr[i]
                    else:
                        value = value2_arr[i]
                    error_code = error_code_arr[i]
                    data_list = [time_str, value, qas, value_type, error_code]
                    dataframe = pd.DataFrame(columns=columns, data=[data_list])
                    result.update({tag: dataframe})
        return result

    def write_snapshot_by_cmd(self, tags, values):
        """
        该方法功能和self.write_snapshot_double()完全相同，但是将写入操作重启一个进程进行，这样写入操作报错时，不会影响主程序崩溃。
        :param tags:
        :param values:
        :return:
        """
        tags_values = {k: v for k, v in zip(tags, values)}
        path = os.path.abspath("temp_write_sis.bat")
        cmd = f'{path} "{tags_values}"'
        runCMD(command=cmd, wait_for_result=False, output_type="REALTIME_NORETURN")

    def write_snapshot_double(self, tags, values):
        """
        写double类型数据到数据库，该方法可能会导致程序异常退出，建议使用第三方exe独立调用该接口

        :param tags: 标签名列表
        :param values: 数值列表
        :return:
        """
        n_size = len(tags)
        tag_names = (ctypes.c_char_p * n_size)()  # 名字
        time_long_arr = (ctypes.c_uint32 * n_size)()  # 时间
        qas_short_array = (ctypes.c_short * n_size)()  # 质量
        value_double_arr = (ctypes.c_double * n_size)()  # 浮点数类型的值
        value2_arr = (ctypes.c_int32 * n_size)()  # 整形类型的值
        value_type = (ctypes.c_int32 * n_size)()  # 数据类型
        time_long = int(time.time())  # 保证写入的数据点都具有同一个时标
        for i in range(n_size):
            tag_names[i] = ctypes_str2char_array(tags[i])
            time_long_arr[i] = time_long
            qas_short_array[i] = 0
            value_double_arr[i] = values[i]
            value2_arr[i] = 0
            value_type[i] = 3  # 3表示通过value_double_arr传输数据，其他表示通过value2_arr传输数据

        error_code_arr = (ctypes.c_short * 2)()  # 数据错误码，输出信息
        try:
            self.dll.DBPWriteSnapshot(
                self.handle,  # 句柄
                tag_names,  # char* sTagNames[],  //in,标签名字符串指针数组  //apistring
                time_long_arr,  # long ltimes[],   //in, 时标
                qas_short_array,  # short snqas[],   //in, 质量
                value_double_arr,  # double  dblvals[],   //in, 存放double值,DT_FLOAT32,DT_FLOAT64存放区
                value2_arr,  # long lvals[],   //in, 存放Long值,DT_DIGITAL,DT_INT32,DT_INT64存放区
                value_type,  # int  ntypes[],   //in, 数据类型,DT_INT32,DT_FLOAT32等。
                error_code_arr,  # short errs[],    //in/out, 错误码
                n_size  # int  nsize    //in, 个数
            )
        except:
            pass
