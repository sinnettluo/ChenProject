# -*- coding: utf-8 -*-
import scrapy
from ganji.items import AutohomeItem
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from selenium import webdriver
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
from lxml import etree
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import requests

import sys
reload(sys)
sys.setdefaultencoding("UTF8")


website ='new_autohome_newcar_v3_20190821_02'

class CarSpider(scrapy.Spider):

    name = website
    allowed_domains = ["autohome.com.cn"]
    start_urls = ["https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=0%20&fctId=0%20&seriesId=0"]


    def __init__(self, **kwargs):
        # problem report
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 1010000
        # Mongo
        settings.set('DOWNLOAD_DELAY', '0', priority='cmdline')
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'newcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')
        self.nationp = dict()
        self.npcounts=0
    # nation select
    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        # proxy = webdriver.Proxy()
        # proxy.proxy_type = ProxyType.MANUAL
        # proxy.http_proxy = self.getProxy()
        # proxy.add_to_capabilities(desired_capabilities)
        # self.browser.start_session(desired_capabilities)
        # self.browser.set_page_load_timeout(12)
        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        self.browser = webdriver.PhantomJS(executable_path="/home/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")

        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)



    def getProxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        html_str = response.body.replace('document.writeln("', '').replace('");', '')
        # print(html_str.decode("gbk").strip())
        res = etree.fromstring("<root>" + html_str.decode("gbk").strip() + "</root>")
        lis = res.xpath("//li")
        # print(len(lis))
        for li in lis:
            meta = {
                "brandname": li.xpath("h3/a/text()")[0],
                "brandid": li.xpath("@id")[0].replace("b", "")
            }
            url = li.xpath("h3/a/@href")[0]
        # yield scrapy.Request(url="https://car.autohome.com.cn/price/brand-33.html", meta=meta, callback=self.parse_fnf)
            yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_fnf)

    
    def parse_fnf(self, response):
        dls = response.xpath("//*[@class='list-dl']")
        print(dls)
        for dl in dls:
            factoryname = dl.xpath("dt/a/text()").extract_first()
            furl = dl.xpath("dt/a/@href").extract_first()
            factoryid = re.findall("\-(\d+)\.html", furl)[0]
            family_list = dl.xpath("dd/div[@class='list-dl-text']/a")
            for family in family_list:
                familyname = family.xpath("text()").extract_first()
                family_url = family.xpath("@href").extract_first()
                familyid = re.findall("series\-(\d+)[\-\.].*?html", family_url)[0]
                meta = {
                    "factoryname": factoryname,
                    "factoryid": factoryid,
                    "familyname": familyname.replace(u" (??????)", ""),
                    "familyid": familyid
                }
                yield scrapy.Request(url=response.urljoin(family_url), meta=dict(meta, **response.meta), callback=self.parse_family)

    def parse_family(self, response):
        pss = response.xpath("//*[@class='tab-nav border-t-no']/*[@data-trigger='click']/li")
        for ps in pss:
            if ps.xpath("@class").extract_first() == 'current':
                producestatus = ps.xpath("a/text()").extract_first()
            if ps.xpath("@class").extract_first() != 'current' and ps.xpath("@class").extract_first != 'disabled':
                yield scrapy.Request(url=response.urljoin(ps.xpath("a/@href").extract_first()), meta=response.meta,
                                     callback=self.parse_family2)

        next = response.xpath("//a[@class='page-item-next']")
        if next:
            yield scrapy.Request(url=response.urljoin(next.xpath('@href').extract_first()), meta=response.meta,
                                 callback=self.parse_family2)

        lis = response.xpath("//*[@class='interval01-list']/li")
        for li in lis:
            model = li.xpath("div/div/p/a/text()").extract_first()
            autohomeid = int(li.xpath("@data-value").extract_first())
            if autohomeid in [32987,40791,40792,40793,40794,37728,38704,36330,1007403,39140,39142,39141,39143,39521,39614,39256,39247,1007607,39981,39675,39803,39619,39802,40176,27188,38858,39804,39805,39806,39708,39711,39940,27537,38798,36326,40135,40134,40133,40200,40128,40129,40199,40130,40131,40132,40198,17372,35688,35687,35686,35684,35685,38436,39710,39709,23815,38946,28616,39115,39112,32840,38046,38263,38294,1002441,39176,37848,20347,39175,1007497,1007515,1007514,1007496,1007504,1007485,1007503,1007605,1007486,1007606,1007517,1007499,1007518,1007498,1007516,1007500,1007502,1007501,1007490,1007508,1007491,1007492,1007493,1007511,1007510,1007509,1007506,1007513,1007495,1007519,1007512,1007488,1007494,1007507,1007505,1007489,1007487,1007357,1007297,1007294,1007296,38868,38867,38864,38866,38865,1007292,1007295,1007301,1007300,1007299,1007285,1007287,35091,40054,38773,40056,36596,40152,21713,39546,39545,39544,33763,38352,39344,1007397,1007398,1007399,37489,36550,36549,34374,23533,32576,32681,32682,1007802,1006917,1006704,1006703,35394,35393,35392,38363,38854,34500,38918,38916,38853,38915,38852,38917,38374,38762,38802,36854,38761,15822,40037,40035,40033,40036,40034,40032,39356,39321,38814,18989,26078,38629,26079,1003681,1003679,1003683,39462,39463,24030,38803,39847,39848,36620,37729,38954,38161,38203,38207,38209,38213,38205,38198,38211,38200,38192,38190,38202,38188,38196,38194,38224,38230,38228,38222,38220,38214,38226,38216,38218,38514,38513,38506,38511,38508,38515,39780,38912,38509,38512,38510,38949,39029,40232,34843,34844,30905,37174,39036,39511,34492,39893,34850,30241,38829,38831,38160,39448,38827,38828,40087,24046,40085,39974,40084,40086,39707,39823,29154,38961,39169,33850,36098,36897,39779,38507,38232,30509,36979,38362,39242,39244,39243,35618,1007400,38075,35535,35453,35452,39345,37734,33779,38747,39747,39799,39748,39798,39801,38890,1007286,1007293,38863,1002440,38293,23816,40136,38545,38857,39972,39973,39753,39610,39603,39609,39608,39607,39605,39604,39606,38950,26807,26806,37098,39976,39975,38971,1007215,1007200,1007205,1007199,1007214,1007204,1007198,1007209,1007203,1007213,1007208,1007210,1007172,1007180,1007196,1007188,1007179,1007187,1007171,1007195,1007186,1007170,1007178,1007194,1007185,1007177,1007176,1007193,1007169,1007168,1007184,1007192,31874]:
                print(autohomeid)
                logging.log(msg=str(autohomeid), level=logging.INFO)
                meta = {
                    "producestatus": producestatus,
                    "model": model,
                    "autohomeid": str(autohomeid)
                }
                url = "https://www.autohome.com.cn/spec/%d" % autohomeid
                yield scrapy.Request(url=url, meta=dict(meta, **response.meta), callback=self.parse_extra)

    def parse_family2(self, response):
        pss = response.xpath("//*[@class='tab-nav border-t-no']/*[@data-trigger='click']/li")
        for ps in pss:
            if ps.xpath("@class").extract_first() == 'current':
                producestatus = ps.xpath("a/text()").extract_first()

        next = response.xpath("//a[@class='page-item-next']")
        if next:
            yield scrapy.Request(url=response.urljoin(next.xpath('@href').extract_first()), meta=response.meta,
                                 callback=self.parse_family2)

        lis = response.xpath("//*[@class='interval01-list']/li")
        for li in lis:
            model = li.xpath("div/div/p/a/text()").extract_first()
            autohomeid = int(li.xpath("@data-value").extract_first())
            if autohomeid in [32987,40791,40792,40793,40794,37728,38704,36330,1007403,39140,39142,39141,39143,39521,39614,39256,39247,1007607,39981,39675,39803,39619,39802,40176,27188,38858,39804,39805,39806,39708,39711,39940,27537,38798,36326,40135,40134,40133,40200,40128,40129,40199,40130,40131,40132,40198,17372,35688,35687,35686,35684,35685,38436,39710,39709,23815,38946,28616,39115,39112,32840,38046,38263,38294,1002441,39176,37848,20347,39175,1007497,1007515,1007514,1007496,1007504,1007485,1007503,1007605,1007486,1007606,1007517,1007499,1007518,1007498,1007516,1007500,1007502,1007501,1007490,1007508,1007491,1007492,1007493,1007511,1007510,1007509,1007506,1007513,1007495,1007519,1007512,1007488,1007494,1007507,1007505,1007489,1007487,1007357,1007297,1007294,1007296,38868,38867,38864,38866,38865,1007292,1007295,1007301,1007300,1007299,1007285,1007287,35091,40054,38773,40056,36596,40152,21713,39546,39545,39544,33763,38352,39344,1007397,1007398,1007399,37489,36550,36549,34374,23533,32576,32681,32682,1007802,1006917,1006704,1006703,35394,35393,35392,38363,38854,34500,38918,38916,38853,38915,38852,38917,38374,38762,38802,36854,38761,15822,40037,40035,40033,40036,40034,40032,39356,39321,38814,18989,26078,38629,26079,1003681,1003679,1003683,39462,39463,24030,38803,39847,39848,36620,37729,38954,38161,38203,38207,38209,38213,38205,38198,38211,38200,38192,38190,38202,38188,38196,38194,38224,38230,38228,38222,38220,38214,38226,38216,38218,38514,38513,38506,38511,38508,38515,39780,38912,38509,38512,38510,38949,39029,40232,34843,34844,30905,37174,39036,39511,34492,39893,34850,30241,38829,38831,38160,39448,38827,38828,40087,24046,40085,39974,40084,40086,39707,39823,29154,38961,39169,33850,36098,36897,39779,38507,38232,30509,36979,38362,39242,39244,39243,35618,1007400,38075,35535,35453,35452,39345,37734,33779,38747,39747,39799,39748,39798,39801,38890,1007286,1007293,38863,1002440,38293,23816,40136,38545,38857,39972,39973,39753,39610,39603,39609,39608,39607,39605,39604,39606,38950,26807,26806,37098,39976,39975,38971,1007215,1007200,1007205,1007199,1007214,1007204,1007198,1007209,1007203,1007213,1007208,1007210,1007172,1007180,1007196,1007188,1007179,1007187,1007171,1007195,1007186,1007170,1007178,1007194,1007185,1007177,1007176,1007193,1007169,1007168,1007184,1007192,31874]:
                print(autohomeid)
                logging.log(msg=str(autohomeid), level=logging.INFO)
                meta = {
                    "producestatus": producestatus,
                    "model": model,
                    "autohomeid": str(autohomeid)
                }
                url = "https://www.autohome.com.cn/spec/%d" % autohomeid
                yield scrapy.Request(url=url, meta=dict(meta, **response.meta), callback=self.parse_extra)


    def parse_extra(self, response):
        car_extra_info = {}
        vehicle_dimensions = response.xpath(
            "//li[contains(text(), '\u8f66\u8eab\u5c3a\u5bf8\uff1a')]/span/text()").extract_first() \
            if response.xpath("//li[contains(text(), '\u8f66\u8eab\u5c3a\u5bf8\uff1a')]/span/text()") else "-"
        makeyear = response.xpath('//*[@class="information-tit"]/h2/text()').re("\d+")[0] \
            if response.xpath('//*[@class="information-tit"]/h2/text()') else "-"
        koubei_score = response.xpath('//*[@class="scroe"]/text()').extract_first().replace(u"\u5206", "") \
            if response.xpath('//*[@class="scroe"]/text()') else "-"
        url = "http://car.m.autohome.com.cn/ashx/car/GetModelConfig.ashx?ids=%s" % response.meta["autohomeid"]
        car_extra_info["vehicle_dimensions"] = vehicle_dimensions
        car_extra_info["makeyear"] = makeyear
        car_extra_info["koubei_score"] = koubei_score
        yield scrapy.Request(url=url, meta=dict(car_extra_info, **response.meta), callback=self.parse_details)


    def parse_details(self, response):
        print(response.body)
        # count
        print "response.url", response.url
        self.counts += 1
        print "download              " + str(self.counts) + "                  items"
        # item loader
        # time.sleep(30)
        item = AutohomeItem()
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        # meta data
        metadata = response.meta
        item = dict(item, **metadata)
        # ????????????
        temp = response.xpath('//p/text()').extract_first()
        # temp = response.xpath('//pre/text()').extract_first()
        item['datasave'] = temp
        jsondata = {}
        if len(temp) != 0:
            data = json.loads(temp)
            # print(data)
            # configlist = json.loads(temp.re('config = (.*?);')[0]) \
            # if temp.re('config = (.*?);')[0] else '-'
            # configlist=data['config']
            # optionlist = data['param']
            try:
                if data.has_key("config"):
                    for i in data['config']:
                        for j in i['configitems']:
                            key = j['name']
                            value = j['valueitems'][0]['value'].replace("&nbsp;", "")
                            jsondata[key] = value
            except:
                pass
            try:
                if data.has_key("param"):
                    for i in data['param']:
                        for j in i['paramitems']:
                            key = j['name']
                            value = j['valueitems'][0]['value'].replace("&nbsp;", "")
                            jsondata[key] = value
            except:
                pass

        namedic = {'front_back_head_airbag': u'\u524d/\u540e\u6392\u5934\u90e8\u6c14\u56ca(\u6c14\u5e18)'
            , 'central_lock': u'\u8f66\u5185\u4e2d\u63a7\u9501'
            , 'keyless_start_system': u'\u65e0\u94a5\u5319\u542f\u52a8\u7cfb\u7edf'
            , 'safety_belt_is_not_prompt': u'\u5b89\u5168\u5e26\u672a\u7cfb\u63d0\u793a'
            , 'engine_electronic_control_unit': u'\u53d1\u52a8\u673a\u7535\u5b50\u9632\u76d7'
            , 'remote_control_key': u'\u9065\u63a7\u94a5\u5319'
            , 'zero_tire_pressure': u'\u96f6\u80ce\u538b\u7ee7\u7eed\u884c\u9a76'
            , 'isofix_child_seat_interface': u'ISOFIX\u513f\u7ae5\u5ea7\u6905\u63a5\u53e3'
            , 'knee_airbag': u'\u819d\u90e8\u6c14\u56ca'
            , 'driver_codrive_airbag': u'\u4e3b/\u526f\u9a7e\u9a76\u5ea7\u5b89\u5168\u6c14\u56ca'
            , 'pke': u'\u65e0\u94a5\u5319\u8fdb\u5165\u7cfb\u7edf'
            , 'tire_pressure_monitoring': u'\u80ce\u538b\u76d1\u6d4b\u88c5\u7f6e'
            , 'front_back_side_airbag': u'\u524d/\u540e\u6392\u4fa7\u6c14\u56ca'
            , 'geartype': u'\u53d8\u901f\u7bb1'
            , 'gear': u'\u7b80\u79f0'
            , 'gearnumber': u'\u6321\u4f4d\u4e2a\u6570'
            , 'geardesc': u'\u53d8\u901f\u7bb1\u7c7b\u578b'
            , 'rearview_mirror_electric_folding': u'\u540e\u89c6\u955c\u7535\u52a8\u6298\u53e0'
            , 'rearview_mirror_memory': u'\u540e\u89c6\u955c\u8bb0\u5fc6'
            , 'window_clip_hand_safety': u'\u8f66\u7a97\u9632\u5939\u624b\u529f\u80fd'
            , 'rearview_mirror_electric_adjustment': u'\u540e\u89c6\u955c\u7535\u52a8\u8c03\u8282'
            , 'visor__mirror': u'\u906e\u9633\u677f\u5316\u5986\u955c'
            , 'back_privacy_glass': u'\u540e\u6392\u4fa7\u9690\u79c1\u73bb\u7483'
            , 'rearview_mirror_auto_anti_glare': u'\u5185/\u5916\u540e\u89c6\u955c\u81ea\u52a8\u9632\u7729\u76ee'
            , 'backglass_sunshade': u'\u540e\u98ce\u6321\u906e\u9633\u5e18'
            , 'windshield_wiper_sensor': u'\u611f\u5e94\u96e8\u5237'
            , 'rear_windshield_wiper': u'\u540e\u96e8\u5237'
            , 'insulating_glass': u'\u9632\u7d2b\u5916\u7ebf\u73bb\u7483'
            , 'backsideglass_sunshade': u'\u540e\u6392\u4fa7\u906e\u9633\u5e18'
            , 'rearview_mirror_heating': u'\u540e\u89c6\u955c\u52a0\u70ed'
            , 'front_rear_lectric_windows': u'\u524d/\u540e\u7535\u52a8\u8f66\u7a97'
            , 'brake_assist_eba_bas_ba': u'\u5239\u8f66\u8f85\u52a9(EBA/BAS/BA\u7b49)'
            , 'hill_descent_control': u'\u9661\u5761\u7f13\u964d'
            , 'back_vaq': u'\u540e\u6865\u9650\u6ed1\u5dee\u901f\u5668/\u5dee\u901f\u9501'
            , 'vehicle_stability_control_esp_dsc_vsc': u'\u8f66\u8eab\u7a33\u5b9a\u63a7\u5236(ESC/ESP/DSC\u7b49)'
            , 'aimatic': u'\u7a7a\u6c14\u60ac\u67b6'
            , 'front_vaq': u'\u524d\u6865\u9650\u6ed1\u5dee\u901f\u5668/\u5dee\u901f\u9501'
            , 'hill_start_assist': u'\u4e0a\u5761\u8f85\u52a9'
            , 'braking_force_distribution_ebd_cbc': u'\u5236\u52a8\u529b\u5206\u914d(EBD/CBC\u7b49)'
            , 'variable_suspension': u'\u53ef\u53d8\u60ac\u67b6'
            , 'automatic_parking': u'\u81ea\u52a8\u9a7b\u8f66'
            , 'limited_slip_differential': u'\u4e2d\u592e\u5dee\u901f\u5668\u9501\u6b62\u529f\u80fd'
            , 'variable_gear_steering_ratio': u'\u53ef\u53d8\u8f6c\u5411\u6bd4'
            , 'traction_control_system_asr_tcs_trc': u'\u7275\u5f15\u529b\u63a7\u5236(ASR/TCS/TRC\u7b49)'
            , 'abs_antilock': u'ABS\u9632\u62b1\u6b7b'
            , 'parking_brake_type': u'\u9a7b\u8f66\u5236\u52a8\u7c7b\u578b'
            , 'frontbrake': u'\u524d\u5236\u52a8\u5668\u7c7b\u578b'
            , 'backbrake': u'\u540e\u5236\u52a8\u5668\u7c7b\u578b'
            , 'sparewheel': u'\u5907\u80ce\u89c4\u683c'
            , 'frontwheel': u'\u524d\u8f6e\u80ce\u89c4\u683c'
            , 'backwheel': u'\u540e\u8f6e\u80ce\u89c4\u683c'
            , 'length': u'\u957f\u5ea6(mm)'
            , 'baggage': u'\u884c\u674e\u53a2\u5bb9\u79ef(L)'
            , 'seats': u'\u5ea7\u4f4d\u6570(\u4e2a)'
            , 'min_ground_distance': u'\u6700\u5c0f\u79bb\u5730\u95f4\u9699(mm)'
            , 'doors': u'\u8f66\u95e8\u6570(\u4e2a)'
            , 'frontgauge': u'\u524d\u8f6e\u8ddd(mm)'
            , 'heigh': u'\u9ad8\u5ea6(mm)'
            , 'wheelbase': u'\u8f74\u8ddd(mm)'
            , 'backgauge': u'\u540e\u8f6e\u8ddd(mm)'
            , 'weigth': u'\u6574\u5907\u8d28\u91cf(kg)'
            , 'width': u'\u5bbd\u5ea6(mm)'
            , 'fulevolumn': u'\u6cb9\u7bb1\u5bb9\u79ef(L)'
            , 'steering_headlights': u'\u8f6c\u5411\u5934\u706f'
            , 'Headlights_full': u'\u8fdc\u5149\u706f'
            , 'inside_atmosphere_lights': u'\u8f66\u5185\u6c1b\u56f4\u706f'
            , 'adjustable_headlight_height': u'\u5927\u706f\u9ad8\u5ea6\u53ef\u8c03'
            , 'headlight_cleaning_device': u'\u5927\u706f\u6e05\u6d17\u88c5\u7f6e'
            , 'antifog_ligths': u'\u524d\u96fe\u706f'
            , 'automatic_headlights': u'\u81ea\u52a8\u5934\u706f'
            , 'daytime__lights': u'LED\u65e5\u95f4\u884c\u8f66\u706f'
            , 'Headlights_dipped': u'\u8fd1\u5149\u706f'
            , 'adaptive_light_distance': u'\u81ea\u9002\u5e94\u8fdc\u8fd1\u5149'
            , 'corner_lamp': u'\u8f6c\u5411\u8f85\u52a9\u706f'
            , 'body_structure': u'\u8f66\u4f53\u7ed3\u6784'
            , 'backhang': u'\u540e\u60ac\u67b6\u7c7b\u578b'
            , 'driveway': u'\u9a71\u52a8\u65b9\u5f0f'
            , 'fronthang': u'\u524d\u60ac\u67b6\u7c7b\u578b'
            , 'assistanttype': u'\u52a9\u529b\u7c7b\u578b'
            , 'mp3_audio_support': u'CD\u652f\u6301MP3/WMA'
            , 'bluetooth_car_phone': u'\u84dd\u7259/\u8f66\u8f7d\u7535\u8bdd'
            , 'speakers_number': u'???????????????'
            , 'speaker_brand': u'\u626c\u58f0\u5668\u54c1\u724c'
            , 'rear_lcd_screen': u'\u540e\u6392\u6db2\u6676\u5c4f'
            , 'gps_navigation': u'GPS\u5bfc\u822a\u7cfb\u7edf'
            , 'power_supply': u'220V/230V\u7535\u6e90'
            , 'single_cd_player': u'\u591a\u5a92\u4f53\u7cfb\u7edf'
            , 'onboard_tv': u'\u8f66\u8f7d\u7535\u89c6'
            , 'external_audio_source_connectors': u'\u5916\u63a5\u97f3\u6e90\u63a5\u53e3'
            , 'interactive_location_services': u'\u5b9a\u4f4d\u4e92\u52a8\u670d\u52a1'
            , 'color_screen_display_control': u'\u4e2d\u63a7\u53f0\u5f69\u8272\u5927\u5c4f'
            , 'fuelmethod': u'\u4f9b\u6cb9\u65b9\u5f0f'
            , 'maxtorque': u'\u6700\u5927\u626d\u77e9\u8f6c\u901f(rpm)'
            , 'maxrpm': u'\u6700\u5927\u529f\u7387\u8f6c\u901f(rpm)'
            , 'maxps': u'\u6700\u5927\u9a6c\u529b(Ps)'
            , 'fuelnumber': u'\u71c3\u6cb9\u6807\u53f7'
                   # , 'fueltype': u'\u71c3\u6599\u5f62\u5f0f'
            , 'fueltype': u'\u80fd\u6e90\u7c7b\u578b'
            , 'strokemm': u'\u884c\u7a0b(mm)'
            , 'lwvnumber': u'\u6c14\u7f38\u6570(\u4e2a)'
            , 'valve': u'\u6bcf\u7f38\u6c14\u95e8\u6570(\u4e2a)'
            , 'valve_mechanism': u'\u914d\u6c14\u673a\u6784'
            , 'emission': u'\u73af\u4fdd\u6807\u51c6'
            , 'boremm': u'\u7f38\u5f84(mm)'
            , 'maxpower': u'\u6700\u5927\u529f\u7387(kW)'
            , 'engine_technology': u'\u53d1\u52a8\u673a\u7279\u6709\u6280\u672f'
            , 'lwv': u'\u6c14\u7f38\u6392\u5217\u5f62\u5f0f'
            , 'method': u'\u8fdb\u6c14\u5f62\u5f0f'
            , 'maxnm': u'\u6700\u5927\u626d\u77e9(N\xb7m)'
            , 'cylinder_material': u'\u7f38\u4f53\u6750\u6599'
            , 'compress': u'\u538b\u7f29\u6bd4'
            , 'engine_type': u'\u53d1\u52a8\u673a\u578b\u53f7'
            , 'cylinder': u'\u6392\u91cf(mL)'
            , 'head_port': u'\u7f38\u76d6\u6750\u6599'
            , 'park_assist': u'\u81ea\u52a8\u6cca\u8f66\u5165\u4f4d'
            , 'doubling_asisst': u'\u5e76\u7ebf\u8f85\u52a9'
            , 'night_vision': u'\u591c\u89c6\u7cfb\u7edf'
            , 'ldws': u'\u8f66\u9053\u504f\u79bb\u9884\u8b66\u7cfb\u7edf'
            , 'adaptive_cruise': u'\u81ea\u9002\u5e94\u5de1\u822a'
            , 'panoramic_camera': u'\u5168\u666f\u6444\u50cf\u5934'
            , 'lcd_screen_display_control': u'\u4e2d\u63a7\u6db2\u6676\u5c4f\u5206\u5c4f\u663e\u793a'
            , 'engine_start_stop': u'\u53d1\u52a8\u673a\u542f\u505c\u6280\u672f'
            , 'abls': u'\u4e3b\u52a8\u5239\u8f66/\u4e3b\u52a8\u5b89\u5168\u7cfb\u7edf'
            , 'active_front_steering': u'\u6574\u4f53\u4e3b\u52a8\u8f6c\u5411\u7cfb\u7edf'
            , 'level': u'\u7ea7\u522b'
            , 'vehicle_warranty': u'\u6574\u8f66\u8d28\u4fdd'
            , 'bodystyle': u'\u8f66\u8eab\u7ed3\u6784'
            , 'salesdesc': u'\u8f66\u578b\u540d\u79f0'
            , 'masspeed': u'\u6700\u9ad8\u8f66\u901f(km/h)'
            , 'price':u'\u5382\u5546\u6307\u5bfc\u4ef7(\u5143)'
            , 'output': u'\u6392\u91cf(mL)'
            , 'factoryname': u'\u5382\u5546'
            , 'accelerate': u'\u5b98\u65b90-100km/h\u52a0\u901f(s)'
            , 'petrol_test': u'\u5b9e\u6d4b\u6cb9\u8017(L/100km)'
            , 'accelerate_test': u'\u5b9e\u6d4b0-100km/h\u52a0\u901f(s)'
            , 'petrol': u'\u5de5\u4fe1\u90e8\u7efc\u5408\u6cb9\u8017(L/100km)'
            , 'ground_distance_test': u'\u5b9e\u6d4b\u79bb\u5730\u95f4\u9699(mm)'
            , 'engine': u'\u53d1\u52a8\u673a'
            , 'brake_test': u'\u5b9e\u6d4b100-0km/h\u5236\u52a8(m)'
            , 'zone_temperature_control': u'\u6e29\u5ea6\u5206\u533a\u63a7\u5236'
            , 'rear_ac': u'\u540e\u5ea7\u51fa\u98ce\u53e3'
            , 'car_refrigerator': u'\u8f66\u8f7d\u51b0\u7bb1'
            , 'rear_independent_ac': u'\u540e\u6392\u72ec\u7acb\u7a7a\u8c03'
            , 'ac_pollen_filter': u'\u8f66\u5185\u7a7a\u6c14\u8c03\u8282/\u82b1\u7c89\u8fc7\u6ee4'
            , 'auto_ac': u'\u7a7a\u8c03\u63a7\u5236\u65b9\u5f0f'
            , 'computer_screen_of_driving': u'\u884c\u8f66\u7535\u8111\u663e\u793a\u5c4f'
            , 'steering_wheel_shift': u'\u65b9\u5411\u76d8\u6362\u6321'
            , 'lhz': u'\u65b9\u5411\u76d8\u52a0\u70ed'
            , 'backing_radar': u'\u524d/\u540e\u9a7b\u8f66\u96f7\u8fbe'
            , 'leather_steering_wheel': u'\u771f\u76ae\u65b9\u5411\u76d8'
            , 'steering_wheel_adjustment': u'\u65b9\u5411\u76d8\u8c03\u8282'
            , 'rear_video_monitor': u'\u5012\u8f66\u89c6\u9891\u5f71\u50cf'
            , 'memory_code': u'\u65b9\u5411\u76d8\u8bb0\u5fc6'
            , 'steering_wheel_electric_adjustment': u'\u65b9\u5411\u76d8\u7535\u52a8\u8c03\u8282'
            , 'cruise_control': u'\u5b9a\u901f\u5de1\u822a'
            , 'multi_function_steering_wheel': u'\u591a\u529f\u80fd\u65b9\u5411\u76d8'
            , 'lcd_panel': u'\u5168\u6db2\u6676\u4eea\u8868\u76d8'
            , 'heads_up_display': u'HUD\u62ac\u5934\u6570\u5b57\u663e\u793a'
            , 'induction_trunk': u'\u7535\u52a8\u540e\u5907\u53a2'
            , 'electric_sunroof': u'\u7535\u52a8\u5929\u7a97'
            , 'hubtype': u'\u94dd\u5408\u91d1\u8f6e\u5708'
            , 'panoramic_sunroof': u'\u5168\u666f\u5929\u7a97'
            , 'electric_trunk': u'\u7535\u52a8\u540e\u5907\u53a2'
            , 'sliding_door': u'\u4fa7\u6ed1\u95e8'
            , 'sport_appearance_suite': u'\u8fd0\u52a8\u5916\u89c2\u5957\u4ef6'
            , 'roof_rack': u'\u8f66\u9876\u884c\u674e\u67b6'
            , 'electric_door': u'\u7535\u52a8\u5438\u5408\u95e8'
            , 'sports_seats': u'\u8fd0\u52a8\u98ce\u683c\u5ea7\u6905'
            , 'adjustable_seat_height': u'\u5ea7\u6905\u9ad8\u4f4e\u8c03\u8282'
            , 'third_row_seats': u'\u7b2c\u4e09\u6392\u5ea7\u6905'
            , 'rear_seat_electric_adjustment': u'\u540e\u6392\u5ea7\u6905\u7535\u52a8\u8c03\u8282'
            , 'leather_seats': u'????????????'
            , 'adjustable_rear_row_backrest_angle': u'\u7b2c\u4e8c\u6392\u9760\u80cc\u89d2\u5ea6\u8c03\u8282'
            , 'rear_seat_down': u'\u540e\u6392\u5ea7\u6905\u653e\u5012\u65b9\u5f0f'
            , 'rear_row_seat_movement': u'\u7b2c\u4e8c\u6392\u5ea7\u6905\u79fb\u52a8'
            , 'seat_armrest': u'\u524d/\u540e\u4e2d\u592e\u6276\u624b'
            , 'driver_seat_electric_adjustment': u'\u4e3b/\u526f\u9a7e\u9a76\u5ea7\u7535\u52a8\u8c03\u8282'
            , 'rear_row_hang_cup': u'\u540e\u6392\u676f\u67b6'
            , 'front_back_seat_heating': u'\u524d/\u540e\u6392\u5ea7\u6905\u52a0\u70ed'
            , 'seat_ventilation': u'\u524d/\u540e\u6392\u5ea7\u6905\u901a\u98ce'
            , 'electric_chair_memory': u'\u7535\u52a8\u5ea7\u6905\u8bb0\u5fc6'
            , 'adjustable_lumbar_support': u'\u8170\u90e8\u652f\u6491\u8c03\u8282'
            , 'massage_seat': u'\u524d/\u540e\u6392\u5ea7\u6905\u6309\u6469'
            , 'adjustable_shoulder_support': u'\u80a9\u90e8\u652f\u6491\u8c03\u8282'
            , 'electric_machinery_type': u'????????????'
            , 'electric_machinery_power': u'??????????????????(kW)'
            , 'electric_machinery_distance': u'??????????????????(N??m)'
            , 'front_electric_machinery_power': u'????????????????????????(kW)'
            , 'front_electric_machinery_distance': u'????????????????????????(N??m)'
            , 'back_electric_machinery_power': u'????????????????????????(kW)'
            , 'back_electric_machinery_distance': u'????????????????????????(N??m)'
            , 'system_power': u'??????????????????(kW)'
            , 'system_distance': u'??????????????????(N??m)'
            , 'electric_machinery_number': u'???????????????'
            , 'electric_machinery_layout': u'????????????'
            , 'battery_type': u'????????????'
            , 'miles': u'?????????????????????(km)'
            , 'battery_capacity': u'????????????(kWh)'
            , 'energy_drain': u'??????????????????(kWh/100km)'
            , 'battery_service': u'???????????????'
            , 'battery_charge_time': u'??????????????????'
            , 'fast_charge': u'????????????(%)'
            , 'charge_device': u'???????????????'}
        values = []
        for ename, uname in namedic.items():
            item[ename] = "-"
            if jsondata.get(uname):
                item[ename] = jsondata.get(uname)
            if ename == 'factoryname' and item[ename] == "-" and "specitems" in data:
                if "fctname" in data["specitems"]:
                    item[ename] = data["specitems"]["fctname"]
            values.append(item[ename])
        if self.nationp.has_key(item['factoryname']):
            print self.nationp[item['factoryname']]
            item = dict(item, **self.nationp[item['factoryname']])
        else:
            item['nation'] = "-"
            item['property'] = "-"
        # print "values",values
        while None in values:
            values.remove(None)
        if not values == []:
            va = "".join(values).encode("utf-8")
        else:
            va = "-"

        if item['price'].startswith("0.00???"):
            item['price'] = "-"

        # try:
        #     status = response.url + str(item['autohomeid']) + item['familyname'] + str(item['familyid']) \
        #              + item['makeyear'] + item['vehicle_dimensions'] \
        #              + item['level'] + item['vehicle_warranty'] + item['bodystyle'] \
        #              + item['salesdesc'] + item['masspeed'] + item['price'] \
        #              + item['output'] + item['factoryname'] + item['accelerate'] \
        #              + item['petrol_test'] + item['accelerate_test'] \
        #              + item['petrol'] + item['ground_distance_test'] \
        #              + item['engine'] + item['brake_test'] + va
        # except Exception, e:
        #     print e
        #     status = response.url
        status = response.url + time.strftime('%Y-%m-%d %X', time.localtime())
        item['status'] = hashlib.md5(status).hexdigest()

        # logging.log(msg=json.dumps(item), level=logging.INFO)
        yield item