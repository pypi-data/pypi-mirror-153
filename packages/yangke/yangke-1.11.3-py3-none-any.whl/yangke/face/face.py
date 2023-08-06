# 人脸识别工具
import numpy as np
import pandas as pd
import cv2
# import face_recognition
import os
from ..base import get_settings, getAbsPath, pic2ndarray, draw_element_on_pic, crop_pic
from PIL import Image, ImageDraw, ImageFont
import dlib
from ..common.config import logger, loggingTitleCall
import yangke.common.mysql as mysql
import datetime
import time
from DBUtils.PooledDB import PooledDB

detect_folder: str = None
save_folder: str = None

model_folder: str = None
shape_predictor_model: str = None  # 人脸68个特征点标定模型文件
cnn_face_detection_model: str = None  # cnn人脸识别模型文件
face_recognition_model: str = None  # 人脸特征值计算模型文件

font_color = None
font_size = None
font_file = None
line_color = None
line_thickness = None
font_style = None

db = 'face'
table_group = 'personGroup'  # 存储人员库信息的表名，非特殊情况不要修改
table_person = 'person'
table_eigen = 'eigen'
table_relation = 'person_rl_group'
table_group_columns = {
    "group_name": "varchar(30) not null",  # 必选字段，人员库的唯一标识符
    "creation_time": "datetime",  # datetime.datetime.now(), 人员库创建时间
    "description1": "varchar(500)",  #
    "description2": "varchar(100)",  #
    "description3": "varchar(100)",  #
    "description4": "varchar(100)",  #
    "description5": "varchar(100)",  #
    "tag": "varchar(100)",  #
}
table_person_columns = {
    "id": "varchar(30) not null",  # 必选字段，人员的唯一标识符
    "name": "varchar(10) not null",  # 姓名，可重复
    "group_name": "varchar(30) not null",  # 人员所属的人员库
    "creation_time": "datetime",
    "description": "varchar(200)",  # 人员描述
    "birthday": "date",  # 生日
    "gender": "varchar(6)",  # 性别
    "company": "varchar(100)",  # 公司
    "position": "varchar(100)",  # 职位
    "phone_number": "varchar(40)",  # 电话号码
    "comments": "TEXT",  # 备注
}
table_eigen_columns = {
    "id": "int auto_increment",  # 总的特征值id，表中唯一
    "name": "varchar(10) not null",  # 人员姓名
    "person_id": "varchar(30) not null",  # 人员id
    "eigen_id": "int not null",  # 人员的特征值id
    "creation_time": "datetime",  # 该人脸特征的创建时间
    "source": "varchar(100)",  # 人脸图片的存储路径，可能是url或本地保存的路径
}
for i in range(1, 129):
    table_eigen_columns['eigen_{}'.format(i)] = "float not null"

detector_default: dlib.fhog_object_detector = None  # 【人脸定位】引擎
detector_cnn: dlib.cnn_face_detection_model_v1 = None  # 【人脸定位】引擎
shape_predictor: dlib.shape_predictor = None  # 特征点识别，68个人脸特征点，根据这68个点计算人脸特征值
face_recognition_engine: dlib.face_recognition_model_v1 = None  # 人脸特征值计算

connection_pool: PooledDB = None  # 连接池


# cursor = None
def close_conn_cursor(conn, cursor):
    cursor.close()
    conn.close()


class Group:
    """
    人员库类
    """

    def __init__(self, group_name: str = None, creation_time=None,
                 description: list = None, tag=None):
        """
        使用指定参数初始化人员库，该方法只会初始化得到一个人员库对象，不会保存到mysql中。
        也可以不指定参数进行初始化，在获得Group对象后调用对应相关方法完成操作，如Group().create_group(...)以保存到数据库中
        :param group_name: 人员库名称，如test
        :param description: 人员库的描述信息
        :param tag: 人员库的备注信息
        :type creation_time: 人员库的创建时间，不需要设置，系统自动生成
        """
        self.group_name = group_name  # 人员库名
        self.description = description  # 人员库的描述信息列表
        self.tag = tag  # 人员库的备注信息
        self.creation_time = creation_time or str(datetime.datetime.now())
        # 如果要实现单人员多库存在，需要修改table_group即'personGroup'表结构，添加人员列，每个人员入库时都要添加记录

    def create_group(self, group_name: str, description=None, tag=None):
        """
        新建人员库

        :param group_name: 人员库名称，[1,60]个字符，可修改，不可重复。
        :param description:
        :param tag:
        """
        self.group_name = group_name  # 人员库名称
        self.description = description
        self.tag = tag
        conn = connection_pool.connection()
        cursor = conn.cursor()
        if mysql.exists_in_table(cursor, table_name=table_group, col_name='group_name', value=group_name):
            info = "已经存在名为 {} 的人员库".format(group_name)
            logger.warning(info)
            close_conn_cursor(conn, cursor)
            return False, info
        values = [group_name, self.creation_time]
        if description is not None:
            assert isinstance(description, list), "description必须是列表格式"
            while len(description) < 5:
                description.append("")
            for index in range(5):
                values.append(description[index] or "")
        else:
            values.extend([None, None, None, None, None])
        values.append(tag)
        # 这里重复插入，即使设置ignore=True，仍然会有警告，但不影响运行结果
        mysql.insert_item_to_mysql(cursor, table_group, values=values,
                                   col_names=list(table_group_columns.keys()),
                                   ignore=True)
        info = "创建人员库成功"
        close_conn_cursor(conn, cursor)
        return True, info

    @staticmethod
    def get_group(group_name):
        """
        通过groupid获得数据库中对应的group对象
        :param group_name:
        :return:
        """
        conn = connection_pool.connection()
        cursor = conn.cursor()
        exists, fetch = mysql.exists_in_table(cursor, table_group, col_name='group_name', value=group_name,
                                              return_result=True)
        if exists:
            fetch = fetch[0]
            group_name = fetch[0]
            creation_time = fetch[1]
            description = list(fetch[2:7])
            tag = fetch[7]
            group = Group(group_name, description=description, tag=tag,
                          creation_time=creation_time)
            close_conn_cursor(conn, cursor)
            return group
        else:
            logger.debug("人员库 {} 不存在")
            close_conn_cursor(conn, cursor)  # 测试发现可以不关
            return None

    @staticmethod
    def modify_group(group_name: str, descriptions: list = None, tag=None):
        """
        修改人员库信息

        :param group_name: 不能为空
        :param descriptions:
        :param tag:
        :return:
        """
        if group_name is None or group_name.strip() == "":
            return {"success": False, "info": "人员库名为空"}
        descriptions = descriptions or [None, None, None, None, None]
        conn = connection_pool.connection()
        cursor = conn.cursor()
        exists, fetch = mysql.exists_in_table(cursor, table_group, col_name='group_name',
                                              value=group_name, return_result=True)
        if not exists:
            info = "尝试修改的人员库不存在：{}".format(group_name)
            logger.debug(info)
            close_conn_cursor(conn, cursor)
            return {"success": False, "info": info}
        else:
            values = descriptions
            values.append(tag)
            columns = list(table_group_columns.keys())[-6:]
            update_dict = {}
            for k, v in zip(columns, values):
                update_dict[k] = v

            # 暂时使用插入语句更新人员库，后面添加更新方法
            mysql.update_in_table(cursor, table_group, condition_dict={'group_name': group_name},
                                  update_dict=update_dict)
        close_conn_cursor(conn, cursor)
        return {"success": True, "info": "修改成功"}

    @staticmethod
    def get_group_list(offset=0, limit=10) -> list:
        """
        获取人员库列表

        :param offset:
        :param limit:
        :return:
        """
        offset = int(offset or 0)
        limit = int(limit or 10)
        if offset != 0:
            logger.debug("当前不支持设置偏移{}".format(offset))
        conn = connection_pool.connection()
        cursor = conn.cursor()
        results = mysql.exec_sql_script(cursor, "select * from {} limit {}".format(table_group, limit))
        if len(results) == 0:
            close_conn_cursor(conn, cursor)
            return []
        else:
            group_list = []
            for result in results:
                group = Group(result[0], result[1], result[-6:-1], result[-1])

                group_list.append(group)
        close_conn_cursor(conn, cursor)
        return group_list

    @staticmethod
    def delete_group(group_name):
        """
        删除人员库，人员库中的人员也会一并删除

        :param group_name:
        :return:
        """
        conn = connection_pool.connection()
        cursor = conn.cursor()
        exists = mysql.exists_in_table(cursor, table_group, col_name='group_name', value=group_name,
                                       return_result=False)
        if exists:
            mysql.delete_in_table(cursor, table_group, col_name='group_name', value=group_name)
        else:
            info = "尝试删除的人员库不存在：{}".format(group_name)
            logger.debug("尝试删除的人员库不存在：{}".format(group_name))
            return {"success": False, "info": info}
        return {"success": True, "info": "删除人员库成功"}

    def to_dict(self):
        desc = self.description
        return {"group_name": self.group_name, 'PersonExDescriptions': desc, "tag": self.tag,
                "creation_time": self.creation_time}


@loggingTitleCall(title="初始化人脸库")
def init_image_lib():
    """
    初始化settings.yaml文件中的各项配置参数；
    初始化人脸数据，将其加载到内存中，以便后续进行匹配；

    :return:
    """
    setting1 = get_settings()
    settings = setting1.get('face')
    mysql_settings = setting1.get('mysql')
    del setting1
    global model_folder, shape_predictor_model, cnn_face_detection_model, face_recognition_model
    model_folder = settings.get('model').get('directory') or os.getcwd()
    shape_predictor_model = settings.get('model').get('shapePredictor') or "shape_predictor_5_face_landmarks.dat"
    cnn_face_detection_model = settings.get('model').get('cnnFaceDetection') or "mmod_human_face_detector.dat"
    face_recognition_model = settings.get('model').get(
        'faceRecognization') or "dlib_face_recognition_resnet_model_v1.dat"
    mysql_host = mysql_settings.get('service') or mysql_settings.get('docker') or 'localhost'
    mysql_port = mysql_settings.get('port') or 3306
    mysql_user = mysql_settings.get('user')
    mysql_passwd = mysql_settings.get('passwd')
    mysql_db = mysql_settings.get('db') or 'face'

    # ----------------------------  加载人脸识别引擎 -----------------------------------------
    global shape_predictor, detector_default, detector_cnn, face_recognition_engine
    detector_default = dlib.get_frontal_face_detector()  # 人脸检测，人脸位置

    model_path = getAbsPath(model_folder, cnn_face_detection_model)
    detector_cnn = dlib.cnn_face_detection_model_v1(model_path)  # 人脸检测，人脸位置，功能同detector_default，但准确度更高，速度慢

    face_recognition_file = getAbsPath(model_folder, face_recognition_model)
    face_recognition_engine = dlib.face_recognition_model_v1(face_recognition_file)  # 【人脸特征值计算】即传统意义上的【人脸识别】

    predictor_path = getAbsPath(model_folder, shape_predictor_model)
    shape_predictor = dlib.shape_predictor(predictor_path)  # 人脸检测，人脸位置
    # ----------------------------  加载人脸识别引擎 -----------------------------------------

    global detect_folder, save_folder
    # lib_folder = settings.get('libFolder') or os.path.abspath("./image")
    detect_folder = settings.get('detectFolder') or os.path.abspath("./image")
    save_folder = settings.get('saveFolder') or os.path.abspath("./image")
    if not os.path.exists(detect_folder):
        os.makedirs(detect_folder)
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # if lib_folder is None:
    #     lib_folder = os.path.abspath("image")
    # else:
    #     lib_folder = os.path.abspath(lib_folder)

    draw_args = settings.get('draw') or {}
    font_args = draw_args.get('font') or {}
    global font_color, font_size, font_file, font_style
    font_color = font_args.get('color') or "255,255,255"
    font_color = tuple([int(rgb) for rgb in font_color.split(",")])
    font_size = int(font_args.get('size') or 20)
    font_ttc = font_args.get('ttc')
    # 字体的格式
    font_file = os.path.abspath(font_ttc) if font_ttc is not None else None
    font_style = ImageFont.truetype(font_file, size=font_size, encoding="utf-8") if font_file is not None else None
    global line_thickness, line_color
    line_args = draw_args.get('line') or {}
    line_color = line_args.get('color') or "255,255,255"
    line_thickness = line_args.get('thickness') or 1

    if not mysql.mysql_available(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_passwd,
                                 db=mysql_db):  # 如果服务不可用，尝试启动服务
        if mysql_host in ['localhost', '127.0.0.1']:  # 如果连接的是本地mysql，就尝试启动本地mysql服务
            result = mysql.start_mysql_service()
            if not result:  # 如果启动失败
                logger.error("mysql服务不可用，请检查配置或手动启动mysql服务")
        else:
            logger.error("mysql服务不可用，请检查配置或手动启动mysql服务")

    # ========================创建项目所需要的数据库表=================================
    # 共有四张表，人员库表、人员表、人员库与人员关系表、人脸表。
    # 其中人脸表从属于人员表，人员表从属于人员库表
    # 人员库与人与关系表，从属于人员表和人员库表，维护了人员与人员库的多对多关系
    # 删除人员库中某条记录，则所有该库中的人员、关系、人脸都会被删除，即会影响四张表
    # 删除人员表中某条记录，则该人员的关系、人脸会被删除，即影响三张表
    # 删除关系和人脸，只会影响单独一张表，这些是由mysql自动维护的。
    global connection_pool
    connection_pool = mysql.connect_mysql(db='face', return_type="pool")  # 如果db='face'不存在，则需要root权限创建db
    if connection_pool is None:  # 如果连接失败，返回None
        logger.error("mysql服务连接失败")
        return False
    conn = connection_pool.connection()
    cursor = conn.cursor()
    if cursor is None:
        logger.error("mysql服务连接失败")
    else:
        if not mysql.has_table(table_group, cursor):
            mysql.create_table(cursor=cursor, table_name=table_group, columns=table_group_columns, primary=0)
            logger.debug("创建人员库表")
        if not mysql.has_table(table_person, cursor):
            mysql.create_table(table_name=table_person, columns=table_person_columns, primary=[0],
                               foreign="FOREIGN KEY (`group_name`) REFERENCES {} (`group_name`)"
                                       " ON DELETE CASCADE ON UPDATE CASCADE".format(table_group))
            logger.debug("创建人员表")
        if not mysql.has_table(table_eigen):
            mysql.create_table(table_eigen, table_eigen_columns, primary=0,
                               foreign="FOREIGN KEY (person_id) REFERENCES {}(id) "
                                       "ON DELETE CASCADE ON UPDATE CASCADE".format(table_person)
                               )
            logger.debug("创建人脸表")
        if not mysql.has_table(table_relation, cursor):
            sql = "create table {}(" \
                  "id int primary key auto_increment, " \
                  "group_name varchar(30) not null, " \
                  "person_id varchar(30) not null, " \
                  "foreign key(group_name) references {}(group_name) ON DELETE CASCADE ON UPDATE CASCADE, " \
                  "foreign key(person_id) references {}(id) ON DELETE CASCADE ON UPDATE CASCADE, " \
                  "unique key(group_name,person_id));".format(table_relation, table_group, table_person)
            mysql.exec_sql_script(cursor, sql, commit=True)
            logger.debug("创建人员库与人员关系表")
        cursor.close()  # 使用连接池，并不是真正的关闭连接，而是把连接放回到连接池中
        conn.close()  # 使用连接池，并不是真正的关闭连接，而是把连接放回到连接池中
        # ========================创建项目所需要的数据库表=================================
    return True


class Person:
    """
    人员库，包括mysql中人员表格以及具体人员信息的管理方法
    """

    def __init__(self, person_id=None, person_name=None, group_name=None, creation_time=None, birthday=None,
                 gender=None, company=None, position=None, phone_number=None, comments=None, **kwargs):
        """
        使用指定参数构建一个人员对象，不会存储到数据库

        :param group_name: 人员
        :param column_person:
        :param cursor:
        """
        self.group_name = group_name  # 归属的人员库名称，该人员库信息在
        self.person_id = person_id
        self.person_name = person_name
        self.creation_time = creation_time
        self.birthday = birthday
        self.gender = gender
        self.company = company
        self.position = position
        self.phone_number = phone_number
        self.comments = comments
        self.description: dict = kwargs

    def create_person(self, group_name, person_id, person_name, pic, birthday=None,
                      gender=0, company=None, position=None, phone_number=None, comments=None,
                      unique_person_control: int = 0, quality_control: int = 0, **kwargs):
        """
        使用指定参数创建一个人员，并存储到人脸数据库

        :param quality_control: [0-4]，取值越大，要求越高。图片质量控制。若图片质量不满足要求，则返回结果中会提示图片质量检测不符要求。
        :param unique_person_control: 此参数用于控制判断图片包含的人脸，是否在人员库中已有疑似的同一人。如果判断为已有相同人在人员库中，则不会创建新的人员，返回疑似同一人的人员信息。
        :param group_name:
        :param person_id:
        :param person_name:
        :param pic:
        :param birthday:
        :param gender: 取值范围0， 1， 2; 0-未知， 1-男， 2-女
        :param company:
        :param position:
        :param phone_number:
        :param comments:
        :param kwargs:
        :return:
        """
        # 校验输入数据是否合法
        try:
            unique_person_control = unique_person_control or 0
            quality_control = quality_control or 0
            gender = gender or 0
            birthday = birthday or "9999-01-01"
            unique_person_control, quality_control = int(unique_person_control), int(quality_control)
            assert (int(gender) in [0, 1, 2]) and (unique_person_control in range(5)) and (
                    quality_control in range(5))
        except (AssertionError or ValueError) as e:
            info = "传入的参数类型有错误，请检查！"
            logger.debug(info)
            return {"success": False, "info": info}
        # 调用初始化方法完成初始化，这里主要更新了self.table_person
        self.__init__(group_name=group_name, person_id=person_id, person_name=person_name,
                      creation_time=str(datetime.datetime.now()), birthday=birthday, gender=gender,
                      company=company, position=position, phone_number=phone_number, comments=comments, **kwargs)
        # 将已知的人员信息插入人员表
        values = [self.person_id, self.person_name, self.group_name, self.creation_time, str(self.description),
                  self.birthday, self.gender,
                  self.company, self.position, self.phone_number, self.comments]
        conn = connection_pool.connection()
        cursor = conn.cursor()
        if mysql.exists_in_table(cursor, table_group, col_name='group_name', value=group_name):
            if mysql.exists_in_table(cursor, table_person, col_name='id',
                                     value=person_id):
                if mysql.exists_in_table(cursor, table_relation, condition_dict={'group_name': group_name,
                                                                                 'person_id': person_id}):
                    info = "人员存在且已在指定的人员库中"
                    logger.debug(info)
                    return {"success": False, "info": info}
                else:  # 创建的人员库和人员都存在的话，则直接插入库与人员的对应关系即可
                    mysql.insert_item_to_mysql(cursor, table_relation, values=[group_name, person_id],
                                               col_names=['group_name', 'person_id'], ignore=True)  # 关系表中插入关系
                    return {"success": True, 'info': '人员 {} 已添加到人员库 {} 中'.format(person_id, group_name)}
            mysql.insert_item_to_mysql(cursor, table_person, values=values, col_names=list(table_person_columns),
                                       ignore=True)  # 人员表中插入人员
            mysql.insert_item_to_mysql(cursor, table_relation, values=[group_name, person_id],
                                       col_names=['group_name', 'person_id'], ignore=True)  # 关系表中插入关系
        else:
            info = "指定的人员库不存在，请先创建人员所属的人员库"
            logger.debug(info)
            return {"success": False, "info": info}
        # 如果图片不为空，提取图片特征插入人脸特征表
        info = None
        if pic is not None:
            face_match_threshold = unique_person_control * 20
            result_dict = Face(cursor=cursor).create_face(person_id=person_id, pic=pic,
                                                          face_match_threshold=face_match_threshold,
                                                          quality_control=quality_control)
        else:
            result_dict = {"success": True}
        return result_dict

    @staticmethod
    def delete_person_from_group(person_id, group_name):
        """
        从某人员库中删除人员，此操作仅影响该人员库。若该人员仅存在于指定的人员库中，该人员将被删除，其所有的人脸信息也将被删除。

        :param person_id:
        :param group_name:
        :return:
        """

        if person_id is None or group_name is None:
            return {"success": False, "info": "必须同时提供人员库名和人员Id"}
        # 查询人员是否存在
        conn = connection_pool.connection()
        cursor = conn.cursor()
        if not mysql.exists_in_table(cursor, table_person, col_name='id', value=person_id):
            return {"success": False, "info": "尝试删除的人员不存在"}
        if not mysql.exists_in_table(cursor, table_group, col_name='group_name', value=group_name):
            return {"success": False, "info": "指定的人员库不存在"}
        mysql.delete_in_table(cursor, table_relation, **{"group_name": group_name, "person_id": person_id})

        # 判断删除的人员是否还属于其他数据库，如果不属于，则删除该人员
        if not mysql.exists_in_table(cursor, table_relation, col_name='person_id', value=person_id):
            Person.delete_person(person_id)

        return {"success": True, "info": "从人员库 {} 中删除id为 {} 的人员成功".format(group_name, person_id)}

    @staticmethod
    def delete_person(person_id):
        """
        删除人员信息。此操作会导致所有人员库均删除此人员。同时，该人员的所有人脸信息将被删除。

        :param person_id:
        :return:
        """
        # 从
        if person_id is None:
            info = "请输入人员id"
            logger.debug(info)
            return {"success": False, "info": info}
        conn = connection_pool.connection()
        cursor = conn.cursor()
        if mysql.exists_in_table(cursor, table_person, col_name='id', value=person_id,
                                 return_result=False):
            mysql.delete_in_table(cursor, table_person, col_name='id', value=person_id)
            return {"success": True, "info": "删除人员成功"}
        else:
            return {"success": False, "info": "尝试删除的人员不存在"}

    def get_person_list(self, group_name, offset=0, limit=10):
        """
        获取指定人员库中的人员列表

        :param group_name:人员库名
        :param offset:起始序号，默认值为0
        :param limit:返回数量，默认值为10，最大值为1000
        :return:
        """
        offset = offset or 0
        limit = limit or 10
        conn = connection_pool.connection()
        cursor = conn.cursor()
        if not mysql.exists_in_table(cursor, table_group, 'group_name', group_name):
            return True, "指定的人员库不存在"

        # 从关系表中查找指定的人员库数据行
        exist, fetchall = mysql.exists_in_table(cursor, table_relation, col_name='group_name', value=group_name,
                                                return_result=True)
        if not exist:
            return True, []

        person_ids = [record[2] for record in fetchall]  # 拿到人员库中所有的人员id

        person_list = []
        for id in person_ids:
            # 从人员表获得人员对象
            exist, fetchall = mysql.exists_in_table(cursor, table_person, col_name='id', value=id, return_result=True)
            record = fetchall[0]
            import json5
            desc = json5.loads(record[4])
            person = Person(record[0], record[1], record[2], record[3], birthday=record[5], gender=record[6],
                            company=record[7], position=record[8], phone_number=record[9], comments=record[10],
                            **dict(desc))
            person_list.append(person)
        return True, person_list

    def to_dict(self):
        """
        将当前Group示例转换为dict格式
        :return:
        """
        return {
            "person_id": self.person_id,
            "person_name": self.person_name,
            "group_name": self.group_name,
            "creation_time": self.creation_time,
            "birthday": self.birthday,
            "gender": self.gender,
            "company": self.company,
            "position": self.position,
            "phone_number": self.phone_number,
            "comments": self.comments,
        }

    @staticmethod
    def get_person_list_num(group_name):
        """
        获取指定人员库中人员数量

        :param group_name:
        :return:
        """
        info = "暂不支持该方法，可以使用替代方法get_person_list"
        logger.debug(info)
        return False, info

    @staticmethod
    def get_person_base_info(person_id):
        """
        获取指定人员的信息，包括姓名、性别、人脸等

        :param person_id:
        :return:
        """
        conn = connection_pool.connection()
        cursor = conn.cursor()
        exist, fetchall = mysql.exists_in_table(cursor, table_person, col_name='id', value=person_id,
                                                return_result=True)
        if not exist:
            return True, "没有id为{}的人员".format(person_id)
        record = fetchall[0]
        import json5
        desc = json5.loads(record[4])
        return True, Person(record[0], record[1], record[2], record[3], birthday=record[5], gender=record[6],
                            company=record[7], position=record[8], phone_number=record[9], comments=record[10],
                            **dict(desc))

    @staticmethod
    def modify_person_base_info(person_id, person_name, gender: int):
        conn = connection_pool.connection()
        cursor = conn.cursor()
        exist = mysql.exists_in_table(cursor, table_person, col_name='id', value=person_id)
        if not exist:
            return True, "没有id为{}的人员".format(person_id)
        update_dict = {}
        if person_name is not None or person_name.strip() != "":
            update_dict['name'] = person_name
        if gender is not None and gender != 0:
            update_dict['gender'] = gender
        if len(update_dict) == 0:
            return False, "修改内容为空"
        mysql.update_in_table(cursor, table_person, condition_dict={"id": person_id},
                              update_dict=update_dict)
        return True, "修改人员 {} 信息成功".format(person_id)

    @staticmethod
    def get_person_group_info(person_id, offset=0, limit=10):
        """
        获取人员所属的人员库

        :param person_id:
        :param offset:
        :param limit:
        :return:
        """
        if person_id is None or person_id.strip() == "":
            return False, "人员Id为空"
        try:
            offset = int(offset or 0)
            limit = int(limit or 0)
        except ValueError:
            return False, "参数非法"
        conn = connection_pool.connection()
        cursor = conn.cursor()
        fetchall = mysql.select_in_table(cursor, table_relation, condition_dict={'person_id': person_id},
                                         result_col=['group_name'], limit=limit, offset=offset)
        if fetchall is None or len(fetchall) == 0:
            return True, "人员 {} 不属于任何人员库".format(person_id)
        else:
            group_list = []
            for record in fetchall:
                group_list.append(Group.get_group(record[0]))
            return True, group_list


class Face:
    """
    人脸识别的mysql数据库操作类
    """

    def __init__(self, person_id=None, pic=None, g_id=None, eigen_id=None, creation_time=None, person_name=None,
                 cursor=None):
        """
        初始化人员库以及人脸特征库，如果需要新建人员库和人脸特征库，需要确保两个库对应的表名不和已有表名重复，否则可能覆盖
        已有数据。

        因为两张表是主从关系，使用已有人员库和人脸特征库时，确保配对使用。

        :param person_name: 人员姓名
        :param person_id: 人员id
        :param eigen_id: 人员特征值id
        :param creation_time: 当前特征值的创建时间，系统自动生成该参数
        :param pic: 人脸图片
        :param cursor: 数据库操作游标
        """
        # 创建时需要的参数
        self.person_id = person_id
        self.pic = pic
        # 获取Face对象时额外传入的参数，用于返回给外部程序
        self.person_name = person_name
        self.eigen_id = eigen_id
        self.id = g_id
        self.creation_time = creation_time

    def add_face_from_folder(self, folder_path):
        """
        从文件夹中加载图片的人脸特征。
        文件名命名方式为 <人员姓名>-<idx>.<后缀名>，如果同一个人存在多张图片，则idx递加命名即可。
        如果多个人同名，则设置single_eigen为True，从而将不同图片认为是不同的人，无论name是否相同。

        :param folder_path: 文件夹路径
        :param single_eigen: 是否每个人一个特征值，如果为False，则folder下同名的人物被认为是同一个人
        :return:
        """
        # 遍历face_lib文件夹，逐个生成人脸特征编码
        # files = []
        for root, dirs, sub_files in os.walk(folder_path):
            for file in sub_files:
                file = os.path.join(root, file)
                name, ext = os.path.splitext(os.path.basename(file))
                if ext.lower() in ['.jpg', '.png', '.jpeg']:
                    logger.debug("加载 '{}' 到人脸库...".format(file))
                    name = name.split("-")[0]
                    # 如果存在同名人物，则查询到人物id，不需要插入人员数据，只需要插入特征值数据
                    self.create_face(file, person_id=name)

    def create_face(self, pic, person_id, face_match_threshold=60, quality_control: int = 0):
        """
        添加人脸到数据库

        腾讯云的创建人员与添加人脸照片都可以使用该方法

        :return: 返回（人脸:Face，创建提示信息:str）
        """
        # 检查输入参数是否合法
        return_dict = {}
        if quality_control > 0:
            info = "暂不支持图片质量控制"
            logger.warning(info)
            return_dict['success'] = False
            return_dict['info'] = info
            return_dict['ret_code'] = -1601
            return return_dict
        if person_id is None or person_id == "":
            info = "人员id为空，请检查！"
            logger.warning(info)
            return_dict['success'] = False
            return_dict['info'] = info
            return_dict['ret_code'] = -1001
            return return_dict
        # 查看人脸所属的人员是否存在，存在或获取人员姓名
        conn = connection_pool.connection()
        cursor = conn.cursor()
        exist, person = mysql.exists_in_table(cursor, table_person, col_name='id', value=person_id,
                                              return_result=True)
        if exist:  # person_id是人员的唯一标识符，如果存在，就对该人员进行操作
            name = person[0][1]
            # 判断person_id在eigen表中是否存在，存在则依次递增获得eigen_id的值
            exist, person_eigens = mysql.exists_in_table(cursor, table_eigen, col_name='person_id',
                                                         value=person_id,
                                                         return_result=True)
            eigen_id = len(person_eigens) + 1  # mysql的自增键值从1开始，这里与mysql默认保持一致

        else:
            # 先在人员表中插入新的人员
            info = "人脸所属的人员id不存在，请检查!"
            return_dict['success'] = False
            return_dict['info'] = info
            return_dict['ret_code'] = -1001
            return return_dict

        # 获取本地保存路径
        global save_folder
        pic_file_name = "face_{}_{}.png".format(person_id, eigen_id)
        pic_file_name = os.path.join(save_folder, pic_file_name)
        eigen_value, face = self.calculate_face_eigenvalue(pic, pic_file_name)  # 该操作比较耗时，上面代码不返回再调用
        if eigen_value is None:
            return {"success": False, "ret_code": -1102, "info": "图片解码失败"}
        if len(eigen_value) == 0:
            info = "未检测到人脸"
            logger.debug(info)
            return {"success": False, "ret_code": -1101, "info": info}
        if len(eigen_value) > 1:
            info = "在图片中检测到了多张人脸，这在人脸入库时时不允许的，跳过该图片"
            logger.warning(info)
            return {"success": False, "ret_code": -1000, "info": info}  # 返回
        eigen_value = eigen_value[0]  # dlib库得到的特征值序列是Vector类型
        eigen_value = list(eigen_value)  # 这里转为list类型
        face = face[0]
        if eigen_id > 1:  # 如果当前人脸特征库中已经存在人脸特征记录，则判断插入数据是否重复
            records = self.get_eigens_by_person_id(person_id)  # 获取已存在特征值
            for eigen_record in records:
                suc, info, distance, score = self.compare_face(eigen_value, eigen_record)
                if distance < 0.0001:  # 如果已有特征值记录和当前图片的特征值相同
                    info = "已有当前人员（姓名：{}，人员id：{}）" \
                           "的当前人脸特征记录（特征id{}）,跳过该插入特征操作！".format(name, person_id, eigen_id)
                    logger.debug(info)
                    return {"success": False, "info": info, "ret_code": -1603}
                if score < face_match_threshold:
                    info = "插入的图片中，人脸特征与已有人脸特征差异过大，很可能不是同一人，拒绝添加该人脸"
                    logger.debug(info)
                    return {"success": False, "info": info, "ret_code": -1604}
            # 当前图片的特征值添加到对应person_id对应的人员下
        values = [name, person_id, eigen_id, str(datetime.datetime.now()), pic_file_name]
        values.extend(list(eigen_value))
        mysql.insert_item_to_mysql(cursor, table_eigen,
                                   values=values,
                                   col_names=list(table_eigen_columns)[1:])
        id = mysql.exec_sql_script(cursor, 'SELECT LAST_INSERT_ID();')[0][0]
        return_dict = {"success": True, "id": id, "ret_code": 0, "face_rect_left": face.left(),
                       "face_rect_top": face.top(),
                       "face_rect_right": face.right(), "face_rect_bottom": face.bottom()}
        return return_dict

    @staticmethod
    def delete_face(face_id):
        """
        删除人脸

        :param face_id:
        :return:
        """
        conn = connection_pool.connection()
        cursor = conn.cursor()
        if mysql.exists_in_table(cursor, table_eigen, col_name='id', value=face_id):
            mysql.delete_in_table(cursor, table_eigen, col_name='id', value=face_id)
            return True, '删除成功'
        else:
            return True, '人脸id不存在'

    def detect_face(self, pic, max_face_num=0, min_face_size=34, need_face_attributes=0,
                    need_quality_detection=0):
        """
        检测给定图片中的人脸（Face）的位置、相应的面部属性和人脸质量信息，位置包括 (x，y，w，h)，面部属性包括
        性别（gender）、年龄（age）、表情（expression）、魅力（beauty）、眼镜（glass）、发型（hair）、口罩
        （mask）和姿态 (pitch，roll，yaw)，人脸质量信息包括整体质量分（score）、模糊分（sharpness）、光照分
        （brightness）和五官遮挡分（completeness）。

        其中，人脸质量信息主要用于评价输入的人脸图片的质量。在使用人脸识别服务时，建议您对输入的人脸图片进行
        质量检测，提升后续业务处理的效果。

        :param pic: 图片的base64编码字符串或者url
        :param max_face_num: 最多处理的人脸数目。默认值为1，最大值为120
        :param min_face_size: 人脸长和宽的最小尺寸，单位为像素。默认为34。建议不低于34。
        :param need_face_attributes: 是否需要返回人脸属性信息（FaceAttributesInfo）。0 为不需要返回，1 为需要返回。默认为 0。
        :param need_quality_detection: 是否开启质量检测。0 为关闭，1 为开启。默认为 0。
        :return: <请求的图片宽度><请求的图片高度><人脸信息列表。包含人脸坐标信息、属性信息（若需要）、质量分信息（若需要）>
        """
        # eigenvalues, faces = calculate_face_eigenvalue(pic=pic)
        # 这个是获得通用的人脸面部信息，不是识别图片是谁
        img, info = pic2ndarray(pic)
        if img is None:
            return {"success": False, "info": info}
        rects, _, img_list = get_face_rect(pic=img, align=False, save_to=False)
        faces = []
        for rect, sub_img in zip(rects, img_list):
            gender = self.predict_gender(sub_img)
            age = self.predict_age(sub_img)
            expression = self.predict_expression(sub_img)
            beauty = self.predict_beauty(sub_img)
            glass = self.predict_glasses(sub_img)
            mask = self.predict_mask(sub_img)
            hair = self.predict_hair(sub_img)

            face_rect = {"x": rect[0], "y": rect[1], "width": rect[2] - rect[0], "height": rect[3] - rect[1]}
            face_info = {"gender": gender, "age": age, "expression": expression, "beauty": beauty,
                         "glass": glass, "mask": mask, "hair": hair}
            faces.append({"face_rect": face_rect, "face_info": face_info})

        info = "暂不支持识别图片中人员性别、年龄、表情、魅力、眼镜、发型、口罩、和姿态"
        logger.debug(info)
        result = {"success": False, 'info': info, "faces": faces}
        return result

    @staticmethod
    def analyze_face(img, mode=0):
        """
        对请求图片进行五官定位（也称人脸关键点定位），计算构成人脸轮廓的 68 个点，包括眉毛（左右各 8 点）、眼睛（左右各 8 点）、鼻子（13 点）、嘴巴（22 点）、脸型轮廓（21 点）、眼珠[或瞳孔]（2点）

        :param img:
        :param mode: 0 为检测所有出现的人脸， 1 为检测面积最大的人脸。
        :return:
        """
        img, info = pic2ndarray(img, mode='RGB')  # 有些图片有alpha通道，而dlib不支持，这里要丢弃掉alpha通道
        if img is None:
            return None, info
        width, height = img.shape[0], img.shape[1]
        face_shape_set = []
        dets = detector_default(img, 1)
        logger.debug("Number of faces detected: {}".format(len(dets)))

        for index, face in enumerate(dets):
            logger.debug(
                'face {}; left {}; top {}; right {}; bottom {}'.format(index, face.left(), face.top(), face.right(),
                                                                       face.bottom()))
            face_points = []
            shape = shape_predictor(img, face)  # 提取68个特征点
            for pt in shape.parts():
                pt_pos = (pt.x, pt.y)
                face_points.append(pt_pos)
                # cv2.circle(img, pt_pos, 2, (255, 0, 0), 1)
            face_shape_set.append({"face_index": index, "face_points": face_points})
        return {"success": True, "width": width, "height": height, "face_shape_set": face_shape_set}

    @staticmethod
    def get_ids_by_person_id(person_id):
        """
        根据人员ID查找该人员已有的人脸ID

        :param person_id:
        :return: Suc, id:list
        """
        conn = connection_pool.connection()
        cursor = conn.cursor()
        exist, fetchall = mysql.exists_in_table(cursor, table_name=table_eigen, col_name='person_id',
                                                value=person_id, return_result=True)
        if not exist:
            if mysql.exists_in_table(cursor, table_person, col_name='id', value=person_id):
                return True, "人员 {} 尚为添加人脸".format(person_id)
            else:
                return True, '人员 {} 不存在'.format(person_id)
        records = []
        for record in fetchall:
            records.append(list(record)[0])
        return True, records

    @staticmethod
    def get_eigens_by_person_id(person_id):
        """
        从人脸特征库中获得对应姓名的所有人脸特征值

        :param person_id:
        :return:
        """
        conn = connection_pool.connection()
        cursor = conn.cursor()
        exist, fetchall = mysql.exists_in_table(cursor, table_name=table_eigen, col_name='person_id',
                                                value=person_id, return_result=True)
        records = []
        if len(fetchall) == 0:
            return None
        for record in fetchall:
            records.append(np.asarray(list(record)[6:]))
        return records

    @staticmethod
    def _eigen_equal_(eigen1, eigen2):
        """
        判断两个人脸特征是否相同

        :param eigen1:
        :param eigen2:
        :return:
        """
        differ = np.max(np.asarray(eigen1) - np.asarray(eigen2))
        return False if differ > 0.001 else True

    @staticmethod
    def calculate_face_eigenvalue(pic, save_to: str = None, face_num: int = 0):
        """
        获取图片中人脸的 128维特征向量 的列表，每一个特征向量对应一张人脸

        :param pic: 人脸图像
        :param save_to: 如果需要保存人脸图片传入图片路径
        :param face_num: 计算的人脸数量，按照面积从大到小，如果取值为0则计算所有识别到的人脸特征值
        :return: 人脸特征值列表和人脸矩形列表
        """
        # _, _, face_pics = get_face_rect(pic, save_to_local=True)
        # 加载人脸识别中的【人脸定位】【五官定位】【人脸特征值计算】三个引擎
        if model_folder is None:
            init_image_lib()
        start = time.clock()
        detector = detector_default  # 【人脸定位】
        img, info = pic2ndarray(pic, save_to, mode='RGB')  # 有些图片有alpha通道，而dlib不支持，这里要丢弃掉alpha通道
        if img is None:
            return None, info

        dets = detector(img, 1)  # 人脸标定
        if len(dets) == 0:
            return None, "未检测到人脸"
        logger.debug("Number of faces detected: {}".format(len(dets)))
        eigenvalues = []
        faces = []
        faces_area = []

        # 按识别到的人脸面积大小进行排序
        for index, face in enumerate(dets):
            faces_area.append((face.right() - face.left()) * (face.bottom() - face.top()))  # 人脸矩形面积
        index_areas = sorted(enumerate([faces_area]), key=lambda x: x[1], reverse=True)  # 使用原索引对faces_area列表排序
        indexes = [index for index, _ in index_areas]
        if face_num < 1 or face_num > len(indexes):
            pass
        else:
            indexes = indexes[:face_num]
        for index in indexes:
            face = dets[index]
            logger.debug(
                'face {}; left {}; top {}; right {}; bottom {}'.format(index, face.left(), face.top(), face.right(),
                                                                       face.bottom()))
            faces.append(face)
            shape = shape_predictor(img, face)  # 提取68个特征点
            # for i, pt in enumerate(shape.parts()):
            #     pt_pos = (pt.x, pt.y)
            #     cv2.circle(img, pt_pos, 2, (255, 0, 0), 1)
            face_descriptor = face_recognition_engine.compute_face_descriptor(img, shape)  # 计算人脸的128维的向量
            # # =====================================对齐人脸进行特征提取================================================
            # logger.debug("Computing descriptor on aligned image ..")
            # # Let's generate the aligned image using get_face_chip
            # face_chip = dlib.get_face_chip(img, shape)
            # # Now we simply pass this chip (aligned image) to the api
            # face_descriptor_from_prealigned_image = face_recognition_engine.compute_face_descriptor(face_chip)
            # # print(face_descriptor_from_prealigned_image)
            # # =======================================================================================================
            # differ = np.max(np.asarray(face_descriptor_from_prealigned_image) - np.asarray(face_descriptor))
            # logger.debug("对人脸进行对齐后获得的特征值与不进行对齐操作获得的特征值差值为{}".format(differ))
            # if differ > 0:
            #     logger.warning("发现对齐操作会影响人脸的特征值")
            eigenvalues.append(np.asarray(face_descriptor))
        end = time.clock()
        logger.debug("人脸预测耗时：{} 秒".format(end - start))
        return eigenvalues, faces

    @staticmethod
    def predict_gender(pic):
        return "unknown"

    @staticmethod
    def predict_age(pic):
        return "unknown"

    @staticmethod
    def predict_expression(pic):
        return "unknown"

    @staticmethod
    def predict_beauty(pic):
        return "unknown"

    @staticmethod
    def predict_glasses(pic):
        return "unknown"

    @staticmethod
    def predict_mask(pic):
        return "unknown"

    @staticmethod
    def predict_hair(pic):
        return "unknown"

    def compare_face(self, pic_or_eigen1, pic_or_eigen2, quality_control: int = 0):
        """
        对比人脸

        :param pic_or_eigen1: 图片或者人脸特征值，对比的两张人脸参数格式必须一致，图片格式支持本地文件，url，特征值请以list格式传入
        :param pic_or_eigen2: 图片或者人脸特征值，对比的两张人脸参数格式必须一致
        :param quality_control:
        :return: suc, info, distance, score，人连特征欧式距离和相似度得分，距离越小越接近，相似度得分越大越接近
        """

        if quality_control:
            logger.debug("目前不支持图片质量控制")
        if isinstance(pic_or_eigen1, str):
            pic1 = pic_or_eigen1
            pic2 = pic_or_eigen2
            # 进行图片的对比
            eigens1, sec_arg = self.calculate_face_eigenvalue(pic1, face_num=1)
            eigens2, sec_arg = self.calculate_face_eigenvalue(pic2, face_num=1)
            if eigens1 is None:
                return False, "图片1中未检测到人脸", 0, 0
            if eigens2 is None:
                return False, "图片2中未检测到人脸", 0, 0
            eigen1 = np.asarray(eigens1[0])
            eigen2 = np.asarray(eigens2[0])
        else:  # 将传入参数认为是特征值列表
            eigen1 = np.asarray(pic_or_eigen1)
            eigen2 = np.asarray(pic_or_eigen2)

        # 进行特征值的对比
        dist = np.sqrt(np.sum(np.square(eigen1 - eigen2)))
        score = 100 - (200.0 / 3.0) * dist
        return True, "成功", dist, score

    def search_faces(self, group_names: list = None, img: str = None,
                     max_person_num: int = 1, quality_control: int = 0,
                     face_match_threshold: float = 0):
        """
        用于对一张待识别的人脸图片，在一个或多个人员库中识别出最相似的 TopK 人员，识别结果按照相似度从大到小排序。

        支持一次性识别图片中的最多 10 张人脸，支持一次性跨 100 个人员库（Group）搜索。

        :param group_names: 人员库名
        :param img: 图片
        :param max_person_num: 最大识别人脸数量
        :param need_person_info: 是否需要返回人员信息
        :param quality_control: 是否对图片质量进行控制
        :param face_match_threshold: 人脸匹配阈值
        :return:
        """
        if group_names is None or len(group_names) == 0:
            return True, "人员库为空"
        if img is None or len(img) == 0:
            return True, "Image为空"
        eigen_values, sec_arg = self.calculate_face_eigenvalue(img, face_num=1)
        if eigen_values is None:  # 当搜索的图片中不存在人脸或人脸图片有问题时，返回
            return False, sec_arg
        eigen_value = np.asarray(eigen_values[0])
        match_score_list = []
        person_ids = set()
        for group_name in group_names:
            conn = connection_pool.connection()
            cursor = conn.cursor()
            fetchall = mysql.select_in_table(cursor, table_relation, condition_dict={"group_name": group_name},
                                             result_col=['person_id'])
            if len(fetchall) == 0:
                continue
            ids = set([record[0] for record in fetchall])
            person_ids = person_ids.union(ids)

        for person_id in person_ids:
            person_eigen_values = self.get_eigens_by_person_id(person_id)
            if person_eigen_values is None:  # 如果当前人员的人脸为空，则跳过该人员
                continue
            max_score_of_person = 0
            for current_eigen_value in person_eigen_values:
                suc, info, distance, score = self.compare_face(eigen_value, current_eigen_value,
                                                               quality_control=quality_control)
                if score < face_match_threshold:
                    continue
                if score > max_score_of_person:
                    max_score_of_person = score
            match_score_list.append({"person_id": person_id, "score": max_score_of_person})

        # 至此，获得了所有人员库中人员的人脸对比评分，下面进行排序
        data = pd.DataFrame(match_score_list)
        data.sort_values(by='score', ascending=False, inplace=True)
        most_like_person = list(data.get('person_id'))[:max_person_num]
        face = sec_arg[0]
        face_rect = {"X": face.left(), "Y": face.top(), "Width": face.right() - face.left(),
                     "Height": face.bottom() - face.top()}
        candidates = []

        for person_id in most_like_person:
            score = float(data[data.person_id == person_id].score)
            if score == 0:
                break
            suc, person = Person().get_person_base_info(person_id=person_id)
            if isinstance(person, Person):
                candidate = {"PersonId": person_id, "PersonName": person.person_name, "Gender": person.gender,
                             "CreationTime": person.creation_time,
                             "Score": score}
                candidates.append(candidate)

        return True, {"Candidates": candidates, "FaceRect": face_rect}

    def verify_face(self, person_id, pic, quality_control=0):
        """
        给定一张人脸图片和一个 PersonId，判断图片中的人和 PersonId 对应的人是否为同一人。

        :param person_id:
        :param pic:
        :param quality_control:
        :return:
        """
        eigen_values = self.get_eigens_by_person_id(person_id)
        pic_eigen_value = self.calculate_face_eigenvalue(pic, face_num=1)
        pic_eigen_value = pic_eigen_value[0][0]

        for eigen_value in eigen_values:
            suc, info, distance, score = self.compare_face(eigen_value, pic_eigen_value, quality_control)
            if score > 70:
                return score, True
        return score, False

    def verify_person(self, person_id, pic, quality_control=0):
        """
        给定一张人脸图片和一个 PersonId，判断图片中的人和 PersonId 对应的人是否为同一人。PersonId 请参考人员库管理相关接口。
         本接口会将该人员（Person）下的所有人脸（Face）进行融合特征处理，即若某个Person下有4张 Face，本接口会将4张 Face
         的特征进行融合处理，生成对应这个 Person 的特征，使人员验证（确定待识别的人脸图片是某人员）更加准确。
        :param person_id:
        :param pic:
        :param quality_control:
        :return:
        """
        return self.verify_face(person_id, pic, quality_control)


def capture_image():
    # capture = cv2.VideoCapture(0)
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = capture.read()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # cv2.circle(frame, (200, 200), 20, (0, 255, 0), 2)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()


def face_clustering():
    """
    应该是归类人脸的方法，暂时用不到

    :return:
    """
    #   This example shows how to use dlib's face recognition tool for clustering using chinese_whispers.
    #   This is useful when you have a collection of photographs which you know are linked to
    #   a particular person, but the person may be photographed with multiple other people.
    #   In this example, we assume the largest cluster will contain photos of the common person in the
    #   collection of photographs. Then, we save extracted images of the face in the largest cluster in
    #   a 150x150 px format which is suitable for jittering and loading to perform metric learning (as shown
    #   in the dnn_metric_learning_on_images_ex.cpp example.
    #   https://github.com/davisking/dlib/blob/master/examples/dnn_metric_learning_on_images_ex.cpp
    #
    # COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
    #   You can install dlib using the command:
    #       pip install dlib
    #
    #   Alternatively, if you want to compile dlib yourself then go into the dlib
    #   root folder and run:
    #       python setup.py install
    #
    #   Compiling dlib should work on any operating system so long as you have
    #   CMake installed.  On Ubuntu, this can be done easily by running the
    #   command:
    #       sudo apt-get install cmake
    #
    #   Also note that this example requires Numpy which can be installed
    #   via the command:
    #       pip install numpy

    import sys
    import os
    import dlib
    import glob

    predictor_path = sys.argv[1]
    face_rec_model_path = sys.argv[2]
    faces_folder_path = sys.argv[3]
    output_folder_path = sys.argv[4]

    # Load all the models we need: a detector to find the faces, a shape predictor
    # to find face landmarks so we can precisely localize the face, and finally the
    # face recognition model.
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(predictor_path)
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)

    descriptors = []
    images = []

    # Now find all the faces and compute 128D face descriptors for each face.
    for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
        print("Processing file: {}".format(f))
        img = dlib.load_rgb_image(f)

        # Ask the detector to find the bounding boxes of each face. The 1 in the
        # second argument indicates that we should upsample the image 1 time. This
        # will make everything bigger and allow us to detect more faces.
        dets = detector(img, 1)
        print("Number of faces detected: {}".format(len(dets)))

        # Now process each face we found.
        for k, d in enumerate(dets):
            # Get the landmarks/parts for the face in box d.
            shape = sp(img, d)

            # Compute the 128D vector that describes the face in img identified by
            # shape.
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            descriptors.append(face_descriptor)
            images.append((img, shape))

    # Now let's cluster the faces.
    labels = dlib.chinese_whispers_clustering(descriptors, 0.5)
    num_classes = len(set(labels))
    print("Number of clusters: {}".format(num_classes))

    # Find biggest class
    biggest_class = None
    biggest_class_length = 0
    for i in range(0, num_classes):
        class_length = len([label for label in labels if label == i])
        if class_length > biggest_class_length:
            biggest_class_length = class_length
            biggest_class = i

    print("Biggest cluster id number: {}".format(biggest_class))
    print("Number of faces in biggest cluster: {}".format(biggest_class_length))

    # Find the indices for the biggest class
    indices = []
    for i, label in enumerate(labels):
        if label == biggest_class:
            indices.append(i)

    print("Indices of images in the biggest cluster: {}".format(str(indices)))

    # Ensure output directory exists
    if not os.path.isdir(output_folder_path):
        os.makedirs(output_folder_path)

    # Save the extracted faces
    print("Saving faces in largest cluster to output folder...")
    for i, index in enumerate(indices):
        img, shape = images[index]
        file_path = os.path.join(output_folder_path, "face_" + str(i))
        # The size and padding arguments are optional with default size=150x150 and padding=0.25
        dlib.save_face_chip(img, shape, file_path, size=150, padding=0.25)


def face_jitter(pic):
    """
    http://dlib.net/face_jitter.py.html

    :param pic:
    :return:
    """

    def show_jittered_images(window, jittered_images):
        '''
            Shows the specified jittered images one by one
        '''
        for img in jittered_images:
            window.set_image(img)
            dlib.hit_enter_to_continue()

    face_file_path = "../examples/faces/Tom_Cruise_avp_2014_4.jpg"

    # Load all the models we need: a detector to find the faces, a shape predictor
    # to find face landmarks so we can precisely localize the face
    detector = dlib.get_frontal_face_detector()
    global shape_predictor_model, model_folder
    predictor_path = getAbsPath(model_folder, shape_predictor_model)
    sp = dlib.shape_predictor(predictor_path)

    # Load the image using dlib
    img = dlib.load_rgb_image(face_file_path)

    # Ask the detector to find the bounding boxes of each face.
    dets = detector(img)

    num_faces = len(dets)

    # Find the 5 face landmarks we need to do the alignment.
    faces = dlib.full_object_detections()
    for detection in dets:
        faces.append(sp(img, detection))

    # Get the aligned face image and show it
    image = dlib.get_face_chip(img, faces[0], size=320)
    window = dlib.image_window()
    window.set_image(image)
    dlib.hit_enter_to_continue()

    # Show 5 jittered images without data augmentation
    jittered_images = dlib.jitter_image(image, num_jitters=5)
    show_jittered_images(window, jittered_images)

    # Show 5 jittered images with data augmentation
    jittered_images = dlib.jitter_image(image, num_jitters=5, disturb_colors=True)
    show_jittered_images(window, jittered_images)


def find_candidate_obj_locations():
    """
    查找图片中可能包含了任何物体的矩形框
    http://dlib.net/find_candidate_object_locations.py.html
    :return:
    """
    dlib.find_candidate_object_locations()


def train_object_detector():
    # !/usr/bin/python
    # The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
    #
    # This example program shows how you can use dlib to make a HOG based object
    # detector for things like faces, pedestrians, and any other semi-rigid
    # object.  In particular, we go though the steps to train the kind of sliding
    # window object detector first published by Dalal and Triggs in 2005 in the
    # paper Histograms of Oriented Gradients for Human Detection.
    #
    #
    # COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
    #   You can install dlib using the command:
    #       pip install dlib
    #
    #   Alternatively, if you want to compile dlib yourself then go into the dlib
    #   root folder and run:
    #       python setup.py install
    #
    #   Compiling dlib should work on any operating system so long as you have
    #   CMake installed.  On Ubuntu, this can be done easily by running the
    #   command:
    #       sudo apt-get install cmake
    #
    #   Also note that this example requires Numpy which can be installed
    #   via the command:
    #       pip install numpy

    import os
    import sys
    import glob

    import dlib

    # In this example we are going to train a face detector based on the small
    # faces dataset in the examples/faces directory.  This means you need to supply
    # the path to this faces folder as a command line argument so we will know
    # where it is.
    if len(sys.argv) != 2:
        print(
            "Give the path to the examples/faces directory as the argument to this "
            "program. For example, if you are in the python_examples folder then "
            "execute this program by running:\n"
            "    ./train_object_detector.py ../examples/faces")
        exit()
    faces_folder = sys.argv[1]

    # Now let's do the training.  The train_simple_object_detector() function has a
    # bunch of options, all of which come with reasonable default values.  The next
    # few lines goes over some of these options.
    options = dlib.simple_object_detector_training_options()
    # Since faces are left/right symmetric we can tell the trainer to train a
    # symmetric detector.  This helps it get the most value out of the training
    # data.
    options.add_left_right_image_flips = True
    # The trainer is a kind of support vector machine and therefore has the usual
    # SVM C parameter.  In general, a bigger C encourages it to fit the training
    # data better but might lead to overfitting.  You must find the best C value
    # empirically by checking how well the trained detector works on a test set of
    # images you haven't trained on.  Don't just leave the value set at 5.  Try a
    # few different C values and see what works best for your data.
    options.C = 5
    # Tell the code how many CPU cores your computer has for the fastest training.
    options.num_threads = 4
    options.be_verbose = True

    training_xml_path = os.path.join(faces_folder, "training.xml")
    testing_xml_path = os.path.join(faces_folder, "testing.xml")
    # This function does the actual training.  It will save the final detector to
    # detector.svm.  The input is an XML file that lists the images in the training
    # dataset and also contains the positions of the face boxes.  To create your
    # own XML files you can use the imglab tool which can be found in the
    # tools/imglab folder.  It is a simple graphical tool for labeling objects in
    # images with boxes.  To see how to use it read the tools/imglab/README.txt
    # file.  But for this example, we just use the training.xml file included with
    # dlib.
    dlib.train_simple_object_detector(training_xml_path, "detector.svm", options)

    # Now that we have a face detector we can test it.  The first statement tests
    # it on the training data.  It will print(the precision, recall, and then)
    # average precision.
    print("")  # Print blank line to create gap from previous output
    print("Training accuracy: {}".format(
        dlib.test_simple_object_detector(training_xml_path, "detector.svm")))
    # However, to get an idea if it really worked without overfitting we need to
    # run it on images it wasn't trained on.  The next line does this.  Happily, we
    # see that the object detector works perfectly on the testing images.
    print("Testing accuracy: {}".format(
        dlib.test_simple_object_detector(testing_xml_path, "detector.svm")))

    # Now let's use the detector as you would in a normal application.  First we
    # will load it from disk.
    detector = dlib.simple_object_detector("detector.svm")

    # We can look at the HOG filter we learned.  It should look like a face.  Neat!
    win_det = dlib.image_window()
    win_det.set_image(detector)

    # Now let's run the detector over the images in the faces folder and display the
    # results.
    print("Showing detections on the images in the faces folder...")
    win = dlib.image_window()
    for f in glob.glob(os.path.join(faces_folder, "*.jpg")):
        print("Processing file: {}".format(f))
        img = dlib.load_rgb_image(f)
        dets = detector(img)
        print("Number of faces detected: {}".format(len(dets)))
        for k, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                k, d.left(), d.top(), d.right(), d.bottom()))

        win.clear_overlay()
        win.set_image(img)
        win.add_overlay(dets)
        dlib.hit_enter_to_continue()

    # Next, suppose you have trained multiple detectors and you want to run them
    # efficiently as a group.  You can do this as follows:
    detector1 = dlib.fhog_object_detector("detector.svm")
    # In this example we load detector.svm again since it's the only one we have on
    # hand. But in general it would be a different detector.
    detector2 = dlib.fhog_object_detector("detector.svm")
    # make a list of all the detectors you want to run.  Here we have 2, but you
    # could have any number.
    detectors = [detector1, detector2]
    image = dlib.load_rgb_image(faces_folder + '/2008_002506.jpg')
    [boxes, confidences, detector_idxs] = dlib.fhog_object_detector.run_multiple(detectors, image, upsample_num_times=1,
                                                                                 adjust_threshold=0.0)
    for i in range(len(boxes)):
        print("detector {} found box {} with confidence {}.".format(detector_idxs[i], boxes[i], confidences[i]))

    # Finally, note that you don't have to use the XML based input to
    # train_simple_object_detector().  If you have already loaded your training
    # images and bounding boxes for the objects then you can call it as shown
    # below.

    # You just need to put your images into a list.
    images = [dlib.load_rgb_image(faces_folder + '/2008_002506.jpg'),
              dlib.load_rgb_image(faces_folder + '/2009_004587.jpg')]
    # Then for each image you make a list of rectangles which give the pixel
    # locations of the edges of the boxes.
    boxes_img1 = ([dlib.rectangle(left=329, top=78, right=437, bottom=186),
                   dlib.rectangle(left=224, top=95, right=314, bottom=185),
                   dlib.rectangle(left=125, top=65, right=214, bottom=155)])
    boxes_img2 = ([dlib.rectangle(left=154, top=46, right=228, bottom=121),
                   dlib.rectangle(left=266, top=280, right=328, bottom=342)])
    # And then you aggregate those lists of boxes into one big list and then call
    # train_simple_object_detector().
    boxes = [boxes_img1, boxes_img2]

    detector2 = dlib.train_simple_object_detector(images, boxes, options)
    # We could save this detector to disk by uncommenting the following.
    # detector2.save('detector2.svm')

    # Now let's look at its HOG filter!
    win_det.set_image(detector2)
    dlib.hit_enter_to_continue()

    # Note that you don't have to use the XML based input to
    # test_simple_object_detector().  If you have already loaded your training
    # images and bounding boxes for the objects then you can call it as shown
    # below.
    print("\nTraining accuracy: {}".format(
        dlib.test_simple_object_detector(images, boxes, detector2)))


def get_face_rect(pic, align: bool = False, save_to: bool = False):
    """
    获得图片中的人脸矩形区域信息。

    返回参数1 - 原图的ndarray格式数据
    返回参数2 - 原图片上的人脸区域的矩形框的坐标的列表，每一个列表项对应一张人脸， 如[[left1, top1, right1, bottom1],[left2, top2, right2, bottom2]]
    返回参数3 - ndarray格式图片列表，每一个对应一张人脸图片

    :param pic:
    :param align: 是否矫正人脸角度，默认不矫正
    :param save_to: 是否保存到本地
    :return: 矩形区域坐标列表[left, top, right, bottom]，原图像（ndarray格式），裁剪出的人脸区域图像（ndarray格式）列表
    """
    if not align:  # 不需要对齐人脸角度时
        detector = detector_default
        # 从pic中加载图片ndarray
        pic = getAbsPath(detect_folder, pic)
        img = pic2ndarray(pic)
        dets = detector(img, 1)
        logger.debug("共检测到了{}张人脸".format(len(dets)))
        rects = []  # 源图片上人脸矩形区域参数列表
        sub_imgs = []
        for index, det in enumerate(dets):
            logger.info("face {}, left {}, top {}, right {}, bottom {}".format(index, det.left(), det.top(),
                                                                               det.right(), det.bottom()))
            rects.append([det.left(), det.top(), det.right(), det.bottom()])
            sub_img = crop_pic(img, det.left(), det.top(), det.right(), det.bottom())
            if save_to:
                cv2.imwrite(os.path.join(save_folder, "cropped_{}.jpg".format(index)), sub_img)
            sub_imgs.append(sub_img)
    else:
        # face_alignment_pic()
        logger.debug("暂不支持对齐人脸，fallback to不对齐模式")
        return get_face_rect(pic, save_to=save_to)
    return rects, img, sub_imgs  # 矩形区域坐标列表，原图像（ndarray格式），裁剪出的人脸区域图像（ndarray格式）列表


@loggingTitleCall(title="人脸对齐")
def face_alignment_pic(pic):
    # Load all the models we need: a detector to find the faces, a shape predictor
    # to find face landmarks so we can precisely localize the face
    detector = detector_default
    sp = shape_predictor

    # 从pic中加载图片ndarray
    pic = getAbsPath(detect_folder, pic)
    img = pic2ndarray(pic)

    # Ask the detector to find the bounding boxes of each face.
    # 第二个参数1表示上采样的次数，上采样会使得图像中的所有元素放大，从而可以检测到尽量多的人脸。
    dets = detector(img, 1)

    num_faces = len(dets)
    if num_faces == 0:
        logger.debug("There were no faces found in the given picture")
        return None

    # 定位到人脸五官位置，以进行对齐
    # faces = dlib.full_object_detections()
    for index, detection in enumerate(dets):
        logger.info("face {}, left {}, top {}, right {}, bottom {}".format(index, detection.left(), detection.top(),
                                                                           detection.right(), detection.bottom()))
        face = sp(img, detection)
        face5 = []
        for point in face.parts():
            face5.append(point)
            xy = (point.x, point.y)
            kwargs = {"circle": {"center": xy, "radius": 4, "fill": 'blue', "outline": "yellow"}}
            img = draw_element_on_pic(img, need_show=False, **kwargs)

        logger.debug("五官定位位置：{}".format(face5))
        # faces.append(face)

    # Image.fromarray(img).show()
    # window = dlib.image_window()
    #
    # # Get the aligned face images
    # # Optionally:
    # # images = dlib.get_face_chips(img, faces, size=160, padding=0.25)
    # images = dlib.get_face_chips(img, faces, size=320)  # images是列表，列表的每一项为ndarray格式的图片
    # for image in images:
    #     window.set_image(image)
    #     dlib.hit_enter_to_continue()
    #
    # # faces[0].rect 是人脸矩形区域的参数
    # image = dlib.get_face_chip(img, faces[0])
    # window.set_image(image)
    # dlib.hit_enter_to_continue()


def recognize_face_pic(pic, use_lib: str = 'dlib', **kwargs):
    """
    从静态图片中识别人脸，返回人脸的矩形框，如果图片中存在多个人脸，将返回多个人脸的矩形框列表

    refer to: http://dlib.net/cnn_face_detector.py.html
    :param pic: 本地图片的地址，或者cv2.imread()获得的ndarray数组
    :param use_lib: 使用的第三方库，有'dlib'，’recognition_face', 'seetaface', 'opencv'
    :return:
    """

    def recognize_dlib():
        # gray = cv2.cvtColor(pic_file, cv2.COLOR_BGR2GRAY)
        if kwargs.get("Speed_Accuracy") == "Accuracy":  # 可以指定速度优先，不指定则精度优先
            global model_folder, cnn_face_detection_model
            model_path = getAbsPath(model_folder, cnn_face_detection_model)
            detector = dlib.cnn_face_detection_model_v1(model_path)
            logger.debug("使用准确度优先模式进行人脸识别")
        else:
            detector = dlib.get_frontal_face_detector()
            logger.debug("使用速度优先模式进行人脸识别")

        # win = dlib.image_window()

        img = pic
        dets = detector(img, 1)  # rectangles[[(349, 142) (617, 409)]]，默认detector的结果

        '''
            This detector returns a mmod_rectangles object. This object contains a list of mmod_rectangle objects.
            These objects can be accessed by simply iterating over the mmod_rectangles object
            The mmod_rectangle object has two member variables, a dlib.rectangle object, and a confidence score.

            It is also possible to pass a list of images to the detector.
                - like this: dets = cnn_face_detector([image list], upsample_num, batch_size = 128)

            In this case it will return a mmod_rectangless object.
            This object behaves just like a list of lists and can be iterated over.
            '''
        logger.debug("Number of faces detected: {}".format(len(dets)))
        rects = []
        for i, d in enumerate(dets):
            if isinstance(d, dlib.mmod_rectangle):  # 说明是精度优先
                left, top, right, bottom = d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom()
                rects.append(d.rect)
                confidence = d.confidence
            else:
                left, top, right, bottom = d.left(), d.top(), d.right(), d.bottom()
                rects.append(d)
                confidence = None
            logger.debug("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(
                i, left, top, right, bottom, confidence))
            # 这里如果使用默认的人脸检测器，则只能得到一个人脸的矩形框，如果使用cnn_face_detection_model_v1，可以额外获得一个
            # 可信度。官网教程之处，CNN的识别准确率更高一些，但速度相对更慢。

            # # ====================================================================================
            # # Finally, if you really want to you can ask the detector to tell you the score
            # # for each detection.  The score is bigger for more confident detections.
            # # The third argument to run is an optional adjustment to the detection threshold,
            # # where a negative value will return more detections and a positive value fewer.
            # # Also, the idx tells you which of the face sub-detectors matched.  This can be
            # # used to broadly identify faces in different orientations.
            # dets, scores, idx = detector.run(img, 1, -1)
            # for i, d in enumerate(dets):
            #     print("Detection {}, score: {}, face_type:{}".format(
            #         d, scores[i], idx[i]))
            # # ====================================================================================

        rects1 = dlib.rectangles()
        rects1.extend([d for d in rects])

        # win.clear_overlay()
        # win.set_image(img)
        # win.add_overlay(rects1)
        # dlib.hit_enter_to_continue()

        return rects1

    # ======================================================================================================
    # if lib_folder is None:
    #     init_image_lib()
    logger.warning("需要查询数据库中的人脸特征数据，功能暂未开发")
    exit(1)
    pic = pic2ndarray(pic)

    if use_lib == "dlib":
        return recognize_dlib()


# def c():
#     """
#     https://github.com/ageitgey/face_recognition/blob/master/examples/find_facial_features_in_picture.py
#     :return:
#     """
#     from PIL import Image, ImageDraw
#     import face_recognition
#
#     if lib_folder is None:
#         init_image_lib()
#     # Load the jpg file into a numpy array
#     image_file = os.path.join(lib_folder, "two_people.jpg")
#     assert os.path.exists(image_file), "文件不存在：{}".format(image_file)
#     image = face_recognition.load_image_file(image_file)
#
#     # Find all facial features in all the faces in the image
#     face_landmarks_list = face_recognition.face_landmarks(image)
#
#     print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))
#
#     # Create a PIL imagedraw object so we can draw on the picture
#     pil_image = Image.fromarray(image)
#     d = ImageDraw.Draw(pil_image)
#
#     for face_landmarks in face_landmarks_list:
#
#         # Print the location of each facial feature in this image
#         for facial_feature in face_landmarks.keys():
#             print("The {} in this face has the following points: {}".format(facial_feature,
#                                                                             face_landmarks[facial_feature]))
#
#         # Let's trace out each facial feature in the image with a line!
#         for facial_feature in face_landmarks.keys():
#             d.line(face_landmarks[facial_feature], width=5)
#
#     # Show the picture
#     pil_image.show()


def putText(img, text, left, top, textColor=font_color, textSize=font_size):
    """
    在cv2的img对象上打印文字

    :param img:
    :param text:
    :param left:
    :param top:
    :param textColor:
    :param textSize:
    :return:
    """
    if textColor is None:
        init_image_lib()
        return putText(img, text, left, top, textColor, textSize)
    if isinstance(img, np.ndarray):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在指定图像上绘图的对象
    draw = ImageDraw.Draw(img)

    # 绘制文本
    draw.text((left, top), text, textColor, font=font_style)
    # 转换回opencv格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def recognize_face_cam():
    """
    识别摄像头前的人脸

    :return:
    """
    # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
    # other example, but it includes some basic performance tweaks to make things run a lot faster:
    #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
    #   2. Only detect faces in every other frame of video.

    # Get a reference to webcam #0 (the default one)
    import face_recognition
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    known_face_encodings = []
    known_face_names = []

    if known_face_names is None:
        init_image_lib()

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            # eigen_values, sec_arg = Face.calculate_face_eigenvalue(rgb_small_frame, face_num=1)
            succ, sec_arg = Face().search_faces('test', rgb_small_frame, max_person_num=1, quality_control=0)
            if succ and isinstance(sec_arg, dict):
                candidate = sec_arg.get('Candidates')

            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                print("face_distances = {}".format(face_distances))
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

            process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(img=frame, text=name, org=(left + 6, bottom - 6), fontFace=font, fontScale=1.0,
            #             color=(255, 255, 255), thickness=1)
            frame = putText(img=frame, text=name, left=left + 12, top=bottom - 25, textColor=(255, 255, 255),
                            textSize=20)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

# capture_image()
# c()
# recognize_face_cam()
# init_image_lib()  # 因为该方法可能会报错：如mysql连接失败错误，因此不要放在这里进行初始化，最好再导入后手动初始化该模块同时捕捉是否报错
# mysql_op: FaceMysql = FaceMysql()
