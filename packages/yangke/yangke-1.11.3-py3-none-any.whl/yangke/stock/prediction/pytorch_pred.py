# import numpy as np
# import globalVar as gv
# import os
# import random
#
# import torch
# import torch.nn as nn
# import dataset.data_reader as dr
# from torch.autograd import Variable
# from torch.utils.data import DataLoader, Dataset, TensorDataset
# import torchtext  # NLP处理数据用
# from torchtext.vocab import Vectors
#
# import matplotlib.pyplot as plt
#
#
# def test1_numpy():
#     """
#     使用numpy构建一个全连接ReLU神经网络，一个隐藏层，没有bias。用来从x预测y，使用L2 Loss。
#         h = W_1*x
#         a = max(0, h)
#         y_hat = W_2*a
#     """
#     N, D_in, H, D_out = 64, 1000, 100, 10
#
#     # 随机创建一些训练数据
#     x = np.random.randn(N, D_in)
#     y = np.random.randn(N, D_out)
#
#     w1 = np.random.randn(D_in, H)
#     w2 = np.random.randn(H, D_out)
#
#     learning_rate = 1e-6
#     for it in range(500):
#         # Forward pass
#         h = x.dot(w1)  # N * H
#         h_relu = np.maximum(h, 0)  # N * H
#         y_pred = h_relu.dot(w2)  # N * D_out
#
#         # compute loss
#         loss = np.square(y_pred - y).sum()
#         print(it, loss)
#
#         # Backward pass
#         # compute the gradient
#         grad_loss_to_y_pred = 2 * (y_pred - y)  # N * D_out
#         grad_y_pred_to_w2 = h_relu.T.dot(grad_loss_to_y_pred)  # H * D_out
#         grad_loss_to_w2 = grad_y_pred_to_w2
#         grad_loss_to_h_relu = grad_loss_to_y_pred.dot(w2.T)  # N * H
#         grad_loss_to_h = grad_loss_to_h_relu.copy()  # N * H
#         grad_loss_to_h[h < 0] = 0  # 激活函数ReLUctant
#         grad_loss_to_w1 = x.T.dot(grad_loss_to_h)  # D_in * H
#
#         # update weights of w1 and w2
#         w1 -= learning_rate * grad_loss_to_w1
#         w2 -= learning_rate * grad_loss_to_w2
#
#
# def test1_torch():
#     """
#     使用pytorch构建一个全连接ReLU神经网络，一个隐藏层，没有bias。用来从x预测y，使用L2 Loss。
#         h = W_1*x
#         a = max(0, h)
#         y_hat = W_2*a
#     """
#     autoGradient = True
#
#     N, D_in, H, D_out = 64, 1000, 100, 10
#
#     # 随机创建一些训练数据
#     x = torch.randn(N, D_in)
#     y = torch.randn(N, D_out)
#
#     w1 = torch.randn(D_in, H, requires_grad=autoGradient)
#     w2 = torch.randn(H, D_out, requires_grad=autoGradient)
#
#     learning_rate = 1e-6
#     for it in range(500):
#         if not autoGradient:
#             # Forward pass
#             h = x.mm(w1)  # N * H
#             h_relu = h.clamp(min=0)  # N * H
#             y_pred = h_relu.mm(w2)  # N * D_out
#
#             # compute loss
#             loss = (y_pred - y).pow(2).sum()
#             print(it, loss.item())
#
#             # Backward pass
#             # compute the gradient
#             grad_loss_to_y_pred = 2 * (y_pred - y)  # N * D_out
#             grad_y_pred_to_w2 = h_relu.t().mm(grad_loss_to_y_pred)  # H * D_out
#             grad_loss_to_w2 = grad_y_pred_to_w2
#             grad_loss_to_h_relu = grad_loss_to_y_pred.mm(w2.t())  # N * H
#             grad_loss_to_h = grad_loss_to_h_relu.clone()  # N * H
#             grad_loss_to_h[h < 0] = 0  # 激活函数ReLUctant
#             grad_loss_to_w1 = x.t().mm(grad_loss_to_h)  # D_in * H
#
#             # update weights of w1 and w2
#             w1 -= learning_rate * grad_loss_to_w1
#             w2 -= learning_rate * grad_loss_to_w2
#         # 以上求导步骤pytorch都可以自动完成
#         else:
#             # Forward pass
#             y_pred = x.mm(w1).clamp(min=0).mm(w2)
#             # compute loss
#             loss = (y_pred - y).pow(2).sum()
#             print(it, loss.item())
#             # Backward pass
#
#             loss.backward()
#             with torch.no_grad():
#                 w1 -= learning_rate * w1.grad
#                 w2 -= learning_rate * w2.grad
#                 w1.grad.zero_()
#                 w2.grad.zero_()
#
#
# def test1_torch_nn():
#     """
#     使用pytorch提供的model进行神经网络拟合
#     :return:
#     """
#     N, D_in, H, D_out = 64, 1000, 100, 10
#
#     # 随机创建一些训练数据
#     x = torch.randn(N, D_in)
#     y = torch.randn(N, D_out)
#
#     model = torch.nn.Sequential(
#         torch.nn.Linear(D_in, H, bias=False),
#         torch.nn.ReLU(),
#         torch.nn.Linear(H, D_out, bias=False)
#     )
#     # 这里显式初始化一下模型的weight，不初始化也可以
#     nn.init.normal_(model[0].weight)
#     nn.init.normal_(model[2].weight)
#
#     loss_fn = nn.MSELoss(reduction='sum')
#
#     learning_rate = 1e-6
#     for it in range(500):
#         # Forward pass
#         y_pred = model(x)
#
#         # compute loss
#         loss = loss_fn(y_pred, y)
#         print(it, loss.item())  # python中，loss.item是方法的地址，loss.item()是方法的返回值，注意小括号别少了
#
#         model.zero_grad()
#
#         # Backward pass
#         loss.backward()
#
#         # update weights of w1 and w2
#         with torch.no_grad():
#             for param in model.parameters():
#                 param -= learning_rate * param.grad
#
#
# def test1_torch_nn_optim():
#     """
#     使用pytorch提供的model进行神经网络拟合
#     优化方法使用optim工具
#     :return:
#     """
#     N, D_in, H, D_out = 64, 1000, 100, 10
#
#     # 随机创建一些训练数据
#     x = torch.randn(N, D_in)
#     y = torch.randn(N, D_out)
#
#     model = torch.nn.Sequential(
#         torch.nn.Linear(D_in, H, bias=False),
#         torch.nn.ReLU(),
#         torch.nn.Linear(H, D_out, bias=False)
#     )
#
#     loss_fn = nn.MSELoss(reduction='sum')
#     learning_rate = 1e-3
#     optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
#
#     for it in range(500):
#         # Forward pass
#         y_pred = model(x)
#
#         # compute loss
#         loss = loss_fn(y_pred, y)
#         print(it, loss.item())  # python中，loss.item是方法的地址，loss.item()是方法的返回值，注意小括号别少了
#
#         optimizer.zero_grad()
#         # Backward pass
#         loss.backward()
#         optimizer.step()
#
#
# def test1_torch_module():
#     """
#     使用继承自nn.Module的类定义模型
#     优化方法使用optim工具
#     :return:
#     """
#     N, D_in, H, D_out = 64, 1000, 100, 10
#
#     # 随机创建一些训练数据
#     x = torch.randn(N, D_in)
#     y = torch.randn(N, D_out)
#
#     class TwoLayerNet(torch.nn.Module):
#         def __init__(self, D_in, H, D_out):
#             # define the model architecture
#             super(TwoLayerNet, self).__init__()
#             self.linear1 = torch.nn.Linear(D_in, H, bias=False)
#             self.linear2 = torch.nn.Linear(H, D_out, bias=False)
#
#         def forward(self, x):
#             y_pred = self.linear2(self.linear1(x).clamp(min=0))
#             return y_pred
#
#     model = TwoLayerNet(D_in, H, D_out)
#
#     loss_fn = nn.MSELoss(reduction='sum')
#     learning_rate = 1e-4
#     optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
#
#     for it in range(500):
#         # Forward pass
#         y_pred = model(x)
#
#         # compute loss
#         loss = loss_fn(y_pred, y)
#         print(it, loss.item())  # python中，loss.item是方法的地址，loss.item()是方法的返回值，注意小括号别少了
#
#         optimizer.zero_grad()
#         # Backward pass
#         loss.backward()
#         optimizer.step()
#
#
# def test1_torch_lstm_language():
#     """
#     https://www.bilibili.com/video/av82398400?p=3
#     语言模型
#
#     :return:
#     """
#     random.seed(53113)
#     np.random.seed(53113)
#     torch.manual_seed(53113)
#
#     BATCH_SIZE = 8
#     EMBEDDING_SIZE = 100
#     MAX_VOCAB_SIZE = 20000
#
#     TEXT = torchtext.data.Field(lower=True)
#     text_path = os.path.join(gv.dataDirectory, 'text8')
#     train, val, test = torchtext.datasets.LanguageModelingDataset.splits(path=text_path,
#                                                                          train='text8.train.txt',
#                                                                          validation='text8.dev.txt',
#                                                                          test='text8.test.txt',
#                                                                          text_field=TEXT)
#     # 根据train数据生成词汇表:Text.vocab，通过vocab.itos[index]将索引转为单词，通过vocab.stoi.get('单词')将单词转为索引
#     TEXT.build_vocab(train, max_size=MAX_VOCAB_SIZE)
#     VOCAB_SIZE = len(TEXT.vocab)  # VOCAB_SIZE会比MAX_VOCAB_SIZE大2，因为torchtext会自动在词汇表中添加<unk>和<pad>两个词
#     print("vocabulary size:{}".format(VOCAB_SIZE))  # {vocabulary size:50002}
#     train_iter, val_iter, test_iter = torchtext.data.BPTTIterator.splits(
#         (train, val, test), batch_size=BATCH_SIZE, device=-1, bptt_len=32, repeat=False, shuffle=True
#     )  # 猜测bptt_len是bptt算法求历史倒数的限制长度，即最多求前bptt_len个历史时刻的倒数，往前则截断，体现在训练数据上则只需要提供bptt_len长度的数据即可
#
#     # 测试数据集是否正确
#     it = iter(train_iter)  # train_iter为torchtext提供的BPTTIterator返回，本身封装了一些语言模型训练时特有的属性
#     for i in range(5):
#         # batch属性在torchtext中定义，包含text和target两个属性，分别对应输入和输出数据，这些数据都是索引值
#         batch = next(it)
#         # batch.text，类型是Tensor，形状是bptt_len*batch_size，我们取batch中第一个输入输出查看
#         print(" ".join([TEXT.vocab.itos[i] for i in batch.text[:, 0].data]))
#         print()
#         print(" ".join([TEXT.vocab.itos[i] for i in batch.target[:, 0].data]))
#
#     class RNNModel(nn.Module):
#         def __init__(self, rnn_type, vocab_size, input_size, hidden_size, num_layers, dropout=0.5):
#             """
#             该模型包含以下几层：
#             -词嵌入层
#             -一个循环神经网络层（RNN、LSTM、GRU）
#             -一个线性层，从hidden state到输出单词表
#             -一个dropout层，用来做regularization
#             """
#             super(RNNModel, self).__init__()
#             self.drop = nn.Dropout(dropout)
#             # 定义一个encoder方法，将输入向量编码为结合词汇表信息的输入变量，会增加输入向量的维度，
#             # 因为输入向量中，一个数字对应一个单词，而编码结果中，一个单词对应一个长度embedding_dim的向量
#             self.embed = nn.Embedding(num_embeddings=vocab_size, embedding_dim=input_size)
#             if rnn_type in ['LSTM', 'GRU']:
#                 inner_model = getattr(nn, rnn_type)
#                 # 根据RNNBase初始化LSTM模型的隐含层数量及各个参数
#                 self.rnn = nn.LSTM(input_size, hidden_size, num_layers, dropout=dropout)
#                 self.rnn = inner_model(input_size, hidden_size, num_layers, dropout=dropout)
#             else:
#                 try:
#                     nonlinearity = {'RNN_TANH': 'tanh', 'RNN_RELU': 'relu'}[rnn_type]
#                 except KeyError:
#                     raise ValueError("""An invalid option for '--model' was supplied,
#                     options are ['LSTM', 'GRU', 'RNN_TANH', or 'RNN_RELU']""")
#                 self.rnn = nn.rnn(input_size, hidden_size, num_layers, nonlinearity=nonlinearity, dropout=dropout)
#
#             # 将隐含层的输入映射到字典索引；输入：N, *, in_features；输出：N, *, out_features
#             self.linear = nn.Linear(in_features=hidden_size, out_features=vocab_size)
#
#             self.init_weights()  # RNN的参数在调用时自动初始化，这里初始化Embedding层和Linear层
#
#             self.rnn_type = rnn_type
#             self.hidden_size = hidden_size
#             self.num_layers = num_layers
#
#         def init_weights(self):
#             init_range = 0.1
#             self.embed.weight.data.uniform_(-init_range, init_range)
#             self.linear.bias.data.zero_()
#             self.linear.weight.data.uniform_(-init_range, init_range)
#
#         # input: [bptt_len, batch_size], hidden: [num_layers, batch_size, hidden_size]
#         def forward(self, input, hidden):
#             emb = self.drop(self.embed(input))  # emb: [bptt_len, batch_size, input_size]
#             # run层的输入和输出形状是相同的
#             output, hidden = self.rnn(emb, hidden)  # output: [bptt_len, batch_size, input_size]
#
#             output = self.drop(output).view(output.size(0) * output.size(1), output.size(2))
#             # [bptt_len * batch_size, input_size]
#             # 这里其实可以不经过变形，因为self.decoder=nn.Linear接受的是[N, *, input_size]形状的数据，
#             # 即只要最后一维的形状对应即可，但展开的话符合线性层神经网络输入到输出的传统对应关系
#             decoded = self.linear(output)  # 将[*, input_size]映射到[*, output_size]，这里output_size=vocab_size
#             decoded = decoded.view(emb.size(0), emb.size(1), decoded.size(1))
#
#             # decoded: [bptt_len, batch_size, vocab_size], hidden: [num_layers, batch_size, hidden_size]
#             return decoded, hidden
#
#         def init_hidden(self, batch_size, required_grad=True):
#             weight = next(self.parameters())
#             new_weight = weight.new_zeros((self.num_layers, batch_size, self.hidden_size),
#                                           requires_grad=required_grad)
#             if self.rnn_type == 'LSTM':
#                 weight_tuple = (new_weight, new_weight)
#                 return weight_tuple
#             else:
#                 return new_weight
#
#     # 初始化模型
#     model = RNNModel('LSTM', VOCAB_SIZE, input_size=EMBEDDING_SIZE, hidden_size=600, num_layers=2, dropout=0.5)
#     loss_fn = nn.CrossEntropyLoss()
#     learning_rate = 0.001
#     optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
#     scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, 0.5)
#
#     def evaluate(model: RNNModel, data):
#         model.eval()
#         total_loss = 0.
#         it = iter(data)
#         total_count = 0.
#         with torch.no_grad():
#             hidden = model.init_hidden(BATCH_SIZE, required_grad=False)
#             for i, batch in enumerate(it):
#                 data, target = batch.text, batch.target
#                 hidden = repackage_hidden(hidden)
#                 with torch.no_grad():
#                     output, hidden = model(data, hidden)
#                 loss = loss_fn(output.view(-1, VOCAB_SIZE), target.view(-1))
#                 total_count += np.multiply(*data.size())
#                 total_loss += loss.item() * np.multiply(*data.size())
#         loss = total_loss / total_count
#         model.train()
#         return loss
#
#     def repackage_hidden(h):
#         if isinstance(h, torch.Tensor):
#             return h.detach()
#         else:
#             return tuple(repackage_hidden(v) for v in h)
#
#     GRAD_CLIP = 1.
#     NUM_EPOCHS = 2
#     val_losses = []
#     for epoch in range(NUM_EPOCHS):  # 训练过程是不需要字典的，因为是数字到数字的映射，与字典无关
#         # 设置为训练模式，nn.Module类的方法，pycharm追踪不到，RNNModule类也有'train'参数，修改它的train参数只影响RNNModule本身，其他的神经网络层不会变化
#         model.train()
#         it = iter(train_iter)
#         hidden = model.init_hidden(BATCH_SIZE)  # 初始化一个hidden用于输入
#         for i, batch in enumerate(it):
#             # data: [bptt_len, batch_size], target: [bptt_len, batch_size]
#             data, target = batch.text, batch.target
#             hidden = repackage_hidden(hidden)
#             model.zero_grad()
#
#             # data: [bptt_len, batch_size], hidden: [num_layers, batch_size, hidden_size]
#             output, hidden = model(data, hidden)  # output: [bptt_len, batch_size, vocab_size]
#             loss = loss_fn(output.view(-1, VOCAB_SIZE), target.view(-1))
#             loss.backward()
#             torch.nn.utils.clip_grad_norm_(model.parameters(), GRAD_CLIP)
#             optimizer.step()
#             if i % 1000 == 0:
#                 print("epoch {}, iter {}, loss: {}".format(epoch, i, loss.item()))
#
#             if i % 10000 == 0:
#                 val_loss = evaluate(model, val_iter)
#
#                 if len(val_losses) == 0 or val_loss < min(val_losses):
#                     print("best model, val loss:", val_loss)
#                     torch.save(model.state_dict(), "lm-best.th")
#                 else:
#                     scheduler.step()
#                     optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
#                 val_losses.append(val_loss)
#
#
# def test2_lstm_stock(stock_code: str):
#     """
#     使用lstm神经元预测股票。
#
#     参考https://blog.csdn.net/a19990412/article/details/85139058
#
#     :param stock_code: 股票代码
#     :return:
#     """
#     file = os.path.join(gv.dataDirectory, stock_code + '.csv')
#     days = 30
#     trainX, trainY, testX, testY = dr.get_data_days_list(file=file, col_x=['close'], days=days, normalization='z-score',
#                                                          split=0.7)
#     gv.logger.debug(
#         "trainX.shape={}, trainY.shape={}, testX.shape={}, testY.shape={}".format(trainX.shape, trainY.shape,
#                                                                                   testX.shape, testY.shape))
#
#     class Model(torch.nn.Module):
#         def __init__(self, input_size):
#             super(Model, self).__init__()
#             self.rnn = nn.LSTM(
#                 input_size=input_size,
#                 hidden_size=64,
#                 num_layers=1,
#             )
#             self.out = nn.Sequential(
#                 nn.Linear(64, 1)
#             )
#
#         def forward(self, x):
#             r_out, (h_n, h_c) = self.rnn(x, None)
#             out = self.out(r_out)
#             return out
#
#     class TrainSet(Dataset):
#         def __init__(self, tx, ty):
#             self.tx, self.ty = tx.float(), ty.float()
#
#         def __getitem__(self, idx):
#             return self.tx[idx], self.ty[idx]
#
#         def __len__(self):
#             return len(self.ty)
#
#     n = 30
#     LR = 0.0001
#     EPOCH = 100
#     trainset = TrainSet(torch.Tensor(trainX), torch.Tensor(trainY))
#     trainloader = DataLoader(trainset, batch_size=16, shuffle=False)
#
#     input_size = days
#     model = Model(input_size)
#     optimizer = torch.optim.Adam(model.parameters(), lr=LR)
#     loss_func = nn.MSELoss()
#
#     for step in range(EPOCH):
#         for x, y in trainloader:
#             x = torch.squeeze(x, dim=2)
#             output = model(x)
#             loss = loss_func(output, y)
#             optimizer.zero_grad()
#             loss.backward()
#             optimizer.step()
#         print(step, loss)
#         if step % 10:
#             torch.save(model, 'model.pkl')
#     torch.save(model, 'model.pkl')
#
#
# def test3_lstm_stock(stock_code: str):
#     """
#     https://blog.csdn.net/weixin_30343157/article/details/102064861
#
#     :param stock_code:
#     :return:
#     """
#     file = os.path.join(gv.dataDirectory, stock_code + '.csv')
#     days = 30
#     train_x, train_y, testX, testY = dr.get_data_days_list(file=file, col_x=['close'], days=days,
#                                                            normalization='z-score',
#                                                            split=0.7)
#     gv.logger.debug(
#         "trainX.shape={}, trainY.shape={}, testX.shape={}, testY.shape={}".format(train_x.shape, train_y.shape,
#                                                                                   testX.shape, testY.shape))
#     train_x = train_x.reshape(-1, 1, 10)
#
#     # train_y = train_y.reshape(-1, 1, 1)
#     train_x = torch.from_numpy(train_x)
#     train_y = torch.from_numpy(train_y)
#
#     class NET(nn.Module):
#         def __init__(self, input_size=10, hidden_size=40, output_size=2, num_layer=2):
#             super(NET, self).__init__()
#             self.rnn = nn.LSTM(input_size, hidden_size, num_layer)
#             self.out = nn.Linear(hidden_size, output_size)
#
#         def forward(self, x):
#             out, _ = self.rnn(x)
#             out = self.out(out[:, -1, :])
#             return out
#
#     net = NET()
#     optimizer = torch.optim.Adam(net.parameters(), lr=0.08, betas=(0.9, 0.999), eps=1e-08, weight_decay=0)
#     loss_func = torch.nn.CrossEntropyLoss()
#
#     for epoch in range(1000):
#         var_x = Variable(train_x).type(torch.FloatTensor)
#         var_y = Variable(train_y).type(torch.LongTensor)
#         out = net(var_x)
#         loss = loss_func(out, var_y)
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
#         if (epoch + 1) % 100 == 0:
#             print('Epoch: {}, Loss: {:.5f}'.format(epoch + 1, loss.data.numpy()))
#
#     test_x = testX.reshape(-1, 1, 10)
#     test_x = torch.from_numpy(test_x)
#     var_data = Variable(test_x)
#     pred_test = net(var_data)
#     # pred_test = pred_test.view(-1).data.numpy()
#     pred_test = torch.max(pred_test, 1)[1].data.numpy().squeeze()
#
#     plt.plot(pred_test, 'r', label='prediction')
#     plt.plot(testY, 'b', label='real')
#     plt.legend(loc='best')
#     plt.show()
#     print(pred_test, 'prediction number')
#     print(testY, 'real number')
#     j = 0
#     test_size = len(testY)
#     for i in range(test_size):
#         if (pred_test[i] == testY[i]):
#             j = j + 1;
#     j = j / test_size
#     print('Identification:', j)
#
#
# def test4_lstm_stock(stock_code: str):
#     """
#     https://blog.csdn.net/weixin_43855152/article/details/103412077
#     :param stock_code:
#     :return:
#     """
#     file = os.path.join(gv.dataDirectory, stock_code + '.csv')
#     days = 30
#     train_x, train_y, testX, testY = dr.get_data_days_list(file=file, col_x=['close'], days=days,
#                                                            normalization='z-score',
#                                                            split=0.7)
#
#
# def lstm_stock_use_in_build_rnn_拟合(stock_code: str):
#     """
#     使用torch内置的LSTM层进行股票预测，与lstm_stock_use_in_build_rnn()功能相同，只是为了保证复现，修改了一些随机数的机制
#
#     :param stock_code:
#     :return:
#     """
#     torch.manual_seed(10000)
#     np.random.seed(10000)
#     random.seed(10000)
#
#     file = os.path.join(gv.dataDirectory, stock_code + '.csv')
#     days = 30
#     trainX, trainY, testX, testY = dr.get_data_days_list(file=file, col_x=['close'], days=days,
#                                                          normalization='z-score',
#                                                          split=0.7)
#
#     trainX, trainY = torch.from_numpy(trainX).type(torch.float), torch.from_numpy(trainY).type(torch.float)
#     testX, testY = torch.from_numpy(testX).type(torch.float), torch.from_numpy(testY).type(torch.float)
#
#     batch_size = 8
#     train_dataset = TensorDataset(trainX, trainY)
#     test_dataset = TensorDataset(testX, testY)
#     # 只有在数据量很大的时候使用多核加载才能提高速度，数据量小时反而会降低速度
#     train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=False)  # , num_workers=2)
#     test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)  # , num_workers=2)
#
#     class RNNModel(nn.Module):
#         # bptt_len=30，即过去30天的数据，input_size=1即每天取一个数据
#         def __init__(self, bptt_len, input_size, hidden_size, num_layers):
#             super(RNNModel, self).__init__()
#             # 定义模型中的神经网络层
#             self.rnn = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
#             # 用于将隐含层的输入映射到输出
#             self.linear = nn.Linear(in_features=hidden_size * bptt_len, out_features=1)
#
#             self.hidden_size = hidden_size
#             self.num_layers = num_layers
#
#         # input: [8, 30, 1], hidden: [batch_size, num_layers, hidden_size] # 这里把batch_size调到第一位
#         def forward(self, input):
#             # rnn层的输入和输出形状是相同的
#             output, _ = self.rnn(input)
#
#             # 需要调用output.contiguous()将Tensor的存储整理为连续存储，否则可能报错，原因可能是多卡存储或其他
#             output = output.contiguous().view(output.size(0), output.size(1) * output.size(2))  # [8, 30, 1]->[8, 30]
#
#             # 这里将lstm层输出的Tensor形状的前两位合并，只有输出的维度是需要传出去，以和labels进行比较计算loss
#             output = self.linear(output)  # 将[*, input_size]映射到[*, output_size], [8, 30]->[8, 1]
#
#             output = output.squeeze(-1)  # [8, 1] -> [8]
#             return output
#
#     def evaluate(model: RNNModel, test_loader):
#         model.eval()
#         total_loss = 0.
#         total_count = 0.
#         with torch.no_grad():
#             for i, (data, labels) in enumerate(test_loader):
#                 output = model(data)
#
#                 loss = loss_fn(output, labels)
#                 total_count += len(data)  # 一共多少数据
#                 total_loss += loss.item() * len(data)  # 总的loss
#         loss = total_loss / total_count
#         model.train()
#         return loss
#
#     input_size = 1  # 输入数据的列数，假如考虑过去30天开盘价和收盘价，则input_size=2, bptt_len=30
#     model = RNNModel(bptt_len=days, input_size=input_size, hidden_size=64, num_layers=2)
#     learning_rate = 0.01
#     optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
#     scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, 0.8)
#
#     loss_fn = torch.nn.MSELoss()
#
#     EPOCHS = 2
#     train_losses = []
#     val_losses = []  # 记录训练过程中的losses，方便后续绘图
#     flag = 0
#     for epoch in range(EPOCHS):
#         # input: [batch_size, bptt_len, input_size], labels: [batch_size]
#         for i, (data, labels) in enumerate(train_loader):
#             # 输入形状是[8, 30, 1]，即[batch_size, bptt_len, input_size]
#             out = model(data)  # out: [8]
#
#             loss = loss_fn(out, labels)
#             optimizer.zero_grad()
#             loss.backward()
#             # torch.nn.utils.clip_grad_norm_(model.parameters(), 1)  # 防止参数过大
#             optimizer.step()
#             if i % 10 == 0:
#                 val_loss = evaluate(model, test_loader)
#
#                 if len(val_losses) == 0 or val_loss < min(val_losses):
#                     gv.logger.info("epoch {}, step {}, loss {}, test loss {}".format(epoch, i, loss, val_loss))
#                     torch.save(model.state_dict(), "./nn_models/pytorchModel/stock-prediction-lstm.th")
#                 elif loss < min(train_losses) and flag < 3:  # 训练集损失减小，测试集损失增大，继续训练，
#                     flag = flag + 1  # 连续三次如此，则更改学习速率
#                     gv.logger.info("epoch {}, step {}, loss {}, test loss {}".format(epoch, i, loss, val_loss))
#                 else:  # 表示训练数据和测试数据都变差
#                     flag = 0
#                     scheduler.step()  # 会自动把optimizer中的lr修改为更小
#                     real_time_lr = optimizer.param_groups[0]['lr']
#                     gv.logger.info("epoch {}, step {}, loss {}, test loss {}, adjust lr to {}"
#                                    .format(epoch, i, loss, val_loss, real_time_lr))
#
#                 # 记录训练和测试数据集的损失
#                 train_losses.append(loss)
#                 val_losses.append(val_loss)
#
#
# def start_mysql_service():
#     # test1_torch_lstm_language()
#     # test3_lstm_stock(gv.symbol)
#     lstm_stock_use_in_build_rnn_拟合(gv.symbol)  # epoch 1, step 50, loss 0.1707535982131958
