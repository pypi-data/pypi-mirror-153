from threading import Timer
from threading import RLock
from threading import Thread
from yangke.base import is_ip_address
from yangke.common.config import logger
import time
import yangke.common.http_client as http_client
import json  # 这里不能用json5替换，因为url请求的post方法接收的json字符串不支持json5，主要是json5生成的key不带双引号会报错
import socket

"""
Status of instances
"""
INSTANCE_STATUS = "UP"
# INSTANCE_STATUS_DOWN = "DOWN"
# INSTANCE_STATUS_STARTING = "STARTING"
# INSTANCE_STATUS_OUT_OF_SERVICE = "OUT_OF_SERVICE"
INSTANCE_STATUS_UNKNOWN = "UNKNOWN"
"""
Default eureka server url.
"""
_DEFAULT_EUREKA_SERVER_URL = "http://127.0.0.1:8761/eureka/"

"""
The timeout seconds that all http request to the eureka server
"""
_DEFAULT_TIME_OUT = 5
"""
Default instance field values
"""
_DEFAULT_INSTNACE_PORT = 9090
_DEFAULT_INSTNACE_SECURE_PORT = 9443
_RENEWAL_INTERVAL_IN_SECS = 30
_DURATION_IN_SECS = 90
_DEFAULT_DATA_CENTER_INFO = "MyOwn"
_DEFAULT_DATA_CENTER_INFO_CLASS = "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo"
"""
Default encoding
"""
_DEFAULT_ENCODING = "utf-8"

""" 
This is for the DiscoveryClient, when this strategy is set, get_service_url will random choose one of the UP instance and return its url
This is the default strategy
"""
HA_STRATEGY_RANDOM = 1
"""
This is for the DiscoveryClient, when this strategy is set, get_service_url will always return one instance until it is down
"""
HA_STRATEGY_STICK = 2
"""
This is for the DiscoveryClient, when this strategy is set, get_service_url will always return a new instance if any other instances are up
"""
HA_STRATEGY_OTHER = 3
__cache_registry_clients_lock = RLock()
__cache_key = "default"
__cache_registry_clients = {}


def init_registry_client(eureka_server=_DEFAULT_EUREKA_SERVER_URL,
                         app_name="",
                         instance_id="",
                         instance_host="",
                         instance_ip="",
                         instance_port=_DEFAULT_INSTNACE_PORT,
                         instance_unsecure_port_enabled=True,
                         instance_secure_port=_DEFAULT_INSTNACE_SECURE_PORT,
                         instance_secure_port_enabled=False,
                         countryId=1,  # @deprecaded
                         data_center_name=_DEFAULT_DATA_CENTER_INFO,  # Netflix, Amazon, MyOwn
                         renewal_interval_in_secs=_RENEWAL_INTERVAL_IN_SECS,
                         duration_in_secs=_DURATION_IN_SECS,
                         home_page_url="",
                         status_page_url="",
                         health_check_url="",
                         secure_health_check_url="",
                         vip_adr="",
                         secure_vip_addr="",
                         is_coordinating_discovery_server=False,
                         metadata={}):
    """
    通过RLock()防止注册服务被多线程调用出错
    """
    with __cache_registry_clients_lock:
        client = RegistryClient(eureka_server=eureka_server,
                                app_name=app_name,
                                instance_id=instance_id,
                                instance_host=instance_host,
                                instance_ip=instance_ip,
                                instance_port=instance_port,
                                instance_unsecure_port_enabled=instance_unsecure_port_enabled,
                                instance_secure_port=instance_secure_port,
                                instance_secure_port_enabled=instance_secure_port_enabled,
                                countryId=countryId,
                                data_center_name=data_center_name,
                                renewal_interval_in_secs=renewal_interval_in_secs,
                                duration_in_secs=duration_in_secs,
                                home_page_url=home_page_url,
                                status_page_url=status_page_url,
                                health_check_url=health_check_url,
                                secure_health_check_url=secure_health_check_url,
                                vip_adr=vip_adr,
                                secure_vip_addr=secure_vip_addr,
                                is_coordinating_discovery_server=is_coordinating_discovery_server,
                                metadata=metadata)
        __cache_registry_clients[__cache_key] = client
        client.start()
        return client


def init(eureka_server=_DEFAULT_EUREKA_SERVER_URL,
         regions=[],
         app_name="",
         instance_id="",
         instance_host="",
         instance_ip="",
         instance_port=_DEFAULT_INSTNACE_PORT,
         instance_unsecure_port_enabled=True,
         instance_secure_port=_DEFAULT_INSTNACE_SECURE_PORT,
         instance_secure_port_enabled=False,
         countryId=1,  # @deprecaded
         data_center_name=_DEFAULT_DATA_CENTER_INFO,  # Netflix, Amazon, MyOwn
         renewal_interval_in_secs=_RENEWAL_INTERVAL_IN_SECS,
         duration_in_secs=_DURATION_IN_SECS,
         home_page_url="",
         status_page_url="",
         health_check_url="",
         secure_health_check_url="",
         vip_adr="",
         secure_vip_addr="",
         is_coordinating_discovery_server=False,
         metadata={},
         ha_strategy=HA_STRATEGY_RANDOM):
    """
    注释主程序入口
    """
    # 注册该服务
    registry_client = init_registry_client(eureka_server=eureka_server,
                                           app_name=app_name,
                                           instance_id=instance_id,
                                           instance_host=instance_host,
                                           instance_ip=instance_ip,
                                           instance_port=instance_port,
                                           instance_unsecure_port_enabled=instance_unsecure_port_enabled,
                                           instance_secure_port=instance_secure_port,
                                           instance_secure_port_enabled=instance_secure_port_enabled,
                                           countryId=countryId,
                                           data_center_name=data_center_name,
                                           renewal_interval_in_secs=renewal_interval_in_secs,
                                           duration_in_secs=duration_in_secs,
                                           home_page_url=home_page_url,
                                           status_page_url=status_page_url,
                                           health_check_url=health_check_url,
                                           secure_health_check_url=secure_health_check_url,
                                           vip_adr=vip_adr,
                                           secure_vip_addr=secure_vip_addr,
                                           is_coordinating_discovery_server=is_coordinating_discovery_server,
                                           metadata=metadata)
    # 发现服务
    # discovery_client = init_discovery_client(eureka_server,
    #                                          regions=regions,
    #                                          renewal_interval_in_secs=renewal_interval_in_secs,
    #                                          ha_strategy=ha_strategy)
    discovery_client = None
    return registry_client, discovery_client


"""====================== Registry Client ======================================="""


class RegistryClient:
    """Eureka client for spring cloud"""

    def __init__(self,
                 eureka_server=_DEFAULT_EUREKA_SERVER_URL,
                 app_name="",
                 instance_id="",
                 instance_host="",
                 instance_ip="",
                 instance_port=_DEFAULT_INSTNACE_PORT,
                 instance_unsecure_port_enabled=True,
                 instance_secure_port=_DEFAULT_INSTNACE_SECURE_PORT,
                 instance_secure_port_enabled=False,
                 countryId=1,  # @deprecaded
                 data_center_name=_DEFAULT_DATA_CENTER_INFO,  # Netflix, Amazon, MyOwn
                 renewal_interval_in_secs=_RENEWAL_INTERVAL_IN_SECS,
                 duration_in_secs=_DURATION_IN_SECS,
                 home_page_url="",
                 status_page_url="",
                 health_check_url="",
                 secure_health_check_url="",
                 vip_adr="",
                 secure_vip_addr="",
                 is_coordinating_discovery_server=False,
                 metadata={}):
        assert eureka_server is not None and eureka_server != "", "eureka server must be specified."
        assert app_name is not None and app_name != "", "application name must be specified."
        assert instance_port > 0, "port is unvalid"
        assert isinstance(metadata, dict), "metadata must be dict"
        instance_host = instance_host or ""
        instance_ip = instance_ip or ""
        self.__net_lock = RLock()  # 获取一把锁，貌似也不一定需要
        self.__eureka_servers = eureka_server.split(",")
        self.__instance_host = self.__instance_ip = None

        def try_to_get_client_ip(url):
            if instance_host == "" and instance_ip == "":  # 如果二者都为空
                self.__instance_host = self.__instance_ip = RegistryClient.__get_instance_ip(url)
            elif instance_host != "" and instance_ip == "":  # 如果host不为空，ip为空
                self.__instance_host = instance_host
                if is_ip_address(instance_host):
                    self.__instance_ip = instance_host
                else:
                    self.__instance_ip = RegistryClient.__get_instance_ip(url)
            else:  # 如果直接配置了ip，直接使用ip即可
                self.__instance_host = instance_ip
                self.__instance_ip = instance_ip

        self.__try_all_eureka_server(try_to_get_client_ip)

        mdata = {
            'management.port': str(instance_port)
        }
        mdata.update(metadata)  # 使用metadata中的值更新mdata
        self.__instance = {
            'instanceId': instance_id if instance_id != "" else "%s:%s:%d" % (
                self.__instance_host, app_name.lower(), instance_port),  # 示例id，如果未指定就是 host:app_name:port
            'hostName': self.__instance_host,
            'app': app_name.upper(),
            'ipAddr': self.__instance_ip,
            'port': {
                '$': instance_port,
                '@enabled': str(instance_unsecure_port_enabled).lower()
            },
            'securePort': {
                '$': instance_secure_port,
                '@enabled': str(instance_secure_port_enabled).lower()
            },
            'countryId': countryId,
            'dataCenterInfo': {
                '@class': _DEFAULT_DATA_CENTER_INFO_CLASS,
                'name': data_center_name
            },
            'leaseInfo': {
                'renewalIntervalInSecs': renewal_interval_in_secs,
                'durationInSecs': duration_in_secs,
                'registrationTimestamp': 0,
                'lastRenewalTimestamp': 0,
                'evictionTimestamp': 0,
                'serviceUpTimestamp': 0
            },
            'metadata': mdata,
            'homePageUrl': RegistryClient.__format_url(home_page_url, self.__instance_host, instance_port),
            'statusPageUrl': RegistryClient.__format_url(status_page_url, self.__instance_host, instance_port, "info"),
            'healthCheckUrl': RegistryClient.__format_url(health_check_url, self.__instance_host, instance_port,
                                                          "health"),
            'secureHealthCheckUrl': secure_health_check_url,
            'vipAddress': vip_adr if vip_adr != "" else app_name.lower(),
            'secureVipAddress': secure_vip_addr if secure_vip_addr != "" else app_name.lower(),
            'isCoordinatingDiscoveryServer': str(is_coordinating_discovery_server).lower()
        }

        self.__alive = False
        self.__heart_beat_timer = Timer(renewal_interval_in_secs, self.__heart_beat)  # 定时调用self.__heart_beat函数
        self.__heart_beat_timer.daemon = True  # 设置为守护线程，不会阻塞主线程执行，主线程也不会等待该线程结束

    def __try_all_eureka_server(self, fun):
        """
        对所有eureka服务器执行函数
        如发送心跳、获取服务、注册服务等

        fun 可能是一个url转换函数，从defaultZone中获取真正的eureka server地址
        fun 也可能是一个
        :param fun:
        :return:
        """
        with self.__net_lock:
            untry_servers = self.__eureka_servers  # yml文件中的eureka的defaultZone列表
            tried_servers = []
            ok = False
            while len(untry_servers) > 0:
                url = untry_servers[0].strip()
                try:
                    fun(url)
                except (http_client.HTTPError, http_client.URLError):
                    logger.warning("Eureka server [%s] is down, use next url to try." % url)
                    tried_servers.append(url)
                    untry_servers = untry_servers[1:]
                else:
                    ok = True
                    break
            if len(tried_servers) > 0:
                untry_servers.extend(tried_servers)
                self.__eureka_servers = untry_servers
            if not ok:
                raise http_client.URLError("All eureka servers are down!")

    @staticmethod
    def __format_url(url, host, port, defalut_ctx=""):
        """
        生成微服务的各个页面的访问地址

        :param url: 访问的地址，如果不指定，该方法默认会使用示例的注册ip:port
        :param host:
        :param port:
        :param defalut_ctx:
        :return:
        """
        if url != "":  # 指定了url
            if url.startswith('http'):  # 说明指定了完整地址
                _url = url
            elif url.startswith('/'):  # 说明仅指定了 路由路径
                _url = 'http://%s:%d%s' % (host, port, url)
            else:
                _url = 'http://%s:%d/%s' % (host, port, url)
        else:  # 没有指定url
            _url = 'http://%s:%d/%s' % (host, port, defalut_ctx)
        return _url

    @staticmethod
    def __get_instance_ip(eureka_server):
        """
        获取系统ip，如果eureka_server中使用了ipv6，则返回本地ipv6地址
        :param eureka_server:
        :return:
        """
        url_obj = http_client.parse_url(eureka_server)  # 从defaultZone字符串中提取host和port
        target_ip = url_obj["host"]
        target_port = url_obj["port"]
        if target_port is None:
            if url_obj["schema"] == "http":
                target_port = 80
            else:
                target_port = 443

        if url_obj["ipv6"] is not None:
            target_ip = url_obj["ipv6"]
            socket_family = socket.AF_INET6
        else:
            socket_family = socket.AF_INET

        s = socket.socket(socket_family, socket.SOCK_DGRAM)
        s.connect((target_ip, target_port))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def register(self, status=INSTANCE_STATUS, overriddenstatus=INSTANCE_STATUS_UNKNOWN):
        """
        将 self.__instance字典作为json数据发送给eureka进行注册

        :param status:
        :param overriddenstatus:
        :return:
        """
        self.__instance["status"] = status
        self.__instance["overriddenstatus"] = overriddenstatus
        self.__instance["lastUpdatedTimestamp"] = str(int(time.time() * 1000))
        self.__instance["lastDirtyTimestamp"] = str(int(time.time() * 1000))
        try:
            # 将匿名函数传入__try_all...，这里用lambda函数是为了传入参数url
            self.__try_all_eureka_server(lambda url: _register(url, self.__instance))
        except:
            logger.exception("error!")
        else:
            self.__alive = True

    def start(self):
        logger.debug("start to registry client...")
        self.register()
        self.__heart_beat_timer.start()

    def send_heart_beat(self, overridden_status=""):
        """
        客户端实例发送心跳，会使用全局的 send_heart_beat()方法发送

        :param overridden_status:
        :return:
        """
        try:
            self.__try_all_eureka_server(lambda url: send_heart_beat(url, self.__instance["app"],
                                                                     self.__instance["instanceId"],
                                                                     self.__instance["lastDirtyTimestamp"],
                                                                     status=self.__instance["status"],
                                                                     overriddenstatus=overridden_status))
        except:
            logger.exception("Error!")
            logger.info("Cannot send heartbeat to server, try to register")
            self.register()

    def __heart_beat(self):
        while True:
            logger.debug("sending heart beat to spring cloud server ")
            self.send_heart_beat()
            time.sleep(self.__instance["leaseInfo"]["renewalIntervalInSecs"])


def send_heart_beat(eureka_server, app_name, instance_id, last_dirty_timestamp, status=INSTANCE_STATUS,
                    overriddenstatus=""):
    """
    发送心跳

    :param eureka_server:
    :param app_name:
    :param instance_id:
    :param last_dirty_timestamp:
    :param status:
    :param overriddenstatus:
    :return:
    """
    url = _format_url(eureka_server) + "apps/%s/%s?status=%s&lastDirtyTimestamp=%s" % \
          (app_name, instance_id, status, str(last_dirty_timestamp))
    logger.debug("heartbeat url::" + url)
    if overriddenstatus != "":
        url += "&overriddenstatus=" + overriddenstatus

    req = http_client.Request(url)
    req.get_method = lambda: "PUT"
    http_client.load(req, timeout=_DEFAULT_TIME_OUT)


def _register(eureka_server, instance_dic):
    req = http_client.Request(_format_url(eureka_server) + "apps/%s" % instance_dic["app"])  # 生成请求对象，准备发送
    req.add_header('Content-Type', 'application/json')
    req.get_method = lambda: "POST"
    http_client.load(req, json.dumps({"instance": instance_dic}).encode(_DEFAULT_ENCODING), timeout=_DEFAULT_TIME_OUT)


def _format_url(url: str) -> str:
    """
    在连接url时，确保网址最后一个字符是 "/"
    """
    if url.endswith('/'):
        return url
    else:
        return url + "/"
