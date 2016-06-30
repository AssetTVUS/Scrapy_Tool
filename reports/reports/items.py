import scrapy

class ReportItem(scrapy.Item):
    og_image = scrapy.field()
    og_title  = scrapy.field()
    og_description  = scrapy.field()
    og_updated_time =  scrapy.field()
    og_url  = scrapy.field()
    published_time  = scrapy.field()
    video_duration  = scrapy.field()
    video_title  = scrapy.field()
    channel_name  = scrapy.field()
    videoCoreID  = scrapy.field()
