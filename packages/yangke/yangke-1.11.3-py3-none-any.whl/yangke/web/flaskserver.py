from flask import Flask, request, jsonify, make_response, send_from_directory
from yangke.base import name_transfer
from flask_cors import *
from yangke.common.config import logger
import traceback
import os

download_func = None
example = None


def start_server_app(deal=None, app_name='yangke.web.flaskserver', instance_path=__file__,
                     instance_relative_config=True, host="0.0.0.0", port="5000", allow_action=None, use_action=True,
                     example_url=None):
    """
    启动Flask Server服务，服务启动后将调用用户传入的deal函数来对url请求进行处理，deal函数通过args参数拿到请求的参数字典。
    如果用户需要自定义deal函数处理http://127.0.0.1:5000这类没有参数的url，则应设置useAction为False，并在deal函数中对空字典进行判断处理。
    如果用户需要过滤允许的Action类型，则需要设置允许的操作类型列表allow_action。

    当use_action为True时，如果请求url不带Action参数，则该方法会自动返回提示信息。因此，传递给用户函数deal的参数字典中确保含有Action参数。
    当use_action为False时，即使请求url不带任何参数，也会调用deal函数，且将对应的参数字典或空字典传递给deal函数，deal函数需要判空。

    使用示例：
    #==============================================================================================
    def deal(args):
        action = args.get('Action')  # 因为下方use_action=True，所以这里的action必然有值，避免eval函数出错
        result = eval("{}(args)".format(action))
        return result

    start_server_app(deal, use_action=True)  # 启动服务器.
    #==============================================================================================

    :param use_action: 是否使用Action参数指定操作类型，不使用则完全由用户定义所有url响应
    :param deal: 用户指定的url处理方法
    :param app_name: Flask app名，一般不需要也不能更改，Flask根据该参数查找模板和静态文件等东西
    :param instance_path:
    :param instance_relative_config:
    :param host:
    :param port:
    :param allow_action:  允许用户调用的方法
    :param example_url: 示例http访问请求，当用户访问出错时提示用户
    :return:
    """
    app = Flask(app_name, instance_path=instance_path, instance_relative_config=instance_relative_config)
    app.config['JSON_AS_ASCII'] = False  # 让Flask返回的字符串可以正确显示中文，默认显示的是utf-8编码
    CORS(app)
    global example
    example = example_url

    @app.route('/', methods=['GET', 'POST'])
    def start_service():
        action = request.args.get('Action')
        # allow_action为空，表示没有设置允许的操作，则放行所有Action
        if allow_action is None or action in allow_action:
            t = request.get_data(as_text=True).split('=')
            t_dict = {}
            if len(t) > 1:
                for ix in range(0, len(t), 2):  # start=0, stop=len(t), step=2
                    t_dict[str(t[ix])] = t[ix + 1]
            args = dict(request.args)
            args.update(t_dict)
            args.update(request.form)
            if len(args) == 0 and use_action:
                global example
                if example is None:
                    example = "http://127.0.0.1:5000/?Action=CreatePerson&GroupName=test&PersonName=yk"
                return jsonify({"Success": True,
                                "Info": "服务正常，请使用Action传入指定的操作！",
                                "Example": example})
            logger.debug("执行操作{}".format(action))
            logger.debug(args)
            try:
                # result = eval("{}(args)".format(action))
                result = deal(args) or {}  # 需要确保result不为空
            except:
                traceback.print_exc()
                logger.debug(f"远程调用了{action}方法，但该方法在服务端没有定义！")
                return jsonify({"Success": False, "Info": "未知命令：{}".format(action)})
            result = name_transfer(result, 'CamelCase')  # 将字典中key的命名方式修改为驼峰命名方式
            result1 = jsonify(result)
            return result1

        else:
            logger.debug("操作{}不允许".format(action))
            return jsonify({"Success": False, "Info": "操作不允许，操作类型：{}".format(action)})

    @app.route('/download/<file_name>', methods=['GET'])
    @cross_origin(origins="*", methods=['GET'])
    def download_file(file_name):
        """
        下载文件功能

        前段通过 ip/download/<下载参数>进行下载，这里的下载参数一般是文件名。
        @download
        def deal(args_str):
            return os.path.join("C:/users", args_str)

        :param file_name: 前段传入的下载参数，一般为文件名
        :return:
        """
        directory = os.path.join(os.getcwd(), 'static')
        try:
            if download_func is not None:
                file_abs = download_func(file_name)
                if file_abs:
                    directory = os.path.dirname(file_abs)
                    file_name = os.path.basename(file_abs)
            response = make_response(send_from_directory(directory, file_name, as_attachment=True))
            return response
        except Exception as e:
            return jsonify({"Info": "文件下载失败！"})

    logger.info(f"服务已启动，通过http://localhost:{port}访问")
    from waitress import serve
    serve(app, host=host, port=port)

    return app


def download(func):
    """
    download装饰器，用于指定用户下载的文件
    用法示例：
    @download
    def transfer_file(args): # 这里args是前段通过 http://ip/download/<args>传递的下载参数
        return os.path.join("C:/static", args)  # 则前段会下载到服务器端 C:/static/args路径对应的函数

    :param func:
    :return:
    """
    global download_func
    download_func = func

    def wrap(*args, **kwargs):
        return func(*args, **kwargs)

    return wrap
