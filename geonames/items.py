# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Data(Item):
	houses = Field()

class Photo(Item):
	house_id = Field()
	url = Field()

class User(Item):
	house_id = Field()
	username = Field()
	pic_url = Field()

class Review(Item):
	house_id = Field()
	username = Field()
	review = Field()
	rating = Field()
	date_review = Field()

class House(Item):
	name = Field()
	query_text = Field()
	guests = Field()
	bedroom = Field()
	bed = Field()
	bath = Field()
	amenities = Field()
	rules = Field()
	reviews_count = Field()
	city = Field()
	tp = Field()
	airbnb_id = Field()
	guest_label = Field()
	lat = Field()
	lng = Field()
