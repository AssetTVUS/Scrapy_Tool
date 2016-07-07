from ReportItem import ReportItem
import scrapy
from datetime import datetime
import re
import json
import logging
from scrapy.selector import Selector


class ReportsSpider(scrapy.Spider):

    name = 'reports'    # name the spider
    allowed_domains = ['asset.tv'] # crawl these domains
    start_urls = [] # array to contain the urls to scrape

    processed_video_core_ids = dict() # keep a dictionary of processed video core ids


    # get the list of urls to scrape from ../../scrape_list.txt
    with open('../scrape_list.txt', 'r') as fp:
        for line in fp:
            start_urls.append(line)


    def parse(self,response):

        #video coreid
        scriptTag = response.xpath('//script').re(r'"videoCoreID"\:"[0-9]+\"')[0]  #get all of the script tags in an array
        temp = scriptTag.encode('utf-8')  # looks like "videoCoreID":"200470"
        temp = '{' + temp + '}'  # looks like '{"videoCoreID":"200470"}'
        dict = json.loads(temp)  # from JSON string to Python dictionary

        if dict['videoCoreID'] in self.processed_video_core_ids:
            item = None
            logging.info("***Skipping " + dict['videoCoreID'])
            return

        logging.info("Processing " + dict['videoCoreID'])

        item = ReportItem()
        item['videoCoreID'] = dict['videoCoreID']
        self.processed_video_core_ids[dict['videoCoreID']] = 0


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
        #item['tagList'] = response.css('.tag-cloud').xpath('./a/@title').extract()

        tag_type =''
        anchor_tag=''
        tagList = []  # a list of tag tuples
        for x in response.css('.tag-cloud').xpath('*').extract():

            # is this a h3 or an anchor tag
            if x.startswith('<h3>'):

                #x is a String convert it back to a Selector to use XPath to grab content of the <h3> tag
                tag_type = Selector(text=x, type='html').xpath('//h3/text()').extract()[0]
            else:
                # x is a String convert it back to a Selector to use XPath to grab content of the <a> tag
                anchor_tag = Selector(text=x, type='html').xpath('//a/@title').extract()[0]
                tagList.append((anchor_tag,tag_type))  # add this tag to our list

        item['tagList'] = tagList # pass back our list of tags <tuple objects>
        # channel name
        item['channel_name'] = response.css('.info').xpath('./a/text()').extract()[0].encode('utf-8').strip()



        yield item