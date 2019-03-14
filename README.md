# content.taggingv1
Content Tagging With NLP:: 3/2019

# Intro

This is a crawler that's designed to scrape content from the LE "Magazine" and "Protocol" sections.

# Software Needed

1. Python2.7X above
2. Pip
3. Anaconda
4. Anaconda Shell
4. Scrapy

# Steps To Run

1. Enusure that you have Anaconda in order to Q/A Scrapy, the shell enables you to see the response and test the desired Xpath.

2. Launch Whatever Shell You Desire

3. Navigate to the /leextensionext/ directory 

4. Run at terminal of your shell or Anaconda Shell "scrapy crawl magazinecontent" -o life_extension_content.csv

* -o "output" name_of_the_file must match the name of the file for the cleaning function and future functions. 

# Steps To Q/A

1. With Anaconda open up the Anaconda Shell 

2. At terminal type scrapy shell "https://lifeextension.com/Magazine/  or whatever url we're scraping, *Protocols*

3. Using the response object you can test Xpath expressions for accuracy on target data extraction.
