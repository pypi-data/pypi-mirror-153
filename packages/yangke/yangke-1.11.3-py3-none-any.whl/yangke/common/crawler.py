import os
import shutil

from pathlib2 import Path

from yangke.base import search_file_in_folders
from yangke.core import runCMD
from yangke.common.config import logger

spider_paths = [Path(__file__).parent.parent / Path("spider"), Path(__file__).parent.parent, os.getcwd()]


def start_scrapy_start(start_crawl_file: str, charset="utf8"):
    """
    开启爬虫项目，使用start.py文件

    :param start_file: 爬虫项目中的开始文件，如r"D:\stock10jqka\start_stock10jqka.py"
    :return:
    """
    # 实现方式，在spider_file目录运行cmd命令
    # python -m scrapy runspider myspider.py
    # 实现方式，在start_file目录运行cmd命令
    # python start_spider.py
    logger.info(start_crawl_file)
    if Path(start_crawl_file).is_absolute():
        pass
    else:
        base_name = Path(start_crawl_file).name
        start_crawl_file = search_file_in_folders(base_name, spider_paths)
    logger.info(f"爬虫启动文件：{start_crawl_file}")
    cwd = Path(start_crawl_file).parent
    logger.info(f"爬虫运行目录：{cwd}")

    # 把settings.yaml复制到爬虫的运行目录，以使爬虫能使用os.getcwd()中配置文件的配置
    settings_file_origin = os.path.join(os.getcwd(), "settings.yaml")
    settings_file_origin1 = os.path.join(os.getcwd(), "settings.yml")
    settings_file_dst = os.path.join(str(cwd), "settings.yaml")
    if os.path.exists(settings_file_origin):
        shutil.copy2(settings_file_origin, settings_file_dst)
    elif os.path.exists(settings_file_origin1):
        shutil.copy2(settings_file_origin1, settings_file_dst)

    runCMD('python "{}"'.format(start_crawl_file), charset=charset, wait_for_result=True, cwd=cwd,
           output_type="REALTIME_NORETURN")


def start_scrapy_spider(spider_file: str, charset="utf8"):
    """
    开启指定爬虫爬取网页

    :param spider_file: 爬虫项目中的爬虫文件，如r"D:\stock10jqka\stock10jqka\spiders\jqka_spider.py"，如果是相对路径，默认会在yangke/spider目录下查找
    :return:
    """
    if Path(spider_file).is_absolute():
        pass
    else:
        base_name = Path(spider_file).name
        spider_file = search_file_in_folders(base_name, spider_paths)
    cwd = Path(spider_file).parent
    runCMD('python -m scrapy runspider "{}"'.format(spider_file), charset=charset, wait_for_result=True, cwd=cwd,
           output_type="REALTIME_NORETURN")
