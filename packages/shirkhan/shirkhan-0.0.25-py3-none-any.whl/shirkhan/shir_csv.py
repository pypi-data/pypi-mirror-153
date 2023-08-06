import csv

'''
我常用的csv 相关操作都放在这里
'''


def load(file: str):
    """
    加载指定的csv文件
    :param file:
    :return: 返回[header,rows] 两个字段
    """
    with open(file) as f:
        reader = list(csv.reader(f))
        header = reader[0]
        rows = reader[1:]
    return [header, rows]


def read(*args, **kwargs):
    """
    加载指定的csv文件
    :param file:
    :return: 返回[header,rows] 两个字段
    """
    return load(*args, **kwargs)


def write(file: str, header: list, rows: list):
    """
    按照给定的header写入rows到文件
    :param file: 文件
    :param header: 标题列
    :param rows: 数据行列表
    :return:
    """
    with open(file, mode='wt') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
