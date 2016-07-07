# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import _mssql
import sys

from scrapy.exceptions import DropItem

class ScrapePipeline(object):
    def process_item(self, item, spider):
        return item




class DataPipline(object):




    def my_msg_handler(msgstate, severity, srvname, procname, line, msgtext):
        """
        Our custom handler -- It simpy prints a string to stdout assembled from
        the pieces of information sent by the server.
        """
        print("my_msg_handler: msgstate = %d, severity = %d, procname = '%s', "
              "line = %d, msgtext = '%s'" % (msgstate, severity, procname,
                                             line, msgtext))

    def __init__(self):
        print '****DataPipline init****'
        self.connection=""
        self.run_date = '2016-06-17 13:51:13'

    def open_spider(self, spider):
        print 'DataPipline open'
        server = "192.168.168.111"
        user = "sa"
        password = "coffee2016"
        database = "reportsdb"
        try:
            #self.connection.set_msghandler(my_msg_handler)  # Install our custom handler
            self.connection = _mssql.connect(server=server, user=user, password=password,database=database)
            print 'Opened Database'

        except:
            print "Connection Failed"
            print  sys.exc_info()[0]
            raise DropItem("Connect Error")

    def close_spider(self, spider):
        print 'DataPipline close'
        self.connection.close()

    def process_item(self, item, spider):

        if not item:   # nothing to process
            return

        if self.connection:

            try:

                insert_table = 'SCRAPED_VIDEO_DATA'
                # add to SCRAPED_VIDEO_DATA
                self.connection.execute_non_query('INSERT INTO SCRAPED_VIDEO_DATA (' + \
                                                  'channel_name,og_image,og_title,' + \
                                                  'og_url,video_core_id, video_duration,run_time'
                                                  ',published_time) values(' +
                                                  '%s,%s,%s,%s,%s,%s,%s,%s)',(item['channel_name'],\
                                                  item['og_image'],item['og_title'],item['og_url'], \
                                                  item['videoCoreID'],item['video_duration'],\
                                                  self.run_date,item['published_time']))

                #self.connection.commit()

                scrape_primary_key =  self.connection.identity #get the primary key of new row in database

                # add to SCRAPED_VIDEO_DATA_TAGS
                insert_table = 'SCRAPED_VIDEO_DATA_TAGS'
                for tag in item['tagList']:
                    # each tag is a tuple that contains 2 elements (tag_name, tag_type)
                    self.connection.execute_non_query('INSERT INTO SCRAPED_VIDEO_DATA_TAGS(' + \
                        'scrape_id ,tag_name,tag_type) values(%s,%s,%s)',(scrape_primary_key,tag[0],tag[1]))


                return item

            except:
                print '--------- Insertion Error ---------'
                print '*** ON ' + insert_table + ' ***'
                print  sys.exc_info()
                print str(item)
                print '-----------------------------------'
                raise DropItem("Insert Error")

        else:
            raise DropItem("No Database Connection")