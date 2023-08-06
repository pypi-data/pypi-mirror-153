from __future__ import absolute_import, division, print_function, unicode_literals
# absolute_import 兼容python2.4及之前的版本，作用是优先引入python自带.py文件
# division库是精确除法
# print_function 使用python3的print语句，因为我们的python版本就是3.7.4，所以可以不需要这个包，加上是为了兼容python2运行环境
# unicode_literals 将所有'xxx'都视为unicode字符串，在python2中字符串分为b'xxx'和u'xxx'，在python3中，全都是unicode字符串
import tensorflow as tf


def test1():
    # 准备mnist数据集
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()  # tensorflow的输入数据格式是ndarray格式
    x_train, x_test = x_train / 255.0, x_test / 255.0

    # 将模型各层堆叠起来
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # 训练并验证模型
    model.fit(x_train, y_train, epochs=5)

    model.evaluate(x_test, y_test, verbose=2)


if __name__ == "__main__":
    test1()
