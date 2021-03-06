# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei_new.items import YicheKoubeiItem
# from scrapy.conf import settings
import pymongo
from pprint import pprint

website ='autohome_koubei_new'


class AutohomeKoubeiNewSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['autohome.com']
    # start_urls = ['https://www.autohome.com.cn/beijing/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeKoubeiNewSpider, self).__init__(**kwargs)
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'public_opinion',
        'MYSQL_TABLE': 'autohome_koubei_new',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'public_opinion',
        'MONGODB_COLLECTION': 'autohome_koubei_new',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = "https://www.autohome.com.cn/beijing/"
        yield scrapy.Request(
            url=url,
        )

    def parse(self, response):
        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar_zhu"]
        result = collection.distinct("autohomeid")
        # result = collection.distinct("familyname")
        # pprint(result)
        for r in result:
            url = f"https://dealer.autohome.com.cn/Ajax/GetPraise?specId={r}&pageIndex=1&pageSize=1"
            # print(url)
            yield scrapy.Request(url, meta={"autohomeid": r}, callback=self.parse_paging)

    def parse_paging(self, response):
        paging_obj = json.loads(response.text)
        if "paging" in paging_obj["result"]:
            paging = paging_obj["result"]["paging"]
            totalCount = paging["totalCount"]

            if totalCount > 0:
                for i in range(1, totalCount+1):
                    url = "https://dealer.autohome.com.cn/Ajax/GetPraise?specId=%s&pageIndex=%d&pageSize=1" % (response.meta["autohomeid"], i)
                    yield scrapy.Request(url, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        info_obj = json.loads(response.text)
        item = YicheKoubeiItem()

        item['url'] = response.url
        # item['website'] = website
        # item['status'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())

        item['familyname'] = info_obj["result"]["seriesName"]
        # item['brand'] = None
        item['familynameid'] = info_obj["result"]["seriesId"]
        item['shortdesc'] = info_obj["result"]["specName"]

        item['buy_date'] = info_obj["result"]["koubei"][0]["purchasing"]["boughtDate"]
        item['buy_location'] = info_obj["result"]["koubei"][0]["purchasing"]["boughtProvinceName"] + " " + info_obj["result"]["koubei"][0]["purchasing"]["boughtCityName"]
        item['buy_pure_price'] = info_obj["result"]["koubei"][0]["purchasing"]["price"]
        item['buyerid'] = info_obj["result"]["koubei"][0]["author"]["userId"]
        item['buyername'] = info_obj["result"]["koubei"][0]["author"]["nickName"]

        item['mileage'] = info_obj["result"]["koubei"][0]["evaluation"]["drivenKiloms"]
        item['oil_consume'] = info_obj["result"]["koubei"][0]["evaluation"]["actualOilConsumption"]

        item['score'] = info_obj["result"]["koubei"][0]["evaluation"]["average"]
        item['score_appearance'] = info_obj["result"]["koubei"][0]["evaluation"]["apperance"]
        item['score_comfort'] = info_obj["result"]["koubei"][0]["evaluation"]["comfortableness"]
        item['score_control'] = info_obj["result"]["koubei"][0]["evaluation"]["maneuverability"]
        item['score_cost'] = info_obj["result"]["koubei"][0]["evaluation"]["costEfficient"]
        item['score_fuel'] = info_obj["result"]["koubei"][0]["evaluation"]["oilConsumption"]
        item['score_power'] = info_obj["result"]["koubei"][0]["evaluation"]["power"]
        item['score_space'] = info_obj["result"]["koubei"][0]["evaluation"]["space"]
        item['score_trim'] = info_obj["result"]["koubei"][0]["evaluation"]["internal"]

        # item['ucid'] = None
        item['guideprice'] = None
        usage = []
        for i in range(len(info_obj["result"]["koubei"][0]["evaluation"]["purposes"])):
            usage.append(info_obj["result"]["koubei"][0]["evaluation"]["purposes"][i]["name"])
        item['usage'] = "|".join(usage)
        item['fuel'] = None
        item['comment_detail'] = None
        item['comment_people'] = None
        item['isGoodComment'] = None
        item['picurl'] = None
        item['score_star'] = None

        item['visitCount'] = info_obj["result"]["koubei"][0]["interactivation"]["visitCount"]
        item['helpfulCount'] = info_obj["result"]["koubei"][0]["interactivation"]["helpfulCount"]
        item['commentCount'] = info_obj["result"]["koubei"][0]["interactivation"]["commentCount"]
        item['post_time'] = info_obj["result"]["koubei"][0]["created"]
        item['spec_id'] = info_obj["result"]["specId"]
        item['description'] = None

        feeling = info_obj["result"]["koubei"][0]["evaluation"]["feeling"]
        satisfied = re.findall("????????????????????????(.*?)???", feeling, re.S)
        if satisfied:
            item['satisfied'] = re.findall("????????????????????????(.*?)???", feeling, re.S)[0].strip()
        unsatisfied = re.findall("???????????????????????????(.*?)???", feeling, re.S)
        if unsatisfied:
            item['unsatisfied'] = re.findall("???????????????????????????(.*?)???", feeling, re.S)[0].strip()
        score_appearance_compare = re.findall("????????????(.*?)???", feeling, re.S)
        if score_appearance_compare:
            item['score_appearance_compare'] = re.findall("????????????(.*?)???", feeling, re.S)[0].strip()
        score_comfort_compare = re.findall("???????????????(.*?)???", feeling, re.S)
        if score_comfort_compare:
            item['score_comfort_compare'] = re.findall("???????????????(.*?)???", feeling, re.S)[0].strip()
        score_control_compare = re.findall("????????????(.*?)???", feeling, re.S)
        if score_control_compare:
            item['score_control_compare'] = re.findall("????????????(.*?)???", feeling, re.S)[0].strip()
        score_cost_compare = re.findall("???????????????(.*?)???", feeling, re.S)
        if score_cost_compare:
            item['score_cost_compare'] = re.findall("???????????????(.*?)???", feeling, re.S)[0].strip()
        score_fuel_compare = re.findall("????????????(.*?)???", feeling, re.S)
        if score_fuel_compare:
            item['score_fuel_compare'] = re.findall("????????????(.*?)???", feeling, re.S)[0].strip()
        score_power_compare = re.findall("????????????(.*?)???", feeling, re.S)
        if score_power_compare:
            item['score_power_compare'] = re.findall("????????????(.*?)???", feeling, re.S)[0].strip()
        score_space_compare = re.findall("????????????(.*?)???", feeling, re.S)
        if score_space_compare:
            item['score_space_compare'] = re.findall("????????????(.*?)???", feeling, re.S)[0].strip()
        score_trim_compare = re.findall("????????????(.*?)???", feeling, re.S)
        if score_trim_compare:
            item['score_trim_compare'] = re.findall("????????????(.*?)???", feeling, re.S)[0].strip()
        item['status'] = str(item['spec_id']) + "-" + str(item['buyerid']) + "-" + str(item['buy_location']) + "-" + str(item['buy_date']) + "-" + str(item['buy_pure_price']) + "-" + str(item['visitCount']) + "-" + str(item['helpfulCount']) + "-" + str(item['commentCount'])
        yield item
        # print(item)