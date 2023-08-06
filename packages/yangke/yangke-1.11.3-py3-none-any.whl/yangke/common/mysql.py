import os
import logging

from mysql.connector.cursor import MySQLCursorBuffered

from yangke.core import runCMD, enableDocker, statusOfContainer, strInList, runAsAdmin
from yangke.base import get_args, get_settings
from yangke.common.config import logger
import pymysql
from pymysql.connections import Connection, Cursor
from sqlalchemy import create_engine, MetaData, Table, NVARCHAR, Float, Date, Integer
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, scoped_session
import traceback
import warnings
import json
import re
import datetime
import pandas as pd

try:
    # noinspection all
    from DBUtils.PooledDB import PooledDB  # DBUtils 1.*版本写法
except ModuleNotFoundError:
    # noinspection all
    from dbutils.pooled_db import PooledDB  # DBUtils 2.*版本写法

# encoding = 'utf-8'
pool: PooledDB = None  # 连接池

dtype_dict = {
    'str': NVARCHAR(length=255),
    'float': Float(),
    'int': Integer(),
    'float64': Float(),
    'date': Date(),
}

# 最后一次调用该模块的方法时使用的engine，单线程可以不传入engine，默认使用上一次的
# 这里之所以不保存cursor，是因为pymysql对cursor不会做连接存活处理，经常发生cursor自动断开导致操作报错的情况。
# 报错类型为：pymysql.err.InterfaceError: (0, '')
last_engine: Engine = None


def __start_mysql__(name_of_container, volume, user, password, mysqlPort):
    def print_lines(lines):
        for line in lines:
            print(line)

    # =========================确保指定名称的容器没有运行，如果在运行则跳过启动操作=================================
    status = statusOfContainer(name_of_container)
    if status is None:
        pass
    elif "up" in status.lower():
        # 容器不存在，则跳过if代码块
        logging.debug("容器{}正在运行！".format(name_of_container))
        return True
    else:
        # 如果存在同名容器，且容器没有运行，则删除该容器
        runCMD("docker container rm --force " + name_of_container)

    # 该条docker命令中 -p 3306:3306最好显式指出，否则JDBC可能连接不上；而adminer无论是否指出端口都可以连接上。
    # MYSQL_USER、MYSQL_PASSWORD和MYSQL_DATABASE也是为了spring使用jdbc连接建立的数据库
    # docker run --rm --name some-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=111111 -e MYSQL_USER=springuser -e MYSQL_PASSWORD=ThePassword -e MYSQL_DATABASE=test -d --privileged=true mysql:latest
    # '-e MYSQL_USER=yangke -e MYSQL_PASSWORD=111111 -e MYSQL_DATABASE=test ' \
    if volume is not None:
        command = 'docker run --rm --name some-mysql -p {}:3306 -e MYSQL_ROOT_PASSWORD={} ' \
                  '-d -v "{}:/var/lib/mysql/" --privileged=true mysql:latest'.format(mysqlPort, password, volume)
    else:
        command = 'docker run --rm --name some-mysql -p {}:3306 -e MYSQL_ROOT_PASSWORD={} ' \
                  '-d --privileged=true mysql:latest'.format(mysqlPort, password)
    logging.debug("执行命令：" + command)
    logging.info('挂载mysql数据卷路径为: "{}"'.format(volume))
    result, err = runCMD(command)
    if strInList('mkdir /host_mnt/d: file exists', err):
        logging.info(err)
        print("Docker服务异常，导致docker的本地卷挂载不上请重启Dockers Desktop后再试!")
        return False
    elif strInList("doesn't exist and is not known to Docker", err):
        logging.info(err)
        print("挂载的卷不存在，请检查卷路径！")
        return False
    elif len(err) > 0:
        logging.info(err)
        return False
    else:
        logging.debug("MySQL服务已经启动，信息如下：")
        title, _ = runCMD('docker container ps | findstr "container"')
        print_lines(title)
        results, _ = runCMD('docker container ps | findstr "some-mysql"')
        print_lines(results)
        return True


def __start_adminer__(db_name, port, ui="nette"):
    """
    启动adminer服务，连接到指定的mysql数据库
    :param db_name: 运行mysql数据库服务端的容器名称
    :param port: 设置adminer映射到本地的端口号
    :param ui: 控制了adminer的界面风格，可选的参数参见https://www.adminer.org/
    :return:
    """
    # 这里列出几个ui风格
    # ui = "mancave"  # mancave-hever, pepa-linha-dark, galkaev, price, mancave
    # ===================== 确保没有 some-adminer 容器在运行==========================
    adminer_name = "some-adminer"
    status = statusOfContainer(adminer_name)
    if status is not None:
        runCMD('docker container rm --force {}'.format(adminer_name))
        logging.debug("发现已经创建的adminer服务，重新创建adminer服务！")
    # ========================== 启动 some-adminer 容器===============================
    status = statusOfContainer(db_name)
    if "up" in status.lower():
        # 如果需要设置adminer的界面，参考https://www.adminer.org/en/
        # 如果需要使用galkaev的界面，设置如下（但测试报错）
        # docker run --name {} --link {}:db -p {}:8080 -e ADMINER_DESIGN="galkaev" adminer
        command = 'docker run --name {} --link {}:db -e ADMINER_DESIGN="{}" -p {}:8080 -d adminer' \
            .format(adminer_name, db_name, ui, port)
        logging.debug('执行docker命令：' + command)
        result, err = runCMD(command)
        # 验证adminer是否正常启动
        import time
        time.sleep(1)
        status = statusOfContainer(adminer_name)
        if "up" in status.lower():
            print("您现在可以通过浏览器访问 http://localhost:{} 连接到mysql数据库".format(port))
        else:  # 说明启动失败，一般情况下，这时候adminer容器的状态是Created；重启一次adminer拿到失败的信息并输出
            logging.debug(result)
            logging.debug(err)
            if strInList("Error starting userland proxy: /forwards/expose/port returned unexpected status: 500", err):
                logging.debug('设置的adminer端口{}不可用，自动尝试端口{}...'.format(port, port + 1))
                __start_adminer__(db_name, port + 1, ui)
            else:
                print("Adminer启动失败，请检查配置！")
                return False
    else:
        logging.warning("Try to start Adminer, but no mysql container found...")
        return False
    return True


def connect_available(user=None, passwd=None, password=None, host=None, port=None,
                      db=None, charset="utf8mb4",
                      return_pool=False, config=None):
    """
    判断指定的参数是否可以连接到mysql服务器，参数含义参考pymysql.connect()方法。
    如果只需判断mysql服务是否可用，而不用判断用户名密码等连接参数是否正确，请使用mysql_available()方法

    :passwd=password,两个参数含义相同，是别名
    :return:
    """

    port = int(port)
    passwd = passwd or password
    result = connect_mysql(user, passwd, host, port,
                           db, charset=charset,
                           return_type="pool", config=config)
    if result is None:
        return False
    else:
        result.close()
        return True


def mysql_available(user=None, passwd=None, host=None, port=None, db=None, create_if_not_exist=True, charset=None,
                    config=None) -> bool:
    """
    测试mysql服务是否可用，不带参数，仅代表本地是否有mysql服务
    如果测试连接是否可用，请使用connect_available()方法

    :config:
    :return:
    """

    # 当带参数判断时，需要借助pymysql，因为如果mysql -u root是交互式的，runCMD会阻塞
    if user is not None and passwd is not None:
        cursor = connect_mysql(user=user, passwd=passwd, host=host, port=port, db=db,
                               create_if_not_exist=create_if_not_exist,
                               charset=charset, config=config)
        if cursor is None:
            return False
        else:
            return True
    # mysql -h 127.0.0.1 -P 3306 -u root -p
    _, err = runCMD("mysql", charset='gbk', wait_for_result=True)
    # 测试mysql8.0.18，运行'mysql'命令，结果如下：
    # 当mysql可用时，提示：ERROR 1045 (28000): Access denied for user 'ODBC'@'localhost' (using password: NO)
    # 当mysql不可用时，提示：ERROR 2003 (HY000): Can't connect to MySQL server on 'localhost' (10061)
    # windows返回ERROR 1045
    # ubuntu远程访问mysql返回ERROR 2002 (HY000): Can't connect to local MySQL server through
    # socket '/var/run/mysqld/mysqld.sock' (2)
    if strInList('ERROR 1045', err) or 'ERROR 1045' in err or 'ERROR 2002' in err:
        return True
    else:  # if strInList("ERROR 2003", err) or 'ERROR 2003' in err or 'mysql: not found' in err:
        return False


def start_mysql_service():
    """
    开启本地mysql服务，如果已启动，则不操作

    :return:
    """
    # args = getArgs('type', 'service_name', 'volume', 'adminer', 'user', 'password', 'mysql_port')

    service_type = 'service'  # 默认启动服务
    service_name = 'mysql'  # 默认启动的服务名
    configs = get_settings()
    if configs.get('mysql') is None:
        pass
    else:
        if configs.get('mysql').get('service') is not None:
            service_type = 'service'
        elif configs.get('mysql').get('docker') is not None:
            service_type = 'docker'

    if service_type == 'service':

        if configs.get('mysql') is not None:
            serviceDict = dict(configs.get('mysql').get('service'))
            service_name = serviceDict.get('service_name') or 'mysql'
        else:
            pass
        # 测试mysql是否可用
        if not mysql_available():
            from threading import Thread
            import platform
            if str(platform.platform()).startswith("Windows"):
                cmd = 'net start {}'.format(service_name)
                t1 = Thread(target=runAsAdmin, args=(cmd,))
            elif str(platform.platform().startswith("Linux")):
                cmd = 'service {} start'.format(service_name)
                t1 = Thread(target=runCMD, args=(cmd,))
            # 这里开个新线程启动mysql，因为当用户拒绝以管理员身份运行时，runAsAdmin命令会卡住

            t1.setDaemon(True)
            t1.start()
            t1.join(20)
            # runAsAdmin('net start {}'.format(service_name))

        if mysql_available():
            return True
        else:
            return False
    elif service_type == 'docker':
        docker_dict = dict(configs.get('mysql').get('docker'))
        user = docker_dict.get('user')
        password = docker_dict.get('passwd')
        volume = docker_dict.get('volume')
        adminer = docker_dict.get('adminer') or None
        mysql_port = docker_dict.get('port') or 3306
        adminer_port = docker_dict.get('adminerPort') or 8080
        container_name = docker_dict.get('containerName') or "some-mysql"
        success = enableDocker()
        assert success, "当前配置使用docker - mysql，但docker服务不可用"
        # path = os.getcwd() # 这个是调用者所在的路径
        success = __start_mysql__(container_name, volume=volume, user=user, password=password, mysqlPort=mysql_port)
        assert success, "当前配置使用docker - mysql，mysql容器启动失败"
        if adminer:
            success = __start_adminer__(container_name, adminer_port)
            if not success:
                return False
        return True


def connect_mysql(user="root", passwd="111111", host="localhost", port=3306,
                  db=None, create_if_not_exist=True, charset="utf8mb4",
                  return_type="cursor", config=None, test_mode=False, use_pymysql=True):
    """
    尝试连接mysql，如果连接成功，则返回return_type指定的对象；如果不传入参数，则从settings文件读取配置信息，
    如果settings文件中存在多个mysql配置，以最后一个为准。
    如果配置文件有配置参数且传入参数，则以配置参数为准。优先级配置文件>制定参数>config参数
    如果使用config连接，示例如下
    mysql_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '111111',
    'charset': 'utf8mb4'
    }
    conn, cursor=connect_mysql(config=mysql_config)  # 这里获得了一个没有指定数据库的cursor
    # 给config参数指定数据库，再次连接
    mysql_config['db'] = db_name
    conn = pymysql.connect(**mysql_config)  # 这里获得另一个指定了数据库的连接
    conn, cursor = connect_mysql(config=mysql_config)  # 这里获得连接了数据库的cursor

    当使用连接池时，示例如下：
    pool = connect_mysql(db='face', return_pool=True)  # 不指定用户名密码则connect_mysql方法从配置文件读取配置参数
    conn = pool.connection()
    cursor = conn.cursor()

    :param use_pymysql: 使用pymysql连接数据库，也可以使用mysqlconnector，目前二者使用engine连接都有一些问题，pymysql有警告但不影响使用
    :param user:
    :param passwd:
    :param host:
    :param port:
    :param db: 需要连接的db名，如果指定的db不存在，该方法会自动创建
    :param create_if_not_exist: 当db不存在时，是否创建
    :param charset:
    :param return_type: “cursor"/"pool"/"engine"，返回类型，分别对应游标，连接池和sqlalchemy的引擎
    :param config:
    :param test_mode: 如果是测试连接是否可用，则不输出错误信息，如果是需要连接，则失败时会输出错误信息
    :return: 根据return_cursor的取值，返回不同数据
    """
    # 依次查询settings.py、config入参、其余指定项入参，存储到config_mysql中
    global pool
    configs = get_settings().get('mysql') or {}
    if configs is not None:  # 读取配置文件的配置
        mysql_configs = configs.get('service') or configs.get('docker') or configs  # 连接时无论那种服务类型，连接方式都是一致的，无需区分
        host = mysql_configs.get('host') or host  # 优先使用传入的参数，没有传入参数，则使用配置文件桉树
        port = mysql_configs.get('port') or port
        user = mysql_configs.get('user') or user
        passwd = mysql_configs.get('passwd') or passwd
        passwd = str(passwd) if passwd is not None else None  # 如果passwd不为None，则将passwd转换为str类型，防止纯数字密度读入为整形
        db = mysql_configs.get('db') or db
        charset = mysql_configs.get('charset') or charset or "utf8mb4"

    if config is not None:  # 如果传入参数不为空，则以传入参数为准
        host = host or config.get('host')
        port = port or config.get('port')
        user = user or config.get('user')
        passwd = passwd or config.get('passwd')
        charset = charset or config.get('charset')
        db = db or config.get('db')
    config_mysql = {'host': host,
                    'port': int(port),
                    'user': user,
                    'passwd': passwd,
                    'charset': charset,
                    'db': db}

    # 将config_mysql中的参数存到短变量名中，便于引用
    port = config_mysql['port']

    if return_type != "engine":
        # 建立mysql数据库连接
        try:
            if return_type == "pool":
                global pool
                pool = PooledDB(pymysql, 5, **config_mysql)  # 可能报错，现在没有考虑报错情况
                _update_cursor(pool.connection().cursor())
                return pool
            elif return_type == "cursor":
                conn = pymysql.connect(**config_mysql)
        except TypeError as e:
            if e.args[0] == "object supporting the buffer API required":  # 说明passwd是整数，目前在入口处已经转换类型
                logger.warning("输入的密码是整形数据，尝试转换为字符串后重新连接...")
        except pymysql.err.InternalError as e:
            if e.args[0] == 1049:  # 说明时不存在指定的db文件
                if create_if_not_exist:
                    config_mysql.pop('db')
                    conn = pymysql.connect(**config_mysql)
                    create_db(conn.cursor(), db_name=db)
                    return connect_mysql(user=user, passwd=passwd, host=host, port=port, db=db, charset=charset,
                                         return_type=return_type)
                else:
                    logger.error("需要连接的mysql数据库db文件不存在：{}".format(db))
                    return None
        except pymysql.err.OperationalError as e:  # 账号或密码错误
            if e.args[0] == 1045:  # (1045, "Access denied for user 'root'@'localhost' (using password: YES)")
                if not test_mode:
                    logger.error("mysql连接被拒绝，请检查账号密码，错误信息：{}".format(e))
            elif e.args[0] == 1044:  # (1044, "Access denied for user 'test'@'localhost' to database 'face'")
                if not test_mode:
                    logger.error("mysql连接被拒绝，连接 {} 的权限不足".format(e))
            elif e.args[
                0] == 1142:  # (1142, "CREATE command denied to user 'test'@'localhost' for table 'persongroup'")
                if not test_mode:
                    logger.error("mysql用户操作 {} 的权限不足".format(e))
            elif e.args[0] == 1049:  # 说明时不存在指定的db文件
                if create_if_not_exist:
                    config_mysql.pop('db')
                    conn = pymysql.connect(**config_mysql)
                    create_db(conn.cursor(), db_name=db)
                    return connect_mysql(user=user, passwd=passwd, host=host, port=port, db=db, charset=charset,
                                         return_type=return_type)
                else:
                    logger.error("需要连接的mysql数据库db文件不存在：{}".format(db))
                    return None
            return None
        # 创建游标
        cursor = conn.cursor()
        _update_cursor(cursor)
        return cursor
    else:
        if use_pymysql:
            eng = "pymysql"  # 有警告
        else:
            eng = "mysqlconnector"  # mysql8版本会报授权验证插件错误
        engine = create_engine(f'mysql+{eng}://{user}:{passwd}@{host}:{port}')
        if db is not None:
            if not exist_db(db_name=db, cursor=engine):  # 如果指定的db不存在，则创建
                create_db(db)
            engine = create_engine(f'mysql+{eng}://{user}:{passwd}@{host}:{port}/{db}')
        _update_cursor(engine)
        return engine


def exec_sql_script(sql_script=None, para=None, close=False, cursor=None):
    """
    执行指定的mysql语句

    Example:
        如果要执行的sql语句需要传入变量，使用如下方法：

        script = "insert into account(company, user, password, fund, stocks) VALUES (?,?,?,?,?)"
        para = (company, user, password, fund, stocks,)
        exec_sql_script(cursor, script, para)


    :param cursor:
    :param sql_script:
    :param para:
    :param commit: 是否需要提交，查询操作不需要提交，更新操作需要提交
    :param close: 操作完成后，是否需要关闭连接
    :return: 执行结果

    """
    cursor = _update_cursor(cursor)
    if isinstance(cursor, str):
        logger.error("当前传入的mysql语句执行游标为 cursor = {}，该错误一般是因为漏掉了应该传入的游标参数".format(cursor))
        return None
    elif isinstance(cursor, Engine):
        cursor: Engine = cursor
        session_ = sessionmaker(bind=cursor)
        session = scoped_session(session_)
        res = session.execute(sql_script)
        session.commit()
        # res = cursor.execute(sql_script)  # engine只能查，修改的话无法commit
        if res.returns_rows:  # 如果执行sql语句有返回结果
            tmp = res.fetchall()
        else:
            tmp = []
        session.remove()
    elif isinstance(cursor, Cursor):
        if para is not None and not isinstance(para, tuple):
            para = (para,)
        cursor.execute(sql_script, para)
        tmp = cursor.fetchall()
        if close:
            cursor.close()
            cursor.connection.close()
    elif isinstance(cursor, MySQLCursorBuffered):
        raise ValueError("暂不支持mysqlconnector的游标")
    return tmp


def _update_cursor(engine):
    """
    记录最后一次使用的游标。如果传入非空，则记录传入参数对应的cursor后返回原参数。如果传入为空，则返回记录的最后一次保存的cursor

    :param engine:
    :return:
    """
    global last_engine
    if engine is None or engine == last_engine:
        return last_engine
    else:
        if isinstance(engine, Cursor):
            last_engine = cursor2engine(engine)
        elif isinstance(engine, Engine):
            last_engine = engine
            return engine
        elif isinstance(engine, MySQLCursorBuffered):
            raise ValueError("暂不支持mysql-connector的游标")


def exist_db(db_name: str = None, cursor: Cursor or Engine = None):
    """判断数据库是否存在，需要确保cursor对应的mysql账号有权限范围对应的db，否则返回False"""
    cursor = _update_cursor(cursor)

    sql = "show databases like '{}'".format(db_name)
    if isinstance(cursor, Cursor):
        result = exec_sql_script(cursor=cursor, sql_script=sql)
        return False if len(result) == 0 else True
    else:
        result = cursor.execute(sql)
        return False if result.rowcount == 0 else True


def engine2cursor(engine: Engine):
    """
    从sqlalchemy的engine拿到对应的cursor，同一个engine多次调用该方法返回不同的cursor

    :param engine:
    :return:
    """
    _update_cursor(engine)  # 更新模块变量last_engine，记录对应的engine
    cursor = engine.pool.connect().cursor()  # 获取engine的cursor
    return cursor


def cursor2engine(cursor: Cursor = None):
    """
    将pymysql的cursor获取sqlalchemy的engine，同一个cursor多次调用该方法返回不同的engine

    :param cursor:
    :return:
    """
    # 这里不能添加_update_cursor()方法，以免行程递归死锁调用
    conn = cursor.connection
    encoding = conn.encoding
    user = conn.user.decode(encoding)
    passwd = conn.password.decode(encoding)
    host = conn.host
    port = conn.port
    db = conn.db.decode(encoding) if conn.db is not None else None
    engine = connect_mysql(user, passwd, host, port, db, return_type="engine")

    return engine


def create_db(db_name: str = None, cursor: Cursor or Engine = None):
    """
    创建数据库文件，确保有root权限
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    sql = "create database `{}`".format(db_name)
    if not exist_db(db_name):
        if isinstance(cursor, Engine):
            _ = cursor.execute(sql)
        else:
            _ = exec_sql_script(sql)
    return True


def has_table(table_name: str = None, cursor: Cursor or Engine = None):
    """
    判断给定代码的股票的数据库表是否存在。确保mysql用户有操作权限

    GRANT ALL on face.* to 'test'@'localhost';

    :param cursor: 游标或engine
    :param table_name: 表名
    :return: bool
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    if isinstance(cursor, Cursor):
        sql = "show tables like '{}'".format(table_name)
        result = exec_sql_script(sql, cursor=cursor)
        return False if len(result) == 0 else True
    else:
        cursor: Engine = cursor
        return cursor.has_table(table_name)


def create_table(table_name: str = None, columns: dict = None, primary=[0],
                 foreign=None,
                 metadata=None, cursor: Cursor or Engine = None) -> bool:
    """
    创建mysql表
    例1：
    from sqlalchemy import Column, Integer, String, Date, CHAR, Table, MetaData
    holiday_table = MetaData()  # 没有关系的表放在不同的metadata中
    Table('holiday', holiday_table,
          Column('calendarDate', Date, primary_key=True),
          Column('isOpen', CHAR, nullable=False))
    engine = sqlalchemy.create_engine("mysql+pymysql://root:111111@localhost:3306/stocks")
    create_table(cursor=engine, metadata=holiday_table)
    如果使用sqlalchemy的metadata创建表，第一个参数必须传入Engine类型对象

    例2：
    create_table(cursor=cursor, table_name="item", columns={"id": "int", "name": "varchar(20)", "price": "float"})
    其中columns的取值参见mysql建表语句中的数据类型说明

    :param metadata: 如果cursor是sqlalchemy的engine，则table为对应的sqlalchemy的metadata对象
    :param cursor: 连接了数据库的游标或engine
    :param table_name: 表名
    :param columns: 列名和数据类型的字典，如{"id": "int", "name": "varchar(20)", "price": "float"}，日期最好用varchar，使用python转换
    :param primary: 主键，默认第一个，多个主键通过[0,1 ]等列索引传入
    :param foreign: 外键引用信息，例如foreign="FOREIGN KEY (person_id) REFERENCES person(id) ON DELETE CASCADE ON UPDATE CASCADE"
    :return: bool
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    if isinstance(cursor, Engine):
        if metadata is not None:
            metadata.create_all(cursor)
            return True
        else:
            engine: Engine = cursor
            cursor = engine2cursor(engine)
    if isinstance(primary, int):
        primary = [primary]
    primaryKey = []
    i = 0

    temp = ""
    for key, data_type in columns.items():
        temp = temp + "`{}` {},".format(key, data_type)
        if i in primary:
            primaryKey.append("`{}`".format(key))
        i = i + 1
    primary_str = ",".join(primaryKey)
    if foreign is not None:
        foreign = ", {}".format(foreign)
    else:
        foreign = ""
    sql = "create table if not exists `{}` ({} primary key ({}) {});".format(table_name, temp, primary_str, foreign)
    exec_sql_script(sql_script=sql)
    return True


def delete_in_table(table_name: str = None, col_name: str = None, value: str = None, return_result=False, cursor=None,
                    **kwargs):
    """
    调用之前确认要删除的表和数据行存在

    :param return_result:
    :param cursor:
    :param table_name:
    :param col_name:
    :param value:
    :return:
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    if len(kwargs) == 0:
        if col_name is None or value is None:
            return False
        sql = "delete from `{}` where `{}`='{}';".format(table_name, col_name, value)
    else:
        k_v_pairs = []
        for k, v in kwargs.items():
            k_v_pairs.append("`{}`='{}'".format(k, v))
        conditions = " and ".join(k_v_pairs)
        if conditions.strip() is None:
            return False
        sql = "delete from `{}` where {};".format(table_name, conditions)
    fetchall = exec_sql_script(cursor=cursor, sql_script=sql)
    if return_result:
        return True, fetchall
    else:
        return True


def exists_in_table(table_name: str = None, col_name: str = None, value: str = None,
                    condition_dict: dict = None,
                    return_result: bool = False, cursor=None):
    """
    表tableName中是否存在列col_name的值位value的行

    :param cursor: 连接了db文件的游标
    :param table_name: 表名
    :param col_name: 列名
    :param value: 列的值
    :param condition_dict: 查询的键值对字典值，优先于col_name和value传入的值，即会覆盖col_name和value传入的值
    :param return_result: 是否需要返回查找到的数据行，如果为真，则返回所有符合查找条件的数据行
    :return:
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    if has_table(table_name, cursor):
        pass
    else:
        return False

    if condition_dict is not None and len(condition_dict) > 0:
        condition_str = []
        for k, v in condition_dict.items():
            condition_str.append("`{}`='{}'".format(k, v))
        condition_str = " and ".join(condition_str)
        col_name = k  # 在不需要返回结果是，随便查找一列
    else:
        condition_str = "`{}`='{}'".format(col_name, value)

    if return_result:
        sql = "(select * from `{}` where {});".format(table_name, condition_str)
    else:
        sql = "(select `{}` from `{}` where {});".format(col_name, table_name, condition_str)

    result = exec_sql_script(cursor=cursor, sql_script=sql)
    if return_result:
        return len(result) != 0, result
    else:
        return len(result) != 0


def insert_dataframe_to_mysql(table_name: str = None,
                              dataframe: pd.Series or pd.DataFrame = None,
                              ignore=False,
                              replace=False, filter_warning=None, cursor: Cursor or Engine = None):
    """
    因为pandas.DataFrame类的to_sql()方法存在一下问题：
    1.to_sql()方法自动创建的表的数据类型难以设置，而外键和PrimaryKey无法设置
    2.to_sql()方法插入dataframe数据时，如果表存在，则只能完全代替或完全追加，但当dataframe中有部分数据和数据库中
    相同时，无法只添加不同的数据，忽略相同的数据。

    该方法可以解决以上问题，尤其是第2个问题。

    将dataframe插入到mysql数据库中，如果dataframe中的某列列名不存在与mysql表中，则该列被忽略。如果mysql中的某列不存在于dataframe中，且
    mysql表定义时设置该列可以为空，则可以正常插入。

    :param cursor:
    :param table_name:
    :param dataframe: 插入的数据，可以是pd.DataFrame或pd.Series
    :param ignore: 当插入数据重复时，是否忽略，ignore和replace不能同时为True
    :param replace: 当插入数据重复时，是否替换，ignore和replace不能同时为True
    :param filter_warning: 过滤警告信息，[1062, 1265, 1366]，分别对应["Duplicate", "Data truncated", "Incorrect integer value"]
    :return:
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    if isinstance(cursor, Engine):
        cursor: Cursor = engine2cursor(cursor)
    assert (ignore and replace) is False, "ignore和replace不能同时为True"
    ignore_ = "ignore" if ignore else ""
    if isinstance(dataframe, pd.DataFrame):
        row_num, col_num = dataframe.shape
        columns_df = set(dataframe.columns)
        columns_sql = set(get_column_name_of_table(table_name))
        columns_common = list(columns_sql & columns_df)
        columns_common.sort()
        value_list = []
        for i in range(row_num):
            temp_value = str(tuple([dataframe[name][i] for name in columns_common]))
            value_list.append(temp_value)
        values_str = ",".join(value_list)
    elif isinstance(dataframe, pd.Series):
        n = dataframe.size
        columns_df = set(dataframe.index)
        columns_sql = set(get_column_name_of_table(table_name))
        columns_common = list(columns_sql & columns_df)
        columns_common.sort()
        values_str = str(tuple([dataframe[name] for name in columns_common]))
    else:
        logger.warning(f"传入的数据类型{type(dataframe)}错误，本方法只支持插入DataFrame或Series类型")
        return None

    columns_str = ",".join([f'`{col}`' for col in columns_common])
    if replace:
        sql = f"REPLACE INTO `{table_name}` ({columns_str}) VALUES {values_str};"
    else:
        sql = "INSERT {} INTO `{}` ({}) VALUES {};".format(ignore_, table_name, columns_str, values_str)

    if filter_warning is None:
        exec_sql_script(sql_script=sql)
    elif isinstance(filter_warning, list):
        try:
            warnings.filterwarnings('error')
            exec_sql_script(cursor=cursor, sql_script=sql)
        except Warning as e:
            if e.args[0] in filter_warning:
                pass
            else:
                traceback.print_exc()


def insert_item_to_mysql(table_name: str = None, values: list = None,
                         col_names: list = None, ignore=False,
                         replace=False, filter_warning=None, cursor: Cursor or Engine = None):
    """
    向mysql数据库中插入数据，这里传入的列名不要用反引号括起来，增

    :param cursor: 连接了db文件的游标
    :param table_name: 表名
    :param values:
    :param col_names: 列名，如果是插入带有auto_increment属性的表数据，则必须指定列名，否则就需要指定auto_increment属性的字段的值
    :param ignore: 当插入数据重复时，是否忽略
    :param replace: 当插入数据重复时，是否替换，ignore和replace不能同时为True
    :param filter_warning: 过滤警告信息，[1062, 1265, 1366]，分别对应["Duplicate", "Data truncated", "Incorrect integer value"]
    """
    # 注意需要将python中的时间日期类型的数据转换为str插入
    import datetime
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    if isinstance(cursor, Cursor):  # 都转换为engine执行
        cursor = cursor2engine(cursor)
    for index, value in enumerate(values):
        if type(value) in [datetime.date, datetime.datetime, datetime.time]:
            values[index] = str(value)
    columns = ""
    if col_names is not None:
        columns = ",".join(
            ["`{}`".format(col) for col in col_names])  # linux下可能要用单引号括起来列名 ",".join("'{}'".format(col_names))
        columns = f"({columns})"
    # 当列名有特殊符号时，不能用?作为占位符进行数据插入
    values = ",".join(["'{}'".format(value) for value in values])
    assert (ignore and replace) is False, "ignore和replace不能同时为True"
    ignore_ = "ignore" if ignore else ""
    if replace:
        sql = "REPLACE INTO `{}` {} VALUES ({});".format(table_name, columns, values)
    else:
        sql = "INSERT {} INTO `{}` {} VALUES ({});".format(ignore_, table_name, columns, values)
    if filter_warning is None:
        exec_sql_script(cursor=cursor, sql_script=sql)
    elif isinstance(filter_warning, list):
        try:
            warnings.filterwarnings('error')
            exec_sql_script(cursor=cursor, sql_script=sql)
        except Warning as e:
            if e.args[0] in filter_warning:
                pass
            else:
                traceback.print_exc()


def update_in_table(table_name=None, condition_dict: dict = None, update_dict: dict = None, cursor=None) -> None:
    """
    更改数据库的值
    :param cursor:
    :param table_name:
    :param condition_dict:
    :param update_dict:
    :return:
    """
    _update_cursor(cursor)  # 更新模块变量last_cursor
    condition_str = []
    update_str = []
    for k, v in condition_dict.items():
        condition_str.append("`{}`='{}'".format(k, v))
    condition_str = " and ".join(condition_str)
    for k, v in update_dict.items():
        update_str.append("`{}`='{}'".format(k, v))
    update_str = ",".join(update_str)
    sql = 'update `{}` set {} where {};'.format(table_name, update_str, condition_str)
    exec_sql_script(sql_script=sql)


def read_dataframe_from_mysql(table_name=None, condition_dict: dict = None, result_col: list = None,
                              limit=10,
                              offset=10, cursor=None, **kwargs):
    """
    将mysql数据库表中的数据读入到pd.DataFrame类型结构中，默认全部读取，通过设置condition_dict添加过滤

    :param cursor: 连接了db文件的游标
    :param table_name: 数据库中表的名称
    :param condition_dict: 读取的数据条目所需满足的条件，默认全部读取
    :param result_col: 返回的数据列，默认全部返回
    :param limit: 返回条目的限制数量，同mysql数据库select语句中limit的用法
    :param offset: 返回条目的数据便宜，同mysql数据库select语句中offset的用法
    :param kwargs:
    :return:
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    if isinstance(cursor, Cursor):
        con = cursor.connection
    elif isinstance(cursor, Engine):
        con = cursor
    data = pd.read_sql(f"select * from {table_name};", con=con)
    return data


def select_in_table(table_name=None, condition_dict: dict = None, result_col: list = None, limit=10,
                    offset=0,
                    fuzzy=False, result_type=None, cursor=None, **kwargs):
    """
    查

    精确查询，设置fuzzy为True，且condition_dict中的value为字符串值
    模糊查询，设置fuzzy为False，日期列不能使用模糊查询，只能使用范围查询
    范围查询，设置fuzzy为True，且condition_dict中的value为长度为2的列表，列表第一、二项分别为范围下、上限，且包含上下限

    当result_type=="json"时，返回的是一个list(dict)的json对象，即[{col1: value1, col2: value2,...}, ...}的json对象
    列表的每一项对应一条匹配的查询结果
    每一项的字典分别是{列名：值}

    kwargs={"date_format": "%Y-%m-%d %H:%M:%S"} 如果mysql中存在日期列，需要将日期转换为字符串，该参数定义日期字符串格式


    :param cursor:
    :param table_name:
    :param condition_dict:
    :param result_col: 不传入或传入空列表，则返回数据库中所有列
    :param limit:
    :param offset:
    :param fuzzy: 是否模糊查询
    :param result_type: 返回类型，如果为json，则返回为json格式的字符串
    :return: None或tuple，出错时返回None，如列明不存在等；否则返回一个tuple类型的数据，长度为0表示未查询到满足条件的数据
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    if result_col is None:
        result_col = []
    condition_str = []
    result_col_str = []
    if fuzzy:
        for k, v in condition_dict.items():
            type_col = get_type_of_column(table_name=table_name, column_name=k)
            if type_col == "datetime":
                logger.error("日期类型不能使用模糊查询，请使用范围查询！")
                raise ValueError("日期类型不能使用模糊查询，请使用范围查询！")
            elif type_col == "int":
                logger.error("int类型不能使用模糊查询，请使用范围查询！")
                raise ValueError("int类型不能使用模糊查询，请使用范围查询！")
            elif type_col == "float":
                logger.error("float类型不能使用模糊查询，请使用范围查询！")
                raise ValueError("float类型不能使用模糊查询，请使用范围查询！")
            elif type_col is None:
                logger.warning(f"列类型未知，检查表中是否存在指定列({k})")
                return None
            condition_str.append(f"`{k}` LIKE '%{v}%'")
        condition_str = " and ".join(condition_str)
        condition_str = f"({condition_str})"
    else:
        for k, v in condition_dict.items():
            # 需要判断k是不是日期类型，日期类型需要将k,v都转成字符串进行对比
            type_col = get_type_of_column(cursor=cursor, table_name=table_name, column_name=k)
            if type_col is None:
                logger.warning(f"列类型未知，检查表中是否存在指定列({k})")
                return None
            elif type_col == "datetime":
                date_format = kwargs.get("date_format") or '%Y-%m-%d %H:%M:%S'
                if isinstance(v, datetime.datetime):  # 单值查询
                    v = datetime.datetime.strftime(v, date_format)
                    condition_str.append(f"DATE_FORMAT(`{k}`, '{date_format}')='{v}'")
                elif isinstance(v, datetime.date):
                    v = datetime.date.strftime(v, date_format)
                    condition_str.append(f"DATE_FORMAT(`{k}`, '{date_format}')='{v}'")
                elif isinstance(v, datetime.time):
                    v = datetime.time.strftime(v, date_format)
                    condition_str.append(f"DATE_FORMAT(`{k}`, '{date_format}')='{v}'")
                elif isinstance(v, str):
                    condition_str.append(f"DATE_FORMAT(`{k}`, '{date_format}')='{v}'")
                elif isinstance(v, list):  # 如果是列表，则说明是日期范围
                    if isinstance(v[0], datetime.datetime):  # 如果是datetime对象，则需要转换为str
                        v[0] = datetime.datetime.strftime(v[0], date_format)
                        v[1] = datetime.datetime.strftime(v[1], date_format)
                    elif isinstance(v[0], datetime.date):
                        v[0] = datetime.date.strftime(v[0], date_format)
                        v[1] = datetime.date.strftime(v[1], date_format)
                    elif isinstance(v[0], datetime.time):
                        v[0] = datetime.time.strftime(v[0], date_format)
                        v[1] = datetime.time.strftime(v[1], date_format)
                    condition_str.append(f"DATE_FORMAT(`{k}`, '{date_format}') "
                                         f"between '{v[0]}' and '{v[1]}'")
            elif type_col == "int" or type_col == "float":  # 如果对应列是数值类型
                if isinstance(v, list):  # 范围查询
                    condition_str.append(f"`{k}` between {v[0]} and {v[1]}")
                else:  # 单值查询
                    condition_str.append(f"`{k}`={v}")
            else:
                if isinstance(v, list):  # 范围查询
                    condition_str.append(f"`{k}` between '{v[0]}' and '{v[1]}'")
                else:  # 单值查询
                    condition_str.append("`{}`='{}'".format(k, v))
        condition_str = " and ".join(condition_str)
    if len(result_col) == 0:
        result_col_str = "*"
    else:
        for col in result_col:
            result_col_str.append(f"`{col}`")
        result_col_str = ",".join(result_col_str)

    sql = 'select {} from `{}` where {} limit {} offset {};'.format(result_col_str, table_name, condition_str, limit,
                                                                    offset)
    # 返回默认格式的检索结果
    result = exec_sql_script(sql_script=sql)
    # 返回json格式的检索数据，是一个列表，每一个列表项对应一条匹配的记录
    if result_type == "json":  # 如果需要返回json格式结果
        date_format = kwargs.get("date_format") or '%Y-%m-%d %H:%M:%S'
        if len(result) > 0:
            temp_dicts = []
            if result_col_str == "*":
                result_col = get_column_name_of_table(cursor=cursor, table_name=table_name)
            for item in result:
                temp_dict = {}
                for i, col in enumerate(result_col):
                    # 如果列是日期类型，需要转为字符串返回，否则json.dumps()方法会报错
                    if get_type_of_column(table_name, col) == "datetime":
                        if item[i] is not None:  # 如果是非必须的时间列，则时间值可能为None
                            temp_dict.update({col: item[i].strftime(date_format)})
                        else:
                            temp_dict.update({col: None})
                    else:
                        temp_dict.update({col: item[i]})
                temp_dicts.append(temp_dict)
            result = json.dumps(temp_dicts, ensure_ascii=False)
        else:
            result = json.dumps({})
    return result


def get_reference_table_column(table_name=None, column_name=None, cursor: Cursor = None):
    """
    根据已知表名和列名查找其外键指向的父表和父表列名

    :param cursor:
    :param table_name: 当前表名
    :param column_name: 当前列名
    :return: 外键指向的所有父表和父表列名的tuple
    """
    # sql = "select REFERENCED_TABLE_NAME,COLUMN_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where" \
    #       " TABLE_NAME = '{}'and COLUMN_NAME='{}' and CONSTRAINT_NAME!='PRIMARY';".format(tableName, columnName)
    # results = exec_sql_script(cursor=cursor, sql_script=sql)
    pass
    return None


def add_foreign_key(table_master=None, key_master=None, table_follow=None, key_follow=None, cursor=None):
    """
    添加外键约束

    适用于一对多关系，一是主表，多是从表，

    :param cursor:
    :param table_follow:
    :param key_follow:
    :param table_master:
    :param key_master:
    :return:
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    constraint_name = f"c_{table_master}_{table_follow}"
    if has_table(table_follow, cursor):  # constraint {constraint_name}
        sql = f"alter table `{table_follow}` add " \
              f"foreign key (`{key_follow}`) references `{table_master}`(`{key_master}`);"
        exec_sql_script(cursor=cursor, sql_script=sql)


def create_mysql_relation_table(table1=None, column1=None, table2=None, column2=None, cursor=None):
    """
    创建关系表

    :param cursor: 游标
    :param table1: 表1
    :param column1: 表1的主键
    :param table2: 表2
    :param column2: 表2的主键
    :return:
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    table_r = f"{table1}_rl_{table2}"
    column1_name_in_this_table = f"{table1}_{column1}"
    column2_name_in_this_table = f"{table2}_{column2}"
    type1 = get_type_of_column(table1, column1)
    type2 = get_type_of_column(table2, column2)

    if not has_table(table_r, cursor):
        sql = f"create table `{table_r}`(" \
              f"id int primary key auto_increment, " \
              f"`{column1_name_in_this_table}` {type1} not null, " \
              f"`{column2_name_in_this_table}` {type2} not null, " \
              f"foreign key(`{column1_name_in_this_table}`) references `{table1}`(`{column1}`) ON DELETE " \
              f"CASCADE ON UPDATE CASCADE, " \
              f"foreign key(`{column2_name_in_this_table}`) references `{table2}`(`{column2}`) ON DELETE " \
              f"CASCADE ON UPDATE CASCADE, " \
              f"unique key(`{column1_name_in_this_table}`,`{column2_name_in_this_table}`));"
        exec_sql_script(cursor=cursor, sql_script=sql)


def get_type_of_column(table_name=None, column_name=None, cursor=None):
    """
    获取mysql表中字段的类型，如果不设置column_name则返回所有的字段类型
    :param cursor:
    :param table_name:
    :param column_name: 为空则依次返回所有列的类型，封装为一个列表
    :return:
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    try:
        results = exec_sql_script(sql_script=f"show columns from `{table_name}`;")
    except pymysql.err.ProgrammingError:
        logger.error(f"表名或字段名不存在！'{table_name}.{column_name}'")
        return None
    type_dict = {}
    if column_name is None:
        for result in results:
            type_dict[result[0]] = result[1].lower()
        return type_dict
    else:
        for result in results:
            if result[0] == column_name:
                return result[1].lower()
    logger.error(f"表名或字段名不存在！'{table_name}.{column_name}'")
    return None


def get_column_name_of_table(table_name=None, cursor=None):
    """
    获取表中所有的字段名

    :param cursor:
    :param table_name:
    :return: list
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    sql = f"select COLUMN_NAME from information_schema.COLUMNS where table_name='{table_name}';"
    res = cursor.execute(sql)
    if isinstance(cursor, Cursor):
        fetchall = cursor.fetchall()
    else:
        fetchall = res.fetchall()
    result = []
    for field in fetchall:
        result.append(field[0])
    return result


def generate_columns_values(info_dict: dict, column_alias_dict: dict,
                            parameters: list = None,
                            extras_field_name: str = "extras_field",
                            null_symbol: list = ['-', '', '/', '－', '—']):
    """
    根据用户自定义的信息字典和数据库中字段的别名字典，生成可以填充到mysql数据库表格中的columns和values，以便使用
    INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)
    语句进行数据库数据条目插入。

    :param null_symbol: 代表值为空的字符串列表
    :param extras_field_name: 当用户传入的变量找不到对应的字段名时，会将该列及其值以字典形式更新进extras_field_name对应的数据库表字段值中
    :param parameters: 需要过滤单位的数据库表字段的列表，有些用户传入变量带有单位，如果不过滤会导致类型不匹配，如0.6MPa不能转为float类型
    :param info_dict: 表格中解析得到的变量名及其对应的数值，如{"生日": "19910305"}，这里的变量名不同来源可能不同，但指的是同一个东西
    :param column_alias_dict: 字段的别名，如{"birthday": ["生日", "出生日期"]}，这里指出了"birthday"字段的所有可能的别名
    :return: [列1, 列2,...], [值1, 值2,...]，例如["birthday"], ["19910305"]，如果为值为空，则返回结果中不包括该字段列
    """

    def find_col_name_in_db(name_variety: str):
        """
        用于获取用户变量在数据库中对应的字段名。

        column_alias_dict是字段对应的别名的字典。其格式如下：
        {
        "p_d_rhs1": ["额定再热汽门前压力", "再热蒸汽压力"],  # p_d_rhs1是数据库中的字段名，右侧列表是用户可能使用的变量名
        "t_d_rhs1": ["额定再热汽门前温度", "再热蒸汽温度"],  #
        }

        因为用户在实际word文档中，同一个变量可能使用不同的名字，这里将其对应到同一个数据库字段上。如果没有找到用户在word中定义的变量的存储字段，
        则该方法返回"extras_field"

        :param name_variety: 用户在word中使用的变量名
        :return: 数据库库中存储的变量名
        """
        for name_table, alias_list in column_alias_dict.items():
            if name_variety in alias_list:
                return name_table
        return extras_field_name

    columns_names = []
    columns_values = []
    extras_field_values = {}
    for k, v in info_dict.items():
        name = find_col_name_in_db(k)
        if name != extras_field_name:
            if name in parameters:
                if v.strip().endswith("%"):
                    v: str = v.replace("%", "").strip()
                    try:
                        v: float = float(v) / 100
                    except ValueError:
                        logger.warning(f"数值错误，错误字段为：{k}={v}，错误表格为：")
                        logger.warning(json.dumps(info_dict, ensure_ascii=False))
                        continue  # 出错了则略过该字段
                elif v.strip() in null_symbol:
                    continue  # 变量值为空则略过该字段
                else:
                    v = re.findall("([0-9\.]*)", v)[0]
            columns_names.append(name)
            columns_values.append(v)
        else:
            extras_field_values.update({k: v})
    if len(extras_field_values) > 0:
        columns_names.append("extras_field")
        columns_values.append(json.dumps(extras_field_values, ensure_ascii=False))
    return columns_names, columns_values


def get_update_time_of_table(table_name, or_create_time=False, cursor=None):
    """
    获取表的最后更新时间

    :param cursor: Cursor or Engine
    :param table_name:
    :param db: 表所属的db，不设置默认在cursor绑定的db中查找
    :param or_create_time: 当表的更新时间为None时，如果该参数为False,则返回None，否则返回表的创建时间，需要注意的是创建时间也可能是None
    :return: datetime.datetime类型的时间或None
    """
    # mysql的更新时间使用该方法是无法获得的，需要后期mysql版本更新看能否解决
    # sql = f"SELECT update_time FROM information_schema.tables WHERE table_name='{table_name}'"
    # fetch = exec_sql_script(cursor=cursor, sql_script=sql )
    # if len(fetch) == 0:
    #     return None
    # else:
    #     if or_create_time:
    #         return get_create_time_of_table(cursor, table_name)
    #     else:
    #         return fetch[0][0]
    # 暂时使用专门的modifyTable表记录每个表的更新时间
    _update_cursor(cursor)  # 更新模块变量last_cursor
    if not has_table("modifytime"):
        return None
    else:
        result = select_in_table("modifytime", condition_dict={"table": table_name}, result_col=['datetime'])
        if len(result) == 1:
            return result[0][0]
        elif len(result) == 0:
            return None
        else:
            logger.error(f"查找到多个表名匹配{table_name}的表，无法确定需要哪个表的更新时间")


def update_update_time_of_table(table_name: str = None, cursor: Cursor or Engine = None):
    """
    更新表的更新时间

    :param cursor:
    :param table_name:
    :return:
    """
    _update_cursor(cursor)  # 更新模块变量last_cursor
    if not has_table("modifyTime"):
        create_table("modifyTime", columns={"table": "varchar(50)", "datetime": "datetime"})
    update_time = datetime.datetime.now()
    insert_item_to_mysql("modifyTime", [table_name, update_time], replace=True)


def get_create_time_of_table(table_name=None, cursor: Cursor = None):
    """
    查询表的创建日期

    :param cursor:
    :param table_name:
    :return:
    """
    cursor = _update_cursor(cursor)  # 更新模块变量last_cursor
    sql = f"SELECT create_time FROM information_schema.tables WHERE table_name='{table_name}'"
    fetch = exec_sql_script(cursor=cursor, sql_script=sql)
    if len(fetch) == 0:
        return None
    else:
        return fetch[0][0]


# 测试的mysql和adminer版本分别为：8.0.19、4.7.6
if __name__ == '__main__':
    if not start_mysql_service():
        os.system("pause")

# 通过命令 pyinstaller -n mysql -i yangke2.ico -F mysql.py 生成exe文件
