from scrapy.cmdline import execute

import sys
import os

website = 'yiche_newcar_2019_02'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])
