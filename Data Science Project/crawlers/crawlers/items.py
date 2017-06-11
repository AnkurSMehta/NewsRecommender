# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    source = scrapy.Field()
    title = scrapy.Field()
    published_date = scrapy.Field()
    crawled_date = scrapy.Field()
    cover_image = scrapy.Field()
    source_url = scrapy.Field()
    img_urls = scrapy.Field()
    author = scrapy.Field()
    related = scrapy.Field()
    blurb = scrapy.Field()
    details = scrapy.Field()
    category = scrapy.Field()
    sub_categories = scrapy.Field()
    location = scrapy.Field()
    tags = scrapy.Field()
    video_url = scrapy.Field()
