import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import os
import math
from pathlib import Path


class MixConv2d(nn.Module):
    def __init__(self, in_channels, out_channels, k=(3, 5, 7), stride=1, dilation=1, bias=True, method='equal_params'):
        """
        不知道这个类是用来干什么的，暂时不实现
        :param in_channels:
        :param out_channels:
        :param k:
        :param stride:
        :param dilation:
        :param bias:
        :param method:
        """
        super(MixConv2d, self).__init__()
        raise Exception("MixConv2d目前没有实现，实现方法参考：https://github.com/ayooshkathuria/YOLO_v3_tutorial_from_scratch")
        groups = len(k)
        if method == 'equal_ch':
            i = torch.linspace(0, groups - 1E-6, out_channels).floor()


class Swish(nn.Module):
    def forward(self, x):
        return x.mul_(torch.sigmoid(x))


class WeightedFeatureFusion(nn.Module):  # weighted sum of 2 or more layers https://arxiv.org/abs/1911.09070
    """
    加权特征融合，残差层的shortcut使用该类，将上一层的输出于残差块层的输入（记录在output[layers]中，output在forward时传入）融合
    """

    def __init__(self, layers, weight=False):
        super(WeightedFeatureFusion, self).__init__()
        self.layers = layers
        self.weight = weight
        self.n = len(layers) + 1  # 表示需要融合的层的数量，如一般shortcut层是将输入和输出叠加融合，则n=2
        if weight:
            self.w = torch.nn.Parameter(torch.zeros(self.n), requires_grad=True)

    def forward(self, x, outputs):
        # Weights
        if self.weight:
            w = torch.sigmoid(self.w) * (2 / self.n)
            x = x * w[0]

        # Fusion
        nx = x.shape[1]  # 通道数
        for i in range(self.n - 1):  # 如果需要融合两层，只需要执行一次融合操作，这里循环n-1次
            a = outputs[self.layers[i]] * w[i + 1] if self.weight else outputs[self.layers[i]]
            na = a.shape[1]  # 拿到需要融合的层的通道数

            # 调整通道数，这块貌似有些粗暴，按理来说在resnet模块中，调整通道数也是通过卷积层来实现的，这块直接对前面层的输出进行截断相加，
            if nx == na:
                x = x + a
            elif nx > na:  # 如果当前通道数量大，残差块的输入全部叠加到当前输出中，但也不是均匀进入
                x[:, :na] = x[:, :na] + a
            else:  # 如果历史通道na大，可能会影响残差的传递
                x = x + a[:, :nx]
        return x


class FeatureConcat(nn.Module):
    def __init__(self, layers):
        super(FeatureConcat, self).__init__()
        self.layers = layers  # 层索引
        self.multiple = len(layers) > 1  # multiple layers flag

    def forward(self, x, outputs):
        return torch.cat([outputs[i] for i in self.layers], dim=1) if self.multiple else outputs[self.layers[0]]

    def count_ops(self, x, y):
        """
        计算yolo层的运算量和参数量，thop库会调用该方法计算自定义层的计算量，计算量为0

        :param x:
        :param y:
        :return:
        """
        self.total_ops += torch.DoubleTensor([int(0)])


class YOLOLayer(nn.Module):
    def __init__(self, anchors, nc, img_size, yolo_index, layers, stride):
        """
        YOLOLayer层

        :param anchors:  预定义边框，在训练时，真实的边框位置相对于预设边框的偏移来构建
        :param nc: 分类数量
        :param img_size:
        :param yolo_index:
        :param layers:
        :param stride:
        """
        super(YOLOLayer, self).__init__()
        self.anchors = torch.Tensor(anchors)  # tensor([[ 81.,  82.], [135., 169.], [344., 319.]])
        self.index = yolo_index
        self.layers = layers
        self.stride = stride  # 按照从上到下yolo层的编号，分别取值[32, 16, 8, 4, 2]
        self.nl = len(layers)
        self.na = len(anchors)  # number of anchors
        self.nc = nc  # 分类数量
        self.no = nc + 5  # number of output 每个格子对应输出的维度=class + 5，其中5代表x,y,w,h,conf
        self.nx, self.ny, self.ng = 0, 0, 0
        # tensor([[2.5312, 2.5625], [4.2188, 5.2812], [10.7500, 9.9688]])，表示anchor box尺寸除以步长，
        # 第一个yolo层步长为32，第二个yolo层步长为16，第三个yolo层步长为8
        self.anchor_vec = self.anchors / self.stride
        # 当前yolo层对应的anchor box宽高为anchor_wh，示例取值如下：
        # tensor([[[[[ 2.5312,  2.5625]]],
        #          [[[ 4.2188,  5.2812]]],
        #          [[[10.7500,  9.9688]]]]])
        self.anchor_wh = self.anchor_vec.view(1, self.na, 1, 1, 2)

    def create_grids(self, ng=(13, 13), device='cpu'):
        """
        划分网格

        :param ng: x和y方向的网格数量
        :param device:
        :return:
        """
        self.nx, self.ny = ng  # x and y grid size
        self.ng = torch.tensor(ng)

        # build xy offsets
        if not self.training:
            # 参考 https://www.cnblogs.com/pprp/p/12228991.html，讲解了划分的操作
            yv, xv = torch.meshgrid(
                [torch.arange(self.ny, device=device), torch.arange(self.nx, device=device)])  # 生成两个形状相同的Tensor
            temp = torch.stack((xv, yv), dim=2)  # stack生成形状为(15,20,2)
            self.grid = temp.view((1, 1, self.ny, self.nx, 2)).float()  # stack生成形状为(15,20,2),view生成形状为(1，1，15，20，2)

        if self.anchor_vec.device != device:
            self.anchor_vec = self.anchor_vec.to(device)
            self.anchor_wh = self.anchor_wh.to(device)

    def forward(self, p, out):  # p是yolo层上一层的输出，对应本层的直接输入，out按需记录了以前部分层的输出，供yolo层使用
        ASFF = False  # https://arxiv.org/abs/1911.09516
        if ASFF:
            i, n = self.index, self.nl  # index in layers, number of layers
            p = out[self.layers[i]]
            bs, _, ny, nx = p.shape  # bs, 255, 13, 13
            if (self.nx, self.ny) != (nx, ny):
                self.create_grids((nx, ny), p.device)

            # outputs and weights
            # w = F.softmax(p[:, -n:], 1)  # normalized weights
            w = torch.sigmoid(p[:, -n:]) * (2 / n)  # sigmoid weights (faster)
            # w = w / w.sum(1).unsqueeze(1)  # normalize across layer dimension

            # weighted ASFF sum
            p = out[self.layers[i]][:, :-n] * w[:, i:i + 1]
            for j in range(n):
                if j != i:
                    p += w[:, j:j + 1] * \
                         F.interpolate(out[self.layers[j]][:, :-n], size=[ny, nx], mode='bilinear',
                                       align_corners=False)


        else:
            bs, _, ny, nx = p.shape  # bs, 255, 13, 13, bs, 255, 15, 20
            if (self.nx, self.ny) != (nx, ny):
                self.create_grids((nx, ny), p.device)

        # 下面两条语句将p的形状由(bs, 255, 13, 13) -- > (bs, 3, 13, 13, 85)，需要说明的是，YOLO层前一层的卷积层的filter个数
        # 具有特殊的要求，filter_num = anchor_num * (5 + class_num)，这里的变形相当于把filter_num拆开了。
        # p.view(bs, 255, 13, 13) -- > (bs, 3, 13, 13, 85)  # (bs, anchors, grid, grid, classes + xywh)
        p = p.view(bs, self.na, self.no, self.ny,
                   self.nx)  # p (1,3,85,15,25)(batch_size,channels, classes+5,height,width)
        p = p.permute(0, 1, 3, 4,
                      2).contiguous()  # p (1,3, 15,20,85)，permute将第三个维度变换到第五个维度 (1,3,30,40,85)(1,3,60,80,85)

        if self.training:
            return p

        else:  # inference
            # 参考 https://www.cnblogs.com/pprp/p/12228991.html
            io = p.clone()  # inference output
            io[..., :2] = torch.sigmoid(io[..., :2]) + self.grid  # xy
            io[..., 2:4] = torch.exp(io[..., 2:4]) * self.anchor_wh  # wh yolo method
            io[..., :4] *= self.stride
            torch.sigmoid_(io[..., 4:])
            return io.view(bs, -1, self.no), p  # view [1, 3, 13, 13, 85] as [1, 507, 85]

    def count_ops(self, x, y):
        """
        计算yolo层的运算量和参数量，thop库会调用该方法计算自定义层的计算量

        :param x:
        :param y:
        :return:
        """
        self.total_ops += torch.DoubleTensor([int(0)])


def create_modules(module_defs, img_size):
    """
    根据配置字典创建神经网络模型

    :param module_defs:
    :param img_size:
    :return: module_list和routes，routes中记录了forward计算过程中需要记录结果的层，这些层一般是shortcut、yolo、routes层的
    输入，在网络的多个分支中会用到，因此需要保存
    """
    img_size = [img_size] * 2 if isinstance(img_size, int) else img_size
    _ = module_defs.pop(0)
    output_filters = [3]  # input channels
    module_list = nn.ModuleList()
    routs = []  # list of layers which rout to deeper layers，routs[i]中的层会在forward时记录该层的输出
    yolo_index = -1

    for i, mdef in enumerate(module_defs):
        modules = nn.Sequential()
        if mdef['type'].startswith('conv'):
            bn = mdef['batch_normalize']
            filters = mdef['filters']  # 卷积核数量每个卷积层都需要指定
            k = mdef['size']
            stride = mdef['stride'] if 'stride' in mdef else (mdef['stride_y'], mdef['stride_x'])
            if isinstance(k, int):  # single-size conv，即卷积核为正方形
                modules.add_module('Conv2d', nn.Conv2d(in_channels=output_filters[-1],
                                                       out_channels=filters,
                                                       kernel_size=k,
                                                       stride=stride,
                                                       padding=k // 2 if mdef['pad'] else 0,
                                                       groups=mdef['groups'] if 'groups' in mdef else 1,
                                                       ))
            else:  #
                modules.add_module('MixConv2d', MixConv2d(in_channels=output_filters,
                                                          out_channels=filters,
                                                          kernel_size=k,
                                                          stride=stride,
                                                          bias=not bn))
            if bn:  # 如果需要bn层，darknet中每一个卷积层后都有一个bn层和一个leakyReLU层
                modules.add_module('BatchNorm2d', nn.BatchNorm2d(filters, momentum=0.03, eps=1E-4))
            else:  # 如果不是bn层，则表明该层是yolo层的上一层，需要记录该层输出结果
                routs.append(i)  # routs中的层在forward计算过程中会记录输出

            if mdef['activation'] == 'leaky':
                modules.add_module('activation', nn.LeakyReLU(0.1, inplace=True))
            elif mdef['activation'] == 'swish':
                modules.add_module('activation', Swish())
        elif mdef['type'] == 'BatchNorm2d':
            filters = output_filters[-1]  # 卷积核数量默认与上一层相同，即bn层不改变通道数
            modules = nn.BatchNorm2d(filters, momentum=0.03, eps=1E-4)
            if i == 0 and filters == 3:  # normalize RGB image
                # 这块貌似与迁移学习有关，按照源代码理解，
                # imagenet mean and var https://pytorch.org/docs/stable/torchvision/models.html#classification
                modules.running_mean = torch.tensor([0.485, 0.456, 0.406])
                modules.running_var = torch.tensor([0.0524, 0.0502, 0.0506])

        elif mdef['type'] == 'maxpool':
            k = mdef['size']
            stride = mdef['stride']
            maxpool = nn.MaxPool2d(kernel_size=k, stride=stride, padding=(k - 1) // 2)
            if k == 2 and stride == 1:  # yolov3-tiny
                modules.add_module('ZeroPad2d', nn.ZeroPad2d((0, 1, 0, 1)))
                modules.add_module('MaxPool2d', maxpool)
            else:
                modules = maxpool

        elif mdef['type'] == 'upsample':
            modules = nn.Upsample(scale_factor=mdef['stride'])

        elif mdef['type'] == 'route':
            # 不懂啥意思，待实现
            layers = mdef['layers']
            filters = sum([output_filters[l + 1 if l > 0 else l] for l in layers])
            routs.extend([i + l if l < 0 else l for l in layers])
            modules = FeatureConcat(layers=layers)

        elif mdef['type'] == 'shortcut':
            layers = mdef['from']
            filters = output_filters[-1]
            routs.extend([i + l if l < 0 else l for l in layers])  # 如果是shortcut层则判断是否需要记录该层的输出，需要的话就添加到routs列表
            modules = WeightedFeatureFusion(layers=layers, weight='weight_type' in mdef)

        elif mdef['type'] == 'reorg3d':
            pass
        elif mdef['type'] == 'yolo':
            yolo_index += 1
            stride = [32, 16, 8, 4, 2][yolo_index]
            layers = mdef.get('from') or []
            modules = YOLOLayer(anchors=mdef['anchors'][mdef['mask']],
                                nc=mdef['classes'],
                                img_size=img_size,
                                yolo_index=yolo_index,
                                layers=layers,
                                stride=stride
                                )

            # Initialize preceding Conv2d() bias (https://arxiv.org/pdf/1708.02002.pdf section 3.3)
            # try:
            #     bo = -4.5  #  obj bias
            #     bc = math.log(1 / (modules.nc - 0.99))  # cls bias: class probability is sigmoid(p) = 1/nc
            #
            #     j = layers[yolo_index] if 'from' in mdef else -1  # yolo层都没有from属性，所以这里总是取-1
            #     bias_ = module_list[j][0].bias  # shape(255,)
            #     bias = bias_[:modules.no * modules.na].view(modules.na, -1)  # shape(3,85)
            #     bias[:, 4] += bo - bias[:, 4].mean()  # obj
            #     bias[:, 5:] += bc - bias[:, 5:].mean()  # cls, view with utils.print_model_biases(model)
            #     # module_list[j] 为当前yolo层的前一层
            #     module_list[j][0].bias = torch.nn.Parameter(bias_, requires_grad=bias_.requires_grad)
            # except:
            #     print('WARNING: smart bias initialization failure.')

        else:
            print('Warning: Unrecognized Layer Type: ' + mdef['type'])

            # Register module list and number of output filters
        module_list.append(modules)
        output_filters.append(filters)

    routs_binary = [False] * (i + 1)
    for i in routs:
        routs_binary[i] = True
    return module_list, routs_binary


def parse_cfg(cfgfile):
    """
    读取配置文件
    :param cfgfile:
    :return: 列表对象,其中每一个元素为一个字典类型对应于一个要建立的神经网络模块（层）
    """
    # 加载文件并过滤掉文本中多余内容
    file = open(cfgfile, 'r')
    lines = file.read().split('\n')
    lines = [x for x in lines if len(x) > 0]
    lines = [x for x in lines if x[0] != '#']
    lines = [x.strip() for x in lines]
    # cfg文件中的每个块用[]括起来最后组成一个列表，一个block存储一个块的内容，即每个层用一个字典block存储
    block = {}
    blocks = []

    for line in lines:
        if line[0] == '[':
            if len(block) != 0:
                blocks.append(block)
                block = {}
            block['type'] = line[1:-1].strip()
        else:
            key, value = line.split('=')
            block[key.strip()] = value.strip()
    blocks.append(block)
    return blocks


def parse_model_cfg(path: str):
    # parse the yolo *.cfg file and return module definitions path may be 'cfg/yolov3.cfg', 'yolov3.cfg', or 'yolov3'
    if not path.endswith('.cfg'):
        path += '.cfg'

    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(__file__), path)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    lines = [x for x in lines if x and not x.startswith('#')]
    lines = [x.strip() for x in lines]
    mdefs = []
    for line in lines:
        if line.startswith('['):
            mdefs.append({})
            mdefs[-1]['type'] = line[1:-1].strip()
            if mdefs[-1]['type'] == 'convolutional':
                mdefs[-1]['batch_normalize'] = 0
        else:
            key, val = line.split('=')
            key = key.strip()

            if key == 'anchors':
                mdefs[-1][key] = np.array([float(x) for x in val.split(',')]).reshape((-1, 2))
            elif (key in ['from', 'layers', 'mask']) or (key == 'size' and ',' in val):
                mdefs[-1][key] = [int(x) for x in val.split(',')]
            else:
                val = str(val.strip())
                if val.isnumeric():
                    mdefs[-1][key] = int(val) if (int(val) - float(val)) == 0 else float(
                        val)  # 这貌似有一些问题，如果数值是1.0的float数，就比较尴尬
                else:
                    mdefs[-1][key] = val

    supported = ['type', 'batch_normalize', 'filters', 'size', 'stride', 'pad', 'activation', 'layers', 'groups',
                 'from', 'mask', 'anchors', 'classes', 'num', 'jitter', 'ignore_thresh', 'truth_thresh', 'random',
                 'stride_x', 'stride_y', 'weights_type', 'weights_normalization', 'scale_x_y', 'beta_nms', 'nms_kind',
                 'iou_loss', 'iou_normalizer', 'cls_normalizer', 'iou_thresh']

    f = []
    for x in mdefs[1:]:  # mdefs字典第一项存储的是网络信息，第二项开始存储的是层信息
        [f.append(k) for k in x if k not in f]
    u = [x for x in f if x not in supported]
    assert not any(u), 'Unsupported fields {} in {}'.format(u, path)
    return mdefs


def scale_img(img, ratio=1.0, same_shape=True):  # img(16,3,256,416), r=ratio
    """
    缩放图像大小，传入参数img的形状类似于(16,3,256,416)，其中16为batch_size, 3为通道数，256，416为图片宽和高
    :param img:
    :param ratio:
    :param same_shape:
    :return:
    """
    # scales img(bs,3,y,x) by ratio
    h, w = img.shape[2:]
    s = (int(h * ratio), int(w * ratio))  # new size
    img = F.interpolate(img, size=s, mode='bilinear', align_corners=False)  # resize
    if not same_shape:  # pad/crop img
        gs = 64  # (pixels) grid size
        h, w = [math.ceil(x * ratio / gs) * gs for x in (h, w)]
    return F.pad(img, [0, w - s[1], 0, h - s[0]], value=0.447)  # value = imagenet mean


def attempt_download(weights):
    msg = weights + '权重文件不存在，尝试下载...'


class Darknet(nn.Module):
    def __init__(self, cfg, img_size=(416, 416), verbose=False):
        """
        根据cfg初始化神经网络模型

        :param cfg:
        :param img_size:
        :param verbose: 是否打印调试信息
        """
        super(Darknet, self).__init__()
        self.module_defs = parse_model_cfg(cfg)
        self.module_list, self.routs = create_modules(self.module_defs, img_size)
        self.yolo_layers = get_yolo_layers(self)
        # torch_utils.initialize_weights(self)

        # Darknet Header https://github.com/AlexeyAB/darknet/issues/2914#issuecomment-496675346
        self.version = np.array([0, 2, 5], dtype=np.int32)  # (int32) version info: major, minor, revision
        self.seen = np.array([0], dtype=np.int64)  # (int64) number of images seen during training
        self.info(verbose)  # print model description

    def forward(self, x, augment=False, verbose=False):

        if not augment:  # 图像增强
            return self.forward_once(x)
        else:  # Augment images (inference and test only) https://github.com/ultralytics/yolov3/issues/931
            img_size = x.shape[-2:]  # height, width
            s = [0.83, 0.67]  # scales
            y = []
            for i, xi in enumerate((x,
                                    scale_img(x.flip(3), s[0], same_shape=False),  # flip-lr and scale
                                    scale_img(x, s[1], same_shape=False),  # scale
                                    )):
                # cv2.imwrite('img%g.jpg' % i, 255 * xi[0].numpy().transpose((1, 2, 0))[:, :, ::-1])
                y.append(self.forward_once(xi)[0])

            y[1][..., :4] /= s[0]  # scale
            y[1][..., 0] = img_size[1] - y[1][..., 0]  # flip lr
            y[2][..., :4] /= s[1]  # scale

            # for i, yi in enumerate(y):  # coco small, medium, large = < 32**2 < 96**2 <
            #     area = yi[..., 2:4].prod(2)[:, :, None]
            #     if i == 1:
            #         yi *= (area < 96. ** 2).float()
            #     elif i == 2:
            #         yi *= (area > 32. ** 2).float()
            #     y[i] = yi

            y = torch.cat(y, 1)
            return y, None

    def forward_once(self, x: torch.Tensor, augment=False, verbose=False):
        img_size = x.shape[-2:]  # height, width
        yolo_out, out = [], []  # 将yolo层的输出记录到yolo_out中，将标记routs[i]为True层的输出记录到out中
        if verbose:
            print('0', x.shape)
            str = ''

        # Augment images (inference and test only)
        if augment:  # https://github.com/ultralytics/yolov3/issues/931  识别增强，采用多次不同策略进行识别，提升识别效果
            nb = x.shape[0]  # batch size
            s = [0.83, 0.67]  # scales
            x = torch.cat((x,
                           scale_img(x.flip(3), s[0]),  # flip-lr and scale
                           scale_img(x, s[1]),  # scale
                           ), 0)

        for i, module in enumerate(self.module_list):
            name = module.__class__.__name__
            if name in ['WeightedFeatureFusion', 'FeatureConcat']:  # sum, concat
                if verbose:
                    l = [i - 1] + module.layers  # layers
                    sh = [list(x.shape)] + [list(out[i].shape) for i in module.layers]  # shapes
                    str = ' >> ' + ' + '.join(['layer %g %s' % x for x in zip(l, sh)])
                x = module(x,
                           out)  # WeightedFeatureFusion(), FeatureConcat()，这里out按需记录了以前层的输出，会传给WeightedFeatureFusion层forward的output参数
            elif name == 'YOLOLayer':
                yolo_out.append(module(x, out))
            else:  # run module directly, i.e. mtype = 'convolutional', 'upsample', 'maxpool', 'batchnorm2d' etc.
                x = module(x)

            out.append(x if self.routs[i] else [])  # 如果routs[i]为True，则记录当前层的输出
            if verbose:
                print('%g/%g %s -' % (i, len(self.module_list), name), list(x.shape), str)
                str = ''

        if self.training:  # train
            return yolo_out
        else:  # inference or test
            x, p = zip(*yolo_out)  # inference output, training output
            x = torch.cat(x, 1)  # cat yolo outputs
            if augment:  # de-augment results
                x = torch.split(x, nb, dim=0)
                x[1][..., :4] /= s[0]  # scale
                x[1][..., 0] = img_size[1] - x[1][..., 0]  # flip lr
                x[2][..., :4] /= s[1]  # scale
                x = torch.cat(x, 1)
            return x, p

    def info(self, verbose=False):
        model_info(self, verbose)

    def count_ops(self, x, y):
        """
        计算yolo层的运算量和参数量，thop库会调用该方法计算自定义层的计算量

        :param x:
        :param y:
        :return:
        """
        self.total_ops += torch.DoubleTensor([int(0)])


def get_yolo_layers(model):
    """
    获取构建的模型中的YOLOLayer层
    """
    return [i for i, m in enumerate(model.module_list) if m.__class__.__name__ == 'YOLOLayer']  # [89, 101, 113]


def model_info(model, verbose=False):
    # Plots a line-by-line description of a PyTorch model
    n_p = sum(x.numel() for x in model.parameters())  # number parameters  将model.parameters()里所有权值的数量加起来
    n_g = sum(x.numel() for x in model.parameters() if x.requires_grad)  # number gradients
    if verbose:
        print('%5s %40s %9s %12s %20s %10s %10s' % ('layer', 'name', 'gradient', 'parameters', 'shape', 'mu', 'sigma'))
        for i, (name, p) in enumerate(model.named_parameters()):
            name = name.replace('module_list.', '')
            print('%5g %40s %9s %12g %20s %10.3g %10.3g' %
                  (i, name, p.requires_grad, p.numel(), list(p.shape), p.mean(), p.std_range()))

    try:  # FLOPS
        from thop import profile
        from thop.vision.basic_hooks import zero_ops
        macs, _ = profile(model,
                          inputs=(torch.zeros(1, 3, 480, 640),),  # 这里以tuple格式传入inputs的数据作为测试
                          custom_ops={YOLOLayer: YOLOLayer.count_ops,
                                      FeatureConcat: FeatureConcat.count_ops,
                                      Darknet: Darknet.count_ops,
                                      nn.Sequential: zero_ops,
                                      nn.ModuleList: zero_ops}  # YOLOLayer: count_yolo_layer}
                          )
        fs = ', %.1f GFLOPS' % (macs / 1E9 * 2)
    except:
        fs = ''

    print('Model Summary: %g layers, %g parameters, %g gradients%s' % (len(list(model.parameters())), n_p, n_g, fs))
