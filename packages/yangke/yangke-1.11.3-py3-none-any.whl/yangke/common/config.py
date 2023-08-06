# 该模块必须位于common文件夹下
import sys
import traceback
import inspect
from yangke.base import get_settings, run_once
import os
from loguru import logger as logger1
import loguru

# noinspection All
Logger = loguru._logger.Logger
# 该类中一律使用logger，不使用全局变量模块中的gv.logger，这样就无须引入全局变量模块.
# 调用模块会将gv.logger设置为这里的logger，但因为该类可以直接访问自己的logger，就无须且不建议使用gv.logger
logger: Logger = logger1
# noinspection all
level: int = None
# 这里声明以下变量，这样在其他模块中引用config时无须引入logging模块即可使用以下变量
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

"""
Level name      Severity value      Logger method
TRACE           5                   logger.trace
DEBUG           10                  logger.debug
INFO            20                  logger.info
SUCCESS         25                  logger.success
WARNING         30                  logger.warning
ERROR           40                  logger.error
CRITICAL        50                  logger.critical
"""


@run_once
def initLogger(level: int = None, log_file="default", level_color=None, format_color=None,
               log_format=None,
               date_format=None, rotation="50 MB", retention="30 days", diagnose=True) -> Logger:
    """
    levelColor和formatColor的取值示例如下，具体配置说明参考https://loguru.readthedocs.io/en/stable/api/logger.html#color

        level_color = {
            "DEBUG": 'green',
            "INFO": 'blue',
            "WARN": 'red',
            "ERROR": 'red d',
            "FATAL": 'red'}
        format_color = {
            "time": "green",
            "level": "light
            }

    :param date_format: 日志中日期的格式
    :param log_file: 日志保存到的文件，文件名中可以引用time，如"runtime_{time}.log"，则time会被自动替换为实时时间
    :param log_format: 日志格式
    :param diagnose: 运行出错时，是否追踪错误原因
    :param retention: 文件日志输出时，指定保留日志的期限，如“30 days”表示只保留最近30天的日志
    :param rotation: 文件日志输出时，输出下一个日志的条件，可以是大小，也可以是时间，如"50 MB"、"00:00", "1 week"等，具体参见loguru
    :param level: 日志级别，可以为logging.DEBUG等等，具体参见logging类的日志级别
    :param level_color: 各日志级别的字体配置，为字典类型，可取值"default"使用默认配色
    :param format_color: 日志各个格式的输出字体配置，可取值"default"使用默认配色
    :return: logger，使用该logger进行日志输出。
    """

    # def sink(msg):
    #     print(msg)
    #     record = msg.record
    #     file = record["file"].name
    #     function = record["function"]
    #     line = record["line"]
    #     message = record['message']
    #     module = record["module"]
    #     name = record["name"]
    #
    #     if record.level.no == DEBUG:
    #         pass

    @classmethod
    def setLevel(logger_cls, *args, **kwargs):
        logger.debug("暂不支持中途更改日志级别")

    Logger.setLevel = setLevel

    if date_format is None:
        date_format = "YYYY-MM-DD HH:mm:ss"
    if log_format is None:
        log_format = "{time:" + date_format + "} - {level} - {module}:{function}:{line} - {message}"
    else:
        if "{time:" not in log_format:  # 日志格式中没有添加日期，则添加
            log_format = log_format.replace("{time", "{time:" + date_format)

    def assemble_log_fmt(color):
        if " " not in color:
            log_fmt = f"<{color}>" + log_format + "</>\n"
        else:  # 说明color中包含color和style两个设置项，都解析出来，顺序无所谓
            color = color.split(" ")[0]
            style = color.split(" ")[1]
            log_fmt = f"<{color}><{style}>" + log_format + "</></>\n"
        return log_fmt

    def format_(record):
        """
        当用户自定义日志格式时，调用该方法生成格式字符串

        :param record:
        :return:
        """
        color = "white"
        if record['level'].no == DEBUG:
            if level_color is not None:
                color = level_color.get('DEBUG') or 'green'
            else:
                color = 'green'
        elif record['level'].no == INFO:
            if level_color is not None:
                color = level_color.get('INFO') or 'blue'
            else:
                color = 'blue'
        elif record['level'].no == WARN:
            if level_color is not None:
                color = level_color.get('WARN') or 'red'
            else:
                color = 'red'
        elif record['level'].no == ERROR:
            if level_color is not None:
                color = level_color.get('ERROR') or 'RED'
            else:
                color = 'RED'
        elif record['level'].no == CRITICAL:
            if level_color is not None:
                color = level_color.get('CRITICAL') or 'blue RED'
            else:
                color = 'blue RED'
        return assemble_log_fmt(color)

    global logger
    if log_file == "default":
        log_file = "runtime_{time}.log"

    if level_color is not None or format_color is not None:
        logger.remove(0)
        logger.add(sys.stdout, level=level, diagnose=diagnose, format=format_, colorize=True)
    logger.add(log_file, level=level, format=format_, rotation=rotation, retention=retention,
               diagnose=diagnose)

    return logger


def holdLoggingLevel(para='end', outer=True):
    """
    临时提高日志级别，例如更改前使用holdLoggingLevel(logging.WARN)将日志级别临时更改为“WARN”，
    更改后调用holdLoggingLevel('end')恢复日志级别为临时更改前的级别。
    holdLoggingLevel(level)和holdLoggingLevel('end')构成一个区间。
    多个区间可以嵌套，以最外层区间的设置为最终设置。如果需要以内部区间的设置为最终设置，将outer设为False即可。

    outer=False和outer=True优先级相同，后设置的生效。

    使用示例：

    ...any code...                                             \n
    holdLoggingLevel(logging.DEBUG, False)  # 1                \n
    ...DEBUG生效...                                            \n
    holdLoggingLevel('logging.WARN, False)  # 2                \n
    ...WARN生效...                                              \n
    holdLoggingLevel('logging.DEBUG, False)  # 3                \n
    ...DEBUG生效...                                             \n
    holdLoggingLevel('logging.WARN')  # 4                       \n
    ...WARN生效...                                              \n
    holdLoggingLevel('logging.DEBUG')  # 5                      \n
    ...WARN生效...，因为outer=True，以当前设置更外层的为准       \n
    holdLoggingLevel('logging.ERROR')  # 6                      \n
    ...WARN生效...，因为outer=True，一直找到最外层的日志级别      \n
    holdLoggingLevel('end')  # 关闭6                            \n
    ...WARN生效...                                              \n
    holdLoggingLevel('end')  # 关闭5                            \n
    ...WARN生效...                                              \n
    holdLoggingLevel('end')  # 关闭4                            \n
    ...DEBUG生效...，因为4对应的设置已经关闭，则以3为准           \n
    holdLoggingLevel('end',outer=False)                        \n
    ...WARN生效...，因为3对应的设置已经关闭，则以2为准            \n
    holdLoggingLevel('end',outer=False)                        \n
    ...DEBUG生效...                                            \n
    ...DEBUG生效...如果outer=False，且与之对应的end语句一直不出现，则级别设置一直到程序结束都生效
    """
    # global level
    # global prior  # 区间嵌套层数
    # if outer:  # 如果外部优先
    #     if para in [DEBUG, INFO, WARN, ERROR, CRITICAL]:
    #         prior += 1
    #         if prior == 1:  # 如果是最外层就操作
    #             level = logger.getEffectiveLevel()  # 记录临时修改前日志级别
    #             logger.setLevel(para)
    #     elif type(para) == str and para.lower() == 'end':
    #         # 如果第一个变量为False，则不会判断第二个变量，所以即使para不是字符串，para.lower()不会报错
    #         prior -= 1
    #         if prior == 0:
    #             logger.setLevel(level)
    #     else:
    #         logger.error('参数未识别，para只能取值logging日志的有效级别或字符串"end"!')
    # else:  # 如果内部优先
    #     if para in [logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL]:
    #         level = logger.getEffectiveLevel()
    #         logger.setLevel(para)
    #     elif type(para) == str and para.lower() == 'end':
    #         # 恢复日志级别为外部级别
    #         logger.setLevel(level)
    #     else:
    #         logger.error('参数未识别，para只能取值logging日志的有效级别或字符串"end"!')
    pass


def smart_decorator(decorator):
    """
    智能装饰器，用于装饰装饰器，使得装饰器无论在有没有参数的情况下可以使用同样的语法。无论是类装饰器和方法装饰其都可以装饰。

    :param decorator:
    :return:

    当func is None时，
    decorator_proxy=smart_decorator(decorator)

    decorator_proxy1=decorator_proxy(func, **kwargs)
    """

    def decorator_proxy(func_method=None, *args, **kwargs):
        if func_method is not None:
            return decorator(func_method, *args, **kwargs)

        def decorator_proxy1(func_method1):
            return decorator(func_method1, *args, **kwargs)

        return decorator_proxy1

    return decorator_proxy


@smart_decorator
def loggingTitleCall(func, title=None):
    """
    装饰器 @loggingTitleCall(title=title)，用于在方法前后打印日志标题和结尾

    疑问：

        这里func是个必要参数，为什么使用时可以不指定func的值？

    解答：

        在带参数使用时， @loggingTitleCall(title='title')相当于调用 loggingTitleCall(title='title')(func=FunctionType)，func默认赋值了被装饰的方法或类名。

        不带参数使用时， @loggingTitleCall 相当于调用 loggingTitleCall(func=FunctionType, title="新环境")。如果该装饰器参数列表中不指定title的默认值，则使用时必须给title赋值。

        不能使用 @loggintTitleCall('title')，即必须将参数写作title="title"，否则，解释器会把'title'赋值给func造成逻辑错误。

    :param func:
    :param title:
    :return:
    """
    if title is None:
        title = func.__name__

    def wrap_f(*args, **kwargs):
        loggingTitle(title=title, start_end='start')
        try:
            result = func(*args, **kwargs)
        except TypeError as e:
            if e.args[0] == "'str' object is not callable":
                logger.error("貌似使用了带参数的装饰器，如需要传递参数，请指定title='参数'")
            traceback.print_exc()
            exit(1)
        loggingTitle(title=title, start_end="end")
        return result

    return wrap_f


@smart_decorator
def SqliteClass(cls, table=None):
    """
    一个装饰器，在其他类上标记@SqliteClass，使得其他类可以用于和sqlite互转

    :param cls:
    :param table:
    :return:
    """
    cls.__tablename__ = 'user'
    columns = [*cls.__init__.__code__.co_names]
    sig = inspect.signature(cls.__init__)
    for par in sig.parameters.values():
        if par.annotation is not inspect._empty:
            print('Parameter: ', par)
            print("name: ", par.name)
            print("type: ", par.annotation)

    class NewClass():
        def __init__(self, *args, **kwargs):
            self.new = cls(*args, **kwargs)

    return NewClass


def loggingTitle(title: str = "default", logger=None, start_end: str = "start"):
    """
    输出以下格式的日志标题
    +-----------------------------------------+
    |                   title                 |
    +-----------------------------------------+
    :param start_end: 可以取值"start"和"end"
    :param title:
    :return:
    """
    if logger is None:  # 没有传入logger，则使用全局logger
        logger = globals().get('logger')

    n, m = __cal_char_length(title)

    if start_end.lower() == "start":
        start_char, end_char = "-", "↓"
        logger.debug("'{}'环境准备中...\n".format(title))
        logger.debug("+" + start_char * n + "+")
        logger.debug("|" + " " * m + title + " " * m + "|")
        logger.debug("+" + end_char * n + "+")
    elif start_end.lower() == "end":
        start_char, end_char = "↑", "-"
        logger.debug("+" + start_char * n + "+")
        logger.debug("|" + " " * m + title + " " * m + "|")
        logger.debug("+" + end_char * n + "+\n")


def __cal_char_length(title: str) -> (int, int):
    """
    获得日志标题边框行和标题行中填充字符的数量

    :return: number_of_border_line, number_of_title_line
    """
    length, _, _ = get_char_number(title)
    if length < 100:
        if length % 2 == 0:  # 标题内容长度是偶数
            number_of_border_line = 100
            number_of_title_line = int(50 - length / 2)
        else:  # 标题内容长度是奇数
            number_of_border_line = 101
            number_of_title_line = int((101 - length) / 2)
    else:
        number_of_border_line = length + 2
        number_of_title_line = 1
    return number_of_border_line, number_of_title_line


def get_char_number(content: str) -> (int, int, int):
    """
    获得字符串的占位长度、汉字个数、字母个数。
    占位长度即输出式占的宽度，汉字占两个长度，英文数字等占一个长度；
    默认的len(string)函数获得是字数，汉字和字符都算一个长度
    :param content: 字符串内容
    :return: length - 汉字算两个长度，字母算一个长度；
    number_Of_Chinese_Chars - 汉字个数；
    number_of_letters - 其他字母个数
    """
    lenText = len(content)  # 总字数，汉字和其他字符都算一个长度
    lenChar = len(content.encode("utf8"))  # 这种长度汉字算3个，其他字符算1个
    number_Of_Chinese_Chars = int((lenChar - lenText) / 2)
    number_of_letters = lenText - number_Of_Chinese_Chars
    length = number_Of_Chinese_Chars * 2 + number_of_letters
    return length, number_Of_Chinese_Chars, number_of_letters


def printInColor(text: str = "",
                 color_fg: str = 'blue', color_bg: str = 'yellow', mode: int = 0,
                 localSet='inline', end=os.linesep):
    """
    以特定颜色输出文本内容

    color_fg和color_bg可以取以下值：

    "white", "red", "green", "yellow", "blue", "purple", "cyan", "gray"

    mode可取以下值：

    0        |     终端默认设置
    1        |     高亮显示
    22       |     非粗体
    4        |     下划线
    24       |     非下划线
    5        |     闪烁
    25       |     非闪烁
    7        |     反显
    27       |     非反显

    :param end:
    :param text: 输出的文本内容，如果只是设置终端输出格式，可以不赋值
    :param color_fg: 终端输出文字的前景色
    :param color_bg: 终端输出的文字背景色
    :param mode: 显示模式
    :param localSet: 'start'、'end'、'inline'，格式开始生效、格式结束生效、格式仅在当前内容生效
    """
    colors_names_list = ["white", "red", "green", "yellow", "blue", "purple", "cyan", "gray", ""]
    colors_fg = [30, 31, 32, 33, 34, 35, 36, 37, '']
    colors_bg = [40, 41, 42, 43, 44, 45, 46, 47, '']

    mode: str = str(mode) + ";"
    code_fg = str(colors_fg[colors_names_list.index(color_fg)]) + ";"
    code_bg = str(colors_bg[colors_names_list.index(color_bg)]) + ";"
    format_str = (mode + code_fg + code_bg).rstrip(';')  # 删掉最后一个分号
    if localSet.lower() == 'start':
        print("\033[{}m".format(format_str), end=end)
    elif localSet.lower() == 'end':
        print("\033[0m", end=end)
    else:
        print("\033[{}m{}\033[0m".format(format_str, text), end=end)


def __import_first__():
    global logger
    # 当被其他模块首次引用时，会执行以下初始化代码
    settings = get_settings().get('logger') or {}
    level = settings.get('level') or 30  # 必须有值
    levelColor = settings.get('levelColor')  # 可以为None
    formatColor = settings.get('formatColor')  # 可以为None
    logFormat = settings.get('format')
    dateFormat = settings.get('dateFormat')
    logger = initLogger(level, level_color=levelColor, format_color=formatColor, log_format=logFormat,
                        date_format=dateFormat)


prior = 0  # 用来控制临时修改日志级别的变量
__import_first__()
