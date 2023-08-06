"""
定义stocks软件中需要存储到数据库的类
"""
from sqlalchemy import Column, Integer, String, Date, CHAR, Table, MetaData, DateTime, VARCHAR

holiday_table = MetaData()  # 没有关系的表放在不同的metadata中
symbols_table = MetaData()

Table('holiday', holiday_table,
      Column('calendarDate', Date, primary_key=True),
      Column('isOpen', CHAR, nullable=False))

Table("symbols", symbols_table,
      Column('symbol', Integer, primary_key=True),
      Column('name', String(20), nullable=False)
      )
