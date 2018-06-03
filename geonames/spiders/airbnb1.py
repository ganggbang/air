# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from items import House, Photo, Review, User
import scrapy
import json
import requests

class Airbnb1Spider(scrapy.Spider):
    name = 'airbnb1'
    allowed_domains = ['airbnb.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(Airbnb1Spider, self).__init__(*a, **kw)
        self.url = kw.get('url')
        self.query_text = 'Arizona'
    
    def start_requests(self):
        proxy = '192.168.244.1:8888'
        yield scrapy.Request('https://www.airbnb.com/api/v2/explore_tabs?version=1.3.5&_format=for_explore_search_web&experiences_per_grid=20&items_per_grid=18&guidebooks_per_grid=20&auto_ib=true&fetch_filters=true&has_zero_guest_treatment=false&is_guided_search=true&is_new_cards_experiment=true&luxury_pre_launch=false&query_understanding_enabled=true&show_groupings=true&supports_for_you_v3=true&timezone_offset=180&client_session_id=985cfba6-b4cb-4337-92c0-5de9e1f4e1d9&metadata_only=false&is_standard_search=true&refinement_paths%5B%5D=%2Fhomes&selected_tab_id=home_tab&adults=1&children=0&infants=0&allow_override%5B%5D=&s_tag=4sCkVqgo&section_offset=14&last_search_session_id=692b60f3-51fa-44fc-bec8-3434085604ea&federated_search_session_id=27b1b335-b801-472f-ac44-0cfb7c5cb6fa&screen_size=medium&query=Arizona&_intents=p1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=RUB&locale=en', callback=self.parse, meta={'proxy': proxy})
        
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
                print 'a: '+str(reviews_count)
                if reviews_count < offset:
                    break
                offset += limit 

            items.append(h)

        ret['houses'] = items
        ret['reviews'] = lreviews
        ret['photos'] = lphotos
        ret['users'] = lusers
        yield ret

   