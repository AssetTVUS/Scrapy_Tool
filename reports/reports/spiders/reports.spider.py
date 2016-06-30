import scrapy
import ReportItem

class ReportsSpider(scrapy.Spider):

    name = 'reports'    # name the spider
    allowed_domains = 'asset.tv' # crawl these domains
    start_urls = ['https://www.asset.tv/video/upping-stakes-when-rules-change-halfway-through-game'
                  ]


#    def parse(selfself,response):
#        filename = response.url.split("/")[-2] + '.html'
#        with open(filename, 'wb') as f:
#           f.write(response.body)
    def parse(selfself,response):