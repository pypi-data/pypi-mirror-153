import json
import requests
from yangke.web.baidu import get_token


def ask(question: str):
    """
    一个思知的对话机器人，但貌似准确度很低
    :param question:
    :return:
    """
    sess = requests.get('https://api.ownthink.com/bot?spoken={}'.format(question))
    answer = sess.text
    answer = json.loads(answer)
    return answer


def ask_baidu(question: str):
    """
    百度的对话机器人，详情参见百度 机器人对话API文档，https://ai.baidu.com/ai-doc/UNIT/qk38gggxg

    Unit主页 https://ai.baidu.com/unit/home

    :param question:
    :return: 问题答案的列表，每一个列表都对应一个可能的答案
    """

    access_token = get_token(client_id="fmt3q4GOHR5lyzjGb78I9Otr", client_secret="DHcIclrolnmPnMFOyf6mjnZ6V2Qda76o")
    url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + access_token  # 机器人对话API，沙盒环境
    # url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + access_token  # 技能对话API

    post_data = {
        "log_id": "7758521",
        "version": "2.0",
        # "service_id": "S10000",
        "skill_ids": ["1033038"],
        "session_id": "",
        "request": {
            "query": question,
            "user_id": "UNIT_DEV_YK"
        },
        "dialog_state": {"contexts": {"SYS_REMEMBERED_SKILLS": ["1033038"]}}
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


# def glove():

if __name__ == "__main__":
    import re

    qingming_dict = {}
    for year in range(1990, 2100):
        ans = ask_baidu(f'{year}年清明节是几月几号')[0]
        ans = re.findall(".*月(.)日.*", ans)
        while len(ans) == 0:
            ans = ask_baidu(f'{year}年清明节是几月几号')[0]
            ans = re.findall(".*月(.)日.*", ans)
        qingming_dict[str(year)] = ans[0]
    print(qingming_dict)
