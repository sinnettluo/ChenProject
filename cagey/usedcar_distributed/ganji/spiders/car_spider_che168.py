#-*- coding: UTF-8 -*-
import json

import requests
import scrapy

import time
import logging

from scrapy_redis.spiders import RedisSpider

from ganji.items import Che168
from ganji.spiders.SpiderInit import spider_original_Init

website ='che168'

# main
class CarSpider(RedisSpider):

    # basesetting
    name = website
    allowed_domains = ["che168.com"]
    # start_urls = [ "http://m.che168.com/carlist/FilterBrand.aspx", ]
    redis_key = 'che168'

    custom_settings = {
        # 'DOWNLOAD_DELAY': 2.5,
        'CONCURRENT_REQUESTS': 8,
        # 'RANDOMIZE_DOWNLOAD_DELAY': True,

        # log
        'LOG_LEVEL': "INFO",
        'LOG_FILE': 'logs/che168.log',
    }

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # setting
        self.counts = 0
        self.carnum = 1500000
        self.dbname = 'usedcar'

        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)

        self.df = 'none'
        self.fa = 'none'

    # city select
    def parse(self, response):

        # city
        cities = [{'name': '合肥', 'py': 'hefei'}, {'name': '芜湖', 'py': 'wuhu'}, {'name': '安庆', 'py': 'anqing'},
                  {'name': '阜阳', 'py': 'fu_yang'}, {'name': '亳州', 'py': 'bozhou'}, {'name': '蚌埠', 'py': 'bangbu'},
                  {'name': '池州', 'py': 'chizhou'}, {'name': '滁州', 'py': 'chuzhou'}, {'name': '黄山', 'py': 'huangshan'},
                  {'name': '淮北', 'py': 'huaibei'}, {'name': '淮南', 'py': 'huainan'}, {'name': '六安', 'py': 'liuan'},
                  {'name': '马鞍山', 'py': 'maanshan'}, {'name': '宿州', 'py': 'su_zhou'}, {'name': '铜陵', 'py': 'tongling'},
                  {'name': '宣城', 'py': 'xuancheng'},
                  {'name': '北京', 'py': 'beijing'}, {'name': '重庆', 'py': 'chongqing'},
                  {'name': '福州', 'py': 'fuzhou'}, {'name': '厦门', 'py': 'xiamen'}, {'name': '泉州', 'py': 'quanzhou'},
                  {'name': '龙岩', 'py': 'longyan'}, {'name': '宁德', 'py': 'ningde'}, {'name': '南平', 'py': 'nanping'},
                  {'name': '莆田', 'py': 'putian'}, {'name': '三明', 'py': 'sanming'}, {'name': '漳州', 'py': 'zhangzhou'},
                  {'name': '广州', 'py': 'guangzhou'}, {'name': '韶关', 'py': 'shaoguan'}, {'name': '深圳', 'py': 'shenzhen'},
                  {'name': '珠海', 'py': 'zhuhai'}, {'name': '汕头', 'py': 'shantou'}, {'name': '佛山', 'py': 'foshan'},
                  {'name': '江门', 'py': 'jiangmen'}, {'name': '惠州', 'py': 'huizhou'}, {'name': '东莞', 'py': 'dongguan'},
                  {'name': '中山', 'py': 'zhongshan'}, {'name': '潮州', 'py': 'chaozhou'}, {'name': '河源', 'py': 'heyuan'},
                  {'name': '揭阳', 'py': 'jieyang'}, {'name': '梅州', 'py': 'meizhou'}, {'name': '茂名', 'py': 'maoming'},
                  {'name': '清远', 'py': 'qingyuan'}, {'name': '汕尾', 'py': 'shanwei'}, {'name': '云浮', 'py': 'yunfu'},
                  {'name': '阳江', 'py': 'yangjiang'}, {'name': '湛江', 'py': 'zhanjiang'},
                  {'name': '肇庆', 'py': 'zhaoqing'},
                  {'name': '南宁', 'py': 'nanning'}, {'name': '柳州', 'py': 'liuzhou'}, {'name': '桂林', 'py': 'guilin'},
                  {'name': '北海', 'py': 'beihai'}, {'name': '百色', 'py': 'baise'}, {'name': '崇左', 'py': 'chongzuo'},
                  {'name': '防城港', 'py': 'fangchenggang'}, {'name': '贵港', 'py': 'guigang'},
                  {'name': '贺州', 'py': 'hezhou'}, {'name': '河池', 'py': 'hechi'}, {'name': '来宾', 'py': 'laibin'},
                  {'name': '钦州', 'py': 'qinzhou'}, {'name': '梧州', 'py': 'wuzhou'}, {'name': '玉林', 'py': 'yu_lin'},
                  {'name': '贵阳', 'py': 'guiyang'}, {'name': '遵义', 'py': 'zunyi'}, {'name': '安顺', 'py': 'anshun'},
                  {'name': '毕节', 'py': 'bijie'}, {'name': '六盘水', 'py': 'liupanshui'},
                  {'name': '黔西南', 'py': 'qianxinan'}, {'name': '黔东南', 'py': 'qiandongnan'},
                  {'name': '黔南', 'py': 'qiannan'}, {'name': '铜仁', 'py': 'tongren'}, {'name': '兰州', 'py': 'lanzhou'},
                  {'name': '白银', 'py': 'baiyin'}, {'name': '定西', 'py': 'dingxi'}, {'name': '甘南', 'py': 'gannan'},
                  {'name': '酒泉', 'py': 'jiuquan'}, {'name': '嘉峪关', 'py': 'jiayuguan'}, {'name': '金昌', 'py': 'jinchang'},
                  {'name': '陇南', 'py': 'longnan'}, {'name': '临夏', 'py': 'linxia'}, {'name': '平凉', 'py': 'pingliang'},
                  {'name': '庆阳', 'py': 'qingyang'}, {'name': '天水', 'py': 'tianshui'}, {'name': '武威', 'py': 'wuwei'},
                  {'name': '张掖', 'py': 'zhangye'},
                  {'name': '海口', 'py': 'haikou'}, {'name': '白沙', 'py': 'baisha'}, {'name': '保亭', 'py': 'baoting'},
                  {'name': '昌江', 'py': 'changjiang'}, {'name': '澄迈', 'py': 'chengmai'},
                  {'name': '东方', 'py': 'dongfang'}, {'name': '定安', 'py': 'dingan'}, {'name': '儋州', 'py': 'danzhou'},
                  {'name': '临高', 'py': 'lingao'}, {'name': '乐东', 'py': 'ledong'}, {'name': '陵水', 'py': 'lingshui'},
                  {'name': '琼中', 'py': 'qiongzhong'}, {'name': '琼海', 'py': 'qionghai'}, {'name': '三亚', 'py': 'sanya'},
                  {'name': '三沙', 'py': 'sansha'}, {'name': '屯昌', 'py': 'tunchang'}, {'name': '文昌', 'py': 'wenchang'},
                  {'name': '万宁', 'py': 'wanning'}, {'name': '五指山', 'py': 'wuzhishan'},
                  {'name': '郑州', 'py': 'zhengzhou'}, {'name': '开封', 'py': 'kaifeng'}, {'name': '洛阳', 'py': 'luoyang'},
                  {'name': '平顶山', 'py': 'pingdingshan'}, {'name': '安阳', 'py': 'anyang'},
                  {'name': '新乡', 'py': 'xinxiang'}, {'name': '焦作', 'py': 'jiaozuo'}, {'name': '濮阳', 'py': 'puyang'},
                  {'name': '许昌', 'py': 'xuchang'}, {'name': '南阳', 'py': 'nanyang'}, {'name': '商丘', 'py': 'shangqiu'},
                  {'name': '信阳', 'py': 'xinyang'}, {'name': '周口', 'py': 'zhoukou'}, {'name': '驻马店', 'py': 'zhumadian'},
                  {'name': '鹤壁', 'py': 'hebi'}, {'name': '济源', 'py': 'jiyuan'}, {'name': '漯河', 'py': 'luohe'},
                  {'name': '三门峡', 'py': 'sanmenxia'},
                  {'name': '武汉', 'py': 'wuhan'}, {'name': '十堰', 'py': 'shiyan'}, {'name': '宜昌', 'py': 'yichang'},
                  {'name': '襄阳', 'py': 'xiangyang'}, {'name': '鄂州', 'py': 'ezhou'}, {'name': '恩施', 'py': 'enshi'},
                  {'name': '黄冈', 'py': 'huanggang'}, {'name': '黄石', 'py': 'huangshi'}, {'name': '荆门', 'py': 'jingmen'},
                  {'name': '荆州', 'py': 'jingzhou'}, {'name': '潜江', 'py': 'qianjiang'},
                  {'name': '神农架', 'py': 'shennongjia'}, {'name': '随州', 'py': 'suizhou'},
                  {'name': '天门', 'py': 'tianmen'}, {'name': '孝感', 'py': 'xiaogan'}, {'name': '咸宁', 'py': 'xianning'},
                  {'name': '仙桃', 'py': 'xiantao'},
                  {'name': '长沙', 'py': 'changsha'}, {'name': '株洲', 'py': 'zhuzhou'}, {'name': '湘潭', 'py': 'xiangtan'},
                  {'name': '衡阳', 'py': 'hengyang'}, {'name': '常德', 'py': 'changde'}, {'name': '郴州', 'py': 'chenzhou'},
                  {'name': '怀化', 'py': 'huaihua'}, {'name': '娄底', 'py': 'loudi'}, {'name': '邵阳', 'py': 'shaoyang'},
                  {'name': '湘西', 'py': 'xiangxi'}, {'name': '永州', 'py': 'yongzhou'}, {'name': '岳阳', 'py': 'yueyang'},
                  {'name': '益阳', 'py': 'yiyang'}, {'name': '张家界', 'py': 'zhangjiajie'},
                  {'name': '石家庄', 'py': 'shijiazhuang'}, {'name': '唐山', 'py': 'tangshan'},
                  {'name': '秦皇岛', 'py': 'qinhuangdao'}, {'name': '邯郸', 'py': 'handan'}, {'name': '邢台', 'py': 'xingtai'},
                  {'name': '保定', 'py': 'baoding'}, {'name': '张家口', 'py': 'zhangjiakou'},
                  {'name': '承德', 'py': 'chengde'}, {'name': '沧州', 'py': 'cangzhou'}, {'name': '廊坊', 'py': 'langfang'},
                  {'name': '衡水', 'py': 'hengshui'},
                  {'name': '哈尔滨', 'py': 'haerbin'}, {'name': '齐齐哈尔', 'py': 'qiqihaer'}, {'name': '大庆', 'py': 'daqing'},
                  {'name': '大兴安岭', 'py': 'daxinganling'}, {'name': '黑河', 'py': 'heihe'}, {'name': '鹤岗', 'py': 'hegang'},
                  {'name': '鸡西', 'py': 'jixi'}, {'name': '佳木斯', 'py': 'jiamusi'}, {'name': '牡丹江', 'py': 'mudanjiang'},
                  {'name': '七台河', 'py': 'qitaihe'}, {'name': '双鸭山', 'py': 'shuangyashan'},
                  {'name': '绥化', 'py': 'suihua'}, {'name': '伊春', 'py': 'yichun'},
                  {'name': '南京', 'py': 'nanjing'}, {'name': '无锡', 'py': 'wuxi'}, {'name': '徐州', 'py': 'xuzhou'},
                  {'name': '常州', 'py': 'changzhou'}, {'name': '苏州', 'py': 'suzhou'}, {'name': '南通', 'py': 'nantong'},
                  {'name': '连云港', 'py': 'lianyungang'}, {'name': '淮安', 'py': 'huaian'},
                  {'name': '盐城', 'py': 'yancheng'}, {'name': '扬州', 'py': 'yangzhou'}, {'name': '镇江', 'py': 'zhenjiang'},
                  {'name': '泰州', 'py': 'tai_zhou'}, {'name': '宿迁', 'py': 'suqian'},
                  {'name': '南昌', 'py': 'nanchang'}, {'name': '九江', 'py': 'jiujiang'}, {'name': '赣州', 'py': 'ganzhou'},
                  {'name': '上饶', 'py': 'shangrao'}, {'name': '抚州', 'py': 'fu_zhou'}, {'name': '吉安', 'py': 'jian'},
                  {'name': '景德镇', 'py': 'jingdezhen'}, {'name': '萍乡', 'py': 'ping_xiang'},
                  {'name': '新余', 'py': 'xinyu'}, {'name': '鹰潭', 'py': 'yingtan'}, {'name': '宜春', 'py': 'yi_chun'},
                  {'name': '长春', 'py': 'changchun'}, {'name': '吉林', 'py': 'jilinshi'}, {'name': '白山', 'py': 'baishan'},
                  {'name': '白城', 'py': 'baicheng'}, {'name': '辽源', 'py': 'liaoyuan'}, {'name': '松原', 'py': 'songyuan'},
                  {'name': '四平', 'py': 'siping'}, {'name': '通化', 'py': 'tonghua'}, {'name': '延边', 'py': 'yanbian'},
                  {'name': '沈阳', 'py': 'shenyang'}, {'name': '大连', 'py': 'dalian'}, {'name': '鞍山', 'py': 'anshan'},
                  {'name': '营口', 'py': 'yingkou'}, {'name': '本溪', 'py': 'benxi'}, {'name': '朝阳', 'py': 'chaoyang'},
                  {'name': '丹东', 'py': 'dandong'}, {'name': '抚顺', 'py': 'fushun'}, {'name': '阜新', 'py': 'fuxin'},
                  {'name': '葫芦岛', 'py': 'huludao'}, {'name': '锦州', 'py': 'jinzhou'}, {'name': '辽阳', 'py': 'liaoyang'},
                  {'name': '盘锦', 'py': 'panjin'}, {'name': '铁岭', 'py': 'tieling'},
                  {'name': '呼和浩特', 'py': 'huhehaote'}, {'name': '包头', 'py': 'baotou'}, {'name': '赤峰', 'py': 'chifeng'},
                  {'name': '通辽', 'py': 'tongliao'}, {'name': '鄂尔多斯', 'py': 'eerduosi'},
                  {'name': '阿拉善盟', 'py': 'alashanmeng'}, {'name': '巴彦淖尔', 'py': 'bayannaoer'},
                  {'name': '呼伦贝尔', 'py': 'hulunbeier'}, {'name': '兴安盟', 'py': 'xinganmeng'},
                  {'name': '乌兰察布', 'py': 'wulanchabu'}, {'name': '乌海', 'py': 'wuhai'},
                  {'name': '锡林郭勒盟', 'py': 'xilinguolemeng'},
                  {'name': '银川', 'py': 'yinchuan'}, {'name': '固原', 'py': 'guyuan'}, {'name': '石嘴山', 'py': 'shizuishan'},
                  {'name': '吴忠', 'py': 'wuzhong'}, {'name': '中卫', 'py': 'zhongwei'}, {'name': '西宁', 'py': 'xining'},
                  {'name': '果洛', 'py': 'guoluo'}, {'name': '海西', 'py': 'haixi'}, {'name': '海东', 'py': 'haidong'},
                  {'name': '海北', 'py': 'haibei'}, {'name': '黄南', 'py': 'huangnan'}, {'name': '海南', 'py': 'hai_nan'},
                  {'name': '玉树', 'py': 'yushu'},
                  {'name': '西安', 'py': 'xian'}, {'name': '榆林', 'py': 'yulin'}, {'name': '安康', 'py': 'ankang'},
                  {'name': '宝鸡', 'py': 'baoji'}, {'name': '汉中', 'py': 'hanzhong'}, {'name': '商洛', 'py': 'shangluo'},
                  {'name': '铜川', 'py': 'tongchuan'}, {'name': '渭南', 'py': 'weinan'}, {'name': '咸阳', 'py': 'xianyang'},
                  {'name': '西咸新区', 'py': 'xixianxinqu'}, {'name': '延安', 'py': 'yanan'},
                  {'name': '成都', 'py': 'chengdu'}, {'name': '德阳', 'py': 'deyang'}, {'name': '绵阳', 'py': 'mianyang'},
                  {'name': '南充', 'py': 'nanchong'}, {'name': '阿坝', 'py': 'aba'}, {'name': '巴中', 'py': 'bazhong'},
                  {'name': '达州', 'py': 'dazhou'}, {'name': '广元', 'py': 'guangyuan'}, {'name': '广安', 'py': 'guangan'},
                  {'name': '甘孜', 'py': 'ganzi'}, {'name': '凉山', 'py': 'liangshan'}, {'name': '乐山', 'py': 'leshan'},
                  {'name': '泸州', 'py': 'luzhou'}, {'name': '眉山', 'py': 'meishan'}, {'name': '内江', 'py': 'neijiang'},
                  {'name': '攀枝花', 'py': 'panzhihua'}, {'name': '遂宁', 'py': 'suining'}, {'name': '宜宾', 'py': 'yibin'},
                  {'name': '雅安', 'py': 'yaan'}, {'name': '资阳', 'py': 'ziyang'}, {'name': '自贡', 'py': 'zigong'},
                  {'name': '上海', 'py': 'shanghai'},
                  {'name': '太原', 'py': 'taiyuan'}, {'name': '大同', 'py': 'datong'}, {'name': '长治', 'py': 'zhangzhi'},
                  {'name': '晋城', 'py': 'jincheng'}, {'name': '晋中', 'py': 'jinzhong'}, {'name': '运城', 'py': 'yuncheng'},
                  {'name': '临汾', 'py': 'linfen'}, {'name': '吕梁', 'py': 'lvliang'}, {'name': '朔州', 'py': 'shuozhou'},
                  {'name': '忻州', 'py': 'xinzhou'}, {'name': '阳泉', 'py': 'yangquan'},
                  {'name': '济南', 'py': 'jinan'}, {'name': '青岛', 'py': 'qingdao'}, {'name': '淄博', 'py': 'zibo'},
                  {'name': '枣庄', 'py': 'zaozhuang'}, {'name': '东营', 'py': 'dongying'}, {'name': '烟台', 'py': 'yantai'},
                  {'name': '潍坊', 'py': 'weifang'}, {'name': '济宁', 'py': 'jining'}, {'name': '泰安', 'py': 'taian'},
                  {'name': '威海', 'py': 'weihai'}, {'name': '日照', 'py': 'rizhao'}, {'name': '莱芜', 'py': 'laiwu'},
                  {'name': '临沂', 'py': 'linyi'}, {'name': '德州', 'py': 'dezhou'}, {'name': '聊城', 'py': 'liaocheng'},
                  {'name': '滨州', 'py': 'binzhou'}, {'name': '菏泽', 'py': 'heze'}, {'name': '天津', 'py': 'tianjin'},
                  {'name': '乌鲁木齐', 'py': 'wulumuqi'}, {'name': '阿克苏', 'py': 'akesu'}, {'name': '阿勒泰', 'py': 'aletai'},
                  {'name': '阿拉尔', 'py': 'aral'}, {'name': '北屯', 'py': 'beitun'}, {'name': '博尔塔拉', 'py': 'boertala'},
                  {'name': '巴音郭楞', 'py': 'bayinguoleng'}, {'name': '昌吉', 'py': 'changji'}, {'name': '哈密', 'py': 'hami'},
                  {'name': '和田', 'py': 'hetian'}, {'name': '伊犁', 'py': 'yili'}, {'name': '克拉玛依', 'py': 'kelamayi'},
                  {'name': '克孜勒苏', 'py': 'kezilesu'}, {'name': '喀什', 'py': 'kashen'}, {'name': '可克达拉', 'py': 'kokdala'},
                  {'name': '昆玉', 'py': 'kunyu'}, {'name': '塔城', 'py': 'tacheng'}, {'name': '石河子', 'py': 'shihezi'},
                  {'name': '双河', 'py': 'shuanghe'}, {'name': '铁门关', 'py': 'tiemenguan'},
                  {'name': '图木舒克', 'py': 'tumxuk'}, {'name': '吐鲁番', 'py': 'turpan'}, {'name': '五家渠', 'py': 'wujiaqu'},
                  {'name': '拉萨', 'py': 'lasa'}, {'name': '林芝', 'py': 'nyingchi'}, {'name': '那曲', 'py': 'naqu'},
                  {'name': '阿里', 'py': 'ali'}, {'name': '昌都', 'py': 'qamdo'}, {'name': '日喀则', 'py': 'rikaze'},
                  {'name': '山南', 'py': 'shannan'},
                  {'name': '昆明', 'py': 'kunming'}, {'name': '曲靖', 'py': 'qujing'}, {'name': '保山', 'py': 'baoshan'},
                  {'name': '楚雄', 'py': 'chuxiong'}, {'name': '大理', 'py': 'dali'}, {'name': '德宏', 'py': 'dehong'},
                  {'name': '迪庆', 'py': 'diqing'}, {'name': '红河', 'py': 'honghe'}, {'name': '临沧', 'py': 'lincang'},
                  {'name': '丽江', 'py': 'lijiang'}, {'name': '怒江', 'py': 'nujiang'}, {'name': '普洱', 'py': 'puer'},
                  {'name': '文山', 'py': 'wenshan'}, {'name': '西双版纳', 'py': 'xishuangbanna'},
                  {'name': '玉溪', 'py': 'yuxi'}, {'name': '昭通', 'py': 'zhaotong'},
                  {'name': '杭州', 'py': 'hangzhou'}, {'name': '宁波', 'py': 'ningbo'}, {'name': '温州', 'py': 'wenzhou'},
                  {'name': '嘉兴', 'py': 'jiaxing'}, {'name': '湖州', 'py': 'huzhou'}, {'name': '绍兴', 'py': 'shaoxing'},
                  {'name': '金华', 'py': 'jinhua'}, {'name': '衢州', 'py': 'quzhou'}, {'name': '台州', 'py': 'taizhou'},
                  {'name': '丽水', 'py': 'lishui'}, {'name': '舟山', 'py': 'zhoushan'},
                  {'name': '舟山群岛新区', 'py': 'zhoushanxinqu'}]

        for href in response.xpath('//li[@class="carbrand"]/@data-pinyin').extract():
            for city in cities:
                brand = href
                city_py = city['py']
                url = "http://www.che168.com/" + city_py + "/" + brand + "/"
                yield scrapy.Request(url, callback=self.select1_parse)

    # car select
    def select1_parse(self, response):
        # car select
        for href in response.xpath('//ul[@class="fn-clear certification-list"]/li')[20:30]:
            urlbase = href.xpath("./a/@href").extract_first()
            datasave1 = href.extract()
            url = response.urljoin(urlbase)
            yield scrapy.Request(url, meta={"datasave1":datasave1}, callback=self.parse_car)

        # next page
        next_page = response.xpath('//a[@class="page-item-next"]/@href')
        if next_page:
            url_next = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url_next, self.select1_parse)

    # get car info
    def parse_car(self, response):
        # status check
        if response.status==200 and len(response.xpath('//html').extract_first()) >=8000:
            # count
            self.counts += 1
            logging.log(msg="download   " + str(self.counts) + "   items", level=logging.INFO)

            # key and status (sold or sale, price,time)
            status = response.xpath('//span[@class="be-scheduled" or @class="tag tag-sale"]')
            if status:
                status = 'sold'
            else:
                status = 'sale'

            price = ".".join(response.xpath('//div[@class="car-price"]/ins/text()').re('\d+'))
            price = price if price else "zero"
            pagetime = "zero"

            # datasave
            if 'datasave1' in response.meta:
                datasave1 = response.meta['datasave1']
            else:
                datasave1 = 'zero'

            # extra
            specid = response.xpath('//input[@id="car_specid"]/@value')
            if specid:
                url = 'https://cacheapi.che168.com/quoted/dealerminpricebyspec.ashx?specid=' + specid.extract_first()
                res = requests.get(url)
                info = json.loads(res.content.decode())
                guideprice = info['result']['price']
                guidepricetax = info['result']['tax']
            else:
                guideprice = '-'
                guidepricetax = '-'

            print(guideprice, guidepricetax)

            #item loader
            item = Che168()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url+ "-" + str(price) + "-" + str(status)+"-" + pagetime
            item['pagetime'] = pagetime
            item['datasave'] = [datasave1, response.xpath('//html').extract_first()]

            # extra
            item['guideprice'] = guideprice
            item['guidepricetax'] = str(float(guidepricetax) + float(guideprice))

            # yield item
            print(item)



