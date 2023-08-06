from yangke.base import *

kwargs = {"circle": {"center": (0, 0), "radius": 100, "fill": "red", "outline": "yellow"}}
pic = r"C:\Users\YangKe\PycharmProjects\lib4python\yangke\panda\UI\stoneFrame.jpg"
show_pic(pic)
r = pic2ndarray(pic, mode="RGB")
r = pic2base64(r)
print(r)
