# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from datetime import datetime
from hashlib import md5
import random

class CrawlersPipeline(object):
	def process_item(self, item, spider):
		print "Item",item
		return item


class MongoDBPipeline(object):

	def __init__(self):
		connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	def process_item(self, item, spider):
		valid = True
		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))

		mongo_doc = {}
		if 'title' in item and item['title'] and 'details' in item and item['details']:
			mongo_doc['title'] = item['title']
			mongo_doc['details']  = item['details']
			mongo_doc['source']  = '' if not 'source' in item else item['source']
			mongo_doc['crawled_date']  = '' if not 'crawled_date' in item else item['crawled_date']
			mongo_doc['source_url']  = '' if not 'source_url' in item else item['source_url']
			mongo_doc['img_urls']  = [] if not 'img_urls' in item else item['img_urls']
			mongo_doc['cover_image']  = '' if not 'cover_image' in item else item['cover_image']
			mongo_doc['blurb']  = '' if not 'blurb' in item else item['blurb']
			mongo_doc['doc_id'] = md5(item['source_url']).hexdigest()
			mongo_doc['published_date'] = '' if not 'published_date' in item else item['published_date']
			mongo_doc['author'] = [] if not 'author' in item else item['author']
			mongo_doc['related'] = [] if not 'related' in item else item['related']
			mongo_doc['category'] = '' if not 'category' in item else item['category']
			mongo_doc['sub_categories'] = [] if not 'sub_categories' in item else item['sub_categories']
			# mongo_doc['location'] = '' if not 'location' in item else item['location']
			mongo_doc['tags'] = [] if not 'tags' in item else item['tags']
			# mongo_doc['video_url'] = '' if not 'video_url' in item else item['video_url']
			avg_rating = round(random.random()*5, 1)
			view_count = int(random.random()*1000)
			no_of_ratings = int(random.random()*view_count)
			mongo_doc['avg_rating'] =  avg_rating
			mongo_doc['view_count'] =  view_count
			mongo_doc['rating_count'] =  no_of_ratings
		else:
			valid = False

		if valid:
			self.collection.update({'title': mongo_doc['title'], 'source':mongo_doc['source']}, mongo_doc, upsert=True)
			log.msg("article added to MongoDB database!",
					level=log.DEBUG, spider=spider)
			spider.log("==Saved in Mongodb=================>>>>>>>> %r" % mongo_doc['doc_id'])
		return item
