# -*- coding: utf-8 -*-
import datetime
import re
import sys

from selenium.common.exceptions import WebDriverException
from yangke.common.config import logger

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import SelectorList
from scrapy.spiders import CrawlSpider, Rule
from pathlib2 import Path

from yangke.common.mysql import read_dataframe_from_mysql, connect_mysql, has_table
from selenium import webdriver

from stock10jqka.items import *

# noinspection NonAsciiCharacters
from stock10jqka.settings import mysql_config

print(f"__file__:{__file__}")
print(f"__package__:{__package__}")


class JqkaSpiderSpider(CrawlSpider):
    name = 'jqka_spider'
    allowed_domains = ['10jqka.com.cn']

    # 初始化mysql数据库
    config = mysql_config.copy()  # 浅拷贝
    try:
        # 建立mysql数据库连接
        connect_mysql(config=config, create_if_not_exist=True, use_pymysql=False, return_type="engine")
    except:
        raise Exception("初始化mysql时发生异常，检查mysql服务是否开启！")
    print("初始化mysql数据库成功！")

    # 如果不存在symbols表，需要初始化该表
    if not has_table("symbols"):
        import yangke.stock.main as get_symbols
        get_symbols.runCMD(f"python {get_symbols.__file__} --command getSymbols")

    codes_list = read_dataframe_from_mysql("symbols")['symbol']
    codes_list = list(codes_list)
    start_urls = []
    for code in codes_list:
        start_urls.append('http://stockpage.10jqka.com.cn/{}/'.format(code))
    # start_urls = ["http://stockpage.10jqka.com.cn/000001/"]
    del codes_list, code

    rules = (
        # 正则\d表示数字，$表示匹配结尾，即必须以\d结尾
        # 匹配 http://stockpage.10jqka.com.cn/600666/ 且不能匹配 http://stockpage.10jqka.com.cn/600666/event/
        # Rule(LinkExtractor(allow=r'http:\/\/stockpage\.10jqka.+\/\d+\/$',
        #                    restrict_xpaths="//ul[@class='news_list stat']"),  # 限制在公司新闻栏进行跟进
        #      # callback='parse_item',
        #      follow=True),
        Rule(LinkExtractor(allow=r'http:\/\/stockpage\.10jqka.+\/\d+\/$'),  # 在当前页面进行解析
             callback='parse_item',
             follow=False),
        # 匹配 http://stock.10jqka.com.cn/20200315/c618455360.shtml
        # Rule(LinkExtractor(allow=r'http:\/\/stock\.10jqka.+\/\d+\/.+\.shtml'), callback='parse_news',
        #        follow=False),  # 在跟进页面进行解析，这里cb_kwargs会传给callback指定的函数，Rule最终也要调用Request类
    )

    def __init__(self, *args, **kwargs):
        # 初始化爬虫使用的browser，必须安装selenium的edge/firefox/chrome中的任意一个
        try:
            self.browser = webdriver.Edge()
            logger.info("使用Edge浏览器进行数据爬取")
        except (FileNotFoundError, WebDriverException):
            try:
                self.browser = webdriver.Firefox()
                logger.info("使用Firefox浏览器进行数据爬取")
            except (FileNotFoundError, WebDriverException):
                try:
                    self.browser = webdriver.Chrome()
                    logger.info("使用Chrome浏览器进行数据爬取")
                except (FileNotFoundError, WebDriverException):
                    logger.error("selenium webdriver初始化失败！")
                    sys.exit(1)
        super(JqkaSpiderSpider, self).__init__()

    def parse_item(self, response):
        # noinspection NonAsciiCharacters
        公司简介 = response.xpath("//dl[@class='company_details']")  # 公司简介栏
        # noinspection NonAsciiCharacters
        牛叉诊股 = response.xpath("//div[@class='sub_cont_4 m_s_l']")  # 牛叉诊股栏
        # noinspection NonAsciiCharacters
        机构评级 = response.xpath("//div[@class='sub_cont_5']")  # 机构评级栏
        # print(len(公司简介), len(牛叉诊股), len(机构评级))
        # noinspection NonAsciiCharacters
        评分, 击败百分数, short_trend, medium_trend, long_trend, tech_trend, fund_trend, msg_trend, industry_trend, basic_trend = self.parse_牛叉诊股(
            牛叉诊股)
        # noinspection NonAsciiCharacters
        评级 = self.parse_机构评级(机构评级)  # 0,1,2,3,4,5对应【没有数据, 卖出, 减持, 中性, 增持, 买入】
        date = datetime.datetime.today()
        # noinspection NonAsciiCharacters
        所属地域, 设计概念, 主营业务, 上市日期, 每股净资产, 每股收益, 净利润, 净利润增长率, 营业收入, 每股现金流, 每股公积金, 每股未分配利润, 总股本, 流通股 = self.parse_公司简介(公司简介)

        temp = response.xpath("//h1[@class='m_logo fl']")[0]
        temp = temp.xpath(".//strong/text()").getall()
        name = temp[0]
        code = temp[1]

        item1 = StockInfoItem(code=code, name=name, location=所属地域, concept=设计概念, business=主营业务,
                              date_listing=上市日期)
        item2 = Stock10JqkaItem(code=code, date=date.date(), 诊股_评分=评分, 诊股_击败=击败百分数, 诊股_短期趋势=short_trend,
                                诊股_中期趋势=medium_trend, 诊股_长期趋势=long_trend, 诊股_技术面=tech_trend,
                                诊股_资金面=fund_trend, 诊股_消息面=msg_trend, 诊股_行业面=industry_trend,
                                诊股_基本面=basic_trend, 评级=评级, 设计概念=设计概念, 主营业务=主营业务, 地域=所属地域,
                                每股净资产=每股净资产, 每股收益=每股收益, 净利润=净利润, 净利润增长率=净利润增长率,
                                营业收入=营业收入, 每股现金流=每股现金流, 每股公积金=每股公积金,
                                每股未分配利润=每股未分配利润, 总股本=总股本, 流通股=流通股)
        yield item1
        yield item2
        # noinspection NonAsciiCharacters
        公司新闻 = response.xpath("//ul[@stat='f10_spqk_gsxw']//@href").getall()
        pattern_news = re.compile(r'http:\/\/stock\.10jqka.+\/\d+\/.+\.shtml')
        urls = [url for url in 公司新闻 if pattern_news.match(url)]

        for href in urls:
            print("GET {}".format(href))
            yield scrapy.Request(url=href, callback=self.parse_news, cb_kwargs={"code": code})

    # noinspection All
    def parse_公司简介(self, selectors: SelectorList):
        dds = selectors[0].xpath(".//dd")
        所属地域 = dds[0].xpath(".//text()").get()
        设计概念 = dds[1].xpath(".//@title").get()
        主营业务 = dds[3].xpath(".//@title").get()
        # 去除括号内的备注内容，删除最后的句号
        主营业务 = 主营业务.strip()
        上市日期 = dds[4].xpath(".//text()").get()
        # 以下为与日期有关的
        # 数字的正则表达式：(-?\d+\.\d+)
        # python中正则表达式中的小括号有特殊的作用，小括号括起来的部分为re.findall()返回的结果，而整个正则表达式决定是不是匹配
        # 如 re.findall('(\d+)%?', '43%')[0] -> 43
        # 而 re.findall('(\d+%?)', '43%')[0] -> 43%
        # 如果没有小括号，则相当于整个正则表达式都在小括号内部
        # 如果有多个小括号，都会返回成tuple，每个小括号内的匹配结果都会成为tuple项
        # 如 re.findall('(\d+)\.(\d+)', '43.23%') -> [('43', '23')]
        float_re = r'(-?\d+\.\d+)'
        character_re = '[\u4e00-\u9fa5]+'  # 汉字的正则表达式，用于校验单位是否不是正常单位

        section = dds[5].xpath(".//text()").get()
        每股净资产 = re.findall(float_re, section)[0]  # 元
        unit = re.findall(character_re, section)[0]  # 元
        assert unit == "元", "网页上爬取的【每股净资产】单位与软件数据库中单位不一致，请检查..."

        section = dds[6].xpath(".//text()").get()
        每股收益 = re.findall(float_re, section)[0]  # 元
        unit = re.findall(character_re, section)[0]  # 元
        assert unit == "元", "网页上爬取的【每股收益】单位与软件数据库中单位不一致，请检查..."

        section = dds[7].xpath(".//text()").get()
        净利润 = re.findall(float_re, section)[0]  # 亿元
        unit = re.findall(character_re, section)[0]  # 亿元
        assert unit == "亿元", "网页上爬取的【净利润】单位与软件数据库中单位不一致，请检查..."

        section = dds[8].xpath(".//text()").get()
        净利润增长率 = re.findall(float_re, section)[0]  #

        section = dds[9].xpath(".//text()").get()
        营业收入 = re.findall(float_re, section)[0]  # 亿元
        unit = re.findall(character_re, section)[0]  # 亿元
        assert unit == "亿元", "网页上爬取的【营业收入】单位与软件数据库中单位不一致，请检查..."

        section = dds[10].xpath(".//text()").get()
        每股现金流 = re.findall(float_re, section)[0]  # 元
        unit = re.findall(character_re, section)[0]  # 元
        assert unit == "元", "网页上爬取的【每股现金流】单位与软件数据库中单位不一致，请检查..."

        section = dds[11].xpath(".//text()").get()
        每股公积金 = re.findall(float_re, section)[0]  # 元
        unit = re.findall(character_re, section)[0]  # 元
        assert unit == "元", "网页上爬取的【每股公积金】单位与软件数据库中单位不一致，请检查..."

        section = dds[12].xpath(".//text()").get()
        每股未分配利润 = re.findall(float_re, section)[0]  # 元
        unit = re.findall(character_re, section)[0]  # 元
        assert unit == "元", "网页上爬取的【每股未分配利润】单位与软件数据库中单位不一致，请检查..."

        section = dds[13].xpath(".//text()").get()
        总股本 = re.findall(float_re, section)[0]  # 亿
        unit = re.findall(character_re, section)[0]  # 亿
        assert unit == "亿", "网页上爬取的【总股本】单位与软件数据库中单位不一致，请检查..."

        section = dds[14].xpath(".//text()").get()
        流通股 = re.findall(float_re, section)[0]  # 亿
        unit = re.findall(character_re, section)[0]  # 亿
        assert unit == "亿", "网页上爬取的【流通股】单位与软件数据库中单位不一致，请检查..."
        return 所属地域, 设计概念, 主营业务, 上市日期, 每股净资产, 每股收益, 净利润, 净利润增长率, 营业收入, 每股现金流, 每股公积金, 每股未分配利润, 总股本, 流通股

    # noinspection All
    def parse_news(self, response, **cb_kwargs):
        code = cb_kwargs.get('code')
        content_div = response.xpath("//div[@class='main-text atc-content']")
        # content_list = content_div.xpath(".//p/text()").getall()  # 只能从<p>节点获得直接的内容
        content_list = content_div.xpath(".//p").xpath('string(.)').getall()  # 可以获得<p><strong>内容</><>
        content_list = [p.strip() for p in content_list if p.strip() != ""]

        # 去掉新闻后的网页宣传后缀
        # post = content_div.xpath(".//a[@target='_blank']").xpath('string(.)').getall()[-2].strip()
        # content_list = content_list[:-2]

        content = "\n".join(content_list)
        title = response.xpath("//h2[@class='main-title']/text()").get()
        temp_section = response.xpath("//div[@class='info-fl fl']")
        date = temp_section.xpath(".//span[@id='pubtime_baidu']/text()").get()
        # source=temp_section.xpath(".//span[@") # 新闻来源可能是个图片，暂时不爬取来源
        item = NewsItem(code=code, 标题=title, date=date, 内容=content, url=response.url)
        yield item

    # noinspection All
    def parse_牛叉诊股(self, sections: SelectorList):
        for selector in sections:
            评分 = selector.xpath(".//span[@class='analyze-num']/text()").get()
            击败百分数 = selector.xpath(".//span[@class='analyze-tips']/text()").get()
            击败百分数 = re.findall(r"(\d+)", 击败百分数)[0]
            trend = selector.xpath(".//div[@class='txt-main']/text()").getall()
            short_trend, medium_trend, long_trend = trend[0], trend[1], trend[2]
            诊股 = selector.xpath(".//div[@class='analyze-stars']/i/text()").getall()
            tech_trend, fund_trend, msg_trend, industry_trend, basic_trend \
                = 诊股[0], 诊股[1], 诊股[2], 诊股[3], 诊股[4]
            result = (评分, 击败百分数, short_trend, medium_trend, long_trend,
                      tech_trend, fund_trend, msg_trend, industry_trend, basic_trend)
        return result

    # noinspection All
    def parse_机构评级(self, sections: SelectorList):
        for selector in sections:
            评级 = selector.xpath(".//div[@class='jg-level']/span/@class").get()
            评级 = re.findall(r"\d+", 评级)[0]

        return 评级

    def close(self, reason):
        # 关闭selenium打开的浏览器
        self.browser.close()
        super(JqkaSpiderSpider, self).close(spider=self, reason="all done")
