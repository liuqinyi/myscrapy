# -*- coding: utf-8 -*-
import re

import scrapy
import pandas as pd


class ClueSpider(scrapy.Spider):
    name = 'clue'
    allowed_domains = ['clue.io', 's3.amazonaws.com']
    start_urls = [
        'https://api.clue.io/api/s3_resources/signFolder?s3_folder=//s3.amazonaws.com/macchiato.clue.io/builds/touchstone/v1.1/arfs/BRD-K38615104/&user_key=b8c8acd1d1a6ec79aa09703c7e07dfd9']
    user_key = '93d391356bffb624f1307253340f4836'

    api_url = 'https://s3.amazonaws.com/macchiato.clue.io/builds/touchstone/v1.1/arfs/BRD-K38615104/pcl_cell.gct"'
    save_dir = 'datasets/clue/'

    def start_requests(self):
        user_key = 'b8c8acd1d1a6ec79aa09703c7e07dfd9'
        api_url = 'https://api.clue.io/api/s3_resources/signFolder?s3_folder=//s3.amazonaws.com/macchiato.clue.io/builds/touchstone/v1.1/arfs/'

        perts = pd.read_csv(self.save_dir + '/index.csv', sep='\t', header=0, encoding='utf-8')
        perts = perts['query_id']
        print('total pert id:', len(perts))
        # perts = ['BRD-K38615104', 'CCSBBROAD304_05749']
        for pert_id in perts:
            url = '{api_url}{pert_id}/&user_key={user_key}'.format(api_url=api_url, pert_id=pert_id, user_key=user_key)
            # 上传cookie以后，已经登录，但是clue.io 部分由动态页面生成
            yield scrapy.Request(url=url,
                                 callback=self.parse)

    def parse(self, response):
        body = response.text
        raw_urls = body.strip('[').strip(']').replace('"', '').split(',')
        with open(self.save_dir + 'pert_urls.txt', 'a+', encoding='utf-8') as f:
            for url in raw_urls[:-1]:
                raw_url = re.compile('\?.*').sub('', url)
                f.write(raw_url + '\n')


