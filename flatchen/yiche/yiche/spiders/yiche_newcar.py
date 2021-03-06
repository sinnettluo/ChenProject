# -*- coding: utf-8 -*-
import re
import scrapy
import time
from scrapy.utils.project import get_project_settings
from scrapy.mail import MailSender
import logging
import json

website = 'yiche_newcar'


class CarSpider(scrapy.Spider):
    name = website
    start_urls = ['http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        settings = get_project_settings()
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.carnum = 1000000
        self.counts = 0

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'yiche',
        'MONGODB_COLLECTION': 'yiche_newcar',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    # def start_requests(self):
    #     cars=[]
    #     for i in range(1,self.carnum):
    #         print(i)
    #         url="http://car.bitauto.com/xinyatu/m"+str(i)+"/"
    #         car=scrapy.Request(url,callback=self.parse)
    #         cars.append(car)
    #     return cars

    def parse(self, response):
        tree_list = json.loads(
            response.text.replace("JsonpCallBack(", "").replace("}]}})", "}]}}").replace("{", "{\"").replace(":",
                                                                                                             "\":").replace(
                ",", ",\"").replace("\"\"", "\"").replace(",\"{", ",{").replace("https\"", "https"))

        for c in tree_list["char"]:
            if tree_list["char"][c] == 1:
                for f in tree_list["brand"][c]:
                    brandname = f["name"]
                    brandid = f["id"]
                    meta = {
                        "brandname": brandname,
                        "brandid": brandid
                    }
                    url = "http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=%d" % brandid
                    yield scrapy.Request(url=url, meta=meta, callback=self.parse_family)
                    break
            break

    def parse_family(self, response):
        # print(response.text)
        result = (
            response.text.replace('AI:', 'AI-').replace("JsonpCallBack(", "").replace("}]}})", "}]}}").replace(':',
                                                                                                               '":"').replace(
                '{', '{"').replace(',', '","').replace('http":"', '').replace('https":"', '').replace('}"',
                                                                                                      '"}').replace(
                '"{',
                '{').replace(
                '"[', '[').replace(']"', ']').replace('""', '"').replace('}]', '"}]').replace(']"', ']')

        )
        result = re.sub(r'//(.*?).png', '', result)
        tree_list = json.loads(result)
        for c in tree_list["char"]:
            # print(c, tree_list['char'])
            # print(tree_list['char'][c])
            if tree_list["char"][c] == '1':
                for f in tree_list["brand"][c]:
                    if f["id"] == str(response.meta["brandid"]):
                        factoryname = f["name"]
                        print('         ', factoryname, f)
                        for factory in f["child"]:
                            if "child" in factory:
                                factoryname = factory["name"]
                                for fam in factory["child"]:
                                    print(fam, '      ??????fam')
                                    familyname = fam["name"]
                                    meta = {
                                        "factoryname": factoryname,
                                        "familyname": familyname,
                                    }
                                    url = "http://car.bitauto.com%s" % fam["url"]
                                    yield scrapy.Request(url=url, meta=dict(meta, **response.meta),
                                                         callback=self.parse_model)
                            else:
                                familyname = factory["name"]
                                meta = {
                                    "factoryname": factoryname,
                                    "familyname": familyname,
                                }
                                url = "http://car.bitauto.com%s" % factory["url"]
                                yield scrapy.Request(url=url, meta=dict(meta, **response.meta),
                                                     callback=self.parse_model)
                        break

    def get_value(self, td, item, name):
        if td.xpath('following-sibling::td[1]/span/text()'):
            item[name] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
        else:
            temp = []
            divs = td.xpath('following-sibling::td[1]/div/div')
            for div in divs:
                option = div.xpath("div/text()[1]").extract_first().strip()
                temp.append(option)
            item[name] = "|".join(temp)
            return

    def parse_model(self, response):
        model_list = response.xpath("//*[contains(@id, 'car_filter_id')]")
        for model in model_list:
            modelid = model.xpath("td[1]/@id").re("\d+")[0]
            meta = {
                "modelid": modelid
            }
            url = response.urljoin(model.xpath("td[1]/a[1]/@href").extract_first())
            yield scrapy.Request(url=url, meta=dict(meta, **response.meta), callback=self.parse_details)

        stop = response.xpath("//*[@id='pop_nosalelist']")
        if stop:
            print("??????&&&&&&&&&&&&&&&&&&&&&&&")
            for a in stop.xpath("a"):
                url = response.urljoin(a.xpath("@href").extract_first())
                print(url)
                yield scrapy.Request(url=url, meta=response.meta, callback=self.parse_model)

    def parse_details(self, response):
        self.counts += 1
        logging.log(msg="down               " + str(self.counts) + "           items", level=logging.INFO)
        # item = YicheItem()
        item = {}
        item['url'] = response.url
        item["chexing_id"] = re.findall(r"http://car.bitauto.com/(.*?)/m(\d*?)/", item["url"])[0][1]
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url + "-" + time.strftime('%Y-%m', time.localtime())
        # item['datasave'] = response.xpath('//html').extract_first()
        item['brandname'] = response.meta["brandname"]
        item['brandid'] = response.meta["brandid"]
        item['familyname'] = response.meta["familyname"]
        item['familyid'] = response.xpath('//input[@id="hidSerialID"]/@value').extract_first()

        # item['familyid'] = response.xpath('//div[@class="crumbs-txst() \t"]/a[5]/@href').extract_fir
        #     if response.xpath('//div[@class="crumbs-txt"]/a[5]/@href').extract_first() else "-"
        item['factoryname'] = response.meta["factoryname"]
        item['salesdesc'] = response.xpath('//div[@class="crumbs-txt"]/strong/text()').extract_first() \
            if response.xpath('//div[@class="crumbs-txt"]/strong/text()').extract_first() else "-"
        item['makeyear'] = response.xpath('//div[@class="crumbs-txt"]/strong/text()').re(u"(\d{4})???")[0] \
            if response.xpath('//div[@class="crumbs-txt"]/strong/text()').extract_first() else "-"

        tds = response.xpath('//*[contains(@class, "config-section")]/div[3]/table/tbody/tr/td')
        print(tds)
        for td in tds:
            if td.xpath('span/text()').extract_first() == u"??????????????????":
                item['guideprice'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip().replace(
                    u"???", "")
            if td.xpath('span/text()').extract_first() == u"???????????????":
                item['shangjiabaojia'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"??????????????????":
                item['beijing_price'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"???????????????":
                item['market_time'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"???????????????":
                item['level'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"???????????????":
                item['body'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"???????????????":
                item['power_type'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"????????????":
                item['engine'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"????????????/???????????????	":
                item['maximum_power_torque'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"??????????????????":
                item['gear_type'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"0-100km/h???????????????":
                item['acceleration_time'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"?????????????????????":
                item['hybrid_oil_comsuption'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"???????????????":
                item['max_speed'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"???????????????":
                item['environmental_standard'] = td.xpath(
                    'following-sibling::td[1]/span/text()').extract_first().strip()
                # item['color'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()
            if td.xpath('span/text()').extract_first() == u"???????????????":
                item['warranty_policy'] = td.xpath('following-sibling::td[1]/span/text()').extract_first().strip()

        try:
            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[2]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"??????":
                    self.get_value(td, item, "length")
                if td.xpath('span/text()').extract_first() == u"??????":
                    self.get_value(td, item, "width")
                if td.xpath('span/text()').extract_first() == u"??????":
                    self.get_value(td, item, "height")
                if td.xpath('span/text()').extract_first() == u"?????????":
                    self.get_value(td, item, "wheelbase")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "curb_weight")
                if td.xpath('span/text()').extract_first() == u"????????????":
                    self.get_value(td, item, "seats_num")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "luggage_compartment_volume")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "tank_volume")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "front_tire_specification")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "rear_tire_specification")
                if td.xpath('span/text()').extract_first() == u"?????????":
                    self.get_value(td, item, "spare_tire")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[4]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"????????????":
                    self.get_value(td, item, "displacement")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "maximum_power")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "maximum_horsepower")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "maximum_power_speed")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "maximum_torque")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "maximum_torque_speed")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "gangtixingshi")
                if td.xpath('span/text()').extract_first() == u"????????????":
                    self.get_value(td, item, "qigangshu")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "jinqifangshi")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "oil_supply_mode")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "fuel_labeling")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "engine_start_stop")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "gear_type2")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "gears_number")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[6]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "driving_mode")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "rear_suspension_type")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "adjustable_suspension")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "front_wheel_brake_type")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "rear_wheel_brake_type")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "parking_brake_type")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "body_structure")
                if td.xpath('span/text()').extract_first() == u"???????????????/????????????":
                    self.get_value(td, item, "differential_gear")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "front_suspension_type")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[8]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"???????????????(ABS)???":
                    self.get_value(td, item, "abs")
                if td.xpath('span/text()').extract_first() == u"???????????????(EBD/CBC???)???":
                    self.get_value(td, item, "braking_force_distribution")
                if td.xpath('span/text()').extract_first() == u"????????????(BA/EBA???)???":
                    self.get_value(td, item, "brake_assistant")
                if td.xpath('span/text()').extract_first() == u"???????????????(ARS/TCS???)???":
                    self.get_value(td, item, "traction_control")
                if td.xpath('span/text()').extract_first() == u"??????????????????(ESP/DSC???)???":
                    self.get_value(td, item, "vehicle_body_stability_control")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "main_driving_safety_airbag")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "auxiliary_driving_safety_airbag")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "front_air_bag")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "rear_air_bag")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "side_safety_air_curtain")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "knee_airbag")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "tire_pressure_monitoring")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "run_flats")
                if td.xpath('span/text()').extract_first() == u"???????????????????????????":
                    self.get_value(td, item, "rear_child_seat_interface")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "seat_belt_airbag")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "rear_central_airbag")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[10]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "cruise_control")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "lane_keeping")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "parallel_auxiliary")
                if td.xpath('span/text()').extract_first() == u"????????????/???????????????":
                    self.get_value(td, item, "collision_alarm")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "fatigue_reminding")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "zidongboche")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "remote_parking")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "automatic_driving_assistance")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "zidongzhuche")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "shangpofuzhu")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "doupohuanjiang")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "yeshixitong")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "kebianchibizhuanxiang")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "qiandaocheleida")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "houdaocheleida")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "daocheyingxiang")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "jiashimoshixuanze")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[12]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"????????????":
                    self.get_value(td, item, "qiandadeng")
                if td.xpath('span/text()').extract_first() == u"LED??????????????????":
                    self.get_value(td, item, "ledrijianxingchedeng")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "zidongdadeng")
                if td.xpath('span/text()').extract_first() == u"????????????":
                    self.get_value(td, item, "qianwudeng")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "dadenggongneng")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "tianchuangleixing")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "qiandiandongchechuang")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "houdiandongchechuang")
                if td.xpath('span/text()').extract_first() == u"???????????????????????????":
                    self.get_value(td, item, "waihoushijingdiandongtiaojie")
                if td.xpath('span/text()').extract_first() == u"??????????????????????????????":
                    self.get_value(td, item, "neihoushijingzidongfangxuanmu")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "liumeitihoushijing")
                if td.xpath('span/text()').extract_first() == u"??????????????????????????????":
                    self.get_value(td, item, "waihoushijingzidongfangxuanmu")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "yinsiboli")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "houpaicezheyanglian")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "houzheyanglian")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "qianyushuaqi")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "houyushuaqi")
                if td.xpath('span/text()').extract_first() == u"????????????":
                    self.get_value(td, item, "dianximen")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "diandongcehuamen")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "diandongxinglixiang")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "chedingxinglijia")
                if td.xpath('span/text()').extract_first() == u"????????????":
                    self.get_value(td, item, "zhongkongsuo")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "zhinengyaoshi")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "yuanchengyaokonggongneng")
                if td.xpath('span/text()').extract_first() == u"??????/????????????":
                    self.get_value(td, item, "weiyi_raoliuban")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "yundongwaiguantaojian")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[14]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "neishicailiao")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "cheneifenweideng")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "zheyangbanhuazhuangjing")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "fangxiangpancaizhi")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "duogongnengfangxiangpan")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "fangxiangpantiaojie")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "fangxiangpanjiare")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "fangxiangpanhuandang")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "qianpaikongtiao")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "houpaikongtiao")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "xiangfenxitong")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "kongqijinghua")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "chezaibingxiang")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "zhudongjiangzao")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[16]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "zuoyicaizhi")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "yundongfenggezuoyi")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "zhuzuoyidiandongtiaojie")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "fuzuoyidiandongtiaojie")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "zhuzuoyitiaojiefangshi")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "fuzuoyitiaojiefangshi")
                if td.xpath('span/text()').extract_first() == u"??????????????????????????????":
                    self.get_value(td, item, "dierpaizuoyidiandongtiaojie")
                if td.xpath('span/text()').extract_first() == u"??????????????????????????????":
                    self.get_value(td, item, "dierpaizuoyitiaojiefangshi")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "qianpaizuoyigongneng")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "houpaizuoyigongneng")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "qianpaizhongyangfushou")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "houpaizhongyangfushou")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "disanpaizuoyi")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "zuoyifangdaofangshi")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "houpaibeijiang")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "houpaizhediezhuoban")

            ###################
            tds = response.xpath('//*[@class="moreinfo"]/div[18]/table/tbody/tr/td')
            for td in tds:
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "zhongkongcaiseyejingping")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "quanyejingyibiaopan")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "xingchediannaoxianshiping")
                if td.xpath('span/text()').extract_first() == u"HUD???????????????":
                    self.get_value(td, item, "hudpingshixianshi")
                if td.xpath('span/text()').extract_first() == u"GPS?????????":
                    self.get_value(td, item, "gpsdaohang")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "zhinenghuliandingwei")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "yuyinkongzhi")
                if td.xpath('span/text()').extract_first() == u"????????????(Carplay&Android)???":
                    self.get_value(td, item, "shoujihulian")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "shoujiwuxianchongdian")
                if td.xpath('span/text()').extract_first() == u"?????????????????????":
                    self.get_value(td, item, "shoushikongzhixitong")
                if td.xpath('span/text()').extract_first() == u"CD/DVD???":
                    self.get_value(td, item, "cd_dvd")
                if td.xpath('span/text()').extract_first() == u"??????/WIFI?????????":
                    self.get_value(td, item, "lanya_wifilianjie")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "waijiejiekou")
                if td.xpath('span/text()').extract_first() == u"????????????????????????":
                    self.get_value(td, item, "chezaixingchejiluyi")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "chezaidianshi")
                if td.xpath('span/text()').extract_first() == u"???????????????":
                    self.get_value(td, item, "yinxiangpinpai")
                if td.xpath('span/text()').extract_first() == u"??????????????????":
                    self.get_value(td, item, "yangshengqishuliang")
                if td.xpath('span/text()').extract_first() == u"???????????????/???????????????":
                    self.get_value(td, item, "houpaiyejingping_yulexitong")
                if td.xpath('span/text()').extract_first() == u"??????220V?????????":
                    self.get_value(td, item, "chezai220vdianyuan")
        except Exception as e:
            pass
            # with open("D:/yiche_newcar.log", "a") as f:
            #     f.write(traceback.format_exc())
            #     f.close()

        print(item)
        # yield item
