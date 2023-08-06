import os
import argparse
from yangke.objDetect.obj_detect import *
from yangke.objDetect.models import *
import yangke.objDetect.yolo_test as test
from yangke.base import get_settings
from yangke.dataset.loadStandardDataset import DataSet_YOLO
import numpy as np
import random
import math
import torch.backends.cudnn as cudnn
import torch
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler
import torch.distributed as dist
from torch.utils.data import Dataset
import glob
from PIL import Image, ExifTags
from tqdm import tqdm
from copy import deepcopy
import matplotlib.pyplot as plt

# from .yolo_test import test

# Get orientation exif tag
for orientation in ExifTags.TAGS.keys():
    if ExifTags.TAGS[orientation] == 'Orientation':
        break
hyp = {'giou': 3.54,  # giou loss gain
       'cls': 37.4,  # cls loss gain
       'cls_pw': 1.0,  # cls BCELoss positive_weight
       'obj': 64.3,  # obj loss gain (*=img_size/320 if img_size != 320)
       'obj_pw': 1.0,  # obj BCELoss positive_weight
       'iou_t': 0.225,  # iou training threshold
       'lr0': 0.01,  # initial learning rate (SGD=5E-3, Adam=5E-4)
       'lrf': 0.0005,  # final learning rate (with cos scheduler)
       'momentum': 0.937,  # SGD momentum
       'weight_decay': 0.000484,  # optimizer weight decay
       'fl_gamma': 0.0,  # focal loss gamma (efficientDet default is gamma=1.5)
       'hsv_h': 0.0138,  # image HSV-Hue augmentation (fraction)
       'hsv_s': 0.678,  # image HSV-Saturation augmentation (fraction)
       'hsv_v': 0.36,  # image HSV-Value augmentation (fraction)
       'degrees': 1.98 * 0,  # image rotation (+/- deg)
       'translate': 0.05 * 0,  # image translation (+/- fraction)
       'scale': 0.05 * 0,  # image scale (+/- gain)
       'shear': 0.641 * 0}  # image shear (+/- deg)
mixed_precision = False
wdir = 'weights' + os.sep
last = get_settings('aiTrain.save.lastModelFile')  # 最后一个迭代步的模型权值
best = get_settings('aiTrain.save.bestModelFile')  # 最有的模型权值
os.makedirs(os.path.dirname(last), exist_ok=True)  # 确保文件的目录存在
os.makedirs(os.path.dirname(best), exist_ok=True)
results_file = 'results.txt'

# Print focal loss if gamma > 0
if hyp['fl_gamma']:
    print('Using FocalLoss(gamma=%g)' % hyp['fl_gamma'])


def init_seeds(seed=100):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    # Remove randomness (may be slower on Tesla GPUs) # https://pytorch.org/docs/stable/notes/randomness.html
    if seed == 0:  # 下面两项设置只是为了加速
        cudnn.deterministic = True
        cudnn.benchmark = False


help_url = 'https://github.com/ultralytics/yolov3/wiki/Train-Custom-Data'


def exif_size(img):
    # Returns exif-corrected PIL size
    s = img.size  # (width, height)
    try:
        rotation = dict(img._getexif().items())[orientation]
        if rotation == 6:  # rotation 270
            s = (s[1], s[0])
        elif rotation == 8:  # rotation 90
            s = (s[1], s[0])
    except:
        pass

    return s


def random_affine(img, targets=(), degrees=10, translate=.1, scale=.1, shear=10, border=0):
    # torchvision.transforms.RandomAffine(degrees=(-10, 10), translate=(.1, .1), scale=(.9, 1.1), shear=(-10, 10))
    # https://medium.com/uruvideo/dataset-augmentation-with-random-homographies-a8f4b44830d4

    if targets is None:  # targets = [cls, xyxy]
        targets = []
    height = img.shape[0] + border * 2
    width = img.shape[1] + border * 2

    # Rotation and Scale
    R = np.eye(3)
    a = random.uniform(-degrees, degrees)
    # a += random.choice([-180, -90, 0, 90])  # add 90deg rotations to small rotations
    s = random.uniform(1 - scale, 1 + scale)
    R[:2] = cv2.getRotationMatrix2D(angle=a, center=(img.shape[1] / 2, img.shape[0] / 2), scale=s)

    # Translation
    T = np.eye(3)
    T[0, 2] = random.uniform(-translate, translate) * img.shape[0] + border  # x translation (pixels)
    T[1, 2] = random.uniform(-translate, translate) * img.shape[1] + border  # y translation (pixels)

    # Shear
    S = np.eye(3)
    S[0, 1] = math.tan(random.uniform(-shear, shear) * math.pi / 180)  # x shear (deg)
    S[1, 0] = math.tan(random.uniform(-shear, shear) * math.pi / 180)  # y shear (deg)

    # Combined rotation matrix
    M = S @ T @ R  # ORDER IS IMPORTANT HERE!!
    if (border != 0) or (M != np.eye(3)).any():  # image changed
        img = cv2.warpAffine(img, M[:2], dsize=(width, height), flags=cv2.INTER_LINEAR, borderValue=(114, 114, 114))

    # Transform label coordinates
    n = len(targets)
    if n:
        # warp points
        xy = np.ones((n * 4, 3))
        xy[:, :2] = targets[:, [1, 2, 3, 4, 1, 4, 3, 2]].reshape(n * 4, 2)  # x1y1, x2y2, x1y2, x2y1
        xy = (xy @ M.T)[:, :2].reshape(n, 8)

        # create new boxes
        x = xy[:, [0, 2, 4, 6]]
        y = xy[:, [1, 3, 5, 7]]
        xy = np.concatenate((x.min(1), y.min(1), x.max(1), y.max(1))).reshape(4, n).T

        # # apply angle-based reduction of bounding boxes
        # radians = a * math.pi / 180
        # reduction = max(abs(math.sin(radians)), abs(math.cos(radians))) ** 0.5
        # x = (xy[:, 2] + xy[:, 0]) / 2
        # y = (xy[:, 3] + xy[:, 1]) / 2
        # w = (xy[:, 2] - xy[:, 0]) * reduction
        # h = (xy[:, 3] - xy[:, 1]) * reduction
        # xy = np.concatenate((x - w / 2, y - h / 2, x + w / 2, y + h / 2)).reshape(4, n).T

        # reject warped points outside of image
        xy[:, [0, 2]] = xy[:, [0, 2]].clip(0, width)
        xy[:, [1, 3]] = xy[:, [1, 3]].clip(0, height)
        w = xy[:, 2] - xy[:, 0]
        h = xy[:, 3] - xy[:, 1]
        area = w * h
        area0 = (targets[:, 3] - targets[:, 1]) * (targets[:, 4] - targets[:, 2])
        ar = np.maximum(w / (h + 1e-16), h / (w + 1e-16))  # aspect ratio
        i = (w > 4) & (h > 4) & (area / (area0 + 1e-16) > 0.2) & (ar < 10)

        targets = targets[i]
        targets[:, 1:5] = xy[i]

    return img, targets


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


def augment_hsv(img, hgain=0.5, sgain=0.5, vgain=0.5):
    x = np.random.uniform(-1, 1, 3) * [hgain, sgain, vgain] + 1  # random gains
    img_hsv = (cv2.cvtColor(img, cv2.COLOR_BGR2HSV) * x).clip(None, 255).astype(np.uint8)
    np.clip(img_hsv[:, :, 0], None, 179, out=img_hsv[:, :, 0])  # inplace hue clip (0 - 179 deg)
    cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR, dst=img)  # no return needed

    # Histogram equalization
    # if random.random() < 0.2:
    #     for i in range(3):
    #         img[:, :, i] = cv2.equalizeHist(img[:, :, i])


def print_mutation(hyp, results, bucket=''):
    # Print mutation results to evolve.txt (for use with train.py --evolve)
    a = '%10s' * len(hyp) % tuple(hyp.keys())  # hyperparam keys
    b = '%10.3g' * len(hyp) % tuple(hyp.values())  # hyperparam values
    c = '%10.4g' * len(results) % results  # results (P, R, mAP, F1, test_loss)
    print('\n%s\n%s\nEvolved fitness: %s\n' % (a, b, c))

    if bucket:
        os.system('gsutil cp gs://%s/evolve.txt .' % bucket)  # download evolve.txt

    with open('evolve.txt', 'a') as f:  # append result
        f.write(c + b + '\n')
    x = np.unique(np.loadtxt('evolve.txt', ndmin=2), axis=0)  # load unique rows
    np.savetxt('evolve.txt', x[np.argsort(-fitness(x))], '%10.3g')  # save sort by fitness

    if bucket:
        os.system('gsutil cp evolve.txt gs://%s' % bucket)  # upload evolve.txt


class DarknetDataset(Dataset):  # for training/testing
    def __init__(self, path, label_folder=None, img_size=416, batch_size=16, augment=False, hyp=None,
                 rect=False,
                 image_weights=False,
                 cache_labels=True, cache_images=False, single_cls=False):
        """
        加载训练和测试数据集

        :param path:  train.txt文件的路径，该文件存储训练集图片的路径名，文件中每一行对应一张图片的路径；因为数据集中图片占用
        硬盘是最大的，一般图片只保存一份，而不同数据格式都引用到图片文件夹，这样就需要修改train.txt中图片的保存路径到真实路径，
        :param img_size:
        :param batch_size:
        :param augment:
        :param hyp:
        :param rect:
        :param image_weights:
        :param cache_labels:
        :param cache_images:
        :param single_cls:
        """
        path = str(Path(path))  # train2017.txt 的路径，train2017.txt中保存了coco图片的路径，这里我们直接给出图片路径
        assert os.path.isfile(path), 'File not found %s. See %s' % (path, help_url)
        with open(path, 'r') as f:
            self.img_files = [x.replace('/', os.sep) for x in f.read().splitlines()  # os-agnostic
                              if os.path.splitext(x)[-1].lower() in img_formats]
        # 这里需要删除不存在的图片对应的路径
        # for img_ in self.img_files.copy():
        #     if not os.path.exists(img_):
        #         self.img_files.remove(img_)

        if label_folder is None:
            # label_files是对应于self.img_files的标签文件，每一个都是'<img同名>.txt'文件
            self.label_files = [x.replace('images', 'labels').replace(os.path.splitext(x)[-1], '.txt')
                                for x in self.img_files]
        else:
            self.label_files = [os.path.join(label_folder, os.path.splitext(os.path.basename(x))[0] + '.txt') for x in
                                self.img_files]
        n = len(self.img_files)
        assert n > 0, 'No images found in %s. See %s' % (path, help_url)
        bi = np.floor(np.arange(n) / batch_size).astype(np.int)  # batch index
        nb = bi[-1] + 1  # number of batches

        self.n = n
        self.batch = bi  # batch index of image
        self.img_size = img_size
        self.augment = augment
        self.hyp = hyp
        self.image_weights = image_weights
        self.rect = False if image_weights else rect
        self.mosaic = self.augment and not self.rect  # load 4 images at a time into a mosaic镶嵌图案/马赛克 (only during training)

        # Rectangular Training  https://github.com/ultralytics/yolov3/issues/232
        if self.rect:
            # Read image shapes (wh)
            sp = path.replace('.txt', '.shapes')  # shapefile path
            try:
                with open(sp, 'r') as f:  # read existing shapefile
                    s = [x.split() for x in f.read().splitlines()]
                    assert len(s) == n, 'Shapefile out of sync'
            except:
                s = [exif_size(Image.open(f)) for f in tqdm(self.img_files, desc='Reading image shapes')]
                np.savetxt(sp, s, fmt='%g')  # overwrites existing (if any)

            # Sort by aspect ratio
            s = np.array(s, dtype=np.float64)
            ar = s[:, 1] / s[:, 0]  # aspect ratio
            i = ar.argsort()
            self.img_files = [self.img_files[i] for i in i]
            self.label_files = [self.label_files[i] for i in i]
            self.shapes = s[i]  # wh
            ar = ar[i]

            # Set training image shapes
            shapes = [[1, 1]] * nb
            for i in range(nb):
                ari = ar[bi == i]
                mini, maxi = ari.min(), ari.max()
                if maxi < 1:
                    shapes[i] = [maxi, 1]
                elif mini > 1:
                    shapes[i] = [1, 1 / mini]

            self.batch_shapes = np.ceil(np.array(shapes) * img_size / 64.).astype(np.int) * 64

        # Preload labels (required for weighted CE training)
        self.imgs = [None] * n  # 图片
        self.labels = [None] * n  # 图片对应的标签
        if cache_labels or image_weights:  # cache labels for faster training
            self.labels = [np.zeros((0, 5))] * n
            extract_bounding_boxes = False
            create_datasubset = False
            pbar = tqdm(self.label_files, desc='Caching labels')  # 进度条
            nm, nf, ne, ns, nd = 0, 0, 0, 0, 0  # number missing, found, empty, datasubset, duplicate
            for i, file in enumerate(pbar):
                try:
                    with open(file, 'r') as f:
                        l = np.array([x.split() for x in f.read().splitlines()], dtype=np.float32)
                except:
                    nm += 1  # print('missing labels for image %s' % self.img_files[i])  # file missing
                    continue

                if l.shape[0]:  # 分类编号 x_center ycenter width height
                    assert l.shape[1] == 5, '> 5 label columns: %s' % file  # 每一行有且只有五个参数
                    assert (l >= 0).all(), 'negative labels: %s' % file  # 分类号不能为负数
                    assert (l[:, 1:] <= 1).all(), 'non-normalized or out of bounds coordinate labels: %s' % file
                    if np.unique(l, axis=0).shape[0] < l.shape[0]:  # duplicate rows
                        nd += 1  # print('WARNING: duplicate rows in %s' % self.label_files[i])  # duplicate rows
                    if single_cls:
                        l[:, 0] = 0  # force dataset into single-class mode
                    self.labels[i] = l
                    nf += 1  # file found

                    # Extract object detection boxes for a second stage classifier
                    if extract_bounding_boxes:
                        p = Path(self.img_files[i])
                        img = cv2.imread(str(p))
                        h, w = img.shape[:2]
                        for j, x in enumerate(l):
                            f = '%s%sclassifier%s%g_%g_%s' % (p.parent.parent, os.sep, os.sep, x[0], j, p.name)
                            if not os.path.exists(Path(f).parent):
                                os.makedirs(Path(f).parent)  # make new output folder

                            b = x[1:] * [w, h, w, h]  # box
                            b[2:] = b[2:].max()  # rectangle to square
                            b[2:] = b[2:] * 1.3 + 30  # pad
                            b = xywh2xyxy(b.reshape(-1, 4)).ravel().astype(np.int)

                            b[[0, 2]] = np.clip(b[[0, 2]], 0, w)  # clip boxes outside of image
                            b[[1, 3]] = np.clip(b[[1, 3]], 0, h)
                            assert cv2.imwrite(f, img[b[1]:b[3], b[0]:b[2]]), 'Failure extracting classifier boxes'
                else:
                    ne += 1  # print('empty labels for image %s' % self.img_files[i])  # file empty
                    # os.system("rm '%s' '%s'" % (self.img_files[i], self.label_files[i]))  # remove

                pbar.desc = 'Caching labels (%g found, %g missing, %g empty, %g duplicate, for %g images)' % (
                    nf, nm, ne, nd, n)
            assert nf > 0, 'No labels found in %s. See %s' % (os.path.dirname(file) + os.sep, help_url)

        # Cache images into memory for faster training (WARNING: large datasets may exceed system RAM)
        if cache_images:  # if training
            gb = 0  # Gigabytes of cached images
            pbar = tqdm(range(len(self.img_files)), desc='Caching images')
            self.img_hw0, self.img_hw = [None] * n, [None] * n
            for i in pbar:  # max 10k images
                self.imgs[i], self.img_hw0[i], self.img_hw[i] = load_image(self, i)  # img, hw_original, hw_resized
                gb += self.imgs[i].nbytes
                pbar.desc = 'Caching images (%.1fGB)' % (gb / 1E9)

        # Detect corrupted images https://medium.com/joelthchao/programmatically-detect-corrupted-image-8c1b2006c3d3
        detect_corrupted_images = False
        if detect_corrupted_images:
            from skimage import io  # conda install -c conda-forge scikit-image
            for file in tqdm(self.img_files, desc='Detecting corrupted images'):
                try:
                    _ = io.imread(file)
                except:
                    print('Corrupted image detected: %s' % file)

    def __len__(self):
        return len(self.img_files)

    # def __iter__(self):
    #     self.count = -1
    #     print('ran dataset iter')
    #     #self.shuffled_vector = np.random.permutation(self.nF) if self.augment else np.arange(self.nF)
    #     return self

    def __getitem__(self, index):
        if self.image_weights:
            index = self.indices[index]

        hyp = self.hyp
        if self.mosaic:
            # Load mosaic
            img, labels = load_mosaic(self, index)
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


def plot_results(start=0, stop=0, bucket='', id=()):  # from utils.utils import *; plot_results()
    # Plot training 'results*.txt' as seen in https://github.com/ultralytics/yolov3#training
    fig, ax = plt.subplots(2, 5, figsize=(12, 6))
    ax = ax.ravel()
    s = ['GIoU', 'Objectness', 'Classification', 'Precision', 'Recall',
         'val GIoU', 'val Objectness', 'val Classification', 'mAP@0.5', 'F1']
    if bucket:
        os.system('rm -rf storage.googleapis.com')
        files = ['https://storage.googleapis.com/%s/results%g.txt' % (bucket, x) for x in id]
    else:
        files = glob.glob('results*.txt') + glob.glob('../../Downloads/results*.txt')
    for f in sorted(files):
        try:
            results = np.loadtxt(f, usecols=[2, 3, 4, 8, 9, 12, 13, 14, 10, 11], ndmin=2).T
            n = results.shape[1]  # number of rows
            x = range(start, min(stop, n) if stop else n)
            for i in range(10):
                y = results[i, x]
                if i in [0, 1, 2, 5, 6, 7]:
                    y[y == 0] = np.nan  # dont show zero loss values
                    # y /= y[0]  # normalize
                ax[i].plot(x, y, marker='.', label=Path(f).stem, linewidth=2, markersize=8)
                ax[i].set_title(s[i])
                if i in [5, 6, 7]:  # share train and val loss y axes
                    ax[i].get_shared_y_axes().join(ax[i], ax[i - 5])
        except:
            print('Warning: Plotting error for %s, skipping file' % f)

    fig.tight_layout()
    ax[1].legend()
    fig.savefig('results.png', dpi=200)


def load_image(self, index):
    """
    加载指定索引的图片，如果图片大于512，则缩小到512，如果图片小于512且开启了图像增强，则保证长宽比不变的同时将最大边放大到512

    :param self: 数据集，Dataset子类
    :param index: 图片索引
    :return: 缩放后的图片，（原图高、宽），缩放后图片的宽、高
    """
    # loads 1 image from dataset, returns img, original hw, resized hw
    img = self.imgs[index]
    if img is None:  # not cached
        img_path = self.img_files[index]
        img = cv2.imread(img_path)  # BGR
        assert img is not None, 'Image Not Found ' + img_path
        h0, w0 = img.shape[:2]  # orig hw
        r = self.img_size / max(h0, w0)  # resize image to img_size
        if r < 1 or (self.augment and r != 1):  # always resize down, only resize up if training with augmentation
            interp = cv2.INTER_AREA if r < 1 and not self.augment else cv2.INTER_LINEAR
            img = cv2.resize(img, (int(w0 * r), int(h0 * r)), interpolation=interp)
        return img, (h0, w0), img.shape[:2]  # img, hw_original, hw_resized
    else:
        return self.imgs[index], self.img_hw0[index], self.img_hw[index]  # img, hw_original, hw_resized


def parse_data_cfg(path):
    # Parses the data configuration file
    if not os.path.exists(path) and os.path.exists('data' + os.sep + path):  # add data/ prefix if omitted
        path = 'data' + os.sep + path

    with open(path, 'r') as f:
        lines = f.readlines()

    options = dict()
    for line in lines:
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue
        key, val = line.split('=')
        options[key.strip()] = val.strip()

    return options


def labels_to_image_weights(labels, nc=80, class_weights=np.ones(80)):
    # Produces image weights based on class mAPs
    n = len(labels)
    class_counts = np.array([np.bincount(labels[i][:, 0].astype(np.int), minlength=nc) for i in range(n)])
    image_weights = (class_weights.reshape(1, nc) * class_counts).sum(1)
    # index = random.choices(range(n), weights=image_weights, k=1)  # weight image sample
    return image_weights


def labels_to_class_weights(labels, nc=80):
    """
    计算分类任务时，训练数据集中每一类物体在所有标注物体中所占的比重。例如：训练数据中，有99个物体为'Person'，有1个物体为'Cat',
    则Person的比重（weight）为99%，Cat的比重为1%，这是典型的不平衡数据集。

    标签类别比重labels_to_class_weights是类别比重的倒数。

    该函数返回归一化后的数组。

    :param labels: labels标签
    :param nc: 类别数量
    :return: 归一化后的标签类别比重，目标数量越少，对应的权值越大
    """
    # Get class weights (inverse frequency) from training labels
    if labels[0] is None:  # no labels loaded
        return torch.Tensor()

    labels = np.concatenate(labels, 0)  # labels.shape = (866643, 5) for COCO
    classes = labels[:, 0].astype(np.int)  # labels = [class xywh]
    weights = np.bincount(classes, minlength=nc)  # occurences per class

    # Prepend gridpoint count (for uCE trianing)
    # gpi = ((320 / 32 * np.array([1, 2, 4])) ** 2 * 3).sum()  # gridpoints per image
    # weights = np.hstack([gpi * len(labels)  - weights.sum() * 9, weights * 9]) ** 0.5  # prepend gridpoints to start

    weights[weights == 0] = 1  # replace empty bins with 1，使得求倒数时分母不会为0
    weights = 1 / weights  # number of targets per class
    weights /= weights.sum()  # normalize
    return torch.from_numpy(weights)


class ModelEMA:
    """ Model Exponential Moving Average from https://github.com/rwightman/pytorch-image-models
    Keep a moving average of everything in the model state_dict (parameters and buffers).
    This is intended to allow functionality like
    https://www.tensorflow.org/api_docs/python/tf/train/ExponentialMovingAverage
    A smoothed version of the weights is necessary for some training schemes to perform well.
    E.g. Google's hyper-params for training MNASNet, MobileNet-V3, EfficientNet, etc that use
    RMSprop with a short 2.4-3 epoch decay period and slow LR decay rate of .96-.99 requires EMA
    smoothing of weights to match results. Pay attention to the decay constant you are using
    relative to your update count per epoch.
    To keep EMA from using GPU resources, set device='cpu'. This will save a bit of memory but
    disable validation of the EMA weights. Validation will have to be done manually in a separate
    process, or after the training stops converging.
    This class is sensitive where it is initialized in the sequence of model init,
    GPU assignment and distributed training wrappers.
    I've tested with the sequence in my own train.py for torch.DataParallel, apex.DDP, and single-GPU.
    累积移动平均 指数滑动平均
    """

    def __init__(self, model, decay=0.9999, device=''):
        # make a copy of the model for accumulating moving average of weights 累计移动平均
        self.ema = deepcopy(model)
        self.ema.eval()
        self.updates = 0  # number of EMA updates
        self.decay = lambda x: decay * (1 - math.exp(-x / 2000))  # decay exponential ramp (to help early epochs)
        self.device = device  # perform ema on different device from model if set
        if device:
            self.ema.to(device=device)
        for p in self.ema.parameters():
            p.requires_grad_(False)

    def update(self, model):
        self.updates += 1
        d = self.decay(self.updates)
        with torch.no_grad():
            if type(model) in (nn.parallel.DataParallel, nn.parallel.DistributedDataParallel):
                msd, esd = model.module.state_dict(), self.ema.module.state_dict()
            else:
                msd, esd = model.state_dict(), self.ema.state_dict()

            for k, v in esd.items():  # 这里要更新esd还是msd中的参数，通过对比测试看哪种有效果
                if v.dtype.is_floating_point:
                    v *= d
                    v += (1. - d) * msd[k].detach()

    def update_attr(self, model):
        # Assign attributes (which may change during training)
        for k in model.__dict__.keys():
            if not k.startswith('_'):
                setattr(self.ema, k, getattr(model, k))


class FocalLoss(nn.Module):
    # Wraps focal loss around existing loss_fcn(), i.e. criteria = FocalLoss(nn.BCEWithLogitsLoss(), gamma=1.5)
    def __init__(self, loss_fcn, gamma=1.5, alpha=0.25):
        super(FocalLoss, self).__init__()
        self.loss_fcn = loss_fcn  # must be nn.BCEWithLogitsLoss()
        self.gamma = gamma
        self.alpha = alpha
        self.reduction = loss_fcn.reduction
        self.loss_fcn.reduction = 'none'  # required to apply FL to each element

    def forward(self, pred, true):
        loss = self.loss_fcn(pred, true)
        # p_t = torch.exp(-loss)
        # loss *= self.alpha * (1.000001 - p_t) ** self.gamma  # non-zero power for gradient stability

        # TF implementation https://github.com/tensorflow/addons/blob/v0.7.1/tensorflow_addons/losses/focal_loss.py
        pred_prob = torch.sigmoid(pred)  # prob from logits
        p_t = true * pred_prob + (1 - true) * (1 - pred_prob)
        alpha_factor = true * self.alpha + (1 - true) * (1 - self.alpha)
        modulating_factor = (1.0 - p_t) ** self.gamma
        loss *= alpha_factor * modulating_factor

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:  # 'none'
            return loss


def wh_iou(wh1, wh2):
    """
    计算边框的IoU损失值，这里假设wh1与wh2的中心点重合，因此，无须边框位置坐标即可计算IoU

    :param wh1: YOLOLayer的anchors_vec，3行代表3个anchor_vec
    :param wh2: 真实目标的边框宽和高，n行代表n个目标
    :return:
    """
    # Returns the nxm IoU matrix. wh1 is nx2, wh2 is mx2
    wh1 = wh1[:, None]  # [N,1,2]
    wh2 = wh2[None]  # [1,M,2]
    inter = torch.min(wh1, wh2).prod(dim=2)  # [N,M], prod()将元素在第二个维度相乘，就是面积=w*h
    return inter / (wh1.prod(2) + wh2.prod(2) - inter)  # iou = inter / (area1 + area2 - inter)


def build_targets(p, targets, model):
    """
    通过YOLO层的输出，构建待匹配的目标，返回待检测目标的实际分类号、边框(xywh),索引(img_idx,anchor_idx,gridy,gridx)
    和对应YOLO层的anchor box宽和高

    根据YOLO层输出图像的大小，将targets与预设边框进行对比计算IoU值,对IoU过大的预设边框进行剔除，返回预设边框的信息列表。
    YOLO层的输出图像大小=原始图像大小/YOLO层的stride。YOLO层的stride从上到下可以取值32, 16, 8, 4, 2。

    :param p: YOLOLayers层的输出，yolov3-tiny有两个YOLOLayer层，yolov3有三个，yolov3-tiny第一个输出的shape=[16,3,16,16,85]
    =[batch_size, num of anchor, img_w, img_h, num of output]，该方法只用到了输出的图像大小，即p.shape[2]和p.shape[3]。
    并基于该图像大小，把targets中归一化的box转换为对应大小的box。
    :param targets: 形状为(n, 6)，6列分别对应[img_idx, class, x, y, w, h]，img_idx是目标所在图片在当前批中的编号
    :param model:
    :return: 最优预设边框的信息(分类,边框(xywh),索引(img_idx,anchor_idx,gridx,gridy), anchor_vec)
    """
    # targets = [image, class, x, y, w, h]

    nt = targets.shape[0]  # number of targets,目标数量
    tcls, tbox, indices, av = [], [], [], []
    reject, use_all_anchors = True, True
    gain = torch.ones(6, device=targets.device)  # normalized to gridspace gain

    # m = list(model.modules())[-1]
    # for i in range(m.nl):
    #    anchors = m.anchors[i]
    multi_gpu = type(model) in (nn.parallel.DataParallel, nn.parallel.DistributedDataParallel)
    for i, j in enumerate(model.yolo_layers):
        # get number of grid points and anchor vec for this yolo layer
        # 当前YOLO层上的anchor box对应的宽高，其值等于原始anchor box宽高/YOLO层的stride
        anchors = model.module.module_list[j].anchor_vec if multi_gpu else model.module_list[j].anchor_vec
        # anchors来源是YOLOLayers层的
        # iou of targets-anchors
        gain[2:] = torch.tensor(p[i].shape)[[3, 2, 3, 2]]  # xyxy gain
        # 下面操作的矩阵形状：(n,6) * (6) = (n,6)*(n,6) = (n,6) 这里的乘法是element-wise乘法，即对应位置相乘
        # 相当于把targets中的目标区域放大为预测结果相同尺度，targets中的xywh是归一化的，得到的t是当前yolo层图像的尺寸
        t, a = targets * gain, []  # a用来储存预设边框的索引，有3个预设边框，则a的每一项可以取值为0,1,2
        gwh = t[:, 4:6]  # 拿到targets对应到当前YOLO层上的宽和高
        if nt > 0:  # 如果目标数量大于0
            # 计算图片中n个目标在3个anchor框上的IoU
            iou = wh_iou(anchors, gwh)  # iou(3,n) = wh_iou(anchors(3,2), gwh(n,2))

            if use_all_anchors:
                na = anchors.shape[0]  # number of anchors
                # 下面令a=tensor([[0], [1], [2]]),torch.arange()类似于range()，view(-1,1)将行向量变形为列向量
                # a储存所有的预设边框编号，因为一个目标处可以存在na个预设边框，所以一共有na*nt个边框区域
                # 这些边框区域都可能包含当前targets对应的目标，为了选出当前位置最优的边框，分别计算预设边框与target_box的IoU
                # 从而进行挑选。或者不挑选，使用所有预设边框进行后续计算
                # 问题：target中的边框就是最优边框，为什么不直接使用target_box
                # 解答：target中的边框是实际边框，我们的目标是要挑选出与实际边框交并比最高的anchor box，然后基于挑选出的
                # anchor box做进一步的位置回归。在实际的目标检测过程中，我们是没有target数据的，因此不能直接使用target边框。
                a = torch.arange(na).view(-1, 1)
                a = a.repeat(1, nt).view(-1)
                t = t.repeat(na, 1)
            else:  # use best anchor only
                iou, a = iou.max(0)  # best iou and anchor

            # reject anchors below iou_thres (OPTIONAL, increases P, lowers R)
            if reject:  # 这里从预设边框中删除与目标边框IoU损失过大的预设边框，如果不删除，所有预设边框都会进行后续计算
                j = iou.view(-1) > model.hyp['iou_t']  # iou threshold hyperparameter
                # t储存了待检测目标的[img_idx, class, 交并比最高的anchor box的x,y,w,h]，a储存交并比最高的anchor box对应
                # 的索引，如YOLO层有3个anchor box，则索引取值范围为[0, 2]
                t, a = t[j], a[j]

        # Indices
        b, c = t[:, :2].long().t()  # target image, class
        gxy = t[:, 2:4]  # grid x, y
        gwh = t[:, 4:6]  # grid w, h
        gi, gj = gxy.long().t()  # grid x, y indices,这里将float类型的xy坐标转换为整形, t()为转置矩阵
        indices.append((b, a, gj, gi))  # 目标所在图片在当前批中的索引，anchor编号，目标所在格子的y和x编号

        # Box
        gxy -= gxy.floor()  # xy 这里为什么减去box原来的值了，可能有问题
        tbox.append(torch.cat((gxy, gwh), dim=1))  # xywh (grids) 按列拼接gxy和gwh为 xywh
        av.append(anchors[a])  # anchors[a]将预设边框索引转换为预设边框大小

        # Class
        tcls.append(c)
        if c.shape[0]:  # if any targets
            assert c.max() < model.nc, 'Model accepts %g classes labeled from 0-%g, however you labelled a class %g. ' \
                                       'See https://github.com/ultralytics/yolov3/wiki/Train-Custom-Data' % (
                                           model.nc, model.nc - 1, c.max())
    # 返回
    return tcls, tbox, indices, av  # 分类,边框(xywh),索引(img_idx,anchor_idx,gridy,gridx), anchor_vec


def smooth_BCE(eps=0.1):  # https://github.com/ultralytics/yolov3/issues/238#issuecomment-598028441
    """
    https://arxiv.org/pdf/1902.04103.pdf 公式3
    https://github.com/ultralytics/yolov3/issues/238#issuecomment-598028441
    在分类任务中，target的分类结果通常是一个one-hot数组，在正确分类上的值为1，在错误分类上的值为0；上述论文认为这
    会鼓励模型在正确分类上过于自信，从而导致过拟合。因此，提出稍微减小正确分类的值，而增加其他值。

    :param eps: 公式3中的epsilon
    :return: 正确分类的one-hot值，错误分类的one-hot值
    """
    # return positive, negative label smoothing BCE targets
    return 1.0 - 0.5 * eps, 0.5 * eps


def bbox_iou(box1, box2, x1y1x2y2=True, GIoU=False, DIoU=False, CIoU=False):
    """
    box1和box2的形状是(n, 4)，每一行的4个参数对应一个边框，且box1和box2的行与行相互对应。
    如果GIoU=DIoU=CIoU=False，则返回IoU值。

    :param box1:
    :param box2:
    :param x1y1x2y2: True则是xyxy格式的边框，False则是xywh格式的边框
    :param GIoU: 需要计算GIoU，则将该参数设置为True，优先级最高，该值为True，则忽略DIoU和CIoU参数
    :param DIoU: 需要计算DIoU，则将该参数设置为True，优先级其次，该值为True，则忽略CIOU参数
    :param CIoU: 需要计算CIoU，则将该参数设置为True，优先级最低
    :return: GIoU值，因为输入是n对边框，所以返回的是每一对边框的指定IoU值，返回类型是长度为n的Tensor
    """
    # Returns the IoU of box1 to box2. box1 is 4, box2 is nx4
    box1 = box1.t()
    box2 = box2.t()

    # Get the coordinates of bounding boxes
    if x1y1x2y2:  # x1, y1, x2, y2 = box1
        b1_x1, b1_y1, b1_x2, b1_y2 = box1[0], box1[1], box1[2], box1[3]
        b2_x1, b2_y1, b2_x2, b2_y2 = box2[0], box2[1], box2[2], box2[3]
    else:  # transform from xywh to xyxy
        b1_x1, b1_x2 = box1[0] - box1[2] / 2, box1[0] + box1[2] / 2
        b1_y1, b1_y2 = box1[1] - box1[3] / 2, box1[1] + box1[3] / 2
        b2_x1, b2_x2 = box2[0] - box2[2] / 2, box2[0] + box2[2] / 2
        b2_y1, b2_y2 = box2[1] - box2[3] / 2, box2[1] + box2[3] / 2

    # Intersection area
    inter = (torch.min(b1_x2, b2_x2) - torch.max(b1_x1, b2_x1)).clamp(0) * \
            (torch.min(b1_y2, b2_y2) - torch.max(b1_y1, b2_y1)).clamp(0)

    # Union Area
    w1, h1 = b1_x2 - b1_x1, b1_y2 - b1_y1
    w2, h2 = b2_x2 - b2_x1, b2_y2 - b2_y1
    union = (w1 * h1 + 1e-16) + w2 * h2 - inter

    iou = inter / union  # iou
    if GIoU or DIoU or CIoU:
        cw = torch.max(b1_x2, b2_x2) - torch.min(b1_x1, b2_x1)  # convex (smallest enclosing box) width
        ch = torch.max(b1_y2, b2_y2) - torch.min(b1_y1, b2_y1)  # convex height
        if GIoU:  # Generalized IoU https://arxiv.org/pdf/1902.09630.pdf
            c_area = cw * ch + 1e-16  # convex area
            return iou - (c_area - union) / c_area  # GIoU
        if DIoU or CIoU:  # Distance or Complete IoU https://arxiv.org/abs/1911.08287v1
            # convex diagonal squared
            c2 = cw ** 2 + ch ** 2 + 1e-16
            # centerpoint distance squared
            rho2 = ((b2_x1 + b2_x2) - (b1_x1 + b1_x2)) ** 2 / 4 + ((b2_y1 + b2_y2) - (b1_y1 + b1_y2)) ** 2 / 4
            if DIoU:
                return iou - rho2 / c2  # DIoU
            elif CIoU:  # https://github.com/Zzh-tju/DIoU-SSD-pytorch/blob/master/utils/box/box_utils.py#L47
                v = (4 / math.pi ** 2) * torch.pow(torch.atan(w2 / h2) - torch.atan(w1 / h1), 2)
                with torch.no_grad():
                    alpha = v / (1 - iou + v)
                return iou - (rho2 / c2 + v * alpha)  # CIoU

    return iou


def strip_optimizer(f='weights/last.pt'):  # from utils.utils import *; strip_optimizer()
    # Strip optimizer from *.pt files for lighter files (reduced by 2/3 size)
    x = torch.load(f, map_location=torch.device('cpu'))
    x['optimizer'] = None
    torch.save(x, f)


def compute_loss(p, targets, model):  # predictions, targets, model
    """
    https://www.cnblogs.com/HIKSEEKER/p/12831744.html
    根据预测结果，实际目标和模型计算损失

    :param p: 预测结果
    :param targets: 实际结果，对应图像中存在的目标的列表，n行6列，第1列到第6列分别对应(index, class, x, y, w, h)，这里index为图像在当前批中的编号，例如batch_size=16，则这里的index取值为0 ~ 15
    :param model: 神经网络模型
    :return: 总损失， 分项损失（lbox, lobj, lcls, loss）
    """
    ft = torch.cuda.FloatTensor if p[0].is_cuda else torch.Tensor
    lcls, lbox, lobj = ft([0]), ft([0]), ft([0])  # 分类损失，边框损失，
    #
    tcls, tbox, indices, anchor_vec = build_targets(p, targets, model)
    h = model.hyp  # hyperparameters
    red = 'mean'

    # Define criteria，定义两个BCELoss，用来计算分类损失
    BCEcls = nn.BCEWithLogitsLoss(pos_weight=ft([h['cls_pw']]), reduction=red)
    BCEobj = nn.BCEWithLogitsLoss(pos_weight=ft([h['obj_pw']]), reduction=red)

    # class label smoothing https://arxiv.org/pdf/1902.04103.pdf eqn 3
    cp, cn = smooth_BCE(eps=0.0)

    # focal loss
    g = h['fl_gamma']  # focal loss gamma
    if g > 0:
        BCEcls, BCEobj = FocalLoss(BCEcls, g), FocalLoss(BCEobj, g)

    # Compute losses
    np, ng = 0, 0  # number grid points, targets
    for i, pi in enumerate(p):  # layer index, layer predictions
        # pi --> (batch_size, na, grid_num_x, grid_num_y, no) 其中，no=(x,y,w,h,obj,cls)
        b, a, gj, gi = indices[i]  # image_idx, anchor_idx, gridy, gridx，是实际参数
        tobj = torch.zeros_like(pi[..., 0])  # target obj, 构造一个和实际的YOLO层输出一样多的置信度矩阵,置信度全为零
        np += tobj.numel()  # tobj.numel()获得tobj中所有元素的个数，np进行了累加

        # Compute losses
        nb = len(b)  # 当前YOLO层返回的预设边框个数
        if nb:  # number of targets
            ng += nb
            # 这里通过索引拿到待检测目标的信息，因为len(b)=len(a)=len(gj)=len(gi)=155=当前YOLO层可以检测到的目标数量，
            # 而pi本身形状为（batch_size, na, img_w, img_h, no)，因此ps形状为(155, 85)，一共155行，每一行对应一个待检测目标
            ps = pi[b, a, gj, gi]  # prediction subset corresponding to targets，预测的no输出，共n行no列
            # ps[:, 2:4] = torch.sigmoid(ps[:, 2:4])  # wh power loss (uncomment)

            # GIoU
            pxy = torch.sigmoid(ps[:, 0:2])  # pxy = pxy * s - (s - 1) / 2,  s = 1.5  (scale_xy)预测的归一化后的xy值
            pwh = torch.exp(ps[:, 2:4]).clamp(max=1E3) * anchor_vec[i]  # 预测的wh值，截断到当前图片大小
            pbox = torch.cat((pxy, pwh), 1)  # predicted box
            giou = bbox_iou(pbox, tbox[i], x1y1x2y2=False, GIoU=True)  # giou computation
            lbox += (1.0 - giou).sum() if red == 'sum' else (1.0 - giou).mean()  # giou loss 边框位置损失
            # 将tobj中存在待检测目标的索引对应的位置处的值置为(1.0 - model.gr) + model.gr * giou.detach().clamp(0).type(tobj.dtype)=1
            tobj[b, a, gj, gi] = (1.0 - model.gr) + model.gr * giou.detach().clamp(0).type(tobj.dtype)  # giou ratio

            if model.nc > 1:  # cls loss (only if multiple classes)
                t = torch.full_like(ps[:, 5:], cn)  # targets
                t[range(nb), tcls[i]] = cp  #
                lcls += BCEcls(ps[:, 5:], t)  # BCE ps的5列之后是代表类别的独热编码，这些编码要尽量与t一致。
                # lcls += CE(ps[:, 5:], tcls[i])  # CE

            # Append targets to text file
            # with open('targets.txt', 'a') as file:
            #     [file.write('%11.5g ' * 4 % tuple(x) + '\n') for x in torch.cat((txy[i], twh[i]), 1)]

        lobj += BCEobj(pi[..., 4], tobj)  # obj loss  pi最后一维分别是x,y,w,h,obj,cls,索引4对应的是obj列

    lbox *= h['giou']
    lobj *= h['obj']
    lcls *= h['cls']
    if red == 'sum':
        bs = tobj.shape[0]  # batch size
        lobj *= 3 / (6300 * bs) * 2  # 3 / np * 2
        if ng:
            lcls *= 3 / ng / model.nc
            lbox *= 3 / ng

    loss = lbox + lobj + lcls
    return loss, torch.cat((lbox, lobj, lcls, loss)).detach()


def print_model_biases(model):
    # prints the bias neurons preceding each yolo layer
    print('\nModel Bias Summary: %8s%18s%18s%18s' % ('layer', 'regression', 'objectness', 'classification'))
    try:
        multi_gpu = type(model) in (nn.parallel.DataParallel, nn.parallel.DistributedDataParallel)
        for l in model.yolo_layers:  # print pretrained biases
            if multi_gpu:
                na = model.module.module_list[l].na  # number of anchors
                b = model.module.module_list[l - 1][0].bias.view(na, -1)  # bias 3x85
            else:
                na = model.module_list[l].na
                b = model.module_list[l - 1][0].bias.view(na, -1)  # bias 3x85
            print(' ' * 20 + '%8g %18s%18s%18s' % (l, '%5.2f+/-%-5.2f' % (b[:, :4].mean(), b[:, :4].std_range()),
                                                   '%5.2f+/-%-5.2f' % (b[:, 4].mean(), b[:, 4].std_range()),
                                                   '%5.2f+/-%-5.2f' % (b[:, 5:].mean(), b[:, 5:].std_range())))
    except:
        pass


def plot_images(imgs, targets, paths=None, fname='images.png'):
    """
    绘制一个批次中所有图片及其target目标。如果该批次中图片超过16张，则只绘制前16张图片。

    :param imgs: 当前批中的所有图像数据，imgs的形状为(batch_size, channels, width, height) (16, 3, 512, 512)
    :param targets: 真实待检测目标的边框
    :param paths:
    :param fname: 保存图片的文件名
    :return:
    """
    # Plots training images overlaid with targets
    imgs = imgs.cpu().numpy()
    targets = targets.cpu().numpy()
    # targets = targets[targets[:, 1] == 21]  # plot only one class

    fig = plt.figure(figsize=(10, 10))
    bs, _, h, w = imgs.shape  # batch size, _, height, width
    bs = min(bs, 16)  # limit plot to 16 images
    ns = np.ceil(bs ** 0.5)  # number of subplots,行列各多少个子图

    for i in range(bs):
        boxes = xywh2xyxy(targets[targets[:, 0] == i, 2:6]).T  # 4行16列，targets[:,0]==i是取图片索引为i的那张图片
        boxes[[0, 2]] *= w  # 因为targets中的box是归一化的，这里要恢复到原始大小
        boxes[[1, 3]] *= h
        plt.subplot(ns, ns, i + 1).imshow(imgs[i].transpose(1, 2, 0))  # 绘制图片
        plt.plot(boxes[[0, 2, 2, 0, 0]], boxes[[1, 1, 3, 3, 1]], '.-')  # 绘制标签边框
        plt.axis('off')
        if paths is not None:
            s = Path(paths[i]).name
            plt.title(s[:min(len(s), 40)], fontdict={'size': 8})  # limit to 40 characters
    fig.tight_layout()
    fig.savefig(fname, dpi=200)
    plt.close()


def fitness(x):
    # Returns fitness (for use with results.txt or evolve.txt)
    w = [0.0, 0.01, 0.99, 0.00]  # weights for [P, R, mAP, F1]@0.5 or [P, R, mAP@0.5, mAP@0.5:0.95]
    return (x[:, :4] * w).sum(1)


def train():
    """
    训练神经网络模型，优先使用settings.yml中的配置参数
    :return:
    """
    imgsz_min, imgsz_max, imgsz_test = opt.img_size  # img sizes (min, max, test)
    cfg = opt.cfg
    data = opt.data
    epochs = opt.epochs
    batch_size = opt.batch_size
    accumulate = opt.accumulate
    weights = opt.weights
    # dataset_yolo = DataSet_YOLO()
    # Image Sizes
    gs = 64  # (pixels) grid size
    assert math.fmod(imgsz_min, gs) == 0, '--img-size %g must be a %g-multiple' % (imgsz_min, gs)
    opt.multi_scale |= imgsz_min != imgsz_max  # multi if different (min, max)  opt.multi_scale = opt.multi_scale | (imgsz_min != imgsz_max)
    if opt.multi_scale:
        if imgsz_min == imgsz_max:
            imgsz_min //= 1.5
            imgsz_max //= 0.667
        grid_min, grid_max = imgsz_min // gs, imgsz_max // gs
        imgsz_min, imgsz_max = grid_min * gs, grid_max * gs
    print('Image sizes %g - %g train, %g test' % (imgsz_min, imgsz_max, imgsz_test))
    img_size = imgsz_max  # initialize with max size

    # Configure run
    init_seeds()
    data_dict = {  # data_dict = parse_data_cfg(data)
        "classes": 80,  # dataset_yolo.classes,
        "names": get_settings('aiTrain.darknet.names'),
        "train": get_settings('aiTrain.darknet.train'),
        "valid": get_settings('aiTrain.darknet.valid'),
        "trainLabelFolder": get_settings('aiTrain.darknet.trainLabelFolder') or None,  # 替换默认Label文件中的路径，保留图片名不变
        "validLabelFolder": get_settings('aiTrain.darknet.validLabelFolder') or None,
    }

    train_path = data_dict['train']
    test_path = data_dict['valid']
    nc = 1 if opt.single_cls else int(data_dict['classes'])  # number of classes
    hyp['cls'] *= nc / 80  # update coco-tuned hyp['cls'] to current train_dataset

    # Remove previous results
    for f in glob.glob('*_batch*.png') + glob.glob(results_file):
        os.remove(f)

    # Initialize model
    model = Darknet(cfg).to(device)

    # Optimizer
    pg0, pg1, pg2 = [], [], []  # optimizer parameter groups
    for k, v in dict(model.named_parameters()).items():
        if '.bias' in k:
            pg2 += [v]  # biases
        elif 'Conv2d.weight' in k:
            pg1 += [v]  # apply weight_decay
        else:
            pg0 += [v]  # all else

    if opt.adam:
        # hyp['lr0'] *= 0.1  # reduce lr (i.e. SGD=5E-3, Adam=5E-4)
        optimizer = optim.Adam(pg0, lr=hyp['lr0'])
        # optimizer = AdaBound(pg0, lr=hyp['lr0'], final_lr=0.1)
    else:  # 如果是继续训练，则params中的每项必须包含initial_lr属性，如果是初次训练，则只需要设置lr即可
        optimizer = optim.SGD(params=[{'params': pg0, 'initial_lr': hyp['lr0']}],
                              lr=hyp['lr0'], momentum=hyp['momentum'], nesterov=True)
    # add pg1 with weight_decay
    optimizer.add_param_group({'params': pg1, 'initial_lr': hyp['lr0'], 'weight_decay': hyp['weight_decay']})
    optimizer.add_param_group({'params': pg2, 'initial_lr': hyp['lr0']})  # add pg2 (biases)
    del pg0, pg1, pg2

    start_epoch = 0
    best_fitness = 0.0
    attempt_download(weights)
    if weights.endswith('.pt'):  # pytorch format
        # possible weights are '*.pt', 'yolov3-spp.pt', 'yolov3-tiny.pt' etc.
        chkpt = torch.load(weights, map_location=device)

        # load model
        try:
            # 如果model中相应权值变量的参数个数和加载的模型参数中对应的参数个数相同，则添加到chkpt['model']的键值对中
            # 这是为了防止读取的预训练模型参数和神经网络模型结构不匹配
            # chkpt['model'] = {k: v for k, v in chkpt['model'].items() if model.state_dict()[k].numel() == v.numel()}
            temp_dict = {}
            for k, v in chkpt['model'].items():
                if k in model.state_dict():
                    if model.state_dict()[k].numel() == v.numel():
                        temp_dict[k] = v

            model.load_state_dict(temp_dict, strict=False)
            del temp_dict
        except KeyError as e:
            s = "%s is not compatible with %s. Specify --weights '' or specify a --cfg compatible with %s. " \
                "See https://github.com/ultralytics/yolov3/issues/657" % (opt.weights, opt.cfg, opt.weights)
            raise KeyError(s) from e

        # load optimizer
        if chkpt['optimizer'] is not None:
            optimizer.load_state_dict(chkpt['optimizer'])
            best_fitness = chkpt['best_fitness']

        # load results
        if chkpt.get('training_results') is not None:
            with open(results_file, 'w') as file:
                file.write(chkpt['training_results'])  # write results.txt

        start_epoch = chkpt['epoch'] + 1
        del chkpt

    # Mixed precision training https://github.com/NVIDIA/apex
    if mixed_precision:
        # model, optimizer = amp.initialize(model, optimizer, opt_level='O1', verbosity=0)
        pass

    # Scheduler https://github.com/ultralytics/yolov3/issues/238
    lf = lambda x: (((1 + math.cos(
        x * math.pi / epochs)) / 2) ** 1.0) * 0.95 + 0.05  # cosine https://arxiv.org/pdf/1812.01187.pdf
    scheduler = lr_scheduler.LambdaLR(optimizer, lr_lambda=lf, last_epoch=start_epoch - 1)
    # scheduler = lr_scheduler.MultiStepLR(optimizer, [round(epochs * x) for x in [0.8, 0.9]], 0.1, start_epoch - 1)

    # Plot lr schedule
    # y = []
    # for _ in range(epochs):
    #     scheduler.step()
    #     y.append(optimizer.param_groups[0]['lr'])
    # plt.plot(y, '.-', label='LambdaLR')
    # plt.xlabel('epoch')
    # plt.ylabel('LR')
    # plt.tight_layout()
    # plt.savefig('LR.png', dpi=300)

    #  分布式训练 ----------------------- Initialize distributed training
    if device.type != 'cpu' and torch.cuda.device_count() > 1 and torch.distributed.is_available():
        dist.init_process_group(backend='nccl',  # 'distributed backend'
                                init_method='tcp://127.0.0.1:9999',  # distributed training init method
                                world_size=1,  # number of nodes for distributed training
                                rank=0)  # distributed training node rank
        model = torch.nn.parallel.DistributedDataParallel(model, find_unused_parameters=True)
        model.yolo_layers = model.module.yolo_layers  # move yolo layer indices to top level

    # Dataset
    train_dataset = DarknetDataset(train_path, label_folder=data_dict.get('trainLabelFolder'), img_size=img_size,
                                   batch_size=batch_size,
                                   augment=True,
                                   hyp=hyp,  # augmentation hyperparameters
                                   rect=opt.rect,  # rectangular training
                                   cache_images=opt.cache_images,
                                   single_cls=opt.single_cls)

    test_dataset = DarknetDataset(test_path, label_folder=data_dict.get('validLabelFolder'), img_size=img_size,
                                  batch_size=batch_size,
                                  # augment=True,
                                  hyp=hyp,  # augmentation hyperparameters
                                  rect=True,
                                  cache_images=opt.cache_images,
                                  single_cls=opt.single_cls)

    # Dataloader
    batch_size = min(batch_size, len(train_dataset))
    nw = min([os.cpu_count(), batch_size if batch_size > 1 else 0, 8])  # number of workers
    nw = 1
    dataloader = torch.utils.data.DataLoader(train_dataset,
                                             batch_size=batch_size,
                                             num_workers=nw,
                                             shuffle=not opt.rect,  # Shuffle=True unless rectangular training is used
                                             pin_memory=True,  # 锁页内存，加速计算
                                             collate_fn=DarknetDataset.collate_fn)
    # Testloader
    testloader = torch.utils.data.DataLoader(test_dataset,
                                             batch_size=batch_size,
                                             num_workers=nw,
                                             pin_memory=True,
                                             collate_fn=DarknetDataset.collate_fn)

    # Model parameters，这里给model添加几个参数
    model.nc = nc  # attach number of classes to model
    model.hyp = hyp  # attach hyperparameters to model
    model.gr = 1.0  # giou loss ratio (obj_loss = 1.0 or giou)这里只是为了声明model.gr，具体赋值在后面有覆盖
    model.class_weights = labels_to_class_weights(train_dataset.labels, nc).to(device)  # attach class weights

    # Model EMA
    ema = ModelEMA(model)

    # Start training
    nb = len(dataloader)  # number of batches
    n_burn = max(3 * nb, 500)  # burn-in iterations, max(3 epochs, 500 iterations)
    maps = np.zeros(nc)  # mAP per class
    # torch.autograd.set_detect_anomaly(True)
    results = (0, 0, 0, 0, 0, 0, 0)  # 'P', 'R', 'mAP', 'F1', 'val GIoU', 'val Objectness', 'val Classification'
    t0 = time.time()
    print('Using %g dataloader workers' % nw)
    print('Starting training for %g epochs...' % epochs)
    if start_epoch >= epochs and opt.resume:
        print('resume training but the "resumed result" has already finished, increase the epochs and retry.')
    for epoch in range(start_epoch, epochs):  # epoch ------------------------------------------------------------------
        model.train()

        # Update image weights (optional)
        if train_dataset.image_weights:
            w = model.class_weights.cpu().numpy() * (1 - maps) ** 2  # class weights
            image_weights = labels_to_image_weights(train_dataset.labels, nc=nc, class_weights=w)
            train_dataset.indices = random.choices(range(train_dataset.n), weights=image_weights,
                                                   k=train_dataset.n)  # rand weighted idx

        mloss = torch.zeros(4).to(device)  # mean losses
        print(('\n' + '%10s' * 8) % ('Epoch', 'gpu_mem', 'GIoU', 'obj', 'cls', 'total', 'targets', 'img_size'))
        pbar = tqdm(enumerate(dataloader), total=nb)  # progress bar, dataloader已经将训练数据分批处理
        for i, (imgs, targets, paths, _) in pbar:  # batch -------------------------------------------------------------
            # imgs是图像信息，但是已经被reshape为（16,3,512,512），分别对应（batch_size, 图像通道数, 图像宽和高）
            # targets 对应图像中存在的目标的列表，n行6列，第1列到第6列分别对应(index, class, x, y, w, h)，这里index为图像在
            # 当前批中的编号，例如batch_size=16，则这里的index取值为0 ~ 15
            # paths图像路径
            ni = i + nb * epoch  # 当前总的训练批数 = 当前epoch中训练到第几批 + 每个epoch包含的批数 * 已经完成epoch数
            imgs = imgs.to(device).float() / 255.0  # uint8 to float32, 0 - 255 to 0.0 - 1.0
            targets = targets.to(device)

            # Burn-in
            if ni <= n_burn * 2:
                model.gr = np.interp(ni, [0, n_burn * 2], [0.0, 1.0])  # giou loss ratio (obj_loss = 1.0 or giou)
                if ni == n_burn:  # burnin complete
                    print_model_biases(model)

                for j, x in enumerate(optimizer.param_groups):
                    # bias lr falls from 0.1 to lr0, all other lrs rise from 0.0 to lr0
                    x['lr'] = np.interp(ni, [0, n_burn], [0.1 if j == 2 else 0.0, x['initial_lr'] * lf(epoch)])
                    if 'momentum' in x:
                        x['momentum'] = np.interp(ni, [0, n_burn], [0.9, hyp['momentum']])

            # Multi-Scale training
            if opt.multi_scale:
                if ni / accumulate % 1 == 0:  #  adjust img_size (67% - 150%) every 1 batch
                    img_size = random.randrange(grid_min, grid_max + 1) * gs
                sf = img_size / max(imgs.shape[2:])  # scale factor
                if sf != 1:
                    ns = [math.ceil(x * sf / gs) * gs for x in imgs.shape[2:]]  # new shape (stretched to 32-multiple)
                    imgs = F.interpolate(imgs, size=ns, mode='bilinear', align_corners=False)

            # Run model
            pred = model(imgs)

            # Compute loss
            loss, loss_items = compute_loss(pred, targets, model)
            if not torch.isfinite(loss):
                print('WARNING: non-finite loss, ending training ', loss_items)
                return results

            # Scale loss by nominal batch_size of 64
            loss *= batch_size / 64

            # Compute gradient
            # if mixed_precision:
            #     with amp.scale_loss(loss, optimizer) as scaled_loss:
            #         scaled_loss.backward()
            # else:
            #     loss.backward()
            loss.backward()  # 计算梯度

            # Optimize accumulated gradient
            if ni % accumulate == 0:
                optimizer.step()  # 根据当前梯度更新模型权值
                optimizer.zero_grad()  # 清空梯度，不清零则梯度会累加，这里累计accumulate次梯度然后一次性更新
                ema.update(model)

            # Print batch results
            mloss = (mloss * i + loss_items) / (i + 1)  # 在上一步平均损失的基础上更新这一步的平均损失
            mem = '%.3gG' % (torch.cuda.memory_cached() / 1E9 if torch.cuda.is_available() else 0)  # (GB)
            s = ('%10s' * 2 + '%10.3g' * 6) % ('%g/%g' % (epoch, epochs - 1), mem, *mloss, len(targets), img_size)
            pbar.set_description(s)

            # Plot images with bounding boxes
            if ni < 1:  # 训练总次数小于1
                f = 'train_batch%g.png' % i  # filename
                plot_images(imgs=imgs, targets=targets, paths=paths, fname=f)
                if tb_writer:
                    tb_writer.add_image(f, cv2.imread(f)[:, :, ::-1], dataformats='HWC')
                    # tb_writer.add_graph(model, imgs)  # add model to tensorboard

            # end batch ------------------------------------------------------------------------------------------------

        # Update scheduler
        scheduler.step()

        # Process epoch results
        ema.update_attr(model)
        final_epoch = epoch + 1 == epochs
        if not opt.notest or final_epoch:  # Calculate mAP
            is_coco = any([x in data for x in ['coco.data', 'coco2014.data', 'coco2017.data']]) and model.nc == 80
            results, maps = test.test(cfg,
                                      data,
                                      batch_size=batch_size,
                                      img_size=imgsz_test,
                                      model=ema.ema,
                                      save_json=final_epoch and is_coco,
                                      single_cls=opt.single_cls,
                                      dataloader=testloader)

        # Write epoch results
        with open(results_file, 'a') as f:
            f.write(s + '%10.3g' * 7 % results + '\n')  # P, R, mAP, F1, test_losses=(GIoU, obj, cls)
        if len(opt.name) and opt.bucket:
            os.system('gsutil cp results.txt gs://%s/results/results%s.txt' % (opt.bucket, opt.name))

        # Write Tensorboard results
        if tb_writer:
            tags = ['train/giou_loss', 'train/obj_loss', 'train/cls_loss',
                    'metrics/precision', 'metrics/recall', 'metrics/mAP_0.5', 'metrics/F1',
                    'val/giou_loss', 'val/obj_loss', 'val/cls_loss']
            for x, tag in zip(list(mloss[:-1]) + list(results), tags):
                tb_writer.add_scalar(tag, x, epoch)

        # Update best mAP
        fi = fitness(np.array(results).reshape(1, -1))  # fitness_i = weighted combination of [P, R, mAP, F1]
        if fi > best_fitness:
            best_fitness = fi

        # Save training results
        save = (not opt.nosave) or (final_epoch and not opt.evolve)
        if save:
            with open(results_file, 'r') as f:
                # Create checkpoint
                chkpt = {'epoch': epoch,
                         'best_fitness': best_fitness,
                         'training_results': f.read(),
                         'model': ema.ema.module.state_dict() if hasattr(model, 'module') else ema.ema.state_dict(),
                         'optimizer': None if final_epoch else optimizer.state_dict()}

            # Save last checkpoint
            torch.save(chkpt, last)

            # Save best checkpoint
            if (best_fitness == fi) and not final_epoch:
                torch.save(chkpt, best)

            # Save backup every 10 epochs (optional)
            # if epoch > 0 and epoch % 10 == 0:
            #     torch.save(chkpt, wdir + 'backup%g.pt' % epoch)

            # Delete checkpoint
            del chkpt

        # end epoch ----------------------------------------------------------------------------------------------------

    # end training
    n = opt.name
    if len(n):
        n = '_' + n if not n.isnumeric() else n
        fresults, flast, fbest = 'results%s.txt' % n, wdir + 'last%s.pt' % n, wdir + 'best%s.pt' % n
        for f1, f2 in zip([wdir + 'last.pt', wdir + 'best.pt', 'results.txt'], [flast, fbest, fresults]):
            if os.path.exists(f1):
                os.rename(f1, f2)  # rename
                ispt = f2.endswith('.pt')  # is *.pt
                strip_optimizer(f2) if ispt else None  # strip optimizer
                os.system('gsutil cp %s gs://%s/weights' % (f2, opt.bucket)) if opt.bucket and ispt else None  # upload

    if not opt.evolve:
        plot_results()  # save as results.png
    print('%g epochs completed in %.3f hours.\n' % (epoch - start_epoch + 1, (time.time() - t0) / 3600))
    dist.destroy_process_group() if torch.cuda.device_count() > 1 else None
    torch.cuda.empty_cache()

    return results


if __name__ == '__main__':
    opt = {'epochs': 3, 'batch_size': 16, 'accumulate': 4,
           'cfg': 'yolov3-tiny.cfg',
           'data': 'data/coco2017.data', 'multi_scale': False, 'img_size': 512,
           'rect': True, 'resume': False, 'nosave': True, 'notest': True, 'evolve': False, 'bucket': '',
           'cache_images': False, 'weights': 'yolov3-tiny.pt', 'name': '', 'device': 0,
           'adam': True, 'single_cls': False}  # 初始化默认配置参数
    opt.update(get_settings('aiTrain.opt'))  # 使用配置文件中参数更新配置参数
    opt = argparse.Namespace(**opt)  # 将dict类型转换为argparse.Namespace类型

    opt.weight = last if opt.resume else opt.weights
    if isinstance(opt.img_size, int):
        opt.img_size = [opt.img_size]
    opt.img_size.extend([opt.img_size[-1]] * (3 - len(opt.img_size)))
    device = select_device(opt.device, apex=mixed_precision, batch_size=opt.batch_size)
    if device.type == 'cpu':
        mixed_precision = False

    tb_writer = None
    if not opt.evolve:  # Train normally
        try:
            # Start Tensorboard with "tensorboard --logdir=runs", view at http://localhost:6006/
            from torch.utils.tensorboard import SummaryWriter

            tb_writer = SummaryWriter()
            print("Run 'tensorboard --logdir=runs' to view tensorboard at http://localhost:6006/")
        except:
            pass
        train()  # train normally
    else:  # Evolve hyperparameters (optional)
        opt.notest, opt.nosave = True, True  # only test/save final epoch
        for _ in range(1):  # generations to evolve
            if os.path.exists('evolve.txt'):  # if evolve.txt exists: select best hyps and mutate
                # Select parent(s)
                parent = 'single'  # parent selection method: 'single' or 'weighted'
                x = np.loadtxt('evolve.txt', ndmin=2)
                n = min(5, len(x))  # number of previous results to consider
                x = x[np.argsort(-fitness(x))][:n]  # top n mutations
                w = fitness(x) - fitness(x).min()  # weights
                if parent == 'single' or len(x) == 1:
                    # x = x[random.randint(0, n - 1)]  # random selection
                    x = x[random.choices(range(n), weights=w)[0]]  # weighted selection
                elif parent == 'weighted':
                    x = (x * w.reshape(n, 1)).sum(0) / w.sum()  # weighted combination

                # Mutate
                method, mp, s = 3, 0.9, 0.2  # method, mutation probability, sigma
                npr = np.random
                npr.seed(int(time.time()))
                g = np.array([1, 1, 1, 1, 1, 1, 1, 0, .1, 1, 0, 1, 1, 1, 1, 1, 1, 1])  # gains
                ng = len(g)
                if method == 1:
                    v = (npr.randn(ng) * npr.random() * g * s + 1) ** 2.0
                elif method == 2:
                    v = (npr.randn(ng) * npr.random(ng) * g * s + 1) ** 2.0
                elif method == 3:
                    v = np.ones(ng)
                    while all(v == 1):  # mutate until a change occurs (prevent duplicates)
                        # v = (g * (npr.random(ng) < mp) * npr.randn(ng) * s + 1) ** 2.0
                        v = (g * (npr.random(ng) < mp) * npr.randn(ng) * npr.random() * s + 1).clip(0.3, 3.0)
                for i, k in enumerate(hyp.keys()):  # plt.hist(v.ravel(), 300)
                    hyp[k] = x[i + 7] * v[i]  # mutate

            # Clip to limits
            keys = ['lr0', 'iou_t', 'momentum', 'weight_decay', 'hsv_s', 'hsv_v', 'translate', 'scale',
                    'fl_gamma']
            limits = [(1e-5, 1e-2), (0.00, 0.70), (0.60, 0.98), (0, 0.001), (0, .9), (0, .9), (0, .9), (0, .9),
                      (0, 3)]
            for k, v in zip(keys, limits):
                hyp[k] = np.clip(hyp[k], v[0], v[1])

            # Train mutation
            results = train()

            # Write mutation results
            print_mutation(hyp, results, opt.bucket)

            # Plot results
            # plot_evolution_results(hyp)
