from ReportItem import ReportItem
import scrapy
from datetime import datetime
import re
import json


class ReportsSpider(scrapy.Spider):

    name = 'reports'    # name the spider
    allowed_domains = ['asset.tv'] # crawl these domains
    start_urls = [] # array to contain the urls to scrape

    # get the list of urls to scrape from ../../scrape_list.txt
    with open('../scrape_list.txt', 'r') as fp:
        for line in fp:
            start_urls.append(line)


    def parse(self,response):
        item = ReportItem()

        # get og_title and remove special chars
        item['og_title'] =  response.xpath('//meta[@property="og:title"]/@content').extract()[0].encode('utf-8')
        item['og_title'] = item['og_title'].replace("\xe2\x80\x99s", "'s")

        # get og_image and og_url
        item['og_image'] = response.xpath('//meta[@property="og:image"]/@content').extract()[0].encode('utf-8')
        item['og_url'] = response.xpath('//meta[@property="og:url"]/@content').extract()[0].encode('utf-8')

        # published_time looks like 2016-05-27T11:02:35+01:00
        temp = response.xpath('//meta[@property="article:published_time"]/@content').re (r'^[0-9]+-[0-9]+-[0-9][0-9]')
        item['published_time'] = temp[0].encode('utf-8')

        # video_duration
        temp = response.xpath('//meta[@property="video:duration"]/@content').extract()[0].encode('utf-8')
        #temp looks like this "0000-01-01 00:03:55" , a string. Get the time portion
        temp_list = temp.split()  # now in a list ['0000-01-01', '00:03:55'] , 0000 is an invalid year!
        # item['video_duration_datetime'] is now a valid datetime object 1900-01-01 00:03:55
        item['video_duration_datetime']= datetime.strptime(temp_list[1], '%H:%M:%S')
        # break datetime object apart and add it up
        item['video_duration'] = str(item['video_duration_datetime'].hour * 60 +\
                                 (item['video_duration_datetime'].minute + float(item['video_duration_datetime'].second/60.0)))

        #tags
        item['tagList'] = response.css('.tag-cloud').xpath('./a/@title').extract()

        # channel name
        item['channel_name'] = response.css('.info').xpath('./a/text()').extract()[0].encode('utf-8')

        #video coreid
        scriptTag = response.xpath('//script').re(r'"videoCoreID"\:"[0-9]+\"')[0]  #get all of the script tags in an array
        temp = scriptTag.encode('utf-8')  # looks like "videoCoreID":"200470"
        temp = '{' + temp + '}'  # looks like '{"videoCoreID":"200470"}'
        dict = json.loads(temp)  # from JSON string to Python dictionary
        item['videoCoreID'] = dict['videoCoreID']


        yield item