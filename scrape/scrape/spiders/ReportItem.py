# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReportItem(scrapy.Item):
    og_image = scrapy.Field()
    og_title  = scrapy.Field()
    #og_description  = scrapy.Field()
    og_updated_time =  scrapy.Field()
    og_url  = scrapy.Field()
    published_time  = scrapy.Field()
    video_duration  = scrapy.Field()
    video_duration_datetime = scrapy.Field()
    video_title  = scrapy.Field()
    channel_name  = scrapy.Field()
    videoCoreID  = scrapy.Field()
    tagList = scrapy.Field()




