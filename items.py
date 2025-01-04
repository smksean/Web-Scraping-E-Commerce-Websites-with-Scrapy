import scrapy

class BeverageScraper(scrapy.Item):
    name = scrapy.Field()        # Product name
    price = scrapy.Field()       # Product price
    image_url = scrapy.Field()   # Product image URL
    product_url = scrapy.Field() # URL of the product page




