# EE208-Stock_news_data_analysis

# 特别警告
爬取页面中有某些页面只有图片！（如某公司当季度业务报告图），这些页面只会返回标题，获取内容是空，垃圾爬虫没有过滤！
# html文件夹用于直接存储网页新闻
每个文件起始行为原网页标题。

每支股票爬取10条最新新闻，其文件命名末尾六位数字代表其股票编号。

# index.txt文件包含了html文件夹中网页源码文件与原网址的关系
格式为 ‘原网址’ + ‘，’ + ‘文件名’ 

## 注意
出于某些原因，index.txt某些行不正常（如780行），需要加异常处理


