# -*- coding: utf-8 -*-
import os
import pickle
import re
from urllib import request

import requests
from six.moves import urllib

import scrapy
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from myscrapy.settings import COOKIES


class CmapSpider(scrapy.Spider):
    name = 'cmap'
    allowed_domains = ['s3.amazonaws.com']
    start_urls = ['']
    user_key = 'b8c8acd1d1a6ec79aa09703c7e07dfd9'
    pert_down_urls = 'datasets/clue/pert_urls_test.txt'
    exception_urls = 'datasets/clue/last_exception.txt'
    output_dir = 'datasets/clue/touchstone/'

    def start_requests(self):
        with open(self.exception_urls, 'r') as f:
            for line in f.readlines():
                items = line.strip('\n').split('/')
                pert_dir = items[-2]
                pert_file = items[-1]
                if not os.path.isdir(self.output_dir+pert_dir):
                    os.makedirs(self.output_dir+pert_dir)
                if not os.path.exists(self.output_dir+pert_dir+'/'+pert_file):
                    yield scrapy.Request(url=line.strip('\n'),
                                         callback=lambda response, path=self.output_dir+pert_dir+'/'+pert_file:
                                         self.parseDown(response, path))

    def parseDown(self, response, save_path):
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

    def parseSourceURL(self, response, pert_id):
        save_dir = 'datasets/clue/touchstone/{}'.format(pert_id)
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        down_urls = response.text
        items = down_urls.strip('[').strip(']').replace('"', '').split(',')
        for item in items[:-1]:
            file_name = re.findall(r'.*\/(.*)\?', item)[0]
            raw_url = re.compile('\?.*').sub('', item)
            save_path = '{dir}/{file}'.format(dir=save_dir, file=file_name)
            if not os.path.exists(path=save_path):
                yield scrapy.Request(url=raw_url, callback=lambda response, path=save_path: self.parseDown(response, path))

    def parse(self, response):
        with open('clue_test.html', 'w') as f:
            f.write(response.text)


