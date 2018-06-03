from spiders.airbnb0 import Airbnb0Spider
#from spiders.airbnb import AirbnbSpider
from spiders.airbnb1 import Airbnb1Spider
from spiders.airbnb2 import Airbnb2Spider
# scrapy api imports
from scrapy import signals
from twisted.internet import reactor
import scrapy.crawler as crawler
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from multiprocessing import Process, Queue
from twisted.internet import reactor

# list of crawlers
TO_CRAWL = [Airbnb0Spider, Airbnb0Spider]

# crawlers that are running 
RUNNING_CRAWLERS = []

def spider_closing(spider):
    RUNNING_CRAWLERS.remove(spider)


query_text = 'Arizona'
section_offset = 1
items_per_grid = 1
items_offset = 1
adults = 1
children = 0
page = 0

def f(q):
    try:
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(Airbnb0Spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        print e
        q.put(e)

q = Queue()
p = Process(target=f, args=(q,))
p.start()
result = q.get()
p.join()

if result is not None:
    raise result

# for spider in TO_CRAWL:
#     s = spider
#     settings = get_project_settings()
#     settings.attributes.get('USER_AGENT').value = "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.7.0"


#     process = CrawlerProcess(settings)
#     url = 'https://www.airbnb.com/api/v2/explore_tabs?version=1.3.5&_format=for_explore_search_web&experiences_per_grid=20&items_per_grid='+str(items_per_grid)+'&guidebooks_per_grid=20&auto_ib=true&fetch_filters=true&has_zero_guest_treatment=false&is_guided_search=true&is_new_cards_experiment=true&luxury_pre_launch=false&query_understanding_enabled=true&show_groupings=true&supports_for_you_v3=true&timezone_offset=180&client_session_id=985cfba6-b4cb-4337-92c0-5de9e1f4e1d9&metadata_only=false&is_standard_search=true&refinement_paths%5B%5D=%2Fhomes&selected_tab_id=home_tab&adults='+str(adults)+'&children='+str(children)+'&items_offset='+str(items_offset)+'&infants=0&allow_override%5B%5D=&s_tag=4sCkVqgo&section_offset='+str(section_offset)+'&last_search_session_id=692b60f3-51fa-44fc-bec8-3434085604ea&federated_search_session_id=27b1b335-b801-472f-ac44-0cfb7c5cb6fa&screen_size=medium&query='+query_text+'&_intents=p1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en'
#     data = {
#         'url': url,
#         'query_text': query_text,
#         }
#     process.crawl(spider, **data)
#     process.start()
#     section_offset += 1
#     if section_offset > 10:
#         break
