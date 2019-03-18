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

class MagazinecontentSpider(scrapy.Spider):
    name = 'magazinecontent'
    allowed_domains = ['lifeextension.com']
    start_urls = ['https://www.lifeextension.com/Magazine/']

    # Function for parsing through the initial year list
    def parse(self, response):

        # ('//article[@class="content"]//div[@class="mag-archive"]//ul//li//a')
        # (//article[@class="content"]//div[@class="mag-archive"]//ul//li//a//@href')
        years = response.xpath("//*[contains(@class, 'mag-archive')]//ul//li//a//@href").extract()
        for year in years:
            url = urljoin(response.url, year)
            yield scrapy.Request(url, callback=self.parse_month)

    def parse_month(self, response):
        months = response.xpath("//*[contains(@class, 'content')]//ul//li//a//@href").extract()
        #months = response.xpath("//*[contains(@class, 'mag-cover-report')]//ul//li//a//@href").extract()
        for month in months:
            url2 = urljoin(response.url, month)
            yield scrapy.Request(url2, callback=self.parse_article_links)

    def parse_article_links(self, response):
        article_links = response.xpath("//*[contains(@class, 'mag-content')]//article//a//@href").extract()
        for article_link in article_links:
            url3 = urljoin(response.url, article_link)
            yield scrapy.Request(url3, callback=self.parse_article)
    
    def parse_article(self, response):
        articles = response.xpath("//*[contains(@class, 'content')]//p").extract()[2:11]
        article = ''.join(articles)

        article_url = response.url
        #article_url = ''.join(article)

        #article_title = response.xpath("//div[contains(@class, 'mag-article')]//table//tbody//tr//td//h1").extract()
        #article_title = ''.join(article)

        #article_date = response.xpath("//div[contains(@class, 'mag-article-top')]//span").extract()
        #article_date = ''.join(article)

        # We must clean out content   

        article = re.sub(r"<.*?>", "", article)
        article = re.sub(r" +", " ", article)
        article = re.sub(r"\"", " ", article)
        article = re.sub(r",,,", ",", article)

        yield {
            'article': article,
            'article_url': article_url
            #'article_title': article_title,
            }
            
    # With Anaconda Shell run: scrapy crawl magazinecontent -o life_extension_content.csv 
    # This will save the csv file and then you can open it in the spiders folder

    # Machine Learning Path Focus & NLP