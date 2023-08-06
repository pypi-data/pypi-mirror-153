import requests
from yangke.base import web_available, get_temp_para, pic2base64
import os, socket, urllib3


def get_token(tries=0, client_id="fmt3q4GOHR5lyzjGb78I9Otr", client_secret="DHcIclrolnmPnMFOyf6mjnZ6V2Qda76o"):
    """
    获取access_token，因为百度Unit智能对话定制与服务平台访问需要access_token才能使用，具体使用方法参见：
    http://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu

    已申请的应用:

    应用名称        API Key                          Secret Key
    yk_ocr        fmt3q4GOHR5lyzjGb78I9Otr         DHcIclrolnmPnMFOyf6mjnZ6V2Qda76o     通用API，几乎包含百度所有功能
    智能问答       KBK6CpyAIaxcfURZiDTPHFyv         bwvENVUj7XtXqGVGyYieqH8F20KhKRjw

    :param tries: 尝试次数
    :param client_id: 应用的API Key
    :param client_secret: 应用的Secret Key
    :return: 返回百度的access_token
    """

    # client_id为官网获取的API Key，client_secret 为官网获取的Secret Key
    def _get_token():
        host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
               f'client_id={client_id}&' \
               f'client_secret={client_secret}'
        try:
            resp = requests.get(host)
            if resp:
                print(resp.json())
                acc_token = resp.json().get('access_token')  # 一般access_token一个月有效期
                return acc_token
            else:
                if tries < 3:  # 如果失败，则重试3次
                    return get_token(tries + 1)
                if web_available():
                    raise Exception("向百度请求access_token参数失败，请核对百度相关接口是否已经更改！")
                else:
                    raise Exception("网络似乎没有连接，请检查重试！")
        except (requests.exceptions.ConnectionError, socket.gaierror, urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError) as e:
            raise Exception("网络似乎没有连接，请检查重试！")

    access_token = get_temp_para('access_token', expires_in=2500000, get_func=_get_token)
    return access_token


def ocr(image: str = None, method: str = "general"):
    """
    百度文字识别，参考https://cloud.baidu.com/doc/OCR/s/vk3h7y58v

    :param image: 包含文字的图片
    :param method: 识别类型，accurate_basic/accurate/general_basic/general/... 具体参见上述百度帮助页面
    :return:
    """

    image_base64 = pic2base64(image)
    access_token = get_token(client_id="fmt3q4GOHR5lyzjGb78I9Otr", client_secret="DHcIclrolnmPnMFOyf6mjnZ6V2Qda76o")
    url = f'https://aip.baidubce.com/rest/2.0/ocr/v1/{method}?access_token=' + access_token  # 机器人对话API，沙盒环境
    # url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + access_token  # 技能对话API

    post_data = {
        "image": image_base64,
        "language_type": "CHN_ENG",  # auto_detect/CHN_ENG/ENG/
        "detect_direction": "true",
        "paragraph": "true",
        "probability": "true",
    }
    post_data = str(post_data).replace("'", '"').encode('utf-8')

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=post_data, headers=headers)
    result = []  # 答案的列表
    if response:
        print(response.json())
        response_list = response.json().get('result').get('response_list')
        for res in response_list:
            action = res.get('action_list')[0]  # action_list是一个列表，这里去列表第一项，如果以后遇到多答案的问题，再更新
            result.append(action.get('say'))

    return result


if __name__ == "__main__":
    ocr(r"C:\Users\YangKe\Pictures\2.png")
