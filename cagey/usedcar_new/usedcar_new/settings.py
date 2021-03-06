# -*- coding: utf-8 -*-

# Scrapy settings for usedcar_new project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'usedcar_new'

SPIDER_MODULES = ['usedcar_new.spiders']
NEWSPIDER_MODULE = 'usedcar_new.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'usedcar_new (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

MYSQL_SERVER = "192.168.1.94"
MYSQL_USER = "dataUser94"
MYSQL_PWD= "94dataUser@2020"
MYSQL_PORT = 3306
MYSQL_DB = "usedcar_update"
MYSQL_TABLE = ""

MONGODB_SERVER = "192.168.1.92"
MONGODB_PORT = 27017
MONGODB_DB = "usedcar"
MONGODB_COLLECTION = "xcar"

WEBSITE = ''

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
COOKIES_ENABLED = False

DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
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
#    'usedcar_new.middlewares.UsedcarNewSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'usedcar_new.middlewares.UsedcarNewDownloaderMiddleware': 543,
   # 'usedcar_new.middlewares.SeleniumMiddleware': 600,
   # 'usedcar_new.middlewares.ProxyMiddleware': 700,
   'scrapy.downloadermiddlewares.retry.RetryMiddleware': 800,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'usedcar_new.pipelines.UsedcarNewPipeline': 300,
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

# DOWNLOAD_TIMEOUT = 8

PHANTOMJS_PATH = "/usr/local/phantomjs/bin/phantomjs"
CHROME_PATH = "/usr/local/bin/chromedriver"

REDIRECT_ENABLED = False

# ???????????????,????????????
RETRY_HTTP_CODES = [500, 502, 302]
# ??????????????????
RETRY_ENABLED = True
# ????????????
RETRY_TIMES = 5


HTTPERROR_ALLOWED_CODES = [301, 302, 503]

REDIS_URL = "redis://192.168.1.92:6379/15"

# ?????????????????????
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER_PERSIST = True

# ?????????????????????
# DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# # # ??????????????????
# SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"

# ????????????????????????, ????????????, ???????????????Redis?????????????????????????????????set?????????True, ???????????????????????????, ??????????????????
SCHEDULER_PERSIST = False

