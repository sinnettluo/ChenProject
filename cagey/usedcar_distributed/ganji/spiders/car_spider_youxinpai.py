#-*- coding: UTF-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from ganji.items import YouXinPai
import time
import logging

from ganji.spiders.SpiderInit import spider_original_Init

website ='youxinpai'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["youxinpai.com"]
    # start_urls=["http://i.youxinpai.com/LoginFromPCClient.aspx?key=5LFu9AuZj+n4mmgHy5M3iIGhoASQzWKX31foFC5N4y0JkTcSKy8e+2nhXxCY+Urw&Redirect=http://i.youxinpai.com/Default.aspx",]
    redis_key = 'youxinpai'

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS': 8,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/youxinpai.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting-
        self.counts = 0
        self.carnum = 150000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df='none'
        self.fa='none'

    # get brand list
    def parse(self, response):
        # print response.body
        url = "http://i.youxinpai.com/AjaxObjectPage/SellCarTypePageTrade.ashx?carAreaID=40"
        yield scrapy.Request(url, callback=self.parse_1)

    def parse_1(self, response):
        # count
        for href in response.xpath('//dd/a'):
            # print(href)
            brandid = href.xpath('@id').re('\d+')[0] if href.xpath('@id').re('\d+') else '-'
            brandname = href.xpath('text()').extract_first()
            urlbase = 'http://i.youxinpai.com/AjaxObjectPage/SellCarTypePageTrade.ashx?carProducerID=' + brandid
            metadata = {'brandid': brandid, 'brandname': brandname}
            yield scrapy.Request(url=urlbase, meta={'metadata': metadata}, callback=self.parse_series)

    # get series list
    def parse_series(self, response):
        # print('111111111111', response.url)
        # count
        for href in response.xpath('//ul/li/a'):
            familyid = href.xpath('@id').re('\d+')[0] if href.xpath('@id').re('\d+') else '-'
            familyname = href.xpath('text()').extract_first()
            metadata = response.meta['metadata']
            brandid = metadata['brandid']
            metadata = dict({'familyid': familyid, 'familyname': familyname}, **metadata)
            urlbase = 'http://i.youxinpai.com/TradeManage/TradeList.aspx?masterBrand=' + brandid + '&serial=' + familyid
            yield scrapy.Request(url=urlbase, meta={'metadata': metadata, 'tag': 'series'}, callback=self.parse_car)


    # get car info
    def parse_car(self, response):
        # print('2222222222', response.url)
        if response.xpath('//span[@class="txt01"]'):
            pass
        else:
            for href in response.xpath('//tr[@class="list-li"]'):
                status = href.xpath('td[3]/input/@requesttype')
                status = "".join(status.re('\d+')) if status else "zero"

                # count
                self.counts += 1
                logging.log(msg="download  " + str(self.counts) + "  items", level=logging.INFO)

                # base info
                datasave1 = response.meta['metadata']

                # key and status (sold or sale, price,time)
                datetime =href.xpath('td[1]/text()')
                datetime ="-".join(datetime.re('\d+')) if datetime else "zero"

                #item loader
                item = YouXinPai()
                item['url'] = response.url
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['website'] = website
                item['status'] = status
                item['pagetime'] = datetime
                item['datasave'] = [datasave1, href.extract()]

                # extra
                item['brand'] = datasave1['brandname']
                item['series'] = datasave1['familyname']

                yield item

            # next page
            next_page = response.xpath(u'//a[contains(text(),"?????????")]/@href')
            if next_page:
                url = response.urljoin(next_page.extract_first())
                yield scrapy.Request(url, self.parse_car)

            # next choose
            if response.meta['tag'] == 'series':
                for i in range(1, 34 + 1):
                    url = response.url + '&proid=' + str(i)
                    metadata = response.meta['metadata']
                    metadata = dict({'proid': str(i)}, **metadata)
                    yield scrapy.Request(url, meta={'metadata': metadata, 'tag': 'prov'},
                                         callback=self.parse_car)

            elif response.meta['tag'] == 'prov':
                for i in range(1, 50 + 1):
                    metadata = response.meta['metadata']
                    proid = metadata['proid']
                    cityid = proid + '0' + str(i) if i < 10 else proid + str(i)
                    url = response.url + '&city=' + cityid
                    metadata = dict({'city': cityid}, **metadata)
                    yield scrapy.Request(url, meta={'metadata': metadata, 'tag': 'city'},
                                         callback=self.parse_car)

            elif response.meta['tag'] == 'city':
                for i in range(1990, 2018 + 1):
                    metadata = response.meta['metadata']
                    url = response.url + '&registDate=' + str(i)
                    metadata = dict({'registDate': str(i)}, **metadata)
                    yield scrapy.Request(url, meta={'metadata': metadata, 'tag': 'year'},
                                         callback=self.parse_car)

            elif response.meta['tag'] == 'year':
                i = 0
                metadata = response.meta['metadata']
                url = response.url + '&trans=' + str(i)
                metadata = dict({'trans': str(i)}, **metadata)
                yield scrapy.Request(url, meta={'metadata': metadata, 'tag': 'trans'},
                                     callback=self.parse_car)