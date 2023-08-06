from yangke.base import *



class SaveData(auto_save_para.AutoSavePara):
    def __init__(self):
        """
        类中的值均为硬盘变量，即无论什么时候启动程序，程序中的变量都是上一次运行最后的值
        """
        self.a = self.update_auto_save_para('self.a', None)
        self.b = self.update_auto_save_para('self.b', None)

    def set_a(self, a):
        self.a = self.update_auto_save_para('self.a', a)

    def set_b(self, b):
        self.b = self.update_auto_save_para('self.b', b)


save_data = SaveData()
print(f"{save_data.a}")
print(f"{save_data.b}")
save_data.set_a(10)
save_data.set_b("x")
print(f"{save_data.a}")
print(f"{save_data.b}")
