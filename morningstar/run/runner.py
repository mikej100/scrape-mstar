import os
import scrapy

from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'crawl',
            'funds1',
            '-o',
            'out.json',
        ]
    )
except SystemExit:
    pass
