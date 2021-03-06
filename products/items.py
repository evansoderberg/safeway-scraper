import scrapy


class SafewayItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    item_id = scrapy.Field()
    price = scrapy.Field()
    price_description = scrapy.Field()
    unit_price = scrapy.Field()
    zip_code = scrapy.Field()
    image_url = scrapy.Field()
    category_link = scrapy.Field()
