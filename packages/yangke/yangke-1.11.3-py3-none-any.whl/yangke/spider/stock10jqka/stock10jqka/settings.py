# -*- coding: utf-8 -*-

# Scrapy settings for stock10jqka project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'stock10jqka'

SPIDER_MODULES = ['stock10jqka.spiders']
NEWSPIDER_MODULE = 'stock10jqka.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'stock10jqka (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66',
}

# Enable or disable spider middlewares  中间件使用selenium进行爬取网页，因为现在大部分网页是动态的，scrapy原生组件不支持动态网页
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'stock10jqka.middlewares.Stock10JqkaSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'stock10jqka.middlewares.Stock10JqkaDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'stock10jqka.pipelines.Stock10JqkaPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# REDIRECT_ENABLED = False  # 拒绝页面重定向，重定向的页面一般都是无法解析的，因为页面元素不一样
LOG_LEVEL = 'WARNING'
mysql_config = {  # 如果变量名为全大写，则可以在爬虫框架中的任何地方以settings.get(变量名的方式)获取settings.py中的变量值，小写则不行
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '111111',
    'charset': 'utf8mb4',
    'db': "stocks",
}
COLUMNS_STOCK = {  # 如果变量名为全大写，则可以在爬虫框架中的任何地方以settings.get(变量名的方式)获取settings.py中的变量值
    # 'code': 'varchar(9)',  # 9个字符长度，mysql8版本指的是字符长度（中英文都视作一个字符），早期版本可能指的是字节长度，
    # 表中不需要code列，因为表是以code命名的。
    'date': 'date',  # 主键
    '评分': 'float',
    '击败/%': 'tinyint',  # (-128,127)
    '短期趋势': 'varchar(50)',  # 0-255字节
    '中期趋势': 'varchar(50)',
    '长期趋势': 'varchar(50)',
    '技术面': 'float',
    '资金面': 'float',
    '消息面': 'float',
    '行业面': 'float',
    '基本面': 'float',
    '评级': 'tinyint',
    '地域': 'varchar(20)',
    '设计概念': 'varchar(500)',
    '主营业务': 'varchar(1000)',
    '每股净资产/元': 'float',
    '每股收益/元': 'float',
    '净利润/亿元': 'float',
    '净利润增长率/%': 'float',
    '营业收入/亿元': 'float',
    '每股现金流/元': 'float',
    '每股公积金/元': 'float',
    '每股未分配利润/元': 'float',
    '总股本/亿': 'float',
    '流通股/亿': 'float'
}
COLUMNS_STOCK_ITEM = {
    # mysql数据库中的列对应的item中的字段名
    'date': 'date',  # 主键
    '评分': '诊股_评分',
    '击败/%': '诊股_击败',
    '短期趋势': '诊股_短期趋势',
    '中期趋势': '诊股_中期趋势',
    '长期趋势': '诊股_长期趋势',
    '技术面': '诊股_技术面',
    '资金面': '诊股_资金面',
    '消息面': '诊股_消息面',
    '行业面': '诊股_行业面',
    '基本面': '诊股_基本面',
    '评级': '评级',
    '地域': '地域',
    '设计概念': '设计概念',
    '主营业务': '主营业务',
    '每股净资产/元': '每股净资产',
    '每股收益/元': '每股收益',
    '净利润/亿元': '净利润',
    '净利润增长率/%': '净利润增长率',
    '营业收入/亿元': '营业收入',
    '每股现金流/元': '每股现金流',
    '每股公积金/元': '每股公积金',
    '每股未分配利润/元': '每股未分配利润',
    '总股本/亿': '总股本',
    '流通股/亿': '流通股'
}
COLUMNS_NEW = {
    # mysql数据库中的列对应的item中的字段名相同，不用再单独配置
    # 'code': 'varchar(9)',
    'date': 'datetime',  # 主键
    '标题': 'varchar(100)',  # 主键s
    'url': 'varchar(200)',  # 可能包含特殊字符，不宜作为主键
    '内容': 'TEXT'  # 0-65535字节
}

NEO4J_CONFIG = {

}
