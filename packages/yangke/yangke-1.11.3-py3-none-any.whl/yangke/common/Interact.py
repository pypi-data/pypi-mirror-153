import sys
import subprocess
import ctypes
import os
import pickle
import threading

# 由于模块的特殊性，不能引入自己编写的其他模块，否则会导致管理员身份运行失败

"""
以管理员方式运行cmd命令，使用方法如下：
import common.fileOperate as fo
data = {"popup": True, "command": "net start {}".format(serviceName)}
fo.writeAsPickle(temp_file, data)
iact.runAdmin()
即必须以临时文件传入命令及相关参数，否则无效
"""


def fprint(msg):
    # print(msg)
    msg = str(msg)
    with open("D:\\log_yangke.txt", "a") as f:
        f.write(msg + "\n\r")


def writeAsPickle(file: str, obj: object, opentype='wb'):
    with open(file, opentype) as f:
        pickle.dump(obj, f)


def readFromPickle(file: str, opentype='rb'):
    with open(file, opentype) as f:
        obj = pickle.load(f)
    return obj


def runAdmin(cmd=None, cwd=None, popup=True, python=None, charset="gbk", config=None, runas=False):
    """
    以管理员身份运行cmd命令，该方法总是会被执行两次，因为引入时会被执行一次

    popup为True时调试正常，运行不正常
    如果将popup设置为False，则不会弹出确认窗口，但是利用了windows的提权漏洞，可能会在以后的版本中被修复，具体参考https://yq.aliyun.com/articles/217616

    参考1：https://blog.csdn.net/MAOZEXIJR/article/details/88117388，该博客介绍的方法在调试时可以正常运行命令net start mysql，但直接运行时，mysql服务启动不起来，且运行不报错
    参考2：https://blog.csdn.net/qq_17550379/article/details/79006655?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
        这里使用参考2中的方法，但稍作修改，主要是参考中使用的python版本是python2，测试发现，单独执行Interact.py可以，但是由第三方调用执行，则服务也启动不起来

    问题解决：发现第三方调用服务起不来的原因是，因为本文件以管理员身份运行时，相当于以__main__模式在运行该方法，因此，必须在
    if __name__=="__main__": 中再次调用runAdmin方法，第三方的调用只是运行了runAdmin()，儿runAdmin()中以管理员方式运行时重新
    调用了该__file__文件。

    :param cmd: 需要运行的命令
    :param cwd: 指定命令运行的目录
    :param popup: 是否弹出确认窗口，False时需要保证命令行中python命令对应的是项目对应的解释器
    :param config: 内置参数，无须传入值
    :param python: python解释器的路径，当本地有多个python解释器的时候，指定非默认解释器时使用，不指定则使用环境变量中的默认python解释器
    :param runas: 标记当前函数的调用者是不是__main__方法
    :return:
    """
    # 必须在第三方调用时将popup保存到另外一个独立文件中，这样当独立调用__file文件时，可以读入动态popup参数
    # temp_file = os.path.join(os.path.dirname(__file__), 'Interact_file')  # 这个文件路径和文件名必须和iact读取的一致
    config = "Interact_temp_file"
    runResult = config + "_runResult"
    cwd = cwd or os.getcwd()  # os.path.dirname(__file__)  # 这里赋值调用目录，不能是文件目录
    config = os.path.join(cwd, config)
    runResult = os.path.join(cwd, runResult)
    fprint("config_file=" + config + "; result_file=" + runResult)
    if cmd is not None:  # 说明是第三方模块调用，保存传入的参数信息
        # fprint("第一次：第三方模块调用")
        data = {"popup": popup, "command": cmd, "cwd": cwd, "charset": charset}
        writeAsPickle(config, data)
        fprint(readFromPickle(config))
        runAdmin(config=config, popup=popup, cwd=cwd, charset=charset)  # 这次调用仍不是管理员身份
        import time
        while not os.path.exists(runResult):  # 等待管理员身份运行结果
            time.sleep(0.1)
            fprint("wait for result...")
        result = readFromPickle(runResult)
        return result

    if os.path.exists(config):
        data = readFromPickle(config)
        popup = data['popup']
        cmd = data['command']
        cwd = data['cwd']
        charset = data['charset']

    if runas:  # 如果是以管理员身份从__main__模块运行的
        # 因为引入该模块时也会执行一次__main__模块，因此这里判断是不是引入时执行的，如果是引入执行的，则不存在config文件
        if os.path.exists(config):  # 如果不是引入该模块时执行的__main__方法
            # 从config文件读入参数
            fprint("第三次：自己以管理员方式运行文件时调用")
            fprint(config)
            data = readFromPickle(config)
            popup = data['popup']
            cmd = data['command']
            cwd = data['cwd']
            charset = data['charset']
            fprint("cmd={}, popup={}, cwd={}, charset={}".format(cmd, popup, cwd, charset))
        else:  # 如果是引入模块时调用的，则直接返回，不做操作
            fprint("第零次：引入时调用")
            fprint(os.path.abspath(config))
            return
    else:
        # 如果不是管理员身份运行的本文件，则此处不执行操作，由以下代码块切换为管理员身份重新运行，且runas设置为True
        fprint("第二次：自己递归调用自己")
        pass
    # 开始以管理员方法运行
    if popup:
        admin = is_admin()
        if admin:
            # 最好给该代码块加单线程锁
            sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sp.wait()
            stderr = str(sp.stderr.read().decode(charset)).strip()
            stdout = str(sp.stdout.read().decode(charset)).strip()
            fprint(stdout)
            fprint(stderr)
            # 将输出写入文件runResult
            fprint("输出运行结果到文件：" + runResult)
            writeAsPickle(runResult, {"stdout": stdout, "stderr": stderr})
            return
        else:  # 使用管理员身份运行本文件
            # fprint("第二次调用完成，开始第三次调用，第三次调用没有调试信息，因为是独立进程")
            fprint("以管理员身份运行：" + __file__ + "工作目录：" + cwd)
            # 最好给下面代码加单线程锁
            pid = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, cwd, 3)
            fprint(pid)
            return
    else:
        CMD = r"C:\Windows\System32\cmd.exe"
        FOD_HELPER = r'C:\Windows\System32\fodhelper.exe'
        PYTHON_CMD = python or "python"
        REG_PATH = 'Software\Classes\ms-settings\shell\open\command'
        DELEGATE_EXEC_REG_KEY = 'DelegateExecute'

        def create_reg_key(key, value):
            """
            Creates a reg key
            """
            try:
                import winreg
                winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)
                winreg.CloseKey(registry_key)
            except WindowsError:
                raise

        def bypass_uac(cmd):
            """
            Tries to bypass the UAC
            """
            try:
                create_reg_key(DELEGATE_EXEC_REG_KEY, '')
                create_reg_key(None, cmd)
            except WindowsError:
                raise

        def execute(cmd):
            if not is_admin():
                # 如果不是管理员身份，则以管理员身份重新运行当前文件，重新运行会进入if __name__ == __main__代码块
                fprint('[!] The script is NOT running with administrative privileges')
                fprint('[+] Trying to bypass the UAC')
                try:
                    current_dir = __file__
                    cmd1 = '{} /k "{}" "{}"'.format(CMD, PYTHON_CMD, current_dir)
                    bypass_uac(cmd1)
                    os.system(FOD_HELPER)
                    sys.exit(0)
                except WindowsError:
                    sys.exit(1)
            else:
                # 这里添加我们需要管理员权限的代码
                fprint('[+] The script is running with administrative privileges!')
                sp = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                sp.wait()
                stderr = str(sp.stderr.read().decode(charset)).strip()
                stdout = str(sp.stdout.read().decode(charset)).strip()
                fprint(stdout)
                fprint(stderr)
                # 将输出写入文件runResult
                writeAsPickle(runResult, {"stdout": stdout, "stderr": stderr})

        execute(cmd)


def is_admin():
    """判断当前运行环境是否具有管理员权限"""
    try:
        o = ctypes.windll.shell32.IsUserAnAdmin()
        if o == 1:
            result = True
        elif o == 0:
            result = False
    except:
        return False
    return result


fprint("__name__=" + __name__)
mutex = threading.Lock()
times = 0

if __name__ == "__main__":
    mutex.acquire()
    fprint("进入__main__模块")
    runAdmin(runas=True)
    mutex.release()
