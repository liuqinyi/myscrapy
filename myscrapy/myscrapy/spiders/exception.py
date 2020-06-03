# -*- coding: utf-8 -*-
import os
import re
import pandas as pd

import scrapy


class ClueExceptionSpider(scrapy.Spider):
    name = 'clue_exception'
    allowed_domains = ['clue.io', 's3.amazonaws.com']
    start_urls = ['http://clue.io/']
    save_dir = 'datasets/clue/'

    def start_requests(self):
        with open(self.save_dir + 'clue.txt', 'r+') as f:
            urls = f.readlines()
            f.truncate(0)
            if not urls:
                print('clue 下载链接爬取结束！！！')
                return
            for url in urls:
                url = url.replace('ccsbBroad', 'CCSBBROAD')
                yield scrapy.Request(url=url.strip('\n'), callback=self.parse)
        self.start_requests()

    def parse(self, response):
        body = response.text
        raw_urls = body.strip('[').strip(']').replace('"', '').split(',')
        with open(self.save_dir + 'pert_urls.txt', 'a+', encoding='utf-8') as f:
            for url in raw_urls[:-1]:
                raw_url = re.compile('\?.*').sub('', url)
                f.write(raw_url + '\n')
