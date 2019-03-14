# Natural Language Processing Using Python and NLTK
# Intall NLTK - pip install nltk
import nltk

# Utilities
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
        articles = response.xpath("//*[contains(@class, 'content')]//p").extract()
        article = ''.join(articles)

        yield {
            'article': article
            }

    # With Anaconda Shell run: scrapy crawl magazinecontent -o life_extension_content.csv 
    # This will save the csv file and then you can open it

    # Machine Learning Path Focus & NLP
    # But First we must clean out content
    def cleaning(self):    
        # Open Our Data Source, Scraped Data That Is
        with open(r'C:\Users\googl\Documents\Python Scripts\life_extension_content.csv') as f:
            data = f.read()

            # Debugging Feature
            print(data)

            for content in range(len(data)):
                data[content] = re.sub(r"\W", "",data[content])

        data.to_csv(r"C:\Users\googl\Documents\Python Scriptslife_extension_final_content.csv", index=None, header=False)

    # Start Natural Language Processing
    # Start Tokenizing Words and Sentences
    def nlp(self):
        # Open Our Data Source, Scraped Data That Is
        with open(r'C:\Users\googl\Documents\Python Scripts\life_extension_final_content.csv') as f:
            data_final = f.read()

            # Debugging Feature
            print(data_final)
        

#{('cancer', 'breas cancer', 'early diagnosis', 'estrogen risk', 'estriol'): https://www.lifeextension.com/Magazine/1996/1/96jan1/Page-01},

