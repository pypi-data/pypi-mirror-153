import xlrd
from xlrd.sheet import Sheet


class xls:
    def __init__(self, file, *args, **kwargs):
        pass
        # 判断文件是否存在
        # 判断文件后缀是否对的上
        # 判断是否可以打开
        # type:xlrd.Book
        self.book = xlrd.open_workbook(file, *args, **kwargs)

    @property
    def active(self):
        return self.sheets()[0]

    def sheet_names(self):
        """
        返回sheet names列表
        :return:
        """
        return self.book.sheet_names()

    def sheets(self):
        """
        返回sheets对象列表
        :return:
        """
        return self.book.sheets()

    def sheet_by_name(self, sheet_name: str):
        """
        通过名字获取sheet对象
        :param sheet_name:
        :return:
        """
        return self.book.sheet_by_name(sheet_name)

    def sheet_by_index(self, sheet_index):
        """
        通过下标获取sheet对象
        :param sheet_index:
        :return:
        """
        return self.book.sheet_by_index(sheet_index)

    def rows(self, sheet_name=None):
        """
        返回指定sheet名下的所有行
        :param sheet_name:
        :return:
        """
        sheet_name = self.active.name if sheet_name is None else sheet_name
        return self.sheet_by_name(sheet_name).get_rows()

    def rows_counts(self, sheet_name: str = None):
        """
        返回指定sheet有多少行
        :param sheet_name:
        :return:
        """
        sheet_name = self.active.name if sheet_name is None else sheet_name
        return self.sheet_by_name(sheet_name).nrows

    def row_values(self, sheet_name: str = None, rowx: int = 0, start_colx=0, end_colx=None):
        """
        返回指定区域的行列表
        :param sheet_name:
        :param rowx:
        :param start_colx:
        :param end_colx:
        :return:
        """
        sheet_name = self.active.name if sheet_name is None else sheet_name
        return self.sheet_by_name(sheet_name).row_values(rowx, start_colx, end_colx)

    def row_types(self, sheet_name: str = None, rowx: int = 0, start_colx=0, end_colx=None):
        """
        返回指定行的 字段类型的数值列表
        :param sheet_name:
        :param rowx:
        :param start_colx:
        :param end_colx:
        :return:
        """
        sheet_name = self.active.name if sheet_name is None else sheet_name
        return self.sheet_by_name(sheet_name).row_types(rowx, start_colx, end_colx)

    def cols_counts(self, sheet_name: str = None):
        """
        返回指定sheet有多少列
        :param sheet_name:
        :return:
        """
        sheet_name = self.active.name if sheet_name is None else sheet_name
        return self.sheet_by_name(sheet_name).ncols

    def col_values(self, sheet_name: str = None, colx: int = 0, start_rowx=0, end_rowx=None):
        """
        返回指定区域的列列表
        :param sheet_name:
        :param colx:
        :param start_rowx:
        :param end_rowx:
        :return:
        """
        sheet_name = self.active.name if sheet_name is None else sheet_name
        return self.sheet_by_name(sheet_name).col_values(colx, start_rowx, end_rowx)

    def col_types(self, sheet_name: str = None, colx: int = 0, start_rowx=0, end_rowx=None):
        """
        返回指定列的 字段类型数值列表
        :param sheet_name:
        :param colx:
        :param start_rowx:
        :param end_rowx:
        :return:
        """
        sheet_name = self.active.name if sheet_name is None else sheet_name
        return self.sheet_by_name(sheet_name).col_types(colx, start_rowx, end_rowx)

    @staticmethod
    def col_name(colx):
        # 通过给定的行和列下标推算并返回列名字
        return xlrd.colname(colx)

    def cell(self, sheet_name: str = None, rowx: int = 0, colx: int = 0):
        """
       通过行和列下标获取 cell 对象
        :param sheet_name:
        :param rowx:
        :param colx:
        :return:
        """
        sheet_name = self.active.name if sheet_name is None else sheet_name
        return self.sheet_by_name(sheet_name).cell(rowx, colx)

    def cell_value(self, sheet_name: str = None, rowx: int = 0, colx: int = 0):
        """
        返回指定sheet名下的指定下标的cell的值
        :param sheet_name:
        :param rowx:
        :param colx:
        :return:
        """
        return self.sheet_by_name(sheet_name).cell_value(rowx, colx)

    @staticmethod
    def cell_name(rowx, colx):
        """
        通过给定的行和列下标推算并返回单元格名字
        :param rowx:
        :param colx:
        :return:
        """
        return xlrd.cellname(rowx, colx)

    @staticmethod
    def load_workbook(file, *args, **kwargs):
        """
        打开excel 返回实例
        :param file:
        :param args:
        :param kwargs:
        :return:
        """
        return xls(file, *args, **kwargs)



