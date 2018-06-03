# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

reload(sys)  
sys.setdefaultencoding('utf8')

class GeonamesPipeline(object):
	host = 'localhost'
	user = 'airbnb_user'
	password = 'CHerxf9A3d0vK7vW'
	db = 'airbnb'

	def __init__(self):

		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
		self.connection.set_character_set('utf8')
		self.cursor = self.connection.cursor()
		self.cursor.execute('SET NAMES utf8;')
		self.cursor.execute('SET CHARACTER SET utf8;')
		self.cursor.execute('SET character_set_connection=utf8;')

	def escape(self,v):
		return MySQLdb.escape_string(v.encode('utf-8').strip())

	def create_query(self, items, table):
		try:
			for i in items:
				keys = '`, `'.join(i).encode('utf-8').strip()
				values = u'", "'.join(list(map(self.escape, i.values()))).encode('utf-8').strip()
				query = 'INSERT INTO `' + table +'`(`'+keys+'`) VALUES("'+values+'")'
				self.cursor.execute(query)
				self.connection.commit()
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])

	def process_item(self, item, spider):
			for rr in item['reviews']:
				self.create_query(rr, 'reviews')
			
			self.create_query(item['houses'], 'houses')
			self.create_query(item['photos'], 'photos')
			self.create_query(item['users'], 'users')


		
