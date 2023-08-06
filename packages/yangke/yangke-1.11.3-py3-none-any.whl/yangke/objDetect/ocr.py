import logging

import paddleocr.paddleocr

from yangke.base import pic2ndarray, timeit


@timeit
def ocr(image, threshold=0.7, paragraph=False, method="easyocr"):
    """
    文字识别

    :param image: 待识别图像
    :param threshold: 阈值
    :param paragraph: 是否合并图片中文字的识别结果，如果为True，则多行会合并输出
    :param method: 文字识别方法，默认为"easyocr"，即使用EasyOCR库，也可取值：paddleocr
    :return:
    """
    if isinstance(image, str):
        image = pic2ndarray(image)  # easyocr自带的图片读取方法不支持中文路径，这里使用自己的图片读取方法将图片转换为ndarray
    result = None
    if method == "easyocr":
        import easyocr
        reader = easyocr.Reader(['ch_sim'], model_storage_directory=r"D:\easyocr")
        result = reader.readtext(image, paragraph=paragraph)
        if paragraph:
            if len(result) > 0:
                result = result[0][1]
    elif method == "paddleocr":
        from paddleocr import PaddleOCR
        paddleocr.paddleocr.logger.setLevel(logging.CRITICAL)
        reader = PaddleOCR(use_angle_cls=False, lang="ch")
        result1 = reader.ocr(image, cls=False)
        if paragraph:
            result = ""
            for r in result1:
                result = result + " " + r[1][0]
    return result


if __name__ == "__main__":
    # ocr(r"D:\Users\YangKe\PycharmProjects\lib4python\yangke\common\temp.png")
    # text = ocr(r"D:\easyocr.png")
    text = ocr(r"D:\迅雷下载\chinese_tra.jpg", method="paddleocr", paragraph=True)
    print(text)
