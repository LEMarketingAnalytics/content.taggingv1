# Natural Language Processing Using Python and NLTK
# Intall NLTK - pip install nltk
import nltk

# Utilities

try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO 

import csv
import re

# -*- coding: utf-8 -*-
import scrapy

from urllib.parse import urljoin

# Debugging, Cleaning Last Minute Data
import pandas as pd
from pandas import DataFrame

class ProtocolContent(scrapy.Spider):
    name = 'protocolcontent'
    allowed_domains = ['lifeextension.com']
    start_urls = ['https://www.lifeextension.com/Protocols/']

    # Function for parsing through the initial year list
    def parse(self, response):
        article_links = response.xpath("//*[contains(@class, 'content')]//ul//li//a//@href").extract()
        for article_link in article_links:
            url = urljoin(response.url, article_link)
            yield scrapy.Request(url, callback=self.parse_article)

    
    def parse_article(self, response):

        articles = response.xpath('//*[@id="protocol_article"]/div[2]').extract()
        for article in articles:
            article = ''.join(articles)
            article_url = response.url
            
            yield {
                'article': article,
                'article_url': article_url
            }
        
        # //*[@id="mp-pusher"]/div/div[2]/div[2]/div/section/article/div[4]/div/ul/li[11]/a
        next_page_url = response.xpath('//section//article//a[text()="Next"]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_article)