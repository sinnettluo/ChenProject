# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import traceback
import logging

import requests
from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from scrapy.utils.python import global_object_name
from twisted.internet.error import TimeoutError
import base64
import logging
logger = logging.getLogger(__name__)

from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from scrapy.http import TextResponse

from gzip import GzipFile
from io import BytesIO
import gzip
import urllib.request
import io

def dezip(data):
    # buf = BytesIO(data)
    f = GzipFile(fileobj=data)
    content = f.read()
    encoded_content = gzip.decompress(content).decode("utf-8")
    return encoded_content

def print_object(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))

class UsedcarNewDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.



        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


def getProxy():
    s = requests.session()
    s.keep_alive = False
    # url = 'http://192.168.2.120:5000'
    url = 'http://120.27.216.150:5000'
    proxy = s.get(url, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        request.headers.setdefault('User-Agent', ua)

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    ]


class SeleniumMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # ?????????????????????????????????????????????12??????1??????
        timeout = 30
        # ?????????????????????
        ext = cls(crawler, timeout)
        # ????????????????????????????????? ???signals.spider_idle ??? spider_idle() ?????????????????????
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def __init__(self, crawler, timeout):
        self.crawler = crawler
        self.driver = webdriver.PhantomJS()
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('disable-infobars')
        # self.driver = webdriver.Chrome(options=options, executable_path=settings["CHROME_PATH"])
        # self.driver = webdriver.Chrome(options=options)

    def process_request(self, request, spider):
        if spider.name in ['hry2car']:
            if '/s' in request.url:
                self.driver.get(request.url)
                data = self.driver.page_source.encode()

                res = HtmlResponse(
                    url=request.url,
                    body=data,
                    request=request,
                    encoding='utf-8'
                )
                return res

    def spider_closed(self, spider):
        self.driver.quit()
        print("??????????????????!")


class ProxyMiddleware(object):

    # def __init__(self):
    #     self.count = 0
    #     self.proxy = "http://" + getProxy()

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            self.proxy = "http://" + getProxy()
            request.meta['proxy'] = self.proxy
            print(f'Get a new ip {self.proxy}!')
            return request

    def process_request(self, request, spider):
        if spider.name in ['youxinpai2', 'chezhibao2', 'youxin', 'ganji', 'youxin_master', 'youxin_test']:
            self.proxy = "http://" + getProxy()
            # if self.count < 2:
            #     request.meta['proxy'] = self.proxy
            #     self.count += 1
            # else:
            #     self.proxy = "http://" + getProxy()
            #     self.count = 0
            request.meta['proxy'] = self.proxy
            print(f'proxy success : {self.proxy}!')

    def process_response(self, request, spider, response):
        # if '??????????????????' in res:
        #     print(res)
        #     print(response.url)
        #     print("1" * 100)
        # if 'arg1' in res:
        #     print(res)
        #     print(response.url)
        #     print("2" * 100)
        return response


class SeleniumIPMiddleware(object):
    """
    selenium ??????????????????ip
    """

    @classmethod
    def from_crawler(cls, crawler):
        # ?????????????????????????????????????????????12??????1??????
        # idle_number = crawler.settings.getint('IDLE_NUMBER', 12)
        timeout = 30
        # ?????????????????????
        ext = cls(crawler, timeout)
        # ????????????????????????????????? ???signals.spider_idle ??? spider_idle() ?????????????????????
        # crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def __init__(self, crawler, timeout):
        self.crawler = crawler
        profile = FirefoxProfile()
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        # ???????????????Chrome????????????????????????????????????
        options.add_argument('disable-infobars')
        # ??????????????????
        profile.set_preference('permissions.default.image', 2)
        # ????????????css?????????
        profile.set_preference('permissions.default.stylesheet', 2)
        options.set_preference("dom.webnotifications.enabled", False)
        # ????????????????????????
        # none?????????br.get??????????????????????????????????????????????????????????????????br????????????????????????url???pagesource????????????
        # desired_capabilities = DesiredCapabilities.CHROME
        # desired_capabilities["pageLoadStrategy"] = "none"
        # self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options,desired_capabilities=desired_capabilities)
        self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        # self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', firefox_profile=profile, firefox_options=options)
        # self.browser_detail = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        self.timeout = timeout
        self.browser.set_page_load_timeout(self.timeout)  # ????????????????????????
        self.browser.set_script_timeout(self.timeout)  # ??????????????????js????????????
        # self.wait = WebDriverWait(self.browser, self.timeout, poll_frequency=0.5)

    def __del__(self):
        self.browser.close()
        # self.browser_detail.close()

    def spider_closed(self, spider):
        self.browser.quit()
        print("??????????????????!")

    def process_request(self, request, spider):
        if spider.name in ['ganji', 'youxin', 'youxin_master']:
            if 'shanghai' in request.url or 'cityid' in request.url:
                proxy, ip, port = self.get_Proxy()
                self.set_proxy(self.browser, ip=ip, port=port)
                browser = self.browser
                # ????????????
                main_win = browser.current_window_handle  # ???????????????????????????
                all_win = browser.window_handles
                try:
                    if len(all_win) == 1:
                        logging.info("-------------------???????????????-------------------")
                        js = 'window.open("https://www.baidu.com");'
                        browser.execute_script(js)
                        # ???????????????main_win??????
                        for win in all_win:
                            if main_win != win:
                                print('?????????WIN', win, 'Main', main_win)
                                browser.switch_to.window(main_win)
                    # ????????????????????????URL
                    browser.get(request.url)
                    # WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.ID, "viewAll")))
                    url = browser.current_url
                    body = browser.page_source

                    if '???????????????????????????' or '??????????????????' in browser.page_source:
                        pass
                    else:
                        # WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'??????')]/preceding-sibling::input"))).click()
                        return HtmlResponse(url=url, body=body, encoding="utf-8", flags=[])
                except:
                    # ??????
                    logging.info("-------------------Time out-------------------")
                    # ???????????????????????????
                    for win in all_win:
                        if main_win != win:
                            logging.info("-------------------??????????????????-------------------")
                            print('WIN', win, 'Main', main_win)
                            browser.close()
                            browser.switch_to.window(win)
                            main_win = win

                    js = 'window.open("https://www.baidu.com");'
                    browser.execute_script(js)
                    if 'time' in str(traceback.format_exc()):
                        # print('??????????????????')
                        logging.info("-------------------??????????????????-------------------")



    def get_Proxy(self):
        # url = 'http://120.27.216.150:5000'
        url = 'http://192.168.2.120:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        ip = proxy.split(":")[0]
        port = proxy.split(":")[1]
        return proxy, ip, port

    def set_proxy(self, driver, ip='', port=0):
        driver.get("about:config")
        script = '''
                    var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
                    prefs.setIntPref("network.proxy.type", 1);
                    prefs.setCharPref("network.proxy.http", "{ip}");
                    prefs.setIntPref("network.proxy.http_port", "{port}");
                    prefs.setCharPref("network.proxy.ssl", "{ip}");
                    prefs.setIntPref("network.proxy.ssl_port", "{port}");
                    prefs.setCharPref("network.proxy.ftp", "{ip}");
                    prefs.setIntPref("network.proxy.ftp_port", "{port}");
        ????????????????????? prefs.setBoolPref("general.useragent.site_specific_overrides",true);
        ????????????????????? prefs.setBoolPref("general.useragent.updates.enabled",true);
                    '''.format(ip=ip, port=port)
        driver.execute_script(script)


class MyproxiesSpiderMiddleware(RetryMiddleware):

    def __init__(self, name):
        super(MyproxiesSpiderMiddleware, self).__init__(name)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            print(response.status)
            print("-"*100)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        # if '??????????????????????????????' in response.body.decode("utf-8"):
        #     reason = "??????????????????????????????"
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        retry_times = self.max_retry_times

        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']

        stats = spider.crawler.stats
        if retries <= retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            # ??????????????????,????????????
            proxy_ip = "http://" + getProxy()
            retryreq.meta['proxy'] = proxy_ip

            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            # print(retryreq)
            # print("*"*100)
            return retryreq
        else:
            stats.inc_value('retry/max_reached')
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})

import redis
pool = redis.ConnectionPool(host='192.168.1.92', port=6379, db=14)
con = redis.Redis(connection_pool=pool)
c = con.client()

class MoGuProxyMiddleware(object):
    def __init__(self):
        # self.proxyServer = "http://secondtransfer.moguproxy.com:9001"
        self.proxyServer = "http://transfer.mogumiao.com:9001"
        # ????????????????????????,??????????????????
        proxyUser = "pZU6DCgWGNVr6r4c"
        proxyPass = "Z0hT7xM3S6R1R2ov"
        appkey = "cFpVNkRDZ1dHTlZyNnI0YzpaMGhUN3hNM1M2UjFSMm92"
        self.proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8") # Python3
        # self.proxyAuth = "Basic" + appkey

    def process_request(self, request, spider):
        # if spider.name in ['youxin']:
        request.meta["proxy"] = self.proxyServer
        # request.headers["Proxy-Authorization"] = self.proxyAuth
        request.headers["Authorization"] = self.proxyAuth

    def process_response(self, request, response, spider):
        if response.status == 302:
            print(request.url)
            print(response.text)
            c.lpush('youxin:start_urls', response.url)
            request.meta["proxy"] = self.proxyServer
            # request.headers["Proxy-Authorization"] = self.proxyAuth
            request.headers["Authorization"] = self.proxyAuth
            return request
        else:
            return response

