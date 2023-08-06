import numpy as np
import paddle
import paddle.fluid as fluid
import math
import os
import sys
import argparse
import matplotlib
from PIL import Image
import globalVar as gv


def test1():
    data = fluid.layers.ones(shape=[5], dtype='int64')
    add = fluid.layers.elementwise_add(data, data)
    cast = fluid.layers.cast(x=data, dtype='float64')
    place = fluid.CPUPlace()
    exe = fluid.Executor(place)
    ones_result = exe.run(fluid.default_main_program(), fetch_list=[data], return_numpy=True)
    print(ones_result)
    print(ones_result[0])
    ones_result = exe.run(fluid.default_main_program(), fetch_list=[add], return_numpy=True)
    print(ones_result)
    print(ones_result[0])
    ones_result = exe.run(fluid.default_main_program(), fetch_list=[cast], return_numpy=True)
    print(ones_result)
    print(ones_result[0])


def test2():
    """
    拟合函数y=9a+5b+2c+10d
    """
    # 生成数据
    np.random.seed(0)
    outputs = np.random.randint(5, size=(10, 4))
    res = []
    for i in range(10):
        # 假设方程式为y=4a+6b+7c+2d
        y = 4 * outputs[i][0] + 6 * outputs[i][1] + 7 * outputs[i][2] + 2 * outputs[i][3]
        res.append([y])
    # 定义数据
    train_data = np.array(outputs).astype('float32')
    y_true = np.array(res).astype('float32')

    # 定义网络
    x = fluid.layers.data(name='x', shape=[4], dtype='float32')  # 四个x对应一个y
    y = fluid.layers.data(name='y', shape=[1], dtype='float32')  # 这里的x,y相当于占位符
    y_predict = fluid.layers.fc(input=x, size=1, act=None)
    # 定义损失函数
    cost = fluid.layers.square_error_cost(input=y_predict, label=y)
    avg_cost = fluid.layers.mean(cost)
    # 定义优化方法
    sgd_optimizer = fluid.optimizer.SGD(learning_rate=0.05)
    sgd_optimizer.minimize(avg_cost)
    # 参数初始化
    cpu = fluid.CPUPlace()
    exe = fluid.Executor(cpu)
    exe.run(fluid.default_startup_program())
    # 开始训练，迭代500次
    for i in range(500):
        outs = exe.run(
            feed={'x': train_data, 'y': y_true},
            fetch_list=[y_predict.name, avg_cost.name]  # 这个fetch_list是什么
        )
        if i % 50 == 0:
            gv.logger.debug('iter={:.0f},cost={}'.format(i, outs[1][0]))
    # 存储训练结果
    params_dirname = "result"
    fluid.io.save_inference_model(params_dirname, ['x'], [y_predict], exe)

    # 开始预测
    infer_exe = fluid.Executor(cpu)
    inference_scope = fluid.Scope()
    # 加载训练好的模型
    with fluid.scope_guard(inference_scope):
        [inference_program, feed_target_names,
         fetch_targets] = fluid.io.load_inference_model(params_dirname, infer_exe)

    # 生成测试数据
    test = np.array([[[9], [5], [2], [10]]]).astype('float32')
    # 进行预测
    results = infer_exe.run(inference_program,
                            feed={'x': test},
                            fetch_list=fetch_targets)
    # 给出题目为[9,5,2,10] 输出为y=...的值
    gv.logger.debug("9a+5b+2c+10d={}".format(results[0][0]))


def test3():
    """
    拟合多项式，线性回归
    """

    def parse_args():
        parser = argparse.ArgumentParser("fit_a_line")
        parser.add_argument(
            '--enable_ce',
            action='store_true',
            help="If set, run the task with continuous evaluation logs.")
        parser.add_argument(
            '--use_gpu',
            type=bool,
            default=False,
            help="Whether to use GPU or not.")
        parser.add_argument(
            '--num_epochs', type=int, default=100, help="number of epochs.")
        args = parser.parse_args()
        return args

    # For training test cost
    def train_test(executor, program, reader, feeder, fetch_list):
        accumulated = 1 * [0]
        count = 0
        for data_test in reader():
            outs = executor.run(
                program=program, feed=feeder.feed(data_test), fetch_list=fetch_list)
            accumulated = [x_c[0] + x_c[1][0] for x_c in zip(accumulated, outs)]
            count += 1
        return [x_d / count for x_d in accumulated]

    def save_result(points1, points2):
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        x1 = [idx for idx in range(len(points1))]
        y1 = points1
        y2 = points2
        l1 = plt.plot(x1, y1, 'r--', label='predictions')
        l2 = plt.plot(x1, y2, 'g--', label='GT')
        plt.plot(x1, y1, 'ro-', x1, y2, 'g+-')
        plt.title('predictions VS GT')
        plt.legend()
        plt.savefig('./image/prediction_gt.png')

    def main(args):
        batch_size = 20

        if args.enable_ce:
            train_reader = paddle.batch(
                paddle.dataset.uci_housing.train(), batch_size=batch_size)
            test_reader = paddle.batch(
                paddle.dataset.uci_housing.test(), batch_size=batch_size)
        else:
            train_reader = paddle.batch(
                paddle.reader.shuffle(
                    paddle.dataset.uci_housing.train(), buf_size=500),
                batch_size=batch_size)
            test_reader = paddle.batch(
                paddle.reader.shuffle(
                    paddle.dataset.uci_housing.test(), buf_size=500),
                batch_size=batch_size)

        # feature vector of length 13
        x = fluid.layers.data(name='x', shape=[13], dtype='float32')
        y = fluid.layers.data(name='y', shape=[1], dtype='float32')

        main_program = fluid.default_main_program()
        startup_program = fluid.default_startup_program()

        if args.enable_ce:
            main_program.random_seed = 90
            startup_program.random_seed = 90

        y_predict = fluid.layers.fc(input=x, size=1, act=None)
        cost = fluid.layers.square_error_cost(input=y_predict, label=y)
        avg_loss = fluid.layers.mean(cost)

        test_program = main_program.clone(for_test=True)

        sgd_optimizer = fluid.optimizer.SGD(learning_rate=0.001)
        sgd_optimizer.minimize(avg_loss)

        # can use CPU or GPU
        use_cuda = args.use_gpu
        place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
        exe = fluid.Executor(place)

        # Specify the directory to save the parameters
        params_dirname = "fit_a_line.inference.model"
        num_epochs = args.num_epochs

        # start_mysql_service train loop.
        feeder = fluid.DataFeeder(place=place, feed_list=[x, y])
        exe.run(startup_program)

        train_prompt = "Train cost"
        test_prompt = "Test cost"
        step = 0

        exe_test = fluid.Executor(place)

        for pass_id in range(num_epochs):
            for data_train in train_reader():
                avg_loss_value, = exe.run(
                    main_program,
                    feed=feeder.feed(data_train),
                    fetch_list=[avg_loss])
                if step % 10 == 0:  # record a train cost every 10 batches
                    gv.logger.debug("%s, Step %d, Cost %f" %
                                    (train_prompt, step, avg_loss_value[0]))

                if step % 100 == 0:  # record a test cost every 100 batches
                    test_metics = train_test(
                        executor=exe_test,
                        program=test_program,
                        reader=test_reader,
                        fetch_list=[avg_loss],
                        feeder=feeder)
                    gv.logger.debug("%s, Step %d, Cost %f" %
                                    (test_prompt, step, test_metics[0]))
                    # If the accuracy is good enough, we can stop the training.
                    if test_metics[0] < 10.0:
                        break

                step += 1

                if math.isnan(float(avg_loss_value[0])):
                    sys.exit("got NaN loss, training failed.")
            if params_dirname is not None:
                # We can save the trained parameters for the inferences later
                fluid.io.save_inference_model(params_dirname, ['x'], [y_predict],
                                              exe)

            if args.enable_ce and pass_id == args.num_epochs - 1:
                gv.logger.debug("kpis\ttrain_cost\t%f" % avg_loss_value[0])
                gv.logger.debug("kpis\ttest_cost\t%f" % test_metics[0])

        infer_exe = fluid.Executor(place)
        inference_scope = fluid.core.Scope()

        # infer
        with fluid.scope_guard(inference_scope):
            [inference_program, feed_target_names, fetch_targets
             ] = fluid.io.load_inference_model(params_dirname, infer_exe)
            batch_size = 10

            infer_reader = paddle.batch(
                paddle.dataset.uci_housing.test(), batch_size=batch_size)

            infer_data = next(infer_reader())
            infer_feat = np.array(
                [data[0] for data in infer_data]).astype("float32")
            infer_label = np.array(
                [data[1] for data in infer_data]).astype("float32")

            assert feed_target_names[0] == 'x'
            results = infer_exe.run(
                inference_program,
                feed={feed_target_names[0]: np.array(infer_feat)},
                fetch_list=fetch_targets)

            gv.logger.debug("infer results: (House Price)")
            for idx, val in enumerate(results[0]):
                gv.logger.debug("%d: %.2f" % (idx, val))

            gv.logger.debug("\nground truth:")
            for idx, val in enumerate(infer_label):
                gv.logger.debug("%d: %.2f" % (idx, val))

            save_result(results[0], infer_label)

    args = parse_args()
    main(args)


def test4():
    """
    recognize_digits 数字识别——MNIST
    """

    def parse_args():
        parser = argparse.ArgumentParser("mnist")
        parser.add_argument(
            '--enable_ce',
            action='store_true',
            help="If set, run the task with continuous evaluation logs.")
        parser.add_argument(
            '--use_gpu',
            type=bool,
            default=False,
            help="Whether to use GPU or not.")
        parser.add_argument(
            '--num_epochs', type=int, default=5, help="number of epochs.")
        args = parser.parse_args()
        return args

    def loss_net(hidden, label):
        prediction = fluid.layers.fc(input=hidden, size=10, act='softmax')
        loss = fluid.layers.cross_entropy(input=prediction, label=label)
        avg_loss = fluid.layers.mean(loss)
        acc = fluid.layers.accuracy(input=prediction, label=label)
        return prediction, avg_loss, acc

    def multilayer_perceptron(img, label):
        img = fluid.layers.fc(input=img, size=200, act='tanh')
        hidden = fluid.layers.fc(input=img, size=200, act='tanh')
        return loss_net(hidden, label)

    def softmax_regression(img, label):
        return loss_net(img, label)

    def convolutional_neural_network(img, label):
        conv_pool_1 = fluid.nets.simple_img_conv_pool(
            input=img,
            filter_size=5,
            num_filters=20,
            pool_size=2,
            pool_stride=2,
            act="relu")
        conv_pool_1 = fluid.layers.batch_norm(conv_pool_1)
        conv_pool_2 = fluid.nets.simple_img_conv_pool(
            input=conv_pool_1,
            filter_size=5,
            num_filters=50,
            pool_size=2,
            pool_stride=2,
            act="relu")
        return loss_net(conv_pool_2, label)

    def train(nn_type, use_cuda, save_dirname=None, model_filename=None, params_filename=None):

        startup_program = fluid.default_startup_program()
        main_program = fluid.default_main_program()

        train_reader = paddle.batch(
            paddle.reader.shuffle(paddle.dataset.mnist.train(), buf_size=500),
            batch_size=BATCH_SIZE)
        test_reader = paddle.batch(
            paddle.dataset.mnist.test(), batch_size=BATCH_SIZE)

        img = fluid.layers.data(name='img', shape=[1, 28, 28], dtype='float32')
        label = fluid.layers.data(name='label', shape=[1], dtype='int64')

        prediction, avg_loss, acc = softmax_regression(img, label)
        # prediction, avg_loss, acc = convolutional_neural_network(img, label)

        test_program = main_program.clone(for_test=True)
        optimizer = fluid.optimizer.Adam(learning_rate=0.001)
        optimizer.minimize(avg_loss)

        def train_test(train_test_program, train_test_feed, train_test_reader):
            acc_set = []
            avg_loss_set = []
            for test_data in train_test_reader():
                acc_np, avg_loss_np = exe.run(
                    program=train_test_program,
                    feed=train_test_feed.feed(test_data),
                    fetch_list=[acc, avg_loss])
                acc_set.append(float(acc_np))
                avg_loss_set.append(float(avg_loss_np))
            # get test acc and loss
            acc_val_mean = np.array(acc_set).mean()
            avg_loss_val_mean = np.array(avg_loss_set).mean()
            return avg_loss_val_mean, acc_val_mean

        place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
        exe = fluid.Executor(place)

        feeder = fluid.DataFeeder(feed_list=[img, label], place=place)
        exe.run(startup_program)
        epochs = [epoch_id for epoch_id in range(PASS_NUM)]

        lists = []
        step = 0
        for epoch_id in epochs:  # 5次大循环
            for step_id, data in enumerate(train_reader()):
                metrics = exe.run(
                    main_program,
                    feed=feeder.feed(data),
                    fetch_list=[avg_loss, acc])
                if step % 100 == 0:
                    gv.logger.debug("Pass %d, Epoch %d, Cost %f" % (step, epoch_id,
                                                                    metrics[0]))
                step += 1
            # test for epoch
            avg_loss_val, acc_val = train_test(
                train_test_program=test_program,
                train_test_reader=test_reader,
                train_test_feed=feeder)

            gv.logger.debug("Test with Epoch %d, avg_cost: %s, acc: %s" %
                            (epoch_id, avg_loss_val, acc_val))
            lists.append((epoch_id, avg_loss_val, acc_val))
            if save_dirname is not None:
                fluid.io.save_inference_model(
                    save_dirname, ["img"], [prediction],
                    exe,
                    model_filename=model_filename,
                    params_filename=params_filename)

        # find the best pass
        best = sorted(lists, key=lambda list: float(list[1]))[0]
        gv.logger.debug('Best pass is %s, testing Avgcost is %s' % (best[0], best[1]))
        gv.logger.debug('The classification accuracy is %.2f%%' % (float(best[2]) * 100))

    def infer(use_cuda, save_dirname=None, model_filename=None, params_filename=None):
        if save_dirname is None:
            return

        place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
        exe = fluid.Executor(place)

        def load_image(file):
            im = Image.open(file).convert('L')
            im = im.resize((28, 28), Image.ANTIALIAS)
            im = np.array(im).reshape(1, 1, 28, 28).astype(np.float32)
            im = im / 255.0 * 2.0 - 1.0
            return im

        cur_dir = os.path.dirname(os.path.realpath(__file__))
        tensor_img = load_image(cur_dir + '/image/infer_3.png')

        inference_scope = fluid.core.Scope()
        with fluid.scope_guard(inference_scope):
            # Use fluid.io.load_inference_model to obtain the inference program desc,
            # the feed_target_names (the names of variables that will be feeded
            # data using feed operators), and the fetch_targets (variables that
            # we want to obtain data from using fetch operators).
            [inference_program, feed_target_names,
             fetch_targets] = fluid.io.load_inference_model(
                save_dirname, exe, model_filename, params_filename)

            # Construct feed as a dictionary of {feed_target_name: feed_target_data}
            # and results will contain a list of data corresponding to fetch_targets.
            results = exe.run(
                inference_program,
                feed={feed_target_names[0]: tensor_img},
                fetch_list=fetch_targets)
            lab = np.argsort(results)
            gv.logger.debug("Inference result of image/infer_3.png is: %d" % lab[0][0][-1])

    def main(use_cuda, nn_type):
        model_filename = None
        params_filename = None
        save_dirname = "paddleModel/recognize_digits_" + nn_type + ".inference.model"

        # call train() with is_local argument to run distributed train
        train(
            nn_type=nn_type,
            use_cuda=use_cuda,
            save_dirname=save_dirname,
            model_filename=model_filename,
            params_filename=params_filename)
        infer(
            use_cuda=use_cuda,
            save_dirname=save_dirname,
            model_filename=model_filename,
            params_filename=params_filename)

    enable_ce = False
    num_epochs = 5
    use_gpu = False
    BATCH_SIZE = 64
    PASS_NUM = num_epochs
    use_cuda = use_gpu
    # predict = 'softmax_regression' # uncomment for Softmax
    # predict = 'multilayer_perceptron' # uncomment for MLP
    predict = 'convolutional_neural_network'  # uncomment for LeNet5
    main(use_cuda=use_cuda, nn_type=predict)


if __name__ == '__main__':
    # test1()
    # test2()
    # test3()
    test4()

    gv.logger.debug("测试完成！")
