# myscrapy
scrapy project for some biologic dataset

## genecard
爬取genecard数据https://www.genecards.org/
主要实现xpath技术对已经下载下来的html文件进行元素匹配抽取
主要困难：数据不规范，有的数据部分属性没有，有的数据在爬取阶段就出现错误

## myscrapy
主要使用爬虫技术对clue.io中的touch展示数据进行爬取
主要问题，需要登录
因为数据是动态的，因此爬取时需要传入userkey
首先爬取没个pert对应的5个文件地址（s3），然后根据每个地址进行文件下载
本地化后使用xxx.py将gtc文件转换为csv文件，然后再写入到mysql中
