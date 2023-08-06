from pycocotools.coco import COCO
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import random
import yangke.common.fileOperate as fo
from tqdm import tqdm
from yangke.base import *
import torch


# def loadPascalVOC(dataset_folder:str):
#     """
#     加载Pascal VOC数据集，返回图像中的目标，bbox等信息
#
#     :param dataset_folder: 数据集所在的目录，如C://VOC2007
#     :return:
#     """
#     def load_single_file(xml_file: str):
#


class DataSet_YOLO:
    """
    初始化训练用的数据集，包括训练集、测试集、验证集
    """

    def __init__(self, image_folder, instance_file, img_size=416, hyp=None, augment=True, rect=True):
        """
        构建数据集

        :param image_folder: 图片文件所在的文件夹
        :param instance_file: coco数据集中的instance文件
        """
        self.img_size = img_size
        self.augment = augment
        self.rect = rect
        self.mosaic = self.augment and not self.rect  # 镶嵌图案/马赛克 (only during training)
        self.hyp = hyp

        coco = COCO(instance_file)
        """
        coco.imgs 数据集中图片信息
        coco.cats 类别信息，类别编号及类别对应的物体
        coco.anns 数据集中标注的物体位置信息，包括segmentation,bbox等，按照注释编号排列
        coco.catToImgs 数据集中每一类物体对应的图片信息（即包含该物体的所有图片的id）
        coco.dataset 数据集中所有信息，一般不用
        coco.imgToAnns 数据集中，每一张图片中的物体的位置及分类信息，按照图片id排列
        """
        self.cats = coco.cats  # 类别信息
        self.classes = len(coco.cats)  # 类别总数
        self.img_files = self.__get_images__(coco.imgs, image_folder)  # 图片的绝对路径列表
        self.images = None
        self.labels = self.__get_labels__(coco.imgToAnns)  # 标签信息，darknet中需要保证图片和labels的顺序一一对应

    def __len__(self):
        return len(self.img_files)

    def __getitem__(self, index):

        hyp = self.hyp
        if self.mosaic:
            # Load mosaic
            img, labels = self.load_mosaic(self, index)
            shapes = None

        else:
            # Load image
            img, (h0, w0), (h, w) = load_image(self, index)

            # Letterbox
            shape = self.batch_shapes[self.batch[index]] if self.rect else self.img_size  # final letterboxed shape
            img, ratio, pad = letterbox(img, shape, auto=False, scaleup=self.augment)
            shapes = (h0, w0), ((h / h0, w / w0), pad)  # for COCO mAP rescaling

            # Load labels
            labels = []
            x = self.labels[index]  # x对应class, x_center, y_center, width, height，其中x,y,w,h是归一化后的数据
            if x is not None and x.size > 0:
                # 数据集的labels文件中坐标是归一化的xywh，即x_center, y_center, width, height
                # 这里将归一化的wywh数据转换为像素为单位的 xyxy数据(矩形左上角xy和右下角xy)
                # 这里得到的像素坐标不是整数，直接取整即可，对实际目标边框的影响可以忽略
                labels = x.copy()
                labels[:, 1] = ratio[0] * w * (x[:, 1] - x[:, 3] / 2) + pad[0]  # pad width
                labels[:, 2] = ratio[1] * h * (x[:, 2] - x[:, 4] / 2) + pad[1]  # pad height
                labels[:, 3] = ratio[0] * w * (x[:, 1] + x[:, 3] / 2) + pad[0]
                labels[:, 4] = ratio[1] * h * (x[:, 2] + x[:, 4] / 2) + pad[1]

        if self.augment:
            # Augment imagespace
            if not self.mosaic:
                img, labels = random_affine(img, labels,
                                            degrees=hyp['degrees'],
                                            translate=hyp['translate'],
                                            scale=hyp['scale'],
                                            shear=hyp['shear'])

            # Augment colorspace
            augment_hsv(img, hgain=hyp['hsv_h'], sgain=hyp['hsv_s'], vgain=hyp['hsv_v'])

            # Apply cutouts
            # if random.random() < 0.9:
            #     labels = cutout(img, labels)

        nL = len(labels)  # number of labels
        if nL:
            # convert xyxy to xywh，仍然是像素为单位
            labels[:, 1:5] = xyxy2xywh(labels[:, 1:5])

            # Normalize coordinates 0 - 1，归一化到0-1
            labels[:, [2, 4]] /= img.shape[0]  # height
            labels[:, [1, 3]] /= img.shape[1]  # width

        if self.augment:
            # random left-right flip
            lr_flip = True
            if lr_flip and random.random() < 0.5:
                img = np.fliplr(img)
                if nL:
                    labels[:, 1] = 1 - labels[:, 1]

            # random up-down flip
            ud_flip = False
            if ud_flip and random.random() < 0.5:
                img = np.flipud(img)
                if nL:
                    labels[:, 2] = 1 - labels[:, 2]

        labels_out = torch.zeros((nL, 6))  # n行6列的Tensor，n对应图片中的目标数
        if nL:
            labels_out[:, 1:] = torch.from_numpy(labels)

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        # imgs, targets, paths, _
        return torch.from_numpy(img), labels_out, self.img_files[index], shapes

    @staticmethod
    def collate_fn(batch):
        """
        取数据的函数

        :param batch: batch是一批训练数据，batch[i]对应一张图片和图片标签，batch[i]是self.__getitem__()方法返回的结果
        :return:
        """
        img, label, path, shapes = zip(*batch)  # transposed
        # 假设batch_size=16，这里依次将16张图片的label[0]设置为i，这样当前图片中全部n个目标的label[0]都指到i
        for i, l in enumerate(label):
            l[:, 0] = i  # add target image index for build_targets()图片中有多少目标，l就有多少行，l的第一列都指到当前图片
        return torch.stack(img, 0), torch.cat(label, 0), path, shapes

    def __get_images__(self, imgs: dict, folders):
        """
        从COCO数据集的imgs中抽取出所有图片文件路径，保存到列表中返回

        :param imgs: COCO数据集的imgs对象，是一个字典
        :param folders: COCO数据集图片存储路径
        :return: 所有图片的绝对路径的列表
        """
        images = []
        if not isinstance(folders, list):
            folders = [folders]
        for k, v in imgs.items():
            file_name = v.get('file_name')
            for folder in folders:
                file_name = os.path.join(folder, file_name)
                if os.path.exists(file_name):
                    images.append(file_name)
                    break
        return images

    def __get_labels__(self, imgToAnns):
        """
        根据instance文件收集边框信息

        :param coco:
        :return:
        """
        labels = []
        for k, v in imgToAnns.items():
            # k是图片id
            # v是图片中的待检测目标信息，因为一张图片中包含多个目标，因此v是一个列表
            bboxs = []
            for obj in v:
                # obj是一个字典
                img_id = obj.get('image_id')
                cat_id = obj.get('category_id')
                bbox = obj.get('bbox')
                bboxs.append([img_id, cat_id].extend(bbox))
            labels.append(bboxs)
        return labels

    def load_image(self, index):
        """
        加载指定索引的图片，如果图片大于512，则缩小到512，如果图片小于512且开启了图像增强，则保证长宽比不变的同时将最大边放大到512

        :param self: 数据集，Dataset子类
        :param index: 图片索引
        :return: 缩放后的图片，（原图高、宽），缩放后图片的宽、高
        """
        # loads 1 image from dataset, returns img, original hw, resized hw

        img_path = self.img_files[index]
        img = cv2.imread(img_path)  # BGR
        assert img is not None, 'Image Not Found ' + img_path
        h0, w0 = img.shape[:2]  # orig hw
        r = self.img_size / max(h0, w0)  # resize image to img_size
        if r < 1 or (self.augment and r != 1):  # always resize down, only resize up if training with augmentation
            interp = cv2.INTER_AREA if r < 1 and not self.augment else cv2.INTER_LINEAR
            img = cv2.resize(img, (int(w0 * r), int(h0 * r)), interpolation=interp)
        return img, (h0, w0), img.shape[:2]  # img, hw_original, hw_resized


def load_mosaic(self, index):
    """
    将4张图片拼接成一张图片

    :param self:
    :param index:
    :return:
    """
    # loads images in a mosaic, https://www.cnblogs.com/wujianming-110117/p/12806502.html

    labels4 = []
    s = self.img_size
    xc, yc = [int(random.uniform(s * 0.5, s * 1.5)) for _ in range(2)]  # mosaic center x, y
    indices = [index] + [random.randint(0, len(self.labels) - 1) for _ in
                         range(3)]  # 3 additional image indices，随机3张附加图片
    for i, index in enumerate(indices):
        # Load image
        img, _, (h, w) = load_image(self, index)

        # place img in img4
        if i == 0:  # top left
            img4 = np.full((s * 2, s * 2, img.shape[2]), 114, dtype=np.uint8)  # base image with 4 tiles
            x1a, y1a, x2a, y2a = max(xc - w, 0), max(yc - h, 0), xc, yc  # xmin, ymin, xmax, ymax (large image)
            x1b, y1b, x2b, y2b = w - (x2a - x1a), h - (y2a - y1a), w, h  # xmin, ymin, xmax, ymax (small image)
        elif i == 1:  # top right
            x1a, y1a, x2a, y2a = xc, max(yc - h, 0), min(xc + w, s * 2), yc
            x1b, y1b, x2b, y2b = 0, h - (y2a - y1a), min(w, x2a - x1a), h
        elif i == 2:  # bottom left
            x1a, y1a, x2a, y2a = max(xc - w, 0), yc, xc, min(s * 2, yc + h)
            x1b, y1b, x2b, y2b = w - (x2a - x1a), 0, max(xc, w), min(y2a - y1a, h)
        elif i == 3:  # bottom right
            x1a, y1a, x2a, y2a = xc, yc, min(xc + w, s * 2), min(s * 2, yc + h)
            x1b, y1b, x2b, y2b = 0, 0, min(w, x2a - x1a), min(y2a - y1a, h)

        img4[y1a:y2a, x1a:x2a] = img[y1b:y2b, x1b:x2b]  # img4[ymin:ymax, xmin:xmax]
        padw = x1a - x1b
        padh = y1a - y1b

        # Load labels
        label_path = self.label_files[index]
        if os.path.isfile(label_path):
            x = self.labels[index]
            if x is None:  # labels not preloaded
                with open(label_path, 'r') as f:
                    x = np.array([x.split() for x in f.read().splitlines()], dtype=np.float32)

            if x.size > 0:
                # Normalized xywh to pixel xyxy format
                labels = x.copy()
                labels[:, 1] = w * (x[:, 1] - x[:, 3] / 2) + padw
                labels[:, 2] = h * (x[:, 2] - x[:, 4] / 2) + padh
                labels[:, 3] = w * (x[:, 1] + x[:, 3] / 2) + padw
                labels[:, 4] = h * (x[:, 2] + x[:, 4] / 2) + padh
            else:
                labels = np.zeros((0, 5), dtype=np.float32)
            labels4.append(labels)

    # Concat/clip labels
    if len(labels4):
        labels4 = np.concatenate(labels4, 0)
        # np.clip(labels4[:, 1:] - s / 2, 0, s, out=labels4[:, 1:])  # use with center crop
        np.clip(labels4[:, 1:], 0, 2 * s, out=labels4[:, 1:])  # use with random_affine

    # Augment
    # img4 = img4[s // 2: int(s * 1.5), s // 2:int(s * 1.5)]  # center crop (WARNING, requires box pruning)
    img4, labels4 = random_affine(img4, labels4,
                                  degrees=self.hyp['degrees'] * 1,
                                  translate=self.hyp['translate'] * 1,
                                  scale=self.hyp['scale'] * 1,
                                  shear=self.hyp['shear'] * 1,
                                  border=-s // 2)  # border to remove

    return img4, labels4


def loadCOCO(coco_folder: str):
    pass


def coco2darknet(train_image_folder=None, test_image_folder=None, val_image_folder=None,
                 instance_annotations_files: list = None, dest_folder: str = None):
    """
    根据COCO数据集生成Darknet数据集

    darknet数据集包括
    图片路径 ： image_folder
    图片中物体标签： label_folder

    训练用图片集： train_image.txt
    测试用图片集： test_image.txt

    :param val_image_folder:
    :param test_image_folder:
    :param train_image_folder:
    :param instance_annotations_files: coco数据集根目录，是
    :param dest_folder: 生成的darknet数据集保存目录
    :return:
    """
    if isinstance(instance_annotations_files, str):
        instance_annotations_files = [instance_annotations_files]

    dest_label_train_folder = os.path.join(dest_folder, 'labels/train')
    dest_label_test_folder = os.path.join(dest_folder, 'labels/test')
    dest_label_val_folder = os.path.join(dest_folder, 'labels/val')
    dest_image_folder = os.path.join(dest_folder, 'images')
    os.makedirs(dest_label_train_folder, exist_ok=True)
    os.makedirs(dest_image_folder, exist_ok=True)
    os.makedirs(dest_label_test_folder, exist_ok=True)
    os.makedirs(dest_label_val_folder, exist_ok=True)

    # 一般COCO数据集目标检测有两个注释文件，分别为instances_train2017.json和instances_val2017.json
    for anns_file in instance_annotations_files:
        assert os.path.exists(anns_file), f"annotations文件不存在，文件路径：{anns_file}"
        if 'train' in instance_annotations_files:
            dataset_type = 'train'
            current_image_folder = train_image_folder
            current_dest_label_folder = dest_label_train_folder
        elif 'test' in instance_annotations_files:
            dataset_type = 'test'
            current_image_folder = test_image_folder
            current_dest_label_folder = dest_label_test_folder
        else:
            dataset_type = 'val'
            current_image_folder = val_image_folder
            current_dest_label_folder = dest_label_val_folder
        coco = COCO(anns_file)
        txt_imgpath = f'{dataset_type}_image.txt'
        txt_labelpath = f'{dataset_type}_label.txt'
        images = set()

        for k, v in tqdm(coco.anns.items()):  # 遍历所有的annotations
            anns_id = k
            seg_coor_list: list = v.get('segmentation')  # 二维列表，一个物体可能有多个多边形组成
            img_id: int = v.get('image_id')
            bbox: list = v.get('bbox')
            category_id: int = v.get('category_id')
            category = coco.cats.get(category_id)  # 根据category_id拿到具体的分类
            # 根据img_id拿到对应的image对象
            image = coco.imgs.get(img_id)
            # 获取图片的绝对路径
            img_file = os.path.join(current_image_folder, image.get('file_name'))
            # 检测本地图片是否存在
            if not os.path.exists(img_file):
                temp_ = os.path.join(train_image_folder, os.path.basename(img_file))
                if os.path.exists(temp_):
                    print(f'{img_file} 所在文件夹错误，文件位于{temp_}')
                temp_ = os.path.join(val_image_folder, os.path.basename(img_file))
                if os.path.exists(temp_):
                    print(f'{img_file} 所属文件夹错误，文件位于{temp_}')
                print(f'{img_file} 不存在')
                continue
            images.add(img_file)  # 将图片添加到图片集中，集合会自动去重
            img_height = image.get('height')
            img_width = image.get('width')
            img_url = image.get('coco_url')

            # 将bbox归一化到0~1
            bbox[0] /= img_width
            bbox[2] /= img_width
            bbox[1] /= img_height
            bbox[3] /= img_height

            dest_label_filename = os.path.splitext(image.get('file_name'))[0] + '.txt'
            dest_label_file = os.path.join(current_dest_label_folder, dest_label_filename)

            with open(dest_label_file, 'a+') as f:  # 写labels文件
                f.write(f'{category_id} {bbox[0]:8.6f} {bbox[1]:8.6f} {bbox[2]:8.6f} {bbox[3]:8.6f}\n')
        fo.writeLines(txt_imgpath, list(images))  # 写训练图片 集合

# coco2darknet(train_image_folder=r'D:\Users\pycharm\face\data\train2017',
#              test_image_folder=r'D:\Users\pycharm\face\data\test2017',
#              val_image_folder=r'D:\Users\pycharm\face\data\val2017',
#              instance_annotations_files=[  # r'D:\Users\pycharm\face\data\annotations\instances_train2017.json',
#                  r'D:\Users\pycharm\face\data\annotations\instances_val2017.json'],
#              dest_folder=r'D:\Users\pycharm\face\data\dark')

# data = DataSet_YOLO(image_folder=r'D:\Users\pycharm\face\data\train2017',
#                     instance_file=r'D:\Users\pycharm\face\data\annotations\instances_train2017.json')
