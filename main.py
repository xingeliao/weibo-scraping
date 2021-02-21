#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
import csv
import urllib.parse
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

class WeiboScraper():

    def __init__(self):
        self.driver = None
        self.csvfile = None
        self.writer = None

    def __enter__(self):
        options = Options()
        options.headless = False
        ffprofile = webdriver.FirefoxProfile(r'C:\Users\Isa\AppData\Roaming\Mozilla\Firefox\Profiles\9020y7g4.default')
        self.driver = webdriver.Firefox(firefox_profile=ffprofile, options=options, executable_path='geckodriver.exe')
        open("output.csv", 'w').close()
        self.csvfile = open("output.csv", "a+", newline = "", encoding = "utf-8")
        columnnames = ["USER","CONTENT","DATE & TIME","COMMENTS","LIKES","LOCATION"]
        self.writer = csv.DictWriter(self.csvfile, fieldnames = columnnames)
        self.writer.writeheader()

        url = 'https://s.weibo.com/weibo?q=BCN&Refer=index'
        self.driver.get(url)
        time.sleep(20)
        return self

    def scraper(self, query_word, page, start_date, end_date):
        encoded_url = urllib.parse.quote(query_word)
        url = 'https://s.weibo.com/weibo?q=' + encoded_url + '&page=' + page + '&typeall=1&suball=1&timescope=custom:' + start_date + ':' + end_date + '&Refer=g' #will need to add date later
        self.driver.get(url)
        time.sleep(5)
        bs = BeautifulSoup(self.driver.page_source)
        list = bs.select('#pl_feed_main .card-wrap')
        for post in list:
            footer = post.select('.card-act ul li')
            comments = 0
            likes = 0
            if( len(footer) > 3 ):
                comments = footer[2].text
                likes = footer[3].text
            username = post.select('.content a.name')
            if(username):
                username = username[0].text
                content = post.select('.content p.txt')
                datetime = post.select('.content p.from a')[0].text.strip()
                z = "展开全文"
                if( (len(content) > 1) and (z in content[0].text.strip()) ):
                    fullcontent = content[1].text.strip()
                    content_code = content[1]
                else:
                    fullcontent = content[0].text.strip()
                    content_code = content[0]

                location = re.findall(r'2</i>(.*?)</a>', str(content_code), re.S)
                location = ''.join([str(a) for a in location])
                location = location.replace('<em class="s-color-red">', '')
                location = location.replace('</em>', '')

                self.writer.writerow({"USER":username,"CONTENT":fullcontent,"DATE & TIME":datetime,"COMMENTS":comments,"LIKES":likes,"LOCATION":location})

    def __exit__(self, type, value, trace):
        self.driver.close()
        self.csvfile.close()


with WeiboScraper() as scr:
    for page in range(1,7):
        scr.scraper('圣家堂', str(page), '2020-12-01', '2020-12-31')
#    for page in range(1,14):
#        scr.scraper('奎尔公园', str(page), '2020-09-01', '2020-12-31')

#    for page in range(1,14):
#        scr.scraper('古埃尔公园', str(page), '2020-05-01', '2020-08-31')
#    for page in range(1,29):
#        scr.scraper('古埃尔公园', str(page), '2018-05-01', '2018-06-30')

#    for page in range(1,20):
#        scr.scraper('奎尔公园', str(page), '2020-05-01', '2020-08-31')

#    for page in range(1,13):
#        scr.scraper('古埃尔公园', str(page), '2020-01-01', '2020-04-30')
#    for page in range(1,21):
#        scr.scraper('奎尔公园', str(page), '2020-01-01', '2020-04-30')
