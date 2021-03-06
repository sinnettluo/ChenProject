# -*- coding: utf-8 -*-
import scrapy
from lxml import etree

import time
import json
from copy import deepcopy
import re
import demjson
from baogang.items import YicheKoubeiItem


class YicheKoubeiNewSpider(scrapy.Spider):
    name = 'yiche_koubei_new'
    allowed_domains = ['car.bitauto.com']
    # start_urls = ['http://car.bitauto.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(YicheKoubeiNewSpider, self).__init__(**kwargs)
        self.counts = 0
        self.is_not_null = True

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '180.167.80.118',
        'MYSQL_DB': 'baogang',
        'MYSQL_PORT': 2502,
        'MYSQL_PWD': 'Baogang@2019',
        'MYSQL_TABLE': 'yiche_koubei_new',
        # 'MONGODB_SERVER': '',
        # 'MONGODB_DB': '',
        'MONGODB_COLLECTION': 'yiche_koubei_new',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        url = 'http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&rt=master'
        yield scrapy.Request(
            url=url,
            dont_filter=True,
        )

    def parse(self, response):
        item = YicheKoubeiItem()
        data = demjson.decode(response.text)
        for i in data['DataList']:
            item["brand"] = i['name']
            series_id = i['id']
            series_url = f'http://api.car.bitauto.com/CarInfo/masterbrandtoserialforsug.ashx?type=7&rt=serial&pid={series_id}'
            yield scrapy.Request(
                url=series_url,
                callback=self.parse_series_list,
                meta={"item": deepcopy(item)},
                dont_filter=True
            )

    def parse_series_list(self, response):
        print(response.url)
        item = response.meta["item"]
        data = demjson.decode(response.text)
        for i in data:
            for c in i["child"]:
                serise_id = c["id"]
                item['familyname'] = c["name"]
                item["usage"] = c["urlSpell"]
                # item["serise_id"] = c["id"]
                for page in range(1, 200):
                    pageSize = 100
                    comment_list_url = f'http://dianping.bitauto.com/web_app/api/v1/review/get_review_list?param=%7B%22cTagId%22%3A%22%22%2C%22tagId%22%3A%22-10%22%2C%22currentPage%22%3A{page}%2C%22serialId%22%3A%22{serise_id}%22%2C%22pageSize%22%3A{pageSize}%7D'
                    if self.is_not_null:
                        yield scrapy.Request(
                            url=comment_list_url,
                            # callback=self.parse_comment_list,
                            callback=self.parse_comment_next_page,
                            meta={"item": deepcopy(item), "serise_id": serise_id},
                            dont_filter=True
                        )
                    else:
                        self.is_not_null = True

    def parse_comment_next_page(self, response):
        item = response.meta["item"]
        d = demjson.decode(response.text)
        if d["status"] == '1' and len(d["data"]) != 1:
            data = d["data"]["list"]
            for i in data:
                tiezi_id = i["id"]
                # item["buyerid"] = i["userId"]
                item["buy_date"] = i["purchaseDate"]
                item["buy_pure_price"] = i["purchasePrice"]
                item["familynameid"] = i["serialId"]
                item["total_score"] = float(i["rating"]) / 2
                item["helpfulCount"] = i["postCount"]
                item["shortdesc"] = i["carName"]
                # item["comment_detail"] = i["content"].replace("\r", "").replace("\n", "")
                if i["user"]:
                    item["buyername"] = i["user"]["showname"]
                if i["fuelValue"]:
                    item["oil_consume"] = i["fuelValue"] + "L/100km"
                else:
                    item["oil_consume"] = '-'
                create_time = i["createTime"]
                detail_url = f"http://dianping.bitauto.com/{item['usage']}/koubei/{tiezi_id}"
                item["url"] = detail_url
                item["create_time"] = create_time
                if create_time > '2019-01-01':
                    # print(create_time)
                    yield scrapy.Request(
                        url=item["url"],
                        callback=self.parse_detail_page,
                        meta={"item": deepcopy(item)},
                        dont_filter=True
                    )
        else:
            self.is_not_null = False

    def parse_detail_page(self, response):
        font_dic = self.settings.get("FONT_DIC")
        item = response.meta["item"]
        response_ = response.text
        # print(font_dic)
        # ????????????
        for k, v in font_dic.items():
            # key_ = k.replace(';', '')
            if k in response_:
                response_ = response_.replace(k, str(v))
        html = etree.HTML(response_)
        content_list = html.xpath("//div[@class='tcid-info']//text()")
        content = ""
        for i in content_list:
            if '\r' in i:
                i = i.replace("\r", "")
            i = i.replace(" ", "").replace("\n", "")
            content += i
        # content = "".join(content_list)
        # print(content_list)
        # print(content)
        xjb = re.findall("#?????????(.*?)#", content)
        zmy = re.findall("#?????????(.*?)#", content)
        my = re.findall("#??????(.*?)#", content)
        zbmy = re.findall("#????????????(.*?)#", content)
        bmy = re.findall("#?????????(.*?)#", content)
        kj = re.findall("#??????(.*?)#", content)
        wg = re.findall("#??????(.*?)#", content)
        ns = re.findall("#??????(.*?)#", content)
        dl = re.findall("#??????(.*?)#", content)
        ck = re.findall("#??????(.*?)#", content)
        yh = re.findall("#??????(.*?)#", content)
        ss = re.findall("#?????????(.*?)#", content)

        if xjb:
            item["bitauto_car_score"] = xjb[0]
            html.xpath("//div[@class='tcid-info']//text()")
        if zmy:
            item["satisfied"] = zmy[0]
        if my:
            item["satisfied"] = my[0]
        if zbmy:
            item["unsatisfied"] = zbmy[0]
        if bmy:
            item["unsatisfied"] = bmy[0]
        if kj:
            item["score_space_compare"] = kj[0]
            kj_star = html.xpath('//div[contains(text(),"??????")]//div[@class="start-icon active"]')
            item["space"] = len(kj_star) if len(kj_star) != 0 else None
        if wg:
            item["score_appearance_compare"] = wg[0]
            wg_star = html.xpath('//div[contains(text(),"??????")]//div[@class="start-icon active"]')
            item["appearance"] = len(wg_star) if len(wg_star) != 0 else None
        if ns:
            item["score_trim_compare"] = ns[0]
            ns_star = html.xpath('//div[contains(text(),"??????")]//div[@class="start-icon active"]')
            item["interior_trim"] = len(ns_star) if len(ns_star) != 0 else None
        if dl:
            item["score_power_compare"] = dl[0]
            dl_star = html.xpath('//div[contains(text(),"??????")]//div[@class="start-icon active"]')
            item["power"] = len(dl_star) if len(dl_star) != 0 else None
        if ck:
            item["score_control_compare"] = ck[0]
            ck_star = html.xpath('//div[contains(text(),"??????")]//div[@class="start-icon active"]')
            item["manipulation"] = len(ck_star) if len(ck_star) != 0 else None
        if yh:
            item["score_fuel_compare"] = yh[0]
            yh_star = html.xpath('//div[contains(text(),"??????")]//div[@class="start-icon active"]')
            item["fuel_consumption"] = len(yh_star) if len(yh_star) != 0 else None
        if ss:
            item["score_comfort_compare"] = ss[0]
            ss_star = html.xpath('//div[contains(text(),"?????????")]//div[@class="start-icon active"]')
            item["comfortability"] = len(ss_star) if len(ss_star) != 0 else None
        item["comment_detail"] = content.replace("\n", "")
        item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        buy_location = html.xpath("//div[@class='fd-bot']/div[@class='fd-txt']/text()")
        if len(buy_location) == 2:
            item["buy_location"] = buy_location[0]
        elif len(buy_location) == 1 and 'km' not in buy_location:
            item["buy_location"] = buy_location[0]
        else:
            item["buy_location"] = None
        # print(item)
        yield item

