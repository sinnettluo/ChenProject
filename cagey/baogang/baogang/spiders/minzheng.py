# -*- coding: utf-8 -*-
import scrapy
import time
from baogang.items import XingzhengItem


class MinzhengSpider(scrapy.Spider):
    name = 'minzheng'
    allowed_domains = ['xzqh.mca.gov.cn']
    # start_urls = ['http://xzqh.mca.gov.cn/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MYSQL_USER': 'dataUser94',
        'MYSQL_PWD': '94dataUser@2020',
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_PORT': 3306,
        'MYSQL_DB': 'xingzhengqu',
        'MYSQL_TABLE': 'xingzhengqu',
        # 'REDIS_URL': 'redis://192.168.1.241:6379/10',
        # 'SCHEDULER_PERSIST': False,
        # 'MONGODB_SERVER': '180.167.80.118',
        # 端口号，默认是27017
        # 'MONGODB_PORT': 1206,
        # 'MONGODB_DB': 'baogang',
        # 'MONGODB_COLLECTION': 'ouyeel_new',
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 0,
        # 'LOG_LEVEL': 'INFO',
        'DOWNLOADER_MIDDLEWARES': {
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
            # 'baogang.middlewares.SeleniumMiddleware': 300,
            # 'baogang.middlewares.SeleniumFirefoxMiddleware': 301,

        },
    }

    def __init__(self, **kwargs):
        super(MinzhengSpider, self).__init__(**kwargs)
        self.detail_url = 'https://www.ouyeel.com/buyer-ng/resource/resourceData?resourceType=10&resId=1392404789'
        self.k = []

    def start_requests(self):
        url_list = "http://xzqh.mca.gov.cn/defaultQuery?shengji=-1&diji=-1&xianji=-1"
        # for url in url_list:
        yield scrapy.Request(
            url=url_list,
        )

    def parse(self, response):
        # if 'tp=4' not in response.url:
        tr_list = response.xpath("//tr[@class='shi_nub']")
        for tr in tr_list:
            item = XingzhengItem()
            item["diji"] = tr.xpath("./td[1]/a[2]/text()").get()
            item["zhudi"] = tr.xpath("./td[2]//text()").get()
            item["people"] = tr.xpath("./td[3]//text()").get().replace("\t", "").replace("\n", "").replace("\r", "").replace(" ", "")
            item["area"] = tr.xpath("./td[4]//text()").get().replace("\t", "").replace("\n", "").replace("\r", "").replace(" ", "")
            item["xz_code"] = tr.xpath("./td[5]//text()").get()
            item["area_code"] = tr.xpath("./td[6]//text()").get()
            item["postal_code"] = tr.xpath("./td[7]//text()").get()
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            try:
                item["shengji"] = area_dic[item["diji"]]
            except :
                item["shengji"] = item["diji"]
            # print(item)
            yield item
        dq_tr_list = response.xpath("//tr[@type='2']")
        for dq_tr in dq_tr_list:
            item = XingzhengItem()
            item["xianji"] = dq_tr.xpath("./td[1]/text()").get()
            item["zhudi"] = dq_tr.xpath("./td[2]/text()").get().replace(" ", "")
            item["people"] = dq_tr.xpath("./td[3]/text()").get()
            item["area"] = dq_tr.xpath("./td[4]/text()").get()
            item["xz_code"] = dq_tr.xpath("./td[5]/text()").get()
            item["area_code"] = dq_tr.xpath("./td[6]/text()").get()
            item["postal_code"] = dq_tr.xpath("./td[7]/text()").get()
            item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item["diji"] = dq_tr.xpath("./@parent").get()
            try:
                item["shengji"] = area_dic[item["diji"]]
            except :
                item["shengji"] = item["diji"]
            yield item
            # print(item)


area_dic = {'北京市': '北京市(京)',
 '天津市': '天津市(津)',
 '石家庄市': '河北省(冀)',
 '唐山市': '河北省(冀)',
 '秦皇岛市': '河北省(冀)',
 '邯郸市': '河北省(冀)',
 '邢台市': '河北省(冀)',
 '保定市': '河北省(冀)',
 '张家口市': '河北省(冀)',
 '承德市': '河北省(冀)',
 '沧州市': '河北省(冀)',
 '廊坊市': '河北省(冀)',
 '衡水市': '河北省(冀)',
 '太原市': '山西省(晋)',
 '大同市': '山西省(晋)',
 '阳泉市': '山西省(晋)',
 '长治市': '山西省(晋)',
 '晋城市': '山西省(晋)',
 '朔州市': '山西省(晋)',
 '晋中市': '山西省(晋)',
 '运城市': '山西省(晋)',
 '忻州市': '山西省(晋)',
 '临汾市': '山西省(晋)',
 '吕梁市': '山西省(晋)',
 '呼和浩特市': '内蒙古自治区(内蒙古)',
 '包头市': '内蒙古自治区(内蒙古)',
 '乌海市': '内蒙古自治区(内蒙古)',
 '赤峰市': '内蒙古自治区(内蒙古)',
 '通辽市': '内蒙古自治区(内蒙古)',
 '鄂尔多斯市': '内蒙古自治区(内蒙古)',
 '呼伦贝尔市': '内蒙古自治区(内蒙古)',
 '巴彦淖尔市': '内蒙古自治区(内蒙古)',
 '乌兰察布市': '内蒙古自治区(内蒙古)',
 '兴安盟': '内蒙古自治区(内蒙古)',
 '锡林郭勒盟': '内蒙古自治区(内蒙古)',
 '阿拉善盟': '内蒙古自治区(内蒙古)',
 '沈阳市': '辽宁省(辽)',
 '大连市': '辽宁省(辽)',
 '鞍山市': '辽宁省(辽)',
 '抚顺市': '辽宁省(辽)',
 '本溪市': '辽宁省(辽)',
 '丹东市': '辽宁省(辽)',
 '锦州市': '辽宁省(辽)',
 '营口市': '辽宁省(辽)',
 '阜新市': '辽宁省(辽)',
 '辽阳市': '辽宁省(辽)',
 '盘锦市': '辽宁省(辽)',
 '铁岭市': '辽宁省(辽)',
 '朝阳市': '辽宁省(辽)',
 '葫芦岛市': '辽宁省(辽)',
 '长春市': '吉林省(吉)',
 '吉林市': '吉林省(吉)',
 '四平市': '吉林省(吉)',
 '辽源市': '吉林省(吉)',
 '通化市': '吉林省(吉)',
 '白山市': '吉林省(吉)',
 '松原市': '吉林省(吉)',
 '白城市': '吉林省(吉)',
 '延边朝鲜族自治州': '吉林省(吉)',
 '哈尔滨市': '黑龙江省(黑)',
 '齐齐哈尔市': '黑龙江省(黑)',
 '鸡西市': '黑龙江省(黑)',
 '鹤岗市': '黑龙江省(黑)',
 '双鸭山市': '黑龙江省(黑)',
 '大庆市': '黑龙江省(黑)',
 '伊春市': '黑龙江省(黑)',
 '佳木斯市': '黑龙江省(黑)',
 '七台河市': '黑龙江省(黑)',
 '牡丹江市': '黑龙江省(黑)',
 '黑河市': '黑龙江省(黑)',
 '绥化市': '黑龙江省(黑)',
 '大兴安岭地区': '黑龙江省(黑)',
 '上海市': '上海市(沪)',
 '南京市': '江苏省(苏)',
 '无锡市': '江苏省(苏)',
 '徐州市': '江苏省(苏)',
 '常州市': '江苏省(苏)',
 '苏州市': '江苏省(苏)',
 '南通市': '江苏省(苏)',
 '连云港市': '江苏省(苏)',
 '淮安市': '江苏省(苏)',
 '盐城市': '江苏省(苏)',
 '扬州市': '江苏省(苏)',
 '镇江市': '江苏省(苏)',
 '泰州市': '江苏省(苏)',
 '宿迁市': '江苏省(苏)',
 '杭州市': '浙江省(浙)',
 '宁波市': '浙江省(浙)',
 '温州市': '浙江省(浙)',
 '嘉兴市': '浙江省(浙)',
 '湖州市': '浙江省(浙)',
 '绍兴市': '浙江省(浙)',
 '金华市': '浙江省(浙)',
 '衢州市': '浙江省(浙)',
 '舟山市': '浙江省(浙)',
 '台州市': '浙江省(浙)',
 '丽水市': '浙江省(浙)',
 '合肥市': '安徽省(皖)',
 '芜湖市': '安徽省(皖)',
 '蚌埠市': '安徽省(皖)',
 '淮南市': '安徽省(皖)',
 '马鞍山市': '安徽省(皖)',
 '淮北市': '安徽省(皖)',
 '铜陵市': '安徽省(皖)',
 '安庆市': '安徽省(皖)',
 '黄山市': '安徽省(皖)',
 '滁州市': '安徽省(皖)',
 '阜阳市': '安徽省(皖)',
 '宿州市': '安徽省(皖)',
 '六安市': '安徽省(皖)',
 '亳州市': '安徽省(皖)',
 '池州市': '安徽省(皖)',
 '宣城市': '安徽省(皖)',
 '福州市': '福建省(闽)',
 '厦门市': '福建省(闽)',
 '莆田市': '福建省(闽)',
 '三明市': '福建省(闽)',
 '泉州市': '福建省(闽)',
 '漳州市': '福建省(闽)',
 '南平市': '福建省(闽)',
 '龙岩市': '福建省(闽)',
 '宁德市': '福建省(闽)',
 '南昌市': '江西省(赣)',
 '景德镇市': '江西省(赣)',
 '萍乡市': '江西省(赣)',
 '九江市': '江西省(赣)',
 '新余市': '江西省(赣)',
 '鹰潭市': '江西省(赣)',
 '赣州市': '江西省(赣)',
 '吉安市': '江西省(赣)',
 '宜春市': '江西省(赣)',
 '抚州市': '江西省(赣)',
 '上饶市': '江西省(赣)',
 '济南市': '山东省(鲁)',
 '青岛市': '山东省(鲁)',
 '淄博市': '山东省(鲁)',
 '枣庄市': '山东省(鲁)',
 '东营市': '山东省(鲁)',
 '烟台市': '山东省(鲁)',
 '潍坊市': '山东省(鲁)',
 '济宁市': '山东省(鲁)',
 '泰安市': '山东省(鲁)',
 '威海市': '山东省(鲁)',
 '日照市': '山东省(鲁)',
 '临沂市': '山东省(鲁)',
 '德州市': '山东省(鲁)',
 '聊城市': '山东省(鲁)',
 '滨州市': '山东省(鲁)',
 '菏泽市': '山东省(鲁)',
 '郑州市': '河南省(豫)',
 '开封市': '河南省(豫)',
 '洛阳市': '河南省(豫)',
 '平顶山市': '河南省(豫)',
 '安阳市': '河南省(豫)',
 '鹤壁市': '河南省(豫)',
 '新乡市': '河南省(豫)',
 '焦作市': '河南省(豫)',
 '濮阳市': '河南省(豫)',
 '许昌市': '河南省(豫)',
 '漯河市': '河南省(豫)',
 '三门峡市': '河南省(豫)',
 '南阳市': '河南省(豫)',
 '商丘市': '河南省(豫)',
 '信阳市': '河南省(豫)',
 '周口市': '河南省(豫)',
 '驻马店市': '河南省(豫)',
 '武汉市': '湖北省(鄂)',
 '黄石市': '湖北省(鄂)',
 '十堰市': '湖北省(鄂)',
 '宜昌市': '湖北省(鄂)',
 '襄阳市': '湖北省(鄂)',
 '鄂州市': '湖北省(鄂)',
 '荆门市': '湖北省(鄂)',
 '孝感市': '湖北省(鄂)',
 '荆州市': '湖北省(鄂)',
 '黄冈市': '湖北省(鄂)',
 '咸宁市': '湖北省(鄂)',
 '随州市': '湖北省(鄂)',
 '恩施土家族苗族自治州': '湖北省(鄂)',
 '长沙市': '湖南省(湘)',
 '株洲市': '湖南省(湘)',
 '湘潭市': '湖南省(湘)',
 '衡阳市': '湖南省(湘)',
 '邵阳市': '湖南省(湘)',
 '岳阳市': '湖南省(湘)',
 '常德市': '湖南省(湘)',
 '张家界市': '湖南省(湘)',
 '益阳市': '湖南省(湘)',
 '郴州市': '湖南省(湘)',
 '永州市': '湖南省(湘)',
 '怀化市': '湖南省(湘)',
 '娄底市': '湖南省(湘)',
 '湘西土家族苗族自治州': '湖南省(湘)',
 '广州市': '广东省(粤)',
 '韶关市': '广东省(粤)',
 '深圳市': '广东省(粤)',
 '珠海市': '广东省(粤)',
 '汕头市': '广东省(粤)',
 '佛山市': '广东省(粤)',
 '江门市': '广东省(粤)',
 '湛江市': '广东省(粤)',
 '茂名市': '广东省(粤)',
 '肇庆市': '广东省(粤)',
 '惠州市': '广东省(粤)',
 '梅州市': '广东省(粤)',
 '汕尾市': '广东省(粤)',
 '河源市': '广东省(粤)',
 '阳江市': '广东省(粤)',
 '清远市': '广东省(粤)',
 '东莞市': '广东省(粤)',
 '中山市': '广东省(粤)',
 '潮州市': '广东省(粤)',
 '揭阳市': '广东省(粤)',
 '云浮市': '广东省(粤)',
 '南宁市': '广西壮族自治区(桂)',
 '柳州市': '广西壮族自治区(桂)',
 '桂林市': '广西壮族自治区(桂)',
 '梧州市': '广西壮族自治区(桂)',
 '北海市': '广西壮族自治区(桂)',
 '防城港市': '广西壮族自治区(桂)',
 '钦州市': '广西壮族自治区(桂)',
 '贵港市': '广西壮族自治区(桂)',
 '玉林市': '广西壮族自治区(桂)',
 '百色市': '广西壮族自治区(桂)',
 '贺州市': '广西壮族自治区(桂)',
 '河池市': '广西壮族自治区(桂)',
 '来宾市': '广西壮族自治区(桂)',
 '崇左市': '广西壮族自治区(桂)',
 '海口市': '海南省(琼)',
 '三亚市': '海南省(琼)',
 '三沙市☆': '海南省(琼)',
 '儋州市': '海南省(琼)',
 '重庆市': '重庆市(渝)',
 '成都市': '四川省(川、蜀)',
 '自贡市': '四川省(川、蜀)',
 '攀枝花市': '四川省(川、蜀)',
 '泸州市': '四川省(川、蜀)',
 '德阳市': '四川省(川、蜀)',
 '绵阳市': '四川省(川、蜀)',
 '广元市': '四川省(川、蜀)',
 '遂宁市': '四川省(川、蜀)',
 '内江市': '四川省(川、蜀)',
 '乐山市': '四川省(川、蜀)',
 '南充市': '四川省(川、蜀)',
 '眉山市': '四川省(川、蜀)',
 '宜宾市': '四川省(川、蜀)',
 '广安市': '四川省(川、蜀)',
 '达州市': '四川省(川、蜀)',
 '雅安市': '四川省(川、蜀)',
 '巴中市': '四川省(川、蜀)',
 '资阳市': '四川省(川、蜀)',
 '阿坝藏族羌族自治州': '四川省(川、蜀)',
 '甘孜藏族自治州': '四川省(川、蜀)',
 '凉山彝族自治州': '四川省(川、蜀)',
 '贵阳市': '贵州省(黔、贵)',
 '六盘水市': '贵州省(黔、贵)',
 '遵义市': '贵州省(黔、贵)',
 '安顺市': '贵州省(黔、贵)',
 '毕节市': '贵州省(黔、贵)',
 '铜仁市': '贵州省(黔、贵)',
 '黔西南布依族苗族自治州': '贵州省(黔、贵)',
 '黔东南苗族侗族自治州': '贵州省(黔、贵)',
 '黔南布依族苗族自治州': '贵州省(黔、贵)',
 '昆明市': '云南省(滇、云)',
 '曲靖市': '云南省(滇、云)',
 '玉溪市': '云南省(滇、云)',
 '保山市': '云南省(滇、云)',
 '昭通市': '云南省(滇、云)',
 '丽江市': '云南省(滇、云)',
 '普洱市': '云南省(滇、云)',
 '临沧市': '云南省(滇、云)',
 '楚雄彝族自治州': '云南省(滇、云)',
 '红河哈尼族彝族自治州': '云南省(滇、云)',
 '文山壮族苗族自治州': '云南省(滇、云)',
 '西双版纳傣族自治州': '云南省(滇、云)',
 '大理白族自治州': '云南省(滇、云)',
 '德宏傣族景颇族自治州': '云南省(滇、云)',
 '怒江傈僳族自治州': '云南省(滇、云)',
 '迪庆藏族自治州': '云南省(滇、云)',
 '拉萨市': '西藏自治区(藏)',
 '日喀则市': '西藏自治区(藏)',
 '昌都市': '西藏自治区(藏)',
 '林芝市': '西藏自治区(藏)',
 '山南市': '西藏自治区(藏)',
 '那曲市': '西藏自治区(藏)',
 '阿里地区': '西藏自治区(藏)',
 '西安市': '陕西省(陕、秦)',
 '铜川市': '陕西省(陕、秦)',
 '宝鸡市': '陕西省(陕、秦)',
 '咸阳市': '陕西省(陕、秦)',
 '渭南市': '陕西省(陕、秦)',
 '延安市': '陕西省(陕、秦)',
 '汉中市': '陕西省(陕、秦)',
 '榆林市': '陕西省(陕、秦)',
 '安康市': '陕西省(陕、秦)',
 '商洛市': '陕西省(陕、秦)',
 '兰州市': '甘肃省(甘、陇)',
 '嘉峪关市': '甘肃省(甘、陇)',
 '金昌市': '甘肃省(甘、陇)',
 '白银市': '甘肃省(甘、陇)',
 '天水市': '甘肃省(甘、陇)',
 '武威市': '甘肃省(甘、陇)',
 '张掖市': '甘肃省(甘、陇)',
 '平凉市': '甘肃省(甘、陇)',
 '酒泉市': '甘肃省(甘、陇)',
 '庆阳市': '甘肃省(甘、陇)',
 '定西市': '甘肃省(甘、陇)',
 '陇南市': '甘肃省(甘、陇)',
 '临夏回族自治州': '甘肃省(甘、陇)',
 '甘南藏族自治州': '甘肃省(甘、陇)',
 '西宁市': '青海省(青)',
 '海东市': '青海省(青)',
 '海北藏族自治州': '青海省(青)',
 '黄南藏族自治州': '青海省(青)',
 '海南藏族自治州': '青海省(青)',
 '果洛藏族自治州': '青海省(青)',
 '玉树藏族自治州': '青海省(青)',
 '海西蒙古族藏族自治州': '青海省(青)',
 '银川市': '宁夏回族自治区(宁)',
 '石嘴山市': '宁夏回族自治区(宁)',
 '吴忠市': '宁夏回族自治区(宁)',
 '固原市': '宁夏回族自治区(宁)',
 '中卫市': '宁夏回族自治区(宁)',
 '乌鲁木齐市': '新疆维吾尔自治区(新)',
 '克拉玛依市': '新疆维吾尔自治区(新)',
 '吐鲁番市': '新疆维吾尔自治区(新)',
 '哈密市': '新疆维吾尔自治区(新)',
 '阿克苏地区': '新疆维吾尔自治区(新)',
 '喀什地区': '新疆维吾尔自治区(新)',
 '和田地区': '新疆维吾尔自治区(新)',
 '昌吉回族自治州': '新疆维吾尔自治区(新)',
 '博尔塔拉蒙古自治州': '新疆维吾尔自治区(新)',
 '巴音郭楞蒙古自治州': '新疆维吾尔自治区(新)',
 '克孜勒苏柯尔克孜自治州': '新疆维吾尔自治区(新)',
 '伊犁哈萨克自治州☆': '新疆维吾尔自治区(新)',
 '塔城地区': '新疆维吾尔自治区(新)',
 '阿勒泰地区': '新疆维吾尔自治区(新)',
 '香港特别行政区': '香港特别行政区(港)'}