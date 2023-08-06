# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Stock10JqkaItem(scrapy.Item):
    """
    该数据item存储到Mysql数据库，这里item的字段需要与settings中COLUMN_STOCK的字段相同
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()  # 代码，唯一标识符，表示数据属于哪个股票
    date = scrapy.Field()
    诊股_评分 = scrapy.Field()
    诊股_击败 = scrapy.Field()
    诊股_短期趋势 = scrapy.Field()
    诊股_中期趋势 = scrapy.Field()
    诊股_长期趋势 = scrapy.Field()
    诊股_技术面 = scrapy.Field()
    诊股_资金面 = scrapy.Field()
    诊股_消息面 = scrapy.Field()
    诊股_行业面 = scrapy.Field()
    诊股_基本面 = scrapy.Field()

    评级 = scrapy.Field()

    # 历史数据
    # 因为所属地域，主营业务等可能会有改变，这里把历史数据也存储下来
    地域 = scrapy.Field()  # 所属地域，当前的
    设计概念 = scrapy.Field()  # 设计概念
    主营业务 = scrapy.Field()  # 主营业务
    每股净资产 = scrapy.Field()
    每股收益 = scrapy.Field()
    净利润 = scrapy.Field()
    净利润增长率 = scrapy.Field()
    营业收入 = scrapy.Field()
    每股现金流 = scrapy.Field()
    每股公积金 = scrapy.Field()
    每股未分配利润 = scrapy.Field()
    总股本 = scrapy.Field()
    流通股 = scrapy.Field()


class StockInfoItem(scrapy.Item):
    """
    该数据item用于构建neo4j图数据

    字段：code, name, location, concept, business, date_listing
    """

    code = scrapy.Field()  # 代码
    name = scrapy.Field()  # 名称
    location = scrapy.Field()  # 所属地域，当前的
    concept = scrapy.Field()  # 设计概念
    business = scrapy.Field()  # 主营业务
    date_listing = scrapy.Field()  # 上市日期


class NewsItem(scrapy.Item):
    """
    股票的历史新闻，因为爬取到的每日新闻数量不固定，计划使用mysql数据库以字符串形式存储
    """
    code = scrapy.Field()  # 代码，唯一标识符，表示数据属于哪个股票
    # 来源 = scrapy.Field()
    标题 = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    内容 = scrapy.Field()
