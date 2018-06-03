# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from items import House, Photo, Review, User
import scrapy
import json
import requests

class Airbnb0Spider(scrapy.Spider):
    name = 'airbnb0'
    allowed_domains = ['airbnb.com']
    start_urls = []

    def __init__(self, url='', *a, **data):
        super(Airbnb0Spider, self).__init__(*a, **data)
        
        print url
        self.query_text = 'Arizona'
    
    def start_requests(self):
        proxy = '192.168.244.1:8888'
        #print self.url
        yield scrapy.Request(url=self.url, callback=self.parse, meta={'proxy': proxy})
        
    def parse_review(self, json_reviews, aid):
        items = []
        for review in json_reviews['reviews']:
            r = Review()
            r['house_id'] = aid;
            r['date_review'] = review['created_at']
            r['rating'] = str(review['rating'])
            r['review'] = review['comments']
            r['username'] = review['reviewer']['first_name']
            items.append(r)
        return items

    def parse(self, response):
        print 'a1'
        ret = {}
        items = []
        lreviews = []
        lphotos = []
        lusers = []
        
        jsonresponse = json.loads(response.body_as_unicode())

        for listing in jsonresponse['explore_tabs'][0]['sections'][0]['listings']:

            h = House()
            
            h['airbnb_id'] =  str(listing['listing']['id'])
            h['name'] = listing['listing']['name']
            h['query_text'] = self.query_text
            h['bedroom'] = str(listing['listing']['bedrooms'])
            h['bed'] = str(listing['listing']['beds'])
            h['bath'] = str(listing['listing']['bathrooms'])
            h['amenities'] = listing['listing']['preview_amenities']
            h['rules'] = ''
            h['reviews_count'] = str(listing['listing']['reviews_count'])
            h['city'] = listing['listing']['city']
            h['guest_label'] = listing['listing']['guest_label']
            h['lat'] = str(listing['listing']['lat'])
            h['lng'] = str(listing['listing']['lng'])

            u = User()
            u['house_id'] = str(listing['listing']['id'])
            u['username'] = listing['listing']['user']['first_name']
            u['pic_url'] = listing['listing']['user']['picture_url']
            lusers.append(u)

            for picture in listing['listing']['picture_urls']:
                p = Photo()
                p['house_id'] = str(listing['listing']['id'])
                p['url'] = picture
                lphotos.append(p)


            offset = 1
            limit = 30
            while True:
                url = 'https://www.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en&listing_id='+str(listing['listing']['id'])+'&role=guest&_format=for_p3&_limit='+str(limit)+'&_offset='+str(offset)+'&_order=language_country';
                resp = requests.get(url)
                review_json = resp.json()
                lreviews.append(self.parse_review(review_json, str(listing['listing']['id'])))
                reviews_count = review_json['metadata']['reviews_count']
                print 'a'+str(reviews_count)
                if reviews_count < offset:
                    break
                offset += limit 

            items.append(h)

        ret['houses'] = items
        ret['reviews'] = lreviews
        ret['photos'] = lphotos
        ret['users'] = lusers
        yield ret

   