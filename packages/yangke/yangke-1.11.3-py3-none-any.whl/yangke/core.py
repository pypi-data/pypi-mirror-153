# 可以使用yk.fun()直接调用的方法写在这里
# __package__ = "yangke"
import sys
import subprocess
import os
from yangke.common import fileOperate as fileOp
from yangke.common.config import logger


def strInList(string: str, str_list: list, revert=False, need_item=False):
    """
    判断list的某个子元素是否包含指定字符串str

    用以和runCMD()配合使用，runCMD返回的的运行结果是list
    output, err=runCMD(...)
    strInList("result str", output)，如果output的某行包含"result str"，则返回True，否则返回False

    :param need_item: 是否需要返回找到的list中的项，默认不返回，设置为True则返回
    :param string: 字符串
    :param str_list: 字符串列表
    :param revert: 是否翻转，如果为True，则依次判断列表中的字符串是否在当前字符串中，为False则判断当前字符串是否在列表中的某个字符串中
    :return: bool/ (bool, str)
    """
    for line in str_list:
        if revert:
            if line in string:
                if need_item:
                    return True, line
                else:
                    return True
        else:
            if string in line:
                if need_item:
                    return True, line
                else:
                    return True
    if need_item:
        return False, None
    else:
        return False


def runCMD(command: str, charset: str = "utf8", wait_for_result: bool = True, cwd=None,
           output_type: str = "RETURN", timeout=None):
    """
    执行cmd命令，并返回标准输出结果，在windows系统下需要管理员权限运行的命令不能使用该方法调用。\n
    在linux系统下也可以使用。

    输出模式：支持"RETURN"(默认),"REALTIME_NORETURN"和"REALTIME_RETURN"，分别表示子进程的输出结果以字符串
    (output, err)形式返回、实时输出结果并且不返回、实时输出且需要以字符串形式返回。第三种方式的实时输出有短暂的缓冲期，实时性不如第二种
    方式，且第三种方式必须等待子线程运行结束

    :param timeout: 超时时间
    :param output_type: 输出模式，
    :param cwd: 工作目录
    :param command: 命令行命令
    :param charset: 编码方式
    :param wait_for_result: 是否等待命令执行完毕
    :return: 如果waitForResult=True，则返回执行结果字符串列表，否则，返回标准输出的接口
    """
    if "|" not in command:
        if output_type == "REALTIME_NORETURN":
            p = subprocess.Popen(command, shell=True, cwd=cwd)
            if wait_for_result:
                p.wait(timeout=timeout)  # 不重定向stdout和stderr，则p.wait()不会死锁
            return
        elif output_type == "RETURN":
            popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
            if wait_for_result:
                line, err = popen.communicate()  # command有大量输出时，popen.wait()可能会死锁
                # 这里获得的lines是字节码格式，pycharm显示为 b'CONTAINER ID ...\n' ，前面的b指的是bytes
                # 解码lines为字符串
                line = line.decode(charset)
                err = err.decode(charset)
                return line, err
            else:
                return popen.stdout, popen.stderr
        elif output_type == "REALTIME_RETURN":
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
            lines = []
            errs = []
            while p.poll() is None:
                """
                poll函数返回码：0-正常结束 1-sleep 2-子进程不存在 -15-kill None-在运行
                """
                if p.stdout is not None:
                    line = p.stdout.readline()
                    line = line.strip().decode(charset)
                    if line:
                        lines.append(line)
                        print(line)
                if p.stderr is not None:
                    err = p.stderr.readline()
                    err = err.strip().decode(charset)
                    if err:
                        errs.append(err)
                        print(err)
            return lines, errs
    else:  # python不支持直接运行command1 | findstr "targetStr" 这种cmd命令
        command = command.split("|")
        results, err = runCMD(command[0].strip())
        if command[1].strip().lower().startswith("findstr"):
            # 获得查找的目标字符串
            str_to_find = command[1].replace("findstr ", "")
            str_to_find = str_to_find.replace('"', "").strip()
            lines = []
            for line in results:
                if str_to_find.lower() in line.lower():
                    lines.append(line)
            return lines, err


def _runAsAdmin(cmd, cwd=None, charset="gbk", python=None, popup=True):
    """
    私有方法，管理员运行命令请使用 runAsAdmin()方法
    不能用于linux系统
    """
    import yangke.common.Interact as act
    # 因为引入包的关系，这个方法总是会被执行两次
    config = "Interact_temp_file"
    cwd = cwd or os.getcwd()  # os.path.dirname(__file__)  # 这里赋值调用目录，不能是文件目录
    config = os.path.join(cwd, config)
    if act.times == 1:  # 因为引入包的关系，这个方法总是会被执行两次，这里对真正的执行次数进行判断
        act.times = 0  # 如果执行过一次了，就直接返回，不再执行，且将执行次数恢复为0
        return
    result = act.runAdmin(cmd=cmd, cwd=cwd, charset=charset, python=python, popup=popup)  # runAdmin必须位于独立的文件中
    act.times = 1  # 将执行次数设置为1
    if os.path.exists(config):
        os.remove(config)

    return result


def runAsAdmin(cmd, cwd=None, charset="gbk", python=None, popup=True):
    """
    windows系统下以管理员身份运行命令

    :param cmd: 需要运行的命令
    :param cwd: 工作目录
    :param charset: 字符编码
    :param python: 需要运行的python解释器路径，默认为系统环境变脸的python解释器，如果系统环境没有配置，请手动指定
    :param popup: 是否弹出确认窗口，默认需要；windows安全策略不允许静默方式运行管理员命令，如果设置为False，则利用了windows的漏洞，在windows10系统会被windows defender当成病毒拦截，测试360安全卫士不会拦截，可以正常运行
    :return:
    """
    _runAsAdmin(cmd, cwd, charset, python, popup)  # 因为_runAsAdmin在第二次执行时返回None，因此只能从runResult文件中获得执行结果
    config = "Interact_temp_file"
    run_result = config + "_runResult"
    cwd = cwd or os.getcwd()
    run_result = os.path.join(cwd, run_result)
    result = fileOp.readFromPickle(run_result)
    os.remove(run_result)  # 删除用于输出的临时文件
    return result


def existModule(module_name: str):
    """
    判断指定的第三方库是否安装
    :return: bool
    """
    python_code = "import " + module_name
    try:
        exec(python_code)
    except ImportError:
        return False
    return True


def enableDocker():
    """
    判断docker是否在运行
    :return: Docker在运行返回True，否则返回False
    """
    title, err = runCMD('docker container ps')
    if len(title) == 0:
        logger.debug(err)
        print("Docker is not running, start Docker Desktop first!")
        return False
    else:
        return True


def statusOfContainer(container_name: str) -> str:
    """
    查询指定名称容器的状态，如果不存在指定名称的容器，则返回 None
    :param container_name:
    :return:
    """
    results, _ = runCMD('docker container ps -a')
    results = results.split("\n")
    for line in results:
        fields = list(filter(None, line.split("  ")))  # 以多个空格分隔line
        fields = [field.strip() for field in fields]  # 去除每个field中的空格
        if container_name in fields:
            return fields[4]
    return None


def image2base64(img_file: str, encoding='utf-8') -> str:
    import base64
    if not os.path.exists(img_file):
        print("img_file不存在，查询路径为{}".format(img_file))
        return None
    with open(img_file, 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding=encoding)
    return image_base64


def base642image(b64_data):
    import base64
    data = base64.b64decode(b64_data)
    return data


def isBase64(string: str):
    try:
        base642image(string)
    except:
        return False
    return True
