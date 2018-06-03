# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector as sel


class GeoSpider(scrapy.Spider):
    name = 'geo'
    allowed_domains = ['geonames.org']
    start_urls = ['http://www.geonames.org/search.html?q=moscow&country=RU&startRow=0']

    def parse(self, response):
    	s = sel(response)
    	hrefs = s.xpath('//table[@class="restable"]/tr/td/a/@href').extract()
    	for h in hrefs:
    		if 'map' in h:
				result = re.findall(r'google_(.*)\.html', h)
				print result
    	

