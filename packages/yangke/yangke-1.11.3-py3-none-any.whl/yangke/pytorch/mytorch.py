import copy
import random
from collections import OrderedDict
from typing import Optional

import numpy as np
import optuna
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torch.utils.tensorboard import SummaryWriter

from yangke.base import get_settings, YkDict
from yangke.common.config import logger
from yangke.common.fileOperate import read_csv_ex
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class DataSetFitting(Dataset):
    def __init__(self, data_source, x_title=None, y_title=None, mean=None, std=None):
        """
        构建数据集

        :param data_source: 数据源，可以为settings.yaml文件配置，也可以是pd.DataFrame对象
        :param x_title: 输入参数的列标题，如果从配置文件加载，则可以为None
        :param y_title: 输出参数的列标题，如果从配置文件加载，则可以为None
        """
        self.dataframe = None
        if isinstance(data_source, pd.DataFrame):
            self.dataframe = data_source
            self.x_title = x_title or []
            self.y_title = y_title or []
        elif isinstance(data_source, YkDict):
            files = data_source.get_settings("dataset.data_file")
            self.normal_method = data_source.get_settings("dataset.normalization") or "z-score"
            input_set = data_source.get("input")
            self.x_title = [item["name"] for item in input_set]
            self.x_range = [None if item.get("range") is None else eval(item["range"]) for item in input_set]
            del input_set
            output_set = data_source.get_settings("output.para")
            if len(output_set) > 0 and isinstance(output_set[0], str):
                self.y_title = output_set
                self.y_range = None
            else:
                self.y_title = [item["name"] for item in output_set]
                self.y_range = [None if item.get("range") is None else eval(item["range"]) for item in output_set]
            for file in files:
                ext = file.get("type")
                filename = file.get("name")
                if not os.path.exists(filename):
                    continue
                if ext == "csv":
                    data_frame = read_csv_ex(filename)
                else:
                    data_frame = pd.read_excel(filename)
                if self.dataframe is not None and data_frame is not None:
                    self.dataframe = pd.concat([self.dataframe, data_frame], axis=0, ignore_index=True)
                else:
                    self.dataframe = self.dataframe or data_frame

            # 删除某些行
            self.drop_by_condition(data_source.get_settings("dataset.drop"))

        # 仅保留x,y相关的数据列，删除其他列
        titles = self.x_title.copy()
        titles.extend(self.y_title)
        if self.dataframe.shape[0] < 1:
            logger.warning("传入的数据文件中数据为空或数据文件不存在")
        self.dataframe = self.dataframe[titles]

        # 数据标准化
        self.mean = mean
        self.std_range = std
        self.dataframe_std = None
        self.set_standard()

    def set_standard(self, mean=None, std_range=None, normal_method=None):
        """
        设置数据的归一化参数，在初始化部分数据时，直接从部分数据集得到的归一化参数可能出现偏差，这里提供一种外部设置的方法。
        不建议中途更改数据归一化方法，否则可能导致模型预测结果很离谱。

        :param mean: 参数的平均值
        :param std_range: 参数的标准差或振幅
        :param normal_method: 数据归一化方法，支持"z-score"和"min-max"
        :return:
        """
        if normal_method is None or normal_method == self.normal_method:
            if mean is None and std_range is None:
                if self.normal_method == "z-score":
                    self.mean = self.mean or self.dataframe.mean()
                    self.std_range = self.std_range or self.dataframe.std()
                else:
                    if self.y_range is not None:
                        x_min = [x[0] for x in self.x_range]
                        y_min = [y[0] for y in self.y_range]
                        x_max = [x[1] for x in self.x_range]
                        y_max = [y[1] for y in self.y_range]
                        x_min.extend(y_min)
                        all_min = np.asarray(x_min)
                        x_max.extend(y_max)
                        all_max = np.asarray(x_max)
                        title = copy.deepcopy(self.x_title)
                        title.extend(self.y_title)
                        self.mean = pd.Series(data=(all_min + all_max) / 2, index=title)
                        self.std_range = pd.Series(data=(all_max - all_min) / 2, index=title)
            else:
                self.mean = mean
                self.std_range = std_range
            if self.mean is not None and self.std_range is not None:
                self.dataframe_std = self.standard(self.dataframe)
            else:
                self.dataframe_std = None
        else:
            self.normal_method = normal_method
            self.set_standard()

    def standard(self, df):
        """
        数据标准化

        :param df: Dataframe(num, input_and_output_dim)
        :return:
        """
        # Dataframe和Series运算的前提是：Dataframe的列标题和Series的索引名必须一一对应，而不仅仅看维度，否则可能会出错，
        return (df - self.mean) / self.std_range  # mean Series (input_and_output_dim,)

    def standard_reverse(self, out):
        """
        将预测结果反标准化

        :param out:
        :return:
        """
        return out * self.std_range[self.y_title] + self.mean[self.y_title]

    def __getitem__(self, index):
        """
        DataSet子类必须实现的方法，用于根据索引返回一条数据，数据类型需要是Tensor

        :param index:
        :return:
        """
        single_item = self.dataframe_std.iloc[index, :]
        x = torch.from_numpy(single_item[self.x_title].to_numpy()).to(torch.float32)
        y = torch.from_numpy(single_item[self.y_title].to_numpy()).to(torch.float32)
        return x, y

    def __len__(self):
        """
        DataSet子类必须实现的方法，用于获取DataSet的大小

        :return:
        """
        return self.dataframe.shape[0]

    def get_size(self):
        return self.dataframe.shape[0]

    def drop_by_condition(self, conditions):
        for cond in conditions:
            if list(cond.keys())[0] == "or":
                for co in cond.get("or"):
                    if "<=" in co:
                        title, value = tuple(co.split("<="))
                        title = str(title).strip()
                        value = float(value)
                        self.dataframe = self.dataframe[self.dataframe[title] > value]  # 删除小于的行 = 保留大于的行
                    elif ">=" in co:
                        title, value = tuple(co.split(">="))
                        title = str(title).strip()
                        value = float(value)
                        self.dataframe = self.dataframe[self.dataframe[title] < value]  # 删除小于的行 = 保留大于的行
                    elif "<" in co:
                        title, value = tuple(co.split("<"))
                        title = str(title).strip()
                        value = float(value)
                        self.dataframe = self.dataframe[self.dataframe[title] >= value]  # 删除小于的行 = 保留大于的行
                    elif ">" in co:
                        title, value = tuple(co.split(">"))
                        title = str(title).strip()
                        value = float(value)
                        self.dataframe = self.dataframe[self.dataframe[title] <= value]  # 删除大于的行 = 保留小于的行

    def split_set(self, part1, part2=None, part3=None):
        """
        按照指定的比例将数据集分割，一般用于将总体数据集分割为训练集，测试集，验证集等

        :param part1:
        :param part2:
        :param part3:
        :return:
        """
        if part3 is not None:
            assert part1 + part2 + part3 == 1, "数据集比例之和不为1"
            size = self.get_size()
            size1, size2 = int(part1 * size), int(part2 * size)
            set1, set2, set3 = torch.utils.data.random_split(self, [size1, size2, size - size1 - size2])
            return set1, set2, set3
        elif part2 is not None:
            if part1 + part2 < 1:
                return self.split_set(part1, part2, 1 - part1 - part2)
            else:
                size = self.get_size()
                size1 = int(part1 * size)
                return torch.utils.data.random_split(self, [size1, size - size1])
        else:
            size = self.get_size()
            size1 = int(part1 * size)
            return torch.utils.data.random_split(self, [size1, size - size1])


class DataFitterNet(torch.nn.Module):
    def __init__(self, settings1, trial=None):
        """
        一个用于数据拟合的神经网络类库，神经网络架构通过settings.yaml文件进行配置

        :param settings1:
        :param trial: 使用optuna超参数调优时会传入该参数
        """
        super(DataFitterNet, self).__init__()
        cfg = settings1.get("networks")  # 获取神经网络结构信息
        self.settings = settings1
        self.trial = trial
        self.cfg = cfg
        self.in_num = 0  # 输入层神经元个数，对应输入参数的个数
        self.out_num = 1
        train_settings = settings1.get_settings("networks.train") or {}
        self.lr = self.get_para_of_optuna_str(train_settings.get("learning_rate") or 1e-3, "lr")
        self.epochs = int(train_settings.get("epochs") or 10)
        self.batch_size = self.get_para_of_optuna_str(train_settings.get("batch_size") or 64, "batch_size")
        if settings1.get_settings("networks.loss_fn.type") == "MSE":
            self.loss_fn = nn.MSELoss(reduction="mean")
        elif settings1.get_settings("networks.loss_fn.type").lower() == "max":
            from yangke.stock.prediction.pytorch_pred_stock import MAXLoss
            self.loss_fn = MAXLoss()
        else:
            self.loss_fn = nn.CrossEntropyLoss()
        self.mean: Optional[pd.Series] = None
        self.std: Optional[pd.Series] = None
        self.normal_method = None  # 数据归一化方法
        self.x_title = []
        self.y_title = []
        self.max_err = 0
        self.average_err = 0
        _cell_num_last_layer = 0  # 循环中记录上一层神经网络的输出个数
        i = 1
        layer_dict = OrderedDict()
        for layer in cfg.get("layers"):  # 从配置中拿到神经网络各层的信息，进而构建神经网络
            _type = self.get_para_of_optuna_str(layer.get("type"), f"layer_type{i}")
            _cell_num = 1
            if _type == "input":  # 输入/输出层的神经元个数可以根据输入/输出参数个数自动确定
                _cell_num = layer.get("cell_num") or 10
                if layer.get("cell_num") == "auto" or layer.get("cell_num") is None:
                    self.in_num = len(settings1.get("input"))
                    _cell_num = self.in_num
                else:
                    self.in_num = int(layer.get("cell_num") or 10)
                    _cell_num = self.in_num
            elif _type == "linear":
                bias = layer.get("bias") or True
                _cell_num = self.get_para_of_optuna_str(layer.get("cell_num") or 10, f"cell_num{i}")
                layer_dict[f"layer{i}"] = nn.Linear(_cell_num_last_layer, _cell_num, bias=bias)
            elif _type == "relu":
                layer_dict[f"layer{i}"] = nn.ReLU()
                _cell_num = _cell_num_last_layer  # 激活函数输入输出个数不变
            # elif _type == 'softmax':
            #     self.layers.append(nn.Softmax())
            elif _type == "sigmoid":
                layer_dict[f"layer{i}"] = nn.Sigmoid()
                _cell_num = _cell_num_last_layer
            elif _type == "tanh":
                layer_dict[f"layer{i}"] = nn.Tanh()
                _cell_num = _cell_num_last_layer
            elif _type == "dropout":
                p = self.get_para_of_optuna_str(layer.get('rate'), "dropout_rate")
                layer_dict[f"layer{i}"] = nn.Dropout(p=p)
                _cell_num = _cell_num_last_layer
            elif _type.lower() == "rbf":
                _cell_num = layer.get("cell_num") or 10
                self.in_num = len(settings1.get("input"))
                self.out_num = len(settings1.get("output"))
                logger.error("暂不支持径向基神经网络")
            elif _type.lower() == "none":  # 空层
                continue
            elif _type == "output":  # 输入/输出层的神经元个数可以根据输入/输出参数个数自动确定
                if settings1.get_settings("output.type") == "single_output":
                    if layer.get("cell_num") != "auto" and int(layer.get("cell_num")) != 1:
                        logger.warning("数据集使用single_output，但神经网络模型输出层单元个数不为1，忽略神经网络输出单元个数设置！")
                    self.out_num = 1
                elif layer.get("cell_num") == "auto" or layer.get("cell_num") is None:
                    self.out_num = len(settings1.get("output"))
                else:
                    self.out_num = layer.get("cell_num")
                bias = layer.get("bias") or True
                layer_dict[f"layer{i}"] = nn.Linear(_cell_num_last_layer, self.out_num, bias=bias)
            else:
                logger.warning(f"发现不支持的layer类型：{_type}")

            _cell_num_last_layer = _cell_num
            i = i + 1

        self.net = nn.Sequential(layer_dict)
        weight_decay = self.get_para_of_optuna_str(settings1.get_settings("networks.optimizer.weight_decay") or 0,
                                                   "weight_decay")
        if settings1.get_settings("networks.optimizer.type") == "adam":
            self.optimizer = torch.optim.Adam(self.parameters(), lr=self.lr, weight_decay=weight_decay)
        else:
            self.optimizer = torch.optim.SGD(self.parameters(), lr=self.lr, weight_decay=weight_decay)

    def forward(self, x):
        out = self.net(x)
        return out

    def set_standard(self, mean, std, x_title, y_title, normal_method="z-score"):
        self.mean = mean
        self.std = std
        self.x_title = x_title
        self.y_title = y_title
        self.normal_method = normal_method

    def standard_reverse(self, tensor, flag="y"):
        """
        将预测结果反标准化

        :param tensor: 反标准化的数据
        :param flag: 反标准化的变量类型，x表示对输入变量进行反标准换，y表示对输出变量
        :return:
        """
        if len(self.y_title) != 1:
            logger.error("暂不支持输出变量个数大于1的神经网络")
        if flag == "x":
            para = tensor.cpu().data.numpy()  # 必须加.data，否则在需要求导的Tensor上直接调用numpy()方法会出错
            std = self.std[self.x_title].to_numpy()
            mean = self.mean[self.x_title].to_numpy()
        elif flag == "y":
            para = tensor.cpu().data.numpy()
            std = self.std[self.y_title].to_numpy()
            mean = self.mean[self.y_title].to_numpy()
        else:  # "all"包括x和y
            para = tensor.cpu().data.numpy()
            std = self.std.to_numpy()
            mean = self.mean.to_numpy()
        result = para * std + mean
        result = torch.from_numpy(result)
        return result

    def prediction(self, x_input):
        """
        预测指定输入参数

        :param x_input: x.shape = torch.Size([batch_size, input_dim])，也可以是长度为input_dim的列表或ndarray
        :return:
        """
        mean = torch.from_numpy(self.mean[self.x_title].to_numpy())
        std = torch.from_numpy(self.std[self.x_title].to_numpy())
        if isinstance(x_input, list):
            x_input = torch.from_numpy(np.asarray(x_input))
        if isinstance(x_input, np.ndarray):
            x_input = torch.from_numpy(x_input)
        x_input = (x_input - mean) / std  # 输入数据归一化
        x_input = x_input.to(torch.float32)
        self.eval()
        y = self.net(x_input)
        return self.standard_reverse(y)

    def save_yk(self, path):
        checkpoint = {
            'normal_method': self.normal_method,
            'mean': self.mean,
            'std': self.std,
            'x_title': self.x_title,
            'y_title': self.y_title,
            'model_state_dict': self.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'max_err': self.max_err,
            'average_err': self.average_err,
            'settings': self.settings
        }
        torch.save(checkpoint, path)

    @staticmethod
    def load_yk(path):
        if path is None or not os.path.exists(path):
            logger.debug("神经网络模型文件不存在！")
            return None
        checkpoint = torch.load(path)
        model1 = DataFitterNet(checkpoint.get("settings"))
        model1.set_standard(checkpoint['mean'], checkpoint['std'], checkpoint['x_title'], checkpoint['y_title'],
                            checkpoint['normal_method'])
        model1.max_err = checkpoint['max_err']
        model1.average_err = checkpoint['average_err']
        model1.load_state_dict(checkpoint['model_state_dict'])
        model1.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return model1

    def __str__(self):
        str1 = super(DataFitterNet, self).__str__()
        return str1[:-1] + "  (Optimizer): " + self.optimizer.__str__().replace("\n", "\n  ", 1).replace("\n",
                                                                                                         "\n  ") + "\n)"

    def device(self):
        return next(self.parameters()).device

    def train_loop(self, data_loader):
        size = len(data_loader.dataset)
        self.train()
        loss = 0
        is_tqdm = self.settings.get_settings("print.tqdm")
        if is_tqdm:
            from tqdm import tqdm
            pbar = tqdm(data_loader)
        else:
            pbar = data_loader
            pbar.set_set_description = print
        for batch, (x, y) in enumerate(pbar):  # 这里的(x, y)是归一化后的数据
            x = x.to(self.device())
            y = y.to(self.device())
            pred = self.net(x)
            loss = self.loss_fn(pred, y)
            self.optimizer.zero_grad()  # 每一次训练梯度要清零
            loss.backward()
            self.optimizer.step()

            if batch % 10 == 0:
                loss, current = loss.item(), batch * len(x)
                pbar.set_description(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}-{self.y_title}]")

        return loss

    def test_loop(self, data_loader):
        num_batches = len(data_loader)
        size = len(data_loader.dataset)
        test_loss = 0
        self.eval()
        relative_err = 0
        max_err = 0
        with torch.no_grad():
            for x, y in data_loader:
                x = x.to(self.device())
                y = y.to(self.device())
                pred = self.net(x)
                test_loss += self.loss_fn(pred, y).item()
                pred = self.standard_reverse(pred)
                y = self.standard_reverse(y)
                # max_err = max(max_err, (abs(pred-y)/abs(y)).max(0))  # tensor.max()返回最大值,tensor.max(0)返回最大值和索引
                max_err = max(max_err, (abs(pred - y) / abs(y)).max())
                relative_err = ((pred - y).abs() / y.abs()).sum() + relative_err

        test_loss /= num_batches
        relative_err = relative_err / size
        logger.debug(f"测试集预测结果({self.y_title[0]}): 平均损失为{test_loss:>8f}")
        return relative_err, max_err

    def start_train(self, train_set, test_set, writer=None):
        """
        开始模型训练
        :param train_set:
        :param test_set:
        :param writer: tensorboard的记录器
        :return:
        """
        relative_err = []  # 预测结果的相对误差
        if writer is None:
            writer = SummaryWriter(f'./runs/{self.y_title[0]}')  # 可视化数据存放在这个文件夹
        writer.add_graph(self, torch.rand([1, self.in_num], device=self.device()))
        train_loader = DataLoader(dataset=train_set, batch_size=self.batch_size, shuffle=True)
        test_loader = DataLoader(dataset=test_set, batch_size=self.batch_size, shuffle=True)
        for t in range(self.epochs):
            logger.debug(f"-------------------------Epoch {t + 1}-------------------------------")
            train_loss = self.train_loop(train_loader)
            current_err, max_err = self.test_loop(test_loader)
            relative_err.append(current_err)
            logger.debug(f"最大相对误差为{max_err.item():>8f}，平均相对误差为：{current_err:>8f}")
            # ------------------------- 损失曲线图 ---------------------------------
            writer.add_scalar('train/损失', train_loss, t)
            writer.add_scalar('test/平均误差', current_err, t)
            writer.add_scalar('test/最大误差', max_err, t)
            # ------------------------- 损失曲线图 ---------------------------------
            # ------------------------- 权重直方图 ---------------------------------
            for i, (name, param) in enumerate(self.named_parameters()):
                if 'bn' not in name:
                    writer.add_histogram(name + "_data", param, t)
                    writer.add_histogram(name + "_grad", param.grad, t)
            # ------------------------- 权重直方图 ---------------------------------
            try:
                if current_err < 0.01 and max_err < 0.07 and t >= 20:
                    self.max_err = max_err
                    self.average_err = current_err
                    break
            except IndexError:  # 当relative_err列表长度小于3时，会报IndexError错误，此处忽略错误继续训练
                pass
            self.max_err = max_err
            self.average_err = current_err
            if self.trial is not None:
                self.trial.report(self.average_err, t)
                if self.trial.should_prune():
                    raise optuna.TrialPruned
        logger.debug(f"测试集预测结果的相对误差随epoch的变化为：{[x.item() for x in relative_err]}")
        writer.close()
        return self.average_err, self.max_err

    def get_para_type(self, p):
        if isinstance(p, list):
            result = "int"
            for p_ in p:
                if self.get_para_type(p_) == "float":
                    result = "float"
                elif self.get_para_type(p_) == "str":
                    result = "str"
            return result
        else:
            if str(p).strip().isnumeric():  # 小数的isnumeric()方法返回的是false
                return "int"
            else:
                try:
                    _ = eval(p)
                    return "float"
                except NameError:
                    return "str"

    def get_para_of_optuna_str(self, string, name):
        """
        处理设置项中的Optuna优化项，当设置项的值以Optuna开头时，则自动返回Optuna的采样值。

        :param string: 设置项的值
        :param name: 变量名，不影响返回值，但是Optuna工具根据该值识别是哪个变量的采样值，从而给出采样值
        :return:
        """
        result = 0
        if str(string).startswith("optuna"):
            p1 = string.replace("optuna(", "").replace(")", "")
            if "[" not in p1:
                p_list = p1.split(",")
                type1 = self.get_para_type(p_list)
                if type1 == "float":
                    step = None if len(p_list) == 2 else float(p_list[2])
                    result = self.trial.suggest_float(name, float(p_list[0]), float(p_list[1]), step=step)
                elif type1 == "int":
                    step = None if len(p_list) == 2 else int(p_list[2])
                    result = self.trial.suggest_int(name, int(p_list[0]), int(p_list[1]), step=step)
            else:
                p_list = eval(p1)
                result = self.trial.suggest_categorical(name, p_list)
        else:
            result = string
        return result


class OptunaModel:
    def __init__(self, settings=None):
        if settings is None:
            settings = YkDict({})
        self.settings = copy.deepcopy(settings)
        self.settings["networks"] = copy.deepcopy(settings.get_settings("optuna.networks"))
        self.n_trials = int(settings.get_settings("optuna.n_trials") or 10)
        self.device = 'cpu'
        self.mean = None
        self.std = None
        self.x_title = None
        self.y_title = None
        self.train_set = None
        self.test_set = None

    def optimize(self):
        study_name = "model_study20220525"
        study = optuna.create_study(study_name=study_name, direction="minimize",
                                    storage=f'sqlite:///{study_name}.db', load_if_exists=True)
        study.optimize(self.objective, n_trials=self.n_trials)
        trial = study.best_trial
        logger.debug(f"最优模型的损失为{trial.value}")
        logger.debug(f"最优模型的参数为{trial.params}")
        df = study.trials_dataframe()
        print(df)
        self.visualization(study_name)

    @staticmethod
    def visualization(study_name):
        study = optuna.create_study(study_name=study_name, direction="minimize",
                                    storage=f'sqlite:///{study_name}.db', load_if_exists=True)
        optuna.visualization.plot_contour(study).show()  # 参数的等高线图
        optuna.visualization.plot_optimization_history(study).show()  # 优化历史曲线
        optuna.visualization.plot_param_importances(study).show()  # 参数的重要性
        optuna.visualization.plot_intermediate_values(study).show()  # Trails的学习曲线
        optuna.visualization.plot_parallel_coordinate(study).show()  # 高纬度参数的关系，看不懂
        optuna.visualization.plot_slice(study).show()  # 可视化独立参数

    def start_train(self, train_set, test_set):
        self.train_set = train_set
        self.test_set = test_set
        return self.optimize()

    def objective(self, trial):
        model = DataFitterNet(self.settings, trial).to(self.device)
        model.set_standard(self.mean, self.std, self.x_title, self.y_title)
        logger.debug("try model:")
        print(model)
        loss, max_err = model.start_train(self.train_set, self.test_set)
        max_err = max_err.item() if isinstance(max_err, torch.Tensor) else max_err
        loss = loss.item() if isinstance(loss, torch.Tensor) else loss
        trial.set_user_attr('max_err', max_err)
        return loss

    def to(self, device):
        self.device = device
        return self

    def set_standard(self, mean, std, x_title, y_title, *args):
        self.mean = mean
        self.std = std
        self.x_title = x_title
        self.y_title = y_title


def train_model(settings1=None):
    """
    按照settings.yaml文件训练神经网络模型，并保存到settings.yaml指定的位置

    如果settings.networks没有定义具体的网络模型，但是settings.optuna.networks中定义了网络模型的寻优空间参数，则会自动使用
    Optuna库对模型超参数进行寻优，并将寻优结果得到的最有网络模型定义写入settings.yml文件中。再次调用该方法，则会使用寻优得到的
    网络模型架构进行数据拟合，将模型权值信息写入settings.output.save_path指定的路径中。

    如果settings.networks定义了具体的网络模型，则该方法只对定义的模型进行训练，将训练后的权值信息写入settings.output.save_path
    指定的路径中。

    如果该方法同时训练多个单输出模型，则模型架构的优化只会进行一次，即第一个模型架构的优化结果会应用于后续的多个单输出数据拟合任务。

    :return:
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"使用{device}进行计算")
    if settings1 is None:
        settings1 = get_settings()

    if settings1.get("networks") is not None:  # 如果存在networks的定义就直接使用该定义
        optimize_model = False
    elif settings1.get("optuna") is not None:  # 如果存在optuna的设置，就使用该设置获取最有网络模型定义
        optimize_model = True
    else:
        logger.error("未找到模型设置信息，请确认！")
        return
    _settings_ = copy.deepcopy(settings1)
    output = _settings_.get("output") or {}
    if output.get("type") == "single_output":
        paras = copy.deepcopy(output.get("para") or {})
        for i, para in enumerate(paras):
            output["para"] = [para]
            output["save_path"] = settings1.get_settings("output.save_path")[i]
            model = OptunaModel(_settings_).to(device) if optimize_model else DataFitterNet(_settings_).to(device)
            logger.debug(model)
            dataset_all = DataSetFitting(_settings_)  # 获取所有的数据集
            model.set_standard(dataset_all.mean, dataset_all.std_range, dataset_all.x_title, dataset_all.y_title,
                               dataset_all.normal_method)  # 将数据集的数据归一化信息添加到模型中，方便以后使用
            part1 = float(_settings_.get_settings("dataset.data_training.proportion"))
            part2 = float(_settings_.get_settings("dataset.data_test.proportion"))
            train_set, test_set = dataset_all.split_set(part1, part2)  # 均已是归一化后的数据
            model.start_train(train_set, test_set)
            if not optimize_model:
                model.save_yk(output["save_path"])
            else:
                model.update_settings_file("settings.yml")
                train_model()


def re_train(data_file, settings1=None):
    """
    在现有模型基础上再次训练，该方法对数据的归一化方法必须与初次训练时一致，因此本方法会忽略settings1中的数据归一化相关设置，而自动采用原模型中
    的数据归一化方法

    :param data_file: 数据文件,csv文件
    :param settings1: 可以直接传入settings字典，则该方法不会再从外部yaml文件读取设置信息
    :return:
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"使用{device}再次训练")
    if settings1 is None:
        settings1 = get_settings()
    _settings_ = copy.deepcopy(settings1)
    if isinstance(data_file, list):
        _data_file = []
        for file in data_file:
            _data_file.append({"name": file, "type": "csv"})
        _settings_["dataset"]["data_file"] = _data_file
    else:
        _settings_["dataset"]["data_file"] = [{"name": data_file, "type": "csv"}]
    output = _settings_.get("output") or {}
    if output.get("type") == "single_output":
        paras = copy.deepcopy(output.get("para") or {})
        for i, para in enumerate(paras):
            output["para"] = [para]
            output["save_path"] = settings1.get_settings("output.save_path")[i]
            model = DataFitterNet.load_yk(output["save_path"])
            model.epochs = _settings_.get_settings("networks.train.epochs")  # 再次训练时的epochs和初次训练时的一般不相同
            logger.debug(model)
            dataset_all = DataSetFitting(_settings_)  # 获取所有的数据集
            if _settings_.get_settings("dataset.normalization") != model.normal_method:
                logger.warning(f"再训练时数据归一化方法({_settings_.get_settings('dataset.normalization')})与"
                               f"模型初次训练时({model.normal_method})不一致，这可能导致预测结果错误")
                logger.warning(f"已强制切换为模型初次训练时使用的数据归一化方法！({model.normal_method})")
            dataset_all.set_standard(model.mean, model.std, model.normal_method)
            part1 = 0.95
            part2 = 0.05
            train_set, test_set = dataset_all.split_set(part1, part2)  # 均已是归一化后的数据
            model.start_train(train_set, test_set)

            model.save_yk(output["save_path"])


def filter_err_condition(model, data_file=None):
    """
    将model在整个数据集上进行测试，过滤小偏差的点，删选出偏差较大的点，一般后续对偏差较大的点继续学习

    :param model:
    :param data_file:
    :return:
    """
    settings = get_settings()
    if data_file is not None:
        settings["dataset"]["data_file"] = [{"name": data_file, "type": "csv"}]
    _settings_ = copy.deepcopy(settings)
    dataset_all = DataSetFitting(_settings_)
    dataset_all.set_standard(model.mean, model.std_range)


def setup_seed(seed=10):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)


def test():
    model = DataFitterNet.load_yk(r"D:\lengduan\data\model_p2.dat")
    args = {
        "power": 400,
        "flow_heat": 0,
        "p_env": 98,
        "t_env": 30,
        "humid": 0.60,
        "p_gas": 3.8,
        "t_gas": 18,
        "flow_fgh": 40,
        "flow_tca": 100,
        "flow_oh": 3,
        "flow_rh": 0
    }
    x = [v for k, v in args.items()]
    pump, fun = 2, 3
    x.extend([pump, fun])
    p = model.prediction(x)
    print(p)


def deal_settings_path(settings, **kwargs):
    """
    当settings.yaml文件中使用了带变量的路径时，如"E:/热工院//retrain{unit}_0.csv",
    本方法将变量{unit}替换为指定的变量。

    :param settings:
    :return:
    """
    files = []

    for data_file in settings.get_settings("dataset.data_file"):
        pth = data_file["name"].replace(r"{unit}", "1")
        type1 = data_file["type"]
        files.append({"name": pth, "type": type1})
    settings["dataset"]["data_file"] = files
    return settings


if __name__ == "__main__":
    setup_seed()
    OptunaModel(None).visualization("model_study20220525")
    # settings1 = get_settings()
    # deal_settings_path(settings1)
    # train_model(settings1)
    # # settings["output"]["save_path"] = [r"D:\lengduan\data\model_p1.dat"]
    # # settings["output"]["para"] = ["背压"]
    # re_train(data_file=[
    #     r"D:\lengduan\data\retrain1_0.csv",
    #     r"D:\lengduan\data\retrain1_1.csv",
    #     r"D:\lengduan\data\retrain1_7.csv",
    #     r"D:\lengduan\data\retrain1_9.csv",
    #     r"D:\lengduan\data\retrain1_10.csv",
    #     r"D:\lengduan\data\retrain1_11.csv",
    # ], settings1=settings_1)
    # re_train(data_file=[
    #     r"D:\lengduan\data\retrain2_0.csv",
    #     r"D:\lengduan\data\retrain2_1.csv",
    #     r"D:\lengduan\data\retrain2_7.csv",
    #     r"D:\lengduan\data\retrain2_8.csv",
    #     r"D:\lengduan\data\retrain2_9.csv",
    #     r"D:\lengduan\data\retrain2_10.csv",
    #     r"D:\lengduan\data\retrain2_11.csv",
    # ], settings1=settings_1)
