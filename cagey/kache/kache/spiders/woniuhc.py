# -*- coding: utf-8 -*-
import scrapy
import time
import json
from copy import deepcopy
from kache.items import woniuItem


class WoniuhcSpider(scrapy.Spider):
    name = 'woniuhc'
    allowed_domains = ['woniuhuoche.com']
    # start_urls = ['http://woniuhuoche.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(WoniuhcSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'truck',
        'MYSQL_TABLE': 'woniuhc',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'truck',
        'MONGODB_COLLECTION': 'woniuhc',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "http://www.woniuhuoche.com/truck-auction-app/api/auction/v1/lotList?source=2&type=0"
        yield scrapy.Request(
            url=url,
            dont_filter=True,
        )

    def parse(self, response):
        item = woniuItem()
        res = json.loads(response.text)
        data_list = res["data"]["lotList"]
        for data in data_list:
            item["title"] = data["title"]
            item["carid"] = data["lotId"]
            item["truckId"] = data["truckId"]
            item["registerdate"] = data["registDate"]
            item["price"] = data["maxPrice"]
            item["emission"] = data["emission"]
            item["startTime"] = data["startTime"]
            item["endTime"] = data["endTime"]
            url = f"http://www.woniuhuoche.com/truck-auction-app/api/auction/v1/truckDetail?lotId={item['carid']}&truckId={item['truckId']}"
            item["url"] = url
            yield scrapy.Request(
                url=url,
                callback=self.parse_detail_url,
                meta={"item": deepcopy(item)},
                dont_filter=True,
            )

    def parse_detail_url(self, response):
        item = response.meta["item"]
        res = json.loads(response.text)
        data = res["data"]
        item["city"] = data["city"]
        basicList = data["basicList"]
        for basic in basicList:
            if "??????" in basic["key"]:
                item["num"] = basic["value"]
            if "????????????" in basic["key"]:
                item["car_type"] = basic["value"]
            if "????????????" in basic["key"]:
                item["mileage"] = basic["value"]
            if "???????????????" in basic["key"]:
                item["engine"] = basic["value"]
            if "????????????" in basic["key"]:
                item["fuel"] = basic["value"]
            if "????????????" in basic["key"]:
                item["let"] = basic["value"]
            if "??????" in basic["key"]:
                item["brand"] = basic["value"]
            if "????????????" in basic["key"]:
                item["color"] = basic["value"]
            if "????????????" in basic["key"]:
                item["hoursepower"] = basic["value"]
            if "????????????" in basic["key"]:
                item["containerLong"] = basic["value"]
            if "????????????" in basic["key"]:
                item["containerHight"] = basic["value"]
            if "????????????" in basic["key"]:
                item["driveType"] = basic["value"]
            if "????????????" in basic["key"]:
                item["containerVolume"] = basic["value"]
            if "????????????" in basic["key"]:
                item["carLocation"] = basic["value"]
        proceduresList = data["proceduresList"]
        for procedures in proceduresList:
            if "???????????????" in procedures["key"]:
                item["isTransfer"] = procedures["value"]
            if "???????????????" in procedures["key"]:
                item["inspectionDate1"] = procedures["value"]
            if "????????????" in procedures["key"]:
                item["isPurchase"] = procedures["value"]
            if "?????????" in procedures["key"]:
                item["inspectionDate2"] = procedures["value"]
            if "???????????????" in procedures["key"]:
                item["inspectionDate3"] = procedures["value"]
            if "???????????????????????????" in procedures["key"]:
                item["isCertificate"] = procedures["value"]
            if "???????????????" in procedures["key"]:
                item["isRules"] = procedures["value"]
            if "???????????????" in procedures["key"]:
                item["isMortgage"] = procedures["value"]
        detect = data["detect"]
        item["grade"] = detect["grade"]
        item["surveyor"] = detect["surveyor"]
        item["detectTime"] = detect["detectTime"]
        item["detectItem"] = json.dumps(detect["detectItem"], ensure_ascii=False)
        item["desc"] = data["descp"]
        item["statusplus"] = item["url"]+'-'+item["price"]
        item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield item
        # print(item)



