#-*- coding: UTF-8 -*-
import scrapy
from ..items import che300_price
import time
from hashlib import md5
from SpiderInit import spider_original_Init
from SpiderInit import spider_new_Init
from SpiderInit import spider_update_Init
from SpiderInit import dfcheck
from SpiderInit import dffile
from Car_spider_update import update
import csv
import datetime
import json
from scrapy.conf import settings
update_code = settings["UPDATE_CODE"]
website ='che300_futureprice_update_20190815'
spidername_new = 'che300_futureprice_new'
spidername_update = 'che300_futureprice_update_old'

#main
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["che300.com"]
    def __init__(self,part=0, parts=1,*args,**kwargs):
        # args
        super(CarSpider, self).__init__(*args, **kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 20000000
        self.dbname = 'usedcar_evaluation'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'
        self.part=int(part)
        self.parts=int(parts)

    #pro_city select
    #brandselect
    def start_requests(self):
        #this month
        thismonth =datetime.date.today().month
        #modellist
        with open('blm/'+self.dbname+'/modellist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            modellist = [row for row in reader]
        #citylist
        with open('blm/'+self.dbname+'/citylist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            citylist = [row for row in reader]
        step=len(modellist)/self.parts+1
        starti = self.part * step
        if self.part==self.parts-1:
            step = len(modellist) - starti
        #urllist
        for city in citylist[2:3]:
            for model in modellist[starti:(starti+step)]:
                for year in range(int(model['min_reg_year']),int(model['max_reg_year'])+1):
                    if year == 2018:
                        for month in range(1, datetime.datetime.now().month+1):
                            date = str(year)+'-'+str(month)
                            mile = 0.2
                            url = "https://dingjia.che300.com/app/EvalResult/getResidualAnalysis?prov="\
                                  + str(city['provid']) +"&city="+ str(city['cityid']) +"&series="+ str(model['familyid']) +"&model="+ \
                                  str(model['salesdescid']) +"&regDate="+ date  +"&mile="+str(mile)
                            if not (dfcheck(self.df, url, self.tag)):
                                meta =dict()
                                meta['provid']= city['provid']
                                meta['cityid']= city['cityid']
                                meta['salesdescid']= model['salesdescid']
                                meta['regDate']= date
                                meta['mile']= str(mile)
                                yield  scrapy.Request(url=url, meta={"datainfo":meta},callback=self.parse)
                    else:
                        for month in range(1, 13):
                            date = str(year)+'-'+str(month)
                            mile = 0.2
                            url = "https://dingjia.che300.com/app/EvalResult/getResidualAnalysis?prov="\
                                  + str(city['provid']) +"&city="+ str(city['cityid']) +"&series="+ str(model['familyid']) +"&model="+ \
                                  str(model['salesdescid']) +"&regDate="+ date  +"&mile="+str(mile)
                            if not (dfcheck(self.df, url, self.tag)):
                                meta =dict()
                                meta['provid']= city['provid']
                                meta['cityid']= city['cityid']
                                meta['salesdescid']= model['salesdescid']
                                meta['regDate']= date
                                meta['mile']= str(mile)
                                yield  scrapy.Request(url=url, meta={"datainfo":meta},callback=self.parse)



    def parse(self, response):
        item = che300_price()
        item = dict(item ,**response.meta['datainfo'])
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        item['status'] = md5(response.url + "-" + update_code).hexdigest()
        if response.xpath('//p/text()').re('\{\"success.*\}\]\}'):
            # dffile
            dffile(self.fa, response.url, self.tag)
            data = json.loads(response.xpath('//p/text()').extract_first())['success']
            for dataitem in data:
                year = dataitem['year']
                price = dataitem['price']
                cols='year_'+str(year)
                item[cols] = price
        yield item


# new
class CarSpider_new(CarSpider):

    # basesetting
    name = spidername_new

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # args
        super(CarSpider_new, self).__init__(**kwargs)
        # tag
        self.tag = 'new'
        # spider setting
        self.df = spider_new_Init(
            spidername=spidername_new,
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
        self.fa = open(filename, "a")
        self.part = int(part)
        self.parts = int(parts)

#update
class CarSpider_update(CarSpider,update):

    #basesetting
    name = spidername_update

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # load
        super(CarSpider_update, self).__init__(**kwargs)
        #settings
        self.urllist = spider_update_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum
        )
        self.carnum = len(self.urllist)
        self.tag='update'
        self.part = int(part)
        self.parts = int(parts)
        #do
        super(update, self).start_requests()
