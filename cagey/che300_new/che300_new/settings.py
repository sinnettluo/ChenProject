# -*- coding: utf-8 -*-

# Scrapy settings for che300_new project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'che300_new'

SPIDER_MODULES = ['che300_new.spiders']
NEWSPIDER_MODULE = 'che300_new.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'che300_new (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

LOG_LEVEL = 'DEBUG'

""" mysql 配置"""
MYSQL_DB = ''
MYSQL_TABLE = ''
MYSQL_PORT = '3306'
MYSQL_SERVER = '192.168.1.94'
MYSQL_USER = "dataUser94"
MYSQL_PWD = "94dataUser@2020"


""" mongodb 配置 """
MONGODB_SERVER = '192.168.1.94'
MONGODB_PORT = 27017
MONGODB_DB = ''
MONGODB_USER = ''
MONGODB_PWD = ''
# 存放本次数据的表名称
MONGODB_COLLECTION = ''

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'che300_new.middlewares.Che300NewSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'che300_new.middlewares.Che300NewDownloaderMiddleware': 543,
    'che300_new.middlewares.Che300NewProxyMiddleware': 400,
    'che300_new.middlewares.Che300NewUserAgentMiddleware': 100,
    'che300_new.middlewares.MyproxiesSpiderMiddleware': 500,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'che300_new.pipelines.Che300NewPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 出现错误吗,重新请求
# RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]
RETRY_HTTP_CODES = [400, 403, 404, 408]
# 是否开启重试
RETRY_ENABLED = True
# 重试次数
RETRY_TIMES = 3

""" redis 配置"""
# # Redis URL
REDIS_URL = 'redis://192.168.1.249:6379'
FEED_EXPORT_ENCODING = 'utf-8'

# # 使用布隆过滤器
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# # 增加调度配置
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 指定排序爬取地址时使用的队列，
# 默认的 按优先级排序(Scrapy默认)，由sorted set实现的一种非FIFO、LIFO方式。
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# 可选的 按先进先出排序（FIFO）
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
# 可选的 按后进先出排序（LIFO）
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

# True：redis中以set集合提取数据的方式提取
# False：redis中以list列表提取数据的方式提取
# REDIS_START_URLS_AS_SET = False

# # Number of Hash Functions to use, defaults to 6
# BLOOMFILTER_HASH_NUMBER = 6
#
# # Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
# BLOOMFILTER_BIT = 30

# 配置调度器持久化, 爬虫结束, 要不要清空Redis中请求队列和去重指纹的set。如果True, 就表示要持久化存储, 否则清空数据
SCHEDULER_PERSIST = False

IDLE_NUMBER = 12  #12*5=60s 一分钟




