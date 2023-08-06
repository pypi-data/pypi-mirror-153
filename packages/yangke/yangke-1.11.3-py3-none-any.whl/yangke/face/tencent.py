# 人脸检测接口
# api接口和腾讯云一致，算法为自定义算法
"""
人脸检测与分析相关接口
接口名称	                                        接口功能
DetectFace	                                        人脸检测与分析

五官定位相关接口
接口名称	                                        接口功能
AnalyzeFace	                                        五官定位

人脸比对相关接口
接口名称	                                        接口功能
CompareFace	                                        人脸比对

人员库管理相关接口
接口名称	                                        接口功能
CreateGroup	                                        创建人员库
DeleteGroup	                                        删除人员库
GetGroupList	                                    获取人员库列表
ModifyGroup	                                        修改人员库
CreatePerson	                                    创建人员
DeletePerson	                                    删除人员
DeletePersonFromGroup	                            人员库删除人员
GetPersonList	                                    获取人员列表
GetPersonListNum	                                获取人员列表长度
GetPersonBaseInfo	                                获取人员基础信息
GetPersonGroupInfo	                                获取人员归属信息
ModifyPersonBaseInfo	                            修改人员基础信息
ModifyPersonGroupInfo	                            修改人员描述信息
CreateFace	                                        增加人脸
DeleteFace	                                        删除人脸
CopyPerson	                                        复制人员
GetGroupInfo	                                    获取人员库信息

人脸搜索相关接口
接口名称	                                        接口功能
SearchFaces	                                        人脸搜索
SearchFacesReturnsByGroup	                        人脸搜索分库返回
SearchPersons	                                    人员搜索
SearchPersonsReturnsByGroup                     	人员搜索按库返回

人脸验证相关接口
接口名称	                                        接口功能
VerifyFace	                                        人脸验证
VerifyPerson	                                    人员验证

人脸静态活体检测相关接口
接口名称	                                        接口功能
DetectLiveFace	                                    人脸静态活体检测

人员查重相关接口
接口名称	                                        接口功能
CheckSimilarPerson	                                人员查重
EstimateCheckSimilarPersonCostTime	                获取人员查重预估需要时间
GetCheckSimilarPersonJobIdList	                    获取人员查重任务列表
GetSimilarPersonResult	                            人员查重结果查询
"""
from ..core import isBase64, base642image
from ..common.config import logger
import uuid
from .face import recognize_face_pic
import cv2
from .tencent_data_struct import *


def CreateGroup(GroupName: str, Description=None, Tag=None):
    """
    用于创建一个空的人员库，如果人员库已存在返回错误。 可根据需要创建自定义描述字段，用于辅助描述该人员库下的人员信息。

    :param GroupName:
    :param GroupID:
    :param Description:
    :param Tag:
    :return:
    """
    from .face import Face
    global group
    group = Face(table_person=GroupName + "_person", table_eigen=GroupName + "_eigen")


def CreatePerson(GroupName: str, PersonName: str, PersonId: str, Image=None, Url=None, UniquePersonControl: int = 4,
                 QualityControl: int = 2):
    """

    :param GroupName:
    :param PersonName:
    :param PersonId:
    :param Image:
    :param Url:
    :param UniquePersonControl: 取值[0, 4]。此参数用于控制判断 Image 或 Url 中图片包含的人脸，是否在人员库中已有疑似的同一人。如果判断为已有相同人在人员库中，则不会创建新的人员，返回疑似同一人的人员信息。如果判断没有，则完成创建人员。
    :param QualityControl: 取值[0, 4]。图片质量控制，若图片质量不满足要求，则返回结果中会提示图片质量检测不符要求。2：图像存在偏亮，偏暗，模糊或一般模糊，眉毛遮挡，脸颊遮挡，下巴遮挡，至少其中三种的情况；数字越大，要求越高
    :return:
    """
    pass

def DetectFace(MaxFaceNum: int = 1, MinFaceSize: int = 34, Image: str = None, ImageUrl=None,
               NeedFaceAttributes=False, NeedQualityDetection=False, FaceModelVersion: str = "default", **kwargs):
    """
    人脸检测与分析

    :param MaxFaceNum:
    :param MinFaceSize:
    :param Image:
    :param ImageUrl:
    :param NeedFaceAttributes:
    :param NeedQualityDetection:
    :param FaceModelVersion: 人脸识别使用的算法库及模型
    :return:
    """
    # 图片来源可能是url(支持file:///开头的本地文件url，requests库本身是不支持的)，也可能是base64字符串
    assert Image is not None or ImageUrl is not None, "需要传入图片进行检测"
    if Image is None:
        # 通过ImageUrl获取图片
        if str(ImageUrl).startswith("file:///"):
            image_file = ImageUrl.replace("file:///", "")
            img = cv2.imread(image_file)
            assert img is not None, "文件不存在：{}".format(image_file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            logger.debug("加载本地文件：{}".format(image_file))
        else:
            import requests
            img = requests.get(ImageUrl)
            logger.debug("加载网络图片：{}".format(ImageUrl))
    else:
        if isBase64(Image):
            img = base642image(Image)
            logger.debug("加载Base64格式图片数据")
        else:
            img = Image
            logger.debug("加载ndarray格式图片数据")

    # img是一个三维的ndarray
    ImageWidth = img.shape[1]
    ImageHeight = img.shape[0]

    rects = recognize_face_pic(pic=img, need_face_details=NeedFaceAttributes,
                               need_quality_detection=NeedQualityDetection, **kwargs)
    FaceInfos = FaceInfo()
    RequestId = uuid.uuid4()

    return ImageWidth, ImageHeight, FaceInfos, FaceModelVersion, RequestId
