from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import numpy as np
from yangke.core import strInList


class YkWordTable:
    def __init__(self, table=None, rows=None, title_list=[], unit_list=[], ignore_list=[], ignore_rows=[],
                 ignore_cols=[]):
        """
        根据python-docx的table对象构建解析table的数据结构

        :param table: 使用python-docx的table对象构建Table对象时，传入该对象值
        :param rows: 使用列表构建Table对象时，按行传入各行的值
        :param title_list: 标题关键字列表
        :param unit_list: 单位关键字列表
        :param ignore_list: 忽略关键字列表，当表格单元中含有该关键字列表中的关键字时，该单元格被认为是应该忽略的
        :param ignore_rows: 忽略的行号列表，默认不忽略任何行
        :param ignore_cols: 忽略的列号列表，默认不忽略任何列
        """
        self.rows = rows  # 按行存储的二维数组
        if table is not None:
            self.rows = []
            for row in table.rows:
                cur_rows = []
                for cell in row.cells:
                    cur_rows.append(cell.text)
                self.rows.append(cur_rows)

        self.cols = self.merge_same_rows_or_cols()  # 按列存储的二维数组

        self.title_list = title_list
        self.unit_list = unit_list
        self.ignore_list = ignore_list
        self.ignore_rows = ignore_rows
        self.ignore_cols = ignore_cols
        self.num_row = len(self.rows)
        self.num_col = len(self.rows[0])
        self.title_row = self.get_title_row()  # 根据标题关键字判断哪些行是标题行
        self.unit_row = []
        self.title_col = self.get_title_column()  # 根据标题关键字判断哪些列是标题列
        self.unit_col = []
        self.table_type = self.get_table_type()

    def get_row(self, idx):
        """
        获取第idx行的数据

        :param idx:
        :return:
        """
        row = []
        for text in self.rows[idx]:
            row.append(text)
        return row

    def get_column(self, idx):
        column = []
        for row in self.rows:
            for ci, text in enumerate(row):
                if ci == idx:
                    column.append(text)
        return column

    def merge_same_rows_or_cols(self):
        """合并表格中相同的行和列，只有所有相邻两行所有数据都相同时，才会合并"""
        rows = [self.rows[0]]

        for i in range(len(self.rows) - 1):
            if self.rows[i] != self.rows[i + 1]:
                rows.append(self.rows[i + 1])
        self.rows = rows
        cols = np.array(rows).T.tolist()
        cs = [cols[0]]
        merge_cols = False  # 用于标记是否有合并列操作发生，如果发生则需要根据列数据更新rows，
        # 无需判断是否有行合并发生，因为此处的列就是根据行生成的
        for j in range(len(cols) - 1):
            if cols[j] != cols[j + 1]:
                cs.append(cols[j + 1])
            else:
                merge_cols = True
        if merge_cols:
            self.rows = np.array(cs).T.tolist()
        return cs

    def __get_title_row_col(self, row_or_col='row'):
        """
        获得列表中的标题所在的行/列

        :param row_or_col: "row"/"col"取标题行还是标题列，
        :return:
        """
        title_row = []
        title_num = []
        if row_or_col == "row":
            rows_cols = self.num_row
            func = self.get_row
        else:
            rows_cols = self.num_col
            func = self.get_column
        for i in range(rows_cols):  # 遍历每一行
            num = 0
            for t in func(i):  # 统计每一行属于标题字段的个数
                if strInList(t, self.title_list, revert=True):
                    num = num + 1
            title_num.append(num)
        if max(title_num) >= 2:
            for i in range(len(title_num)):
                if title_num[i] == max(title_num):
                    title_row.append(i)
        return title_row

    def get_title_row(self):
        """
        获取标题所在的行索引
        """
        return self.__get_title_row_col("row")

    def get_title_column(self):
        """
        获取标题所在的列索引
        """
        return self.__get_title_row_col("col")

    def get_table_type(self):
        """
        分析表格类型，类型目前包括以下几种
        table_type=1 如下 ↓
        ---------------------------------------------------------
             title1               |              value1
             title2               |              value2
             ...                  |              ...
        ---------------------------------------------------------

        table_type=2 如下
        ---------------------------------------------------------
         title1  |  title2  |  title3  |  title4   |   ...
         value1  |  value2  |  value3  |  value4   |   ...
         ...
        ---------------------------------------------------------

        table_type=3 如下
        ---------------------------------------------------------
           **    |  title1  |  title2  |  title3  |  ...
         titleA  |  valueA1 |  valueA2 |  valueA3 |  ...
         titleB  |  valueB1 |  valueB2 |  valueB3 |  ...
         ...
        ---------------------------------------------------------

        table_type=4 如下
        ---------------------------------------------------------
         titleA  |                 valueA
         titleB  |                 valueB
         ...
           **    |  title1  |  title2  |  title3  |  ...
         titleC  |  valueC1 |  valueC2 |  valueC3 |  ...
         titleD  |  valueD1 |  valueD2 |  valueD3 |  ...
         ...
        ---------------------------------------------------------
        table_type=5, 为table_type=4的转置预留


        :return:
        """
        if len(self.title_row) == 0:  # 没有标题行
            return 1
        if len(self.title_col) == 0:  # 没有标题列
            return 2
        if len(self.title_row) == 1 and self.title_row[0] == 0:
            if len(self.title_col) == 1 and self.title_col[0] == 0:
                return 3
        if len(self.title_col) == 1 and self.title_col[0] == 0:
            if len(self.title_col) >= 1 and self.title_row[0] > 1:
                return 4

    def split_table(self):
        """
        将复杂表格拆分为对应table_type=1,2,3的三类表格
        :return:
        """
        if self.table_type in [1, 2, 3]:
            return [self]
        elif self.table_type == 4:
            split_row = self.title_row[0]
            table1 = YkWordTable(rows=self.rows[0:split_row], title_list=self.title_list, unit_list=self.unit_list,
                                 ignore_list=self.ignore_list, ignore_rows=self.ignore_rows,
                                 ignore_cols=self.ignore_cols)
            table2 = YkWordTable(rows=self.rows[split_row:], title_list=self.title_list, unit_list=self.unit_list,
                                 ignore_list=self.ignore_list, ignore_rows=self.ignore_rows,
                                 ignore_cols=self.ignore_cols)
            return [table1, table2]

    def analyze_table(self, sep="_"):
        """
        分析表格数据，返回{property_name: property_value}型式的字典

        :param sep: 用来连接行标题和列标题的连接符，默认为_
        :return:
        """
        properties = {}
        if self.table_type == 1:
            for row in self.rows:
                properties[row[0]] = row[1]
            return properties
        elif self.table_type == 2:
            for k, v in zip(self.get_row(0), self.get_row(1)):
                properties[k] = v
            return properties
        elif self.table_type == 3:
            for i in range(1, self.num_row):
                for j in range(1, self.num_col):
                    k = f"{self.rows[i][0]}{sep}{self.rows[0][j]}"
                    v = self.rows[i][j]
                    properties[k] = v
            return properties
        elif self.table_type == 4:
            tables = self.split_table()
            for table in tables:
                properties.update(table.analyze_table())
            return properties

    # 表明没有标题行，


def iter_block_items(parent, ignore=None):
    """
    依次返回word文档中的段落和表格

    example:
    import docx
    doc = docx.Document(file)
    for idx, block in enumerate(iter_block_items(doc, ignore="")):
        if isinstance(block, Paragraph):
            logger.info(block.text)
        elif isinstance(block, Table):
            table = YkWordTable(block, title_list=title)

    Yield each paragraph and table child within *parent*, in document order.
    Each returned value is an instance of either Table or Paragraph. *parent*
    would most commonly be a reference to a main Document object, but
    also works for a _Cell object, which itself can contain paragraphs and tables.
    
    :param ignore: 过滤属性，设置为空则会过滤为空的paragraph
    """
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            if ignore is not None:
                if Paragraph(child, parent).text == ignore:
                    continue
                else:
                    yield Paragraph(child, parent)
            else:
                yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)
