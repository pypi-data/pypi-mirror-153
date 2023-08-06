class FaceQualityCompleteness:
    def __init__(self, eyebrow: int, eye: int, nose: int, cheek: int, mouth: int, chin: int):
        """
        五官遮挡分，评价眉毛（Eyebrow）、眼睛（Eye）、鼻子（Nose）、脸颊（Cheek）、嘴巴（Mouth）、下巴（Chin）的被遮挡程度。

        :param eyebrow: 眉毛的遮挡分数[0,100]，分数越高遮挡越少。[0,80]表示发生遮挡。
        :param eye: 眼睛的遮挡分数[0,100],分数越高遮挡越少。[0,80]表示发生遮挡。
        :param nose: 鼻子的遮挡分数[0,100],分数越高遮挡越少。[0,60]表示发生遮挡。
        :param cheek: 脸颊的遮挡分数[0,100],分数越高遮挡越少。[0,70]表示发生遮挡。
        :param mouth: 嘴巴的遮挡分数[0,100],分数越高遮挡越少。[0,50]表示发生遮挡。
        :param chin: 下巴的遮挡分数[0,100],分数越高遮挡越少。[0,70]表示发生遮挡。
        """
        self.Eyebrow = eyebrow
        self.Eye = eye
        self.Nose = nose
        self.Cheek = cheek
        self.Mouth = mouth
        self.Chin = chin


class FaceQualityInfo:
    def __init__(self, score: int, sharpness: int, brightness: int, completeness: FaceQualityCompleteness):
        """
        人脸质量信息

        :param score: 质量分: [0,100]，综合评价图像质量是否适合人脸识别，分数越高质量越好。正常情况，只需要使用Score作为质量分总体的判断标准即可。Sharpness、Brightness、Completeness等细项分仅供参考。参考范围：[0,40]较差，[40,60] 一般，[60,80]较好，[80,100]很好。
        :param sharpness: 清晰分：[0,100]，评价图片清晰程度，分数越高越清晰。参考范围：[0,40]特别模糊，[40,60]模糊，[60,80]一般，[80,100]清晰。建议：人脸入库选取80以上的图片。
        :param brightness: 光照分：[0,100]，评价图片光照程度，分数越高越亮。参考范围： [0,30]偏暗，[30,70]光照正常，[70,100]偏亮。建议：人脸入库选取[30,70]的图片。
        :param completeness: 五官遮挡分，评价眉毛（Eyebrow）、眼睛（Eye）、鼻子（Nose）、脸颊（Cheek）、嘴巴（Mouth）、下巴（Chin）的被遮挡程度。
        """
        self.Score = score  # 可以由dlib库获得，detector.run(img, 1, -1)
        self.Sharpness = sharpness
        self.Brightness = brightness
        self.Completeness = completeness


class FaceHairAttributesInfo:
    def __init__(self, length: int, bang: int, color: int):
        """
        头发属性信息

        :param length: 0：光头，1：短发，2：中发，3：长发，4：绑发  注意：此字段可能返回 null，表示取不到有效值。
        :param bang: 0：有刘海，1：无刘海  注意：此字段可能返回 null，表示取不到有效值。
        :param color: 0：黑色，1：金色，2：棕色，3：灰白色  注意：此字段可能返回 null，表示取不到有效值。
        """
        self.Length = length
        self.Bang = bang
        self.Color = color


class FaceAttributesInfo:
    def __init__(self, gender: int, age: int, expression: int, glass: bool, pitch: int, yaw: int, roll: int,
                 beauty: int, hat: bool, mask: bool, hair: FaceHairAttributesInfo, eyeOpen: bool):
        """

        :param gender: 性别[0~49]为女性，[50，100]为男性，越接近0和100表示置信度越高。
        :param age: 年龄 [0~100]。NeedFaceAttributes 不为1或检测超过 5 张人脸时，此参数仍返回，但不具备参考意义。
        :param expression: 微笑[0(normal，正常)~50(smile，微笑)~100(laugh，大笑)]。NeedFaceAttributes 不为1 ，此参数仍返回，但不具备参考意义。
        :param glass: 是否有眼镜 [true,false]。
        :param pitch: 上下偏移[-30,30]，单位角度。
        :param yaw: 左右偏移[-30,30]，单位角度。
        :param roll: 平面旋转[-180,180]，单位角度。
        :param beauty: 魅力[0~100]。
        :param hat: 是否有帽子 [true,false]
        :param mask: 是否有口罩 [true,false]
        :param hair: 头发信息，包含头发长度（length）、有无刘海（bang）、头发颜色（color）
        :param eyeOpen: 双眼是否睁开 [true,false]
        """
        self.Hair = hair
        self.Mask = mask
        self.Hat = hat
        self.Beauty = beauty
        self.Roll = roll
        self.Yaw = yaw
        self.Pitch = pitch
        self.Glass = glass
        self.Expression = expression
        self.Gender = gender
        self.Age = age
        self.EyeOpen = eyeOpen


class FaceInfo:
    def __init__(self, x: int, y: int, width: int, height: int, faceAttributesInfo: FaceAttributesInfo,
                 faceQualityInfo: FaceQualityInfo):
        """
        人脸信息列表

        :param x: 人脸框左上角横坐标。
        :param y: 人脸框左上角纵坐标。
        :param width: 人脸框宽度
        :param height: 人脸框高度
        :param faceAttributesInfo: 人脸属性信息
        :param faceQualityInfo: 人脸质量信息
        """
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
        self.FaceAttributesInfo = faceAttributesInfo
        self.FaceQualityInfo = faceQualityInfo
