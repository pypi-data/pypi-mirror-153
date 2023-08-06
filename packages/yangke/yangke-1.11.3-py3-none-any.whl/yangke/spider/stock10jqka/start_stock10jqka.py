from scrapy import cmdline
import os, sys

# 创建scrapy项目的命令： python -m scrapy startproject <project-name>
# 进入爬虫项目目录：     cd <project-name>
# 初始化一个爬虫：       python -m scrapy genspider <爬虫名> <网站域名>
# 初始化另一个爬虫：     python -m scrapy genspider -t crawl jqka_spider "10jqka.com.cn"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
cmdline.execute("scrapy crawl jqka_spider".split())  # 执行cmdline.execute()方法

# scrapy爬虫执行顺序
# 1. cmdline中的execute方法进入爬虫，初始化settings中的各类参数
# 2. crawler.py中启动CrawlerProcess，CrawlerProcess初始化SpiderLoader
# 2.1 SpiderLoader通过from_settings()加载settings中定义的spider，通过self._load_all_spiders()方法
# 2.2 加载用户在settings.py文件的SPIDER_MODULES中定义的文件夹中的所有spider
# 2.3 初始化pipelines.py中的自定义Pipeline
# 3. 开始爬取
