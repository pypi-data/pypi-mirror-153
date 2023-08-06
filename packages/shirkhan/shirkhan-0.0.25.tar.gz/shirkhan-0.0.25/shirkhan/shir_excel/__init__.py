from shirkhan.shir_excel.xls import xls
from shirkhan.shir_excel.xlsx import xlsx

"""
excel中xls和xlsx的区别是什么?
excel中xls和xlsx的区别是：
1、xls是复合文档类型的结构，而xlsx的核心结构是XML类型的结构；
2、xls是excel2003及以前版本生成的文件格式，而xlsx是excel2007及以后版本生成的文件格式

其他区别:
1、文件格式不同。xls是一个特有的二进制格式，其核心结构是复合文档类型的结构，而xlsx的核心结构是XML类型的结构，采用的是基于 XML 的压缩方式，使其占用的空间更小。xlsx 中最后一个 x 的意义就在于此。
2、版本不同。xls是excel2003及以前版本生成的文件格式，而xlsx是excel2007及以后版本生成的文件格式。
3、兼容性不同。xlsx格式是向下兼容的，可兼容xls格式。

总结:
xlsx 是Microsoft Office EXCEL 2007/2010/2013/2016/2019文档的扩展名。
xlsx 是从Office2007开始使用的。
xlsx 是用新的基于XML的压缩文件格式取代了其目前专有的默认文件格式，在传统的文件名扩展名后面添加了字母x（即：docx取代doc、.xlsx取代xls等等），使其占用空间更小

----------------------------------------------------------------------------
excel中1个sheet页里能装下多少数据量？
Excel2003 版本的     xls 格式文件可以支持最多  65，536     行数据
Excel2007 以上版本的 xlsx 格式文件可以支持2^20 1，048，576  行数据，最大列数能达到2^14= 16，384

----------------------------------------------------------------------------
python用于读写excel文件的库有很多，除了pandas，还有xlrd、xlwt、openpyxl、xlwings等等。

主要模块：
xlrd库： 从excel中读取数据，支持xls、xlsx
xlwt库： 对excel进行修改操作，不支持对xlsx格式的修改
xlutils库： 在xlw和xlrd中，对一个已存在的文件进行修改
openpyxl： 主要针对xlsx格式的excel进行读取和编辑
xlwings： 对xlsx、xls、xlsm格式文件进行读写、格式修改等操作
xlsxwriter： 用来生成excel表格，插入数据、插入图标等表格操作，不支持读取
Microsoft Excel API： 需安装pywin32，直接与Excel进程通信，可以做任何在Excel里可以做的事情，但比较慢
"""
