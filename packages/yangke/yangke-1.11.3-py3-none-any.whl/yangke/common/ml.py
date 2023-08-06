"""
机器学习 Machine Learning
"""


class DataPredictionModel:
    def __init__(self, data_file=None, config_file=None, x=None, y=None):
        """
        初始化神经网络预测模型。
        训练数据可以通过data_file传入，也可以通过x,y传入。

        :param data_file: 训练数据集文件
        :param config_file: 配置文件
        :param x: 数据集的输入参数，可选
        :param y: 数据集的输出参数，可选
        """
        super(DataPredictionModel, self).__init__()
        self.x = x  # 输入参数
        self.y = y  # 输出参数

    def update_model(self, x, y):
        """
        根据新的数据点更新模型

        :param x:
        :param y:
        :return:
        """
        # todo
        pass

    def predict(self, x):
        """
        根据输入的数据预测输出

        :param x:
        :return:
        """
