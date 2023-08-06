# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from stock10jqka.items import Stock10JqkaItem, NewsItem, StockInfoItem
from stock10jqka.settings import COLUMNS_STOCK, COLUMNS_NEW, COLUMNS_STOCK_ITEM
from yangke.common.mysql import insert_item_to_mysql, has_table, create_table, update_update_time_of_table


class Stock10JqkaPipeline(object):
    """
    爬虫中yield的item会送到该类中执行，调用该类中的process_item()方法
    """

    def __init__(self):
        pass

    def open_spider(self, spider):
        # 确保mysql服务开启
        print("开始爬取数据...")

    def process_item(self, item, spider):
        if isinstance(item, Stock10JqkaItem):
            # 保存数据
            print("插入股票数据，股票代码：{}".format(item['code']))
            tableName = "ths{}".format(item['code'])
            if not has_table(tableName):  # 这句实际不需要判断，因为创建表时，只有表不存在时才会创建
                create_table(tableName, COLUMNS_STOCK)  # 如果表存在时调用该函数，会有warning提示重复

            item_dict = item.deepcopy()
            item_dict.pop('code')
            ITEM_TO_COLUMNS_STOCK = dict(zip(COLUMNS_STOCK_ITEM.values(), COLUMNS_STOCK_ITEM.keys()))  # 反转字典
            COLUMNS_LIST = [ITEM_TO_COLUMNS_STOCK.get(key) for key in item_dict.keys()]  # 逐个获得item对应的mysql列名
            insert_item_to_mysql(table_name=tableName, values=list(item_dict.values()),
                                 col_names=COLUMNS_LIST, ignore=True)
            update_update_time_of_table(tableName)
        elif isinstance(item, NewsItem):
            # 保存新闻
            if item['date'] is None and item['标题'] is None:  # 有些重定向的页面链接到了同花顺以外的域名，且获取不到数据
                return
            print("插入股票新闻，股票代码：{}".format(item['code']))
            tableName = "news{}".format(item['code'])
            item_dict = item.deepcopy()
            item_dict.pop('code')
            if not has_table(table_name=tableName):
                create_table(tableName, COLUMNS_NEW, primary=[0, 1])
            insert_item_to_mysql(table_name=tableName, values=list(item_dict.values()),
                                 col_names=(list(item_dict.keys())), replace=True)
            update_update_time_of_table(tableName)
        # 将item保存到mysql
        elif isinstance(item, StockInfoItem):  # 记录各个股票的基本信息
            if not has_table(table_name="stocksInfo"):
                create_table("stocksInfo", columns={"symbol": "varchar(6)", "business": "varchar(1000)",
                                                    "concept": "varchar(100)", "date_listing": "date",
                                                    "location": "varchar(100)", "name": "varchar(20)"}, primary=[0])
            insert_item_to_mysql(table_name="stocksInfo", col_names=["symbol", "business", "concept", "date_listing",
                                                                     "location", "name"],
                                 values=[item['code'], item['business'], item['concept'], item['date_listing'],
                                         item['location'], item['name']], replace=True)
            update_update_time_of_table("stocksInfo")
            # 构建neo4j数据库

        return item

    def close_spider(self, spider):
        print("爬取结束！")


def get_cursor_news():
    global cursor_news
    if cursor_news is None:
        return Stock10JqkaPipeline().cursor_news
    else:
        return cursor_news


def get_cursor_stocks():
    global cursor_stocks
    if cursor_stocks is None:
        cursor_stocks = Stock10JqkaPipeline().cursor_stocks
    return cursor_stocks
