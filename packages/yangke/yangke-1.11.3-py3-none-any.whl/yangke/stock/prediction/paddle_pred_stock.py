import numpy as np
import dataset.data_reader as dr
import paddle.fluid as fluid
import paddle
import globalVar as gv


def prediction1(datafile):
    """
    根据过去30天的股票数据，预测下一天收盘时的股价涨幅

    :param datafile: 股票数据存储的文件
    :return:
    """
    epochs = 10
    BATCH_SIZE = 10

    # 生成数据集
    # days, cols, labels意义参见dr.get_data_days_for_change()方法
    # 这里生成的是用于分类预测的数据集，按涨幅是否大于1%将标签分为两类
    days, cols, labels = 30, ['open', 'high', 'low', 'close', 'volume'], [1]
    generator, _, _ = dr.get_data_days_generator(datafile, days, cols, labels, normalization='min-max')

    # x, y = dr.get_data_days_list(datafile, days, cols, labels)

    # 定义数据的形状
    stocks_info = fluid.layers.data(name='stocks_info', shape=[days, len(cols)], dtype='float32')
    label = fluid.layers.data(name='label', shape=[1], dtype='int64')

    # 定义网络结构
    label_pred = fluid.layers.fc(input=stocks_info, size=len(labels) + 1, act='softmax')
    loss = fluid.layers.cross_entropy(input=label_pred, label=label)
    avg_loss = fluid.layers.mean(loss)
    acc = fluid.layers.accuracy(input=label_pred, label=label)

    # 定义优化器
    optimizer = fluid.optimizer.Adam(learning_rate=0.001)
    optimizer.minimize(avg_loss)

    # 定义调试器
    place = fluid.CPUPlace()
    exe = fluid.Executor(place)
    exe.run(fluid.default_startup_program())  # 初始化调试器
    main_program = fluid.default_main_program()

    # 定义数据的generator
    train_reader = paddle.batch(generator,
                                batch_size=BATCH_SIZE)  # 一次拿到BATCH_SIZE个数据
    feeder = fluid.DataFeeder(feed_list=[stocks_info, label], place=place)

    epochs_list = [epoch_id for epoch_id in range(epochs)]
    for epoch_id in epochs_list:
        for step, data in enumerate(train_reader()):
            metrics = exe.run(
                main_program, feed=feeder.feed(data), fetch_list=[avg_loss, acc]
            )
            step += 1
            if step % 10 == 0:
                gv.logger.debug(
                    "Epoch: {}; Step: {}; Cost: {}; Accuracy: {}".format(epoch_id, step, metrics[0], metrics[1]))
        gv.logger.debug("avg_loss is {}, accuracy is {}".format(metrics[0], metrics[1]))
