import torch
import torch.nn as nn
from torchvision.models.resnet import resnet50
import torchvision as tv


class Conv2d(nn.Module):
    """
    这个网络主要由一系列的1×1和3×3的卷积层组成，每个卷积层后都会跟一个BN层和一个LeakyReLU层，
    这里将这三个封装为新的卷积层
    """

    def __init__(self, in_channels, out_channels, kernal_size, stride, padding):
        super(Conv2d, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=out_channels,
                      kernel_size=kernal_size, stride=stride, padding=padding),
            nn.BatchNorm2d(num_features=out_channels),
            nn.LeakyReLU()
        )

    def forward(self, x):
        return self.conv(x)


class Residual(nn.Module):
    """
    Darknet-53中的残差模块，参考https://blog.csdn.net/qq_37541097/article/details/81214953#commentBox
    """

    def __init__(self, in_channels):
        super(Residual, self).__init__()
        self.r = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=in_channels // 2, kernel_size=1, stride=1, padding=0),
            nn.Conv2d(in_channels=in_channels // 2, out_channels=in_channels, kernel_size=3, stride=1, padding=1)
        )

    def forward(self, x):
        return x + self.r(x)


class DownSample(nn.Module):
    """
    降采样层，网络结构块之间的卷积层
    """

    def __init__(self, in_channels, kernal_size=3, stride=2, padding=1):
        super(DownSample, self).__init__()
        self.downsample = Conv2d(in_channels=in_channels, out_channels=in_channels, kernal_size=kernal_size,
                                 stride=stride, padding=padding)


def block_times(block, times):
    """
    重复block模块times次
    :param block:
    :param times:
    :return:
    """
    blocks = nn.Sequential()
    for i in range(times):
        blocks.add_module(block)
    return blocks


class ConvSet(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ConvSet, self).__init__()
        self.conv = nn.Sequential(
            Conv2d(in_channels=in_channels, out_channels=out_channels, kernal_size=1, stride=1, padding=0),
            Conv2d(out_channels, out_channels, 3, 1, 0),
            Conv2d(out_channels, out_channels * 2, 1, 1, 0),
            Conv2d(out_channels * 2, out_channels * 2, 3, 1, 1),
            Conv2d(out_channels * 2, out_channels, 1, 1, 0)
        )

    def forward(self, x):
        return self.conv(x)


class Darknet52(nn.Module):
    """
    这是Darknet53层不包括最后平均池化层之后三层的部分，一共52个卷积层。这里的卷积层计数不算残差层内的卷积层，

    Darknet52可用于构建Dark53和Yolov3网络结构，这是这两个结构的共有部分。
    """

    def __init__(self, in_channels):
        super(Darknet52, self).__init__()
        self.d52 = nn.Sequential(
            Conv2d(in_channels, 32, 3, 1, 1),  # in_channel为图片通道数，一般都是3
            Conv2d(32, 64, 3, 2, 1),

            # 1x
            Conv2d(64, 32, 1, 1, 0),
            Conv2d(32, 64, 3, 1, 1),  # 这里的padding数量都是计算出来的
            Residual(64),

            Conv2d(64, 128, 3, 2, 1),  # 降采样的同时提升通道数
        )
        # 后面涉及到重复的块，这里使用循环分别添加不同的层
        for i in range(2):
            self.d52.add_module(Conv2d(128, 64, 1, 1, 0))
            self.d52.add_module(Conv2d(64, 128, 3, 1, 1))
            self.d52.add_module(Residual(128))

        self.d52.add(Conv2d(128, 256, 3, 2, 1))

        # 8x
        for i in range(8):
            self.d52.add_module(Conv2d(256, 128, 1, 1, 0))
            self.d52.add_module(Conv2d(128, 258, 3, 1, 1))
            self.d52.add_module(Residual(256))

        self.d52.add_module(Conv2d(256, 512, 3, 2, 1))

        # 8x
        for i in range(8):
            self.d52.add_module(Conv2d(512, 256, 1, 1, 0))
            self.d52.add_module(Conv2d(256, 512, 3, 1, 1))
            self.d52.add_module(Residual(512))

        self.d52.add_module(Conv2d(512, 1024, 3, 2, 1))

        # 4x
        for i in range(4):
            self.d52.add_module(Conv2d(1024, 512, 1, 1, 0))
            self.d52.add_module(Conv2d(512, 1024, 3, 1, 1))
            self.d52.add_module(Residual(1024))

    def forward(self, x):
        return self.d52(x)


class YOLOV3(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(YOLOV3, self).__init__()
        self.darknet52 = Darknet52(in_channels, out_channels)
        self.convSet1=ConvSet(in_channels=1024, )

    def forward(self, x):
        x_52 = self.darknet52(x)
