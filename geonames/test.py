
from scrapy.utils.project import get_project_settings
from spiders.airbnb0 import Airbnb0Spider
from spiders.airbnb1 import Airbnb1Spider

# scrapy api
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings


TO_CRAWL = [Airbnb1Spider, Airbnb0Spider]

def spider_closing(spider):
	#print 'here!'
    reactor.stop()


settings = get_project_settings()
settings.attributes.get('USER_AGENT').value = "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.7.0"

data = {
    'url': 'https://www.airbnb.com/api/v2/explore_tabs?version=1.3.5&_format=for_explore_search_web&experiences_per_grid=20&items_per_grid=18&guidebooks_per_grid=20&auto_ib=true&fetch_filters=true&has_zero_guest_treatment=false&is_guided_search=true&is_new_cards_experiment=true&luxury_pre_launch=false&query_understanding_enabled=true&show_groupings=true&supports_for_you_v3=true&timezone_offset=180&client_session_id=985cfba6-b4cb-4337-92c0-5de9e1f4e1d9&metadata_only=false&is_standard_search=true&refinement_paths%5B%5D=%2Fhomes&selected_tab_id=home_tab&adults=1&children=0&infants=0&allow_override%5B%5D=&s_tag=4sCkVqgo&section_offset=14&last_search_session_id=692b60f3-51fa-44fc-bec8-3434085604ea&federated_search_session_id=27b1b335-b801-472f-ac44-0cfb7c5cb6fa&screen_size=medium&query=Arizona&_intents=p1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=RUB&locale=en',
    'query_text': 'Arizona',
}

for spider in TO_CRAWL:
	crawler = Crawler(Airbnb0Spider('aaa'), settings)
	crawler.signals.connect(spider_closing, signal=signals.spider_closed)
	crawler.crawl(spider)
reactor.run()
