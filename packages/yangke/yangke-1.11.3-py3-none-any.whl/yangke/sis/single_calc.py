from yangke.web.flaskserver import start_server_app, logger
from yangke.sis.sis_io import run, pred, get_coal_cos, get_gas_cos, get_fan_range


def deal(args):
    action = args.get("Action")
    result = eval("{}(args)".format(action))
    return result


def set_value(args):
    """

    :param args:
    :return:
    """
    ncv_new = float(args.get("ncv") or 34340)
    from yangke.sis.sis_io import set_ncv
    set_ncv(ncv_new)


def calculate(args):
    """
    后台计算服务的计算函数
    :param args:
    :return:
    """
    try:
        # 获取前端传入的数据
        power = float(args.get("power"))
        flow_heat = float(args.get("heat"))
        p_env = float(args.get("p_env") or 98)
        t_env = float(args.get("t0"))
        humid = float(args.get("humid") or 60) / 100
        p_gas = float(args.get("p_gas"))
        t_gas = float(args.get("t_gas"))
        flow_fgh = float(args.get("f_fgh"))
        flow_tca = float(args.get("t_tca"))
        flow_oh = float(args.get("f_oh"))
        flow_rh = float(args.get("f_rh"))

        result = {}
        hr1_min = 10000
        fun_list = get_fan_range(power, t_env)
        pump_list = [2]
        if t_env >= 35 and power >= 420:
            pump_list = [2, 3]
        for pump in pump_list:
            for fun in fun_list:
                hr1, p1 = pred(unit_num=1, power=power, flow_heat=flow_heat, p_env=p_env, t_env=t_env,
                               humid=humid, p_gas=p_gas, t_gas=t_gas, flow_fgh=flow_fgh, flow_tca=flow_tca,
                               flow_oh=flow_oh, flow_rh=flow_rh, pump=pump, fun=fun)
                hr1, p1 = hr1.item(), p1.item()
                eta1 = 3600 / hr1
                if hr1 < hr1_min:
                    hr1_min = hr1
                    气耗 = get_gas_cos(eta1, power, 47748.32)
                    煤耗 = get_coal_cos(气耗, 47748.32)
                    power_fun = fun * 175
                    power_pump = pump * 690
                    power_total = power_fun + power_pump
                    rate_cold = power_total / power / 10
                    result.update({"p": p1, "hr": hr1, "eta": eta1, "pump": pump, "fun": fun, "PowerFun": power_fun,
                                   "PowerPump": power_pump, "PowerTotal": power_total, "RateCold": rate_cold,
                                   "coal": 煤耗, "gas": 气耗})

        # 返回计算结果给前端
        return result

    except (TypeError, ValueError):
        logger.warning("类型转换错误")
        return {"error": "类型转换错误，calculate函数接受参数类型见提示", }


def start_server():
    run()  # 启动定时执行
    start_server_app(deal=deal, port=5000,
                     example_url="http://127.0.0.1:5000/?Action=calculate&power=400&heat=0&p_env=98&"
                                 "t0=30&humid=63&p_gas=3.8&t_gas=18&f_fgh=40&t_tca=100&f_oh=0&f_rh=0")


if __name__ == "__main__":
    start_server()
