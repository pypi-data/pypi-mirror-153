import torch
import torch.nn as nn
import random
import numpy as np
import yangke.stock.globalVar as gv
import os
import sys
import yangke.stock.dataset.data_reader as dr
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset, Dataset
from yangke.common.config import holdLoggingLevel
import logging

torch.manual_seed(10000)
np.random.seed(10000)
random.seed(10000)


class MAXLoss(nn.Module):
    """
    自定义Loss函数，主要在于指定loss为批数据中最大的，torch自带的loss只能使用批数据的平均值
    """
    def __init__(self):
        super(MAXLoss, self).__init__()

    def forward(self, pred, target):
        ret = torch.abs(pred - target)
        ret = torch.pow(ret, 2)
        loss = ret.max()
        return loss


def prediction(stock_codes: list, method: str = "fit") -> pd.DataFrame:
    """
    预测列表中的股票涨幅，不会预测最近上市的股票——即股票上市时间小于(bptt_len+100)天的股票。

    新上市股票建议使用专用方法进行预测。

    :param stock_codes: 股票代码的列表
    :param method: 预测方法，目前支持'fit','classify','fit-1'
    :return: pd.DataFrame()，第一列为股票代码，第二列为涨幅
    """
    if method == "fit":
        method1 = lstm_stock_use_in_build_rnn_fit
    elif method == "classify":
        method1 = lstm_stock_classify
    elif method == "fit-1":
        method1 = lstm_stock_fit  # 所有股票共用同一个预测模型
    else:
        gv.logger.critical("method名不正确，接受到{}，但目前只支持{}".format(method, ['fit', 'classify', 'fit-1']))
        sys.exit(0)

    model_saved_folder = os.path.join(gv.dataDirectory, "nn-model/pytorch/lstm-{}".format(method))
    if not os.path.exists(model_saved_folder):
        os.makedirs(model_saved_folder)

    pred_list = []
    stock_codes_ = []  # 重新声明一个股票代码列表，用于记录可以正确预测涨跌幅的股票代码

    for i in range(len(stock_codes)):
        stock_code = stock_codes[i]
        model_saved_path = os.path.join(model_saved_folder, "{}.pth".format(stock_code))
        holdLoggingLevel(logging.WARNING)
        if '-1' in method:  # 如果是共用model进行预测，则传入公共model名
            pred = method1(stock_code, os.path.join(model_saved_folder, 'allInOneModel.pth'))
        else:
            pred = method1(stock_code, model_saved_path)
        holdLoggingLevel()
        gv.logger.debug("预测进度(完成预测的股票数)/(总股票数)：{}/{}，当前预测股票代码：{}".format(i, len(stock_codes), stock_code))
        if pred is not None:  # 如果有预测结果，则添加，有些没有结果的则不添加
            stock_codes_.append(stock_code)
            pred_list.append(pred)
        else:
            gv.logger.info("股票{}的预测结果为空，该股票可能是新股，数据量不足以进行预测！".format(stock_code))

    pred_dict = {'stock_code': stock_codes_, 'p_change': pred_list}
    result = pd.DataFrame.from_dict(pred_dict)
    return result


def get_data(stock_code: str or list, col_x=['close'], col_y=None, days=30, split=0.7):
    """
    对应每只股票获得其所有历史数据，组成训练集，测试集和需要预测的数据predX。

    可用于拟合模型和分类模型

    :param stock_code:
    :param col_x: 神经网络输入的数据列
    :param col_y: 神经网络输出的数据列
    :param days: 使用前days天的数据预测后一天的数据
    :param split: 数据集分割比例，如训练数据：验证数据 = 7:3，则split=0.7
    :return:
    """
    batch_size = 8
    result = dr.get_data_days_list(stock_code, col_x=col_x, col_y=col_y, days=days,
                                   normalization='z-score', need_pred=True,
                                   split=split)
    if result is None:  # 有些新开股票，数据太少不足以生成一条训练数据，则返回结果是None
        return None
    train_x, train_y, test_x, test_y, predict_x = result

    if col_y is None:
        train_x, train_y = torch.from_numpy(train_x).type(torch.float), torch.from_numpy(train_y).type(torch.float)
        test_x, test_y = torch.from_numpy(test_x).type(torch.float), torch.from_numpy(test_y).type(torch.float)
    elif isinstance(col_y, list):  # 如果是分类问题，则y是整数，表示类别
        train_x, train_y = torch.from_numpy(train_x).type(torch.float), torch.from_numpy(train_y).type(torch.long)
        test_x, test_y = torch.from_numpy(test_x).type(torch.float), torch.from_numpy(test_y).type(torch.long)
    predict_x = torch.from_numpy(predict_x).type(torch.float)

    train_dataset = TensorDataset(train_x, train_y)
    test_dataset = TensorDataset(test_x, test_y)
    # 只有在数据量很大的时候使用多核加载才能提高速度，数据量小时反而会降低速度
    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)  # , num_workers=2)
    test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True)  # , num_workers=2)
    if isinstance(col_y, list):  # 如果是分类问题
        num_classes = len(col_y) + 1
        return train_loader, test_loader, batch_size, days, num_classes, predict_x
    else:  # 如果是拟合问题
        return train_loader, test_loader, batch_size, days, predict_x


def need_update_model(model):
    """
    判断一个pytorch模型是否需要更新

    :param model:
    :return:
    """
    if os.path.exists(model):
        return False
    return True


class RNN_fit(nn.Module):
    # bptt_len=30，即过去30天的数据，input_size=1即每天取一个数据
    def __init__(self, bptt_len, input_size, hidden_size, num_layers):
        super(RNN_fit, self).__init__()
        # 定义模型中的神经网络层
        self.rnn = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)

        # 用于将隐含层的输入映射到输出
        self.linear = nn.Linear(in_features=hidden_size * bptt_len, out_features=1)

    # input: [8, 30, 1], hidden: [batch_size, num_layers, hidden_size] # 这里把batch_size调到第一位
    def forward(self, x):
        # rnn层的输入和输出形状是相同的
        output, _ = self.rnn(x)

        # 需要调用output.contiguous()将Tensor的存储整理为连续存储，否则可能报错，原因可能是多卡存储或其他
        output = output.contiguous().view(output.size(0), output.size(1) * output.size(2))  # [8, 30, 1]->[8, 30]

        # 添加一个激活函数，该层为非线性，使得网络可以处理非线性关系，LSTM中有非线性，可能不需要，这里对比下训练结果
        # 不添加激活函数 # 0.20275171101093292, test loss 4.4828590740358205, adjust lr to 0.000625
        output = torch.sigmoid(output)  # loss 0.00398010341450572, test loss 4.799441468508946
        # output = torch.tanh(output)  # loss 0.209489107131958, test loss 4.479561124922912, adjust lr to 0.000625
        # output = torch.relu(output)  # loss 1.0070337057113647, test loss 4.457948378744842
        # output = torch.nn.functional.softplus(output)  # loss 0.0015654880553483963, test loss 4.68150989030827

        # 这里将lstm层输出的Tensor形状的前两位合并，只有输出的维度是需要传出去，以和labels进行比较计算loss
        output = self.linear(output)  # 将[*, input_size]映射到[*, output_size], [8, 30]->[8, 1]

        output = output.squeeze(-1)  # [8, 1] -> [8]
        return output

    def prediction(self, x):
        with torch.no_grad():
            if x.dim() == 2:  # 说明只有一个数据，则添加batch对应的维度
                x = x.unsqueeze(0)
            output = self.forward(x)
        return output.item()


class RNN_classify(nn.Module):
    # bptt_len=30，即过去30天的数据，input_size=1即每天取一个数据, num_classes即分类数量
    def __init__(self, bptt_len, input_size, hidden_size, num_layers, num_classes):
        super(RNN_classify, self).__init__()
        # 定义模型中的神经网络层
        self.rnn = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        # 用于将隐含层的输入映射到输出
        self.linear = nn.Linear(in_features=hidden_size * bptt_len, out_features=num_classes)

    # input: [8, 30, 1], hidden: [batch_size, num_layers, hidden_size] # 这里把batch_size调到第一位
    def forward(self, x):
        # rnn层的输入和输出形状是相同的
        output, _ = self.rnn(x)

        # 需要调用output.contiguous()将Tensor的存储整理为连续存储，否则可能报错，原因可能是多卡存储或其他
        output = output.contiguous().view(output.size(0), output.size(1) * output.size(2))  # [8, 30, 1]->[8, 30]

        # 添加一个激活函数，该层为非线性，使得网络可以处理非线性关系
        # output = torch.sigmoid(output)  # loss 0.5425181984901428, test loss 0.7410567089312339, adjust lr to 0.000625
        # output = torch.tanh(output)  # loss 0.19794771075248718, test loss 0.6420857055338821
        output = torch.relu(output)  # loss 0.12568356096744537, test loss 0.6467462378430229
        # output = torch.nn.functional.softplus(output)  # loss 0.5891538262367249, test loss 0.7501011504603259, adjust lr to 0.000625

        # 这里将lstm层输出的Tensor形状的前两位合并，只有输出的维度是需要传出去，以和labels进行比较计算loss
        output = self.linear(output)  # 将[*, input_size]映射到[*, output_size], [8, 30]->[8, hidden_size]

        return output

    def prediction(self, x):
        with torch.no_grad():
            if x.dim() == 2:
                x = x.unsqueeze(0)  # 增加一维作为batch_size为1的数据，如果batch_first=False，则x.unsqueeze(1)
            output = self.forward(x).squeeze(0)
            sm = nn.Softmax(dim=0)
            output = sm(output).numpy()
            classes = output.argmax()  # 获得最大元素的索引，是为分类号
        return classes, output


def evaluate(model: RNN_fit, test_loader, loss_fn):
    model.eval()
    total_loss = 0.
    total_count = 0.
    with torch.no_grad():
        for i, (data, labels) in enumerate(test_loader):
            output = model(data)

            loss = loss_fn(output, labels)
            total_count += len(data)  # 一共多少数据
            total_loss += loss.item() * len(data)  # 总的loss
    loss = total_loss / total_count
    model.train()
    return loss


def train(model, epochs, train_loader, test_loader, optimizer, scheduler, loss_fn, model_path):
    train_losses = []
    val_losses = []  # 记录训练过程中的losses，方便后续绘图
    flag = 0
    for epoch in range(epochs):
        # input: [batch_size, bptt_len, input_size], labels: [batch_size]
        for i, (data, labels) in enumerate(train_loader):
            # 输入形状是[8, 30, 1]，即[batch_size, bptt_len, input_size]
            out = model(data)  # out: [8]

            loss = loss_fn(out, labels)
            optimizer.zero_grad()
            loss.backward()
            # torch.nn.utils.clip_grad_norm_(model.parameters(), 1)  # 防止参数过大
            optimizer.step()
            if i % 10 == 0:
                val_loss = evaluate(model, test_loader, loss_fn)

                if len(val_losses) == 0 or val_loss < min(val_losses):
                    gv.logger.info("epoch {}, step {}, loss {}, test loss {}".format(epoch, i, loss, val_loss))
                    torch.save(model.state_dict(), model_path)
                elif loss < min(train_losses) and flag < 3:  # 训练集损失减小，测试集损失增大，继续训练，
                    flag = flag + 1  # 连续三次如此，则更改学习速率
                    gv.logger.info("epoch {}, step {}, loss {}, test loss {}".format(epoch, i, loss, val_loss))
                else:  # 表示训练数据和测试数据都变差
                    flag = 0
                    scheduler.step()  # 会自动把optimizer中的lr修改为更小
                    real_time_lr = optimizer.param_groups[0]['lr']
                    gv.logger.info("epoch {}, step {}, loss {}, test loss {}, adjust lr to {}"
                                   .format(epoch, i, loss, val_loss, real_time_lr))

                # 记录训练和测试数据集的损失
                train_losses.append(loss)
                val_losses.append(val_loss)
    return model


def lstm_stock_use_in_build_rnn_fit(stock_code: str, model_path: str = None):
    """
    使用torch内置的LSTM层进行股票预测，与lstm_stock_use_in_build_rnn()功能相同，只是为了保证复现，修改了一些随机数的机制

    :param stock_code:
    :param model_path: 神经网络模型的保存路径，最好是绝对路径，否则会保存到主程序的目录下
    :return:
    """
    stock_code = str(stock_code)
    if model_path is None:
        os.makedirs(f"{gv.dataDirectory}/torch/model/", exist_ok=True)  # 确保路径存在
        saved_model_pth = f"{gv.dataDirectory}/torch/model/{stock_code}.pth"
    else:
        saved_model_pth = model_path

    col_x = ['close', 'volume']
    result = get_data(stock_code, col_x=col_x)
    if result is None:  # 没有股票数据
        return None
    train_loader, test_loader, batch_size, days, predX = result

    model = RNN_fit(bptt_len=days, input_size=len(col_x), hidden_size=64, num_layers=2)
    if not need_update_model(saved_model_pth):  # 如果不需要更新模型
        model.load_state_dict(torch.load(saved_model_pth))
        model.eval()
        predY = model.prediction(predX)
        return predY

    learning_rate = 0.01
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, 0.5)

    # loss_fn = torch.nn.MSELoss()
    loss_fn = MAXLoss()  # 因为我们主要关心最差的时候别太差

    model = train(model, 2, train_loader, test_loader, optimizer, scheduler, loss_fn, saved_model_pth)

    pred = model.prediction(predX)
    gv.logger.info("预测股票{}明天的涨幅为{}".format(stock_code, pred))
    return pred


def lstm_stock_classify(stock_code: str, model_path: str = None):
    stock_code = str(stock_code)
    if model_path is None:
        saved_model_pth = "{}.pth".format(stock_code)
    else:
        saved_model_pth = model_path

    # 输入数据的列数，假如考虑过去30天开盘价和收盘价，则input_size=2, bptt_len=30
    def main(input_size):
        EPOCHS = 2

        model = RNN_classify(bptt_len, input_size, hidden_size=64, num_layers=2, num_classes=num_classes)

        if not need_update_model(saved_model_pth):  # 如果不需要更新模型
            model.load_state_dict(torch.load(saved_model_pth))
            model.eval()
            predY = model.prediction(predX)
            return predY

        learning_rate = 0.01
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, 0.5)

        loss_fn = torch.nn.CrossEntropyLoss()

        train_losses = []
        val_losses = []  # 记录训练过程中的losses，方便后续绘图
        flag = 0
        flag1 = 0
        for epoch in range(EPOCHS):
            # input: [batch_size, bptt_len, input_size], labels: [batch_size]
            for i, (data, labels) in enumerate(train_loader):
                # 输入形状是[8, 30, 1]，即[batch_size, bptt_len, input_size]
                out = model(data)  # out: [batch_size, num_classes]:[8, 3]

                loss = loss_fn(out, labels)  # out: [8, 3], labels: [8]
                optimizer.zero_grad()
                loss.backward()
                # torch.nn.utils.clip_grad_norm_(model.parameters(), 1)  # 防止参数过大
                optimizer.step()
                if i % 10 == 0:
                    val_loss = evaluate(model, test_loader, loss_fn)

                    if len(val_losses) == 0 or val_loss < min(val_losses):
                        gv.logger.info("epoch {}, step {}, loss {}, test loss {}".format(epoch, i, loss, val_loss))
                        torch.save(model.state_dict(), saved_model_pth)
                    elif loss < min(train_losses) and flag < 3:  # 训练集损失减小，测试集损失增大，继续训练，
                        flag = flag + 1  # 连续三次如此，则更改学习速率
                        gv.logger.info("epoch {}, step {}, loss {}, test loss {}".format(epoch, i, loss, val_loss))
                    elif flag < 3:  # 表示训练数据和测试数据都变差
                        flag = 0
                        flag1 = flag1 + 1
                        scheduler.step()  # 会自动把optimizer中的lr修改为更小
                        real_time_lr = optimizer.param_groups[0]['lr']
                        gv.logger.info("epoch {}, step {}, loss {}, test loss {}, adjust lr to {}"
                                       .format(epoch, i, loss, val_loss, real_time_lr))

                    # 记录训练和测试数据集的损失
                    train_losses.append(loss)
                    val_losses.append(val_loss)

        # predY=0表示涨幅小于1%，predY=1：涨幅[1%, 5%)，predY=2：涨幅[5%,)
        predY, probability = model.prediction(predX)  # 获得分类号，model(x)获得的是最后一个线性层的输出
        return predY, probability

    col_x = ['close', 'volume']
    col_y = [1, 5]
    result = get_data(stock_code, col_x=col_x, col_y=col_y, days=30)
    if result is None:  # 没有股票数据
        return None
    train_loader, test_loader, batch_size, bptt_len, num_classes, predX = result
    pred, prob = main(len(col_x))
    gv.logger.info("预测股票{}的明天涨幅为{}，概率分布为{}".format(stock_code, pred, prob))
    return pred, prob.max()


def lstm_stock_fit(stock_code, model_path: str = None):
    """
    将所有股票数据用同一个模型拟合

    :param stock_code:
    :param model_path:
    :return:
    """
    if model_path is None:
        saved_model_pth = "allInOneModel.pth"
        saved_model_pth = os.path.abspath(saved_model_pth)
        gv.logger.warning('No model path is specified, The model is saved in {}'.format(saved_model_pth))
    else:
        saved_model_pth = model_path

    col_x = ['close']
    col_y = None
    days, split = 30, 0.7
    input_size = len(col_x)
    epochs = 2
    learning_rate = 0.01
    # 根据股票代码获得predX
    result = dr.get_data_days_list(stock_code, col_x=col_x, col_y=col_y, days=days,
                                   normalization='z-score', need_pred=True,
                                   split=split)
    if result is None:  # 有些新开股票，数据太少不足以生成一条训练数据，则返回结果是None
        return None
    _, _, _, _, predX = result
    predX = torch.from_numpy(predX).type(torch.float)

    # 无论如何，使用全部股票数据进行模型训练
    stock_codes = gv.tsd.download_all_stocks()
    train_codes, _, test_codes, _ = dr.__split_dataset(stock_codes, stock_codes, split)
    dataset_train = dr.StockDataset(train_codes)
    dataset_test = dr.StockDataset(test_codes)
    train_loader = DataLoader(dataset=dataset_train, batch_size=8, shuffle=True)
    test_loader = DataLoader(dataset=dataset_test, batch_size=8, shuffle=False)

    model = RNN_fit(bptt_len=days, input_size=input_size, hidden_size=64, num_layers=2)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, 0.5)

    # loss_fn = torch.nn.MSELoss()
    loss_fn = MAXLoss()  # 因为我们主要关心最差的时候别太差
    model = train(model, epochs=epochs, train_loader=train_loader, test_loader=test_loader,
                  optimizer=optimizer, scheduler=scheduler, loss_fn=loss_fn, model_path=saved_model_pth)

    result = model.prediction(predX)
    return result
