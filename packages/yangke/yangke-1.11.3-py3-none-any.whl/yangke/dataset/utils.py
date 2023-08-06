# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import glob
import copy


def pascalVOC_2_dlibXML(src_path, dst_path):
    """
    将Pascal VOC格式的数据集转换为dlib可以使用的XML格式，该转换会损失一些信息，因为Pascal VOC包含的信息更丰富，如图片中物体
    是否被遮挡，识别难度等。因此是单向转换，不能从dlibXML转换为Pascal VOC数据。

    发现有些VOC数据不规范，添加了对图片文件的校对功能，如果annotation/xml文件中对应的图片不存在，则不会添加，如果只是图片后缀
    错误，如jpg错写为jpeg，则会修正

    Example:

    pascalVOC_2_dlibXML(src_path="D:\\Users\\pycharm\\face\\helmet\\VOC2028",
                        dst_path="D:\\Users\\pycharm\\face\\helmet\\VOC2028\\dlib")

    :param src_path:
    :return:
    """

    def add_pic(dlib_xml: ET.ElementTree, voc_xml, pic_name):
        """
        将voc_xml文件中的信息添加到dlib_xml对应的ElementTree的images节点下，图片路径为pic_name
        :param dlib_xml:
        :param voc_xml:
        :param pic_name:
        :return:
        """
        # 拿到dlib_xml的images节点
        dlib_images = dlib_xml.find("images")

        # 校对图片文件是否存在，如果只是后缀错误则修正
        if not os.path.exists(pic_name):
            folder = os.path.dirname(pic_name)
            basename = os.path.splitext(os.path.basename(pic_name))[0]
            if os.path.exists(os.path.join(folder, basename + ".jpg")):
                pic_name = os.path.join(folder, basename + ".jpg")

        # 构建image节点，并添加到dlib_images中
        dlib_image = ET.Element("image", file=os.path.abspath(pic_name))
        dlib_images.append(dlib_image)

        voc_xml_et = ET.parse(file)
        # 购进image的box子节点
        for e in voc_xml_et.findall("object"):
            name01 = e.find("name").text  # 物体名
            bndbox = e.find("bndbox")
            xmin = bndbox.find("xmin").text
            ymin = bndbox.find("ymin").text
            xmax = bndbox.find("xmax").text
            ymax = bndbox.find("ymax").text
            width = str(int(xmax) - int(xmin))
            height = str(int(ymax) - int(ymin))
            box = ET.Element("box", top=ymin, left=xmin, width=width, height=height)

            label = ET.SubElement(box, 'label')
            label.text = name01
            dlib_image.append(box)

    # 获得文件夹目录结构
    annotations_folder = os.path.join(src_path, "Annotations")
    image_sets_folder = os.path.join(src_path, "ImageSets")
    jpeg_folder = os.path.join(src_path, "JPEGImages")
    dlib_train_xml = os.path.join(dst_path, 'train.xml')
    dlib_test_xml = os.path.join(dst_path, 'test.xml')
    dlib_val_xml = os.path.join(dst_path, 'val.xml')
    dlib_trainval_xml = os.path.join(dst_path, 'trainval.xml')
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    # 验证数据集完整性
    if not os.path.exists(annotations_folder):
        info = "Annotations目录不存在，请确认输入路径 {} 是否正确，查找路径为 {}".format(src_path, annotations_folder)

    # 验证数据集是否可以根据Pascal VOC进行划分
    train_image = []
    test_image = []
    val_image = []
    trainval_image = []
    if os.path.exists(image_sets_folder):
        if os.path.exists(os.path.join(image_sets_folder, 'Main/train.txt')):
            with open(os.path.join(image_sets_folder, 'Main/train.txt'), 'r') as f:
                for line in f.readlines():
                    train_image.append(line.strip())
        if os.path.exists(os.path.join(image_sets_folder, 'Main/test.txt')):
            with open(os.path.join(image_sets_folder, 'Main/test.txt'), 'r') as f:
                for line in f.readlines():
                    test_image.append(line.strip())
        if os.path.exists(os.path.join(image_sets_folder, 'Main/val.txt')):
            with open(os.path.join(image_sets_folder, 'Main/val.txt'), 'r') as f:
                for line in f.readlines():
                    val_image.append(line.strip())
        if os.path.exists(os.path.join(image_sets_folder, 'Main/trainval.txt')):
            with open(os.path.join(image_sets_folder, 'Main/trainval.txt'), 'r') as f:
                for line in f.readlines():
                    trainval_image.append(line.strip())

    # 构建dlibXML框架
    dlib_dataset = ET.Element("dataset")
    dlib_name = ET.SubElement(dlib_dataset, "name")  # 添加name标签
    dlib_name.text = "imglab dataset"
    ET.SubElement(dlib_dataset, "images")  # 添加images标签
    dlib_datasetTree_train = copy.deepcopy(ET.ElementTree(element=dlib_dataset))
    dlib_datasetTree_test = copy.deepcopy(ET.ElementTree(element=dlib_dataset))
    dlib_datasetTree_val = copy.deepcopy(ET.ElementTree(element=dlib_dataset))
    dlib_datasetTree_trainval = copy.deepcopy(ET.ElementTree(element=dlib_dataset))

    for file in glob.glob1(annotations_folder, '*.xml'):
        file = os.path.join(annotations_folder, file)
        et = ET.parse(file)
        pic_name = et.find("filename").text  # 图片名
        basename = os.path.splitext(os.path.basename(pic_name))[0]
        if os.path.basename(basename) in train_image:
            add_pic(dlib_datasetTree_train, os.path.abspath(file), os.path.join(jpeg_folder, pic_name))
        if os.path.basename(basename) in test_image:
            add_pic(dlib_datasetTree_test, os.path.abspath(file), os.path.join(jpeg_folder, pic_name))
        if os.path.basename(basename) in val_image:
            add_pic(dlib_datasetTree_val, os.path.abspath(file), os.path.join(jpeg_folder, pic_name))
        if os.path.basename(basename) in trainval_image:
            add_pic(dlib_datasetTree_trainval, os.path.abspath(file), os.path.join(jpeg_folder, pic_name))

    dlib_datasetTree_train.write(dlib_train_xml, encoding='utf-8', xml_declaration=True)
    dlib_datasetTree_test.write(dlib_test_xml, encoding='utf-8', xml_declaration=True)
    dlib_datasetTree_val.write(dlib_val_xml, encoding='utf-8', xml_declaration=True)
    dlib_datasetTree_trainval.write(dlib_trainval_xml, encoding='utf-8', xml_declaration=True)


# pascalVOC_2_dlibXML(src_path="D:\\Users\\pycharm\\face\\helmet\\VOC2028",
#                     dst_path="D:\\Users\\pycharm\\face\\helmet\\VOC2028\\dlib")

def COCO_2_Darknet():
    pass
