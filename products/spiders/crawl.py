# -*- coding: utf-8 -*-
from lxml import etree, html
import json
from scrapy import Request
from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from ..items import SafewayItem


class CrawlSpider(InitSpider):
    name = "safeway"
    login_page = 'https://shop.safeway.com/ecom/account/sign-in/'
    allowed_domains = ["shop.safeway.com"]
    zip_code = ''
    start_urls = (
        'http://shop.safeway.com/ecom/shop-by-aisle/Baby-Care/Baby-Accessories',
        'http://shop.safeway.com/ecom/shop-by-aisle/Beverages/Coffee',
        'http://shop.safeway.com/ecom/shop-by-aisle/Bread-Bakery/Bakery-Bread',
        'http://shop.safeway.com/ecom/shop-by-aisle/Breakfast-Cereal/Breakfast-Bars-Snacks',
        'http://shop.safeway.com/ecom/shop-by-aisle/Canned-Goods-Soups/Canned-Fruit',
        'http://shop.safeway.com/ecom/shop-by-aisle/Condiments-Spice-Bake/Baking-Dough-Mixes',
        'http://shop.safeway.com/ecom/shop-by-aisle/Cookies-Snacks-Candy/Candy-Gum-Mints',
        'http://shop.safeway.com/ecom/shop-by-aisle/Dairy-Eggs-Cheese/Butter-Sour-Cream',
        'http://shop.safeway.com/ecom/shop-by-aisle/Deli/Deli-Catering-Trays',
        'http://shop.safeway.com/ecom/shop-by-aisle/Flowers',
        'http://shop.safeway.com/ecom/shop-by-aisle/Frozen-Foods/Frozen-Appetizers',
        'http://shop.safeway.com/ecom/shop-by-aisle/Fruits-Vegetables/Fresh-Fruits',
        'http://shop.safeway.com/ecom/shop-by-aisle/Grains-Pasta-Sides/Dinner-Side-Dishes',
        'http://shop.safeway.com/ecom/shop-by-aisle/International-Cuisine/Asian-Foods',
        'http://shop.safeway.com/ecom/shop-by-aisle/Meat-Seafood/Beef',
        'http://shop.safeway.com/ecom/shop-by-aisle/Paper-Cleaning-Home/Air-Fresheners-Candles',
        'http://shop.safeway.com/ecom/shop-by-aisle/Personal-Care-Health/Antacid-Digestive-Aids',
        'http://shop.safeway.com/ecom/shop-by-aisle/Pet-Care/Cat-Care',
        'http://shop.safeway.com/ecom/shop-by-aisle/Tobacco/Cigarettes-Tobacco',
        'http://shop.safeway.com/ecom/shop-by-aisle/Tobacco/Cigarettes-Tobacco/Tobacco-e-Cigarettes',
        'http://shop.safeway.com/ecom/shop-by-aisle/Wine-Beer-Spirits/Beer-Coolers'
    )

    # rules = (
    #     Rule(LinkExtractor(allow=r'-\w+.html$'),
    #          callback='parse_item', follow=True),
    # )

    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        zip_code = raw_input('Zip code: ')
        self.zip_code = zip_code
        return FormRequest.from_response(response,
                    formnumber=5,
                    clickdata={'name': 'Browse'},
                    formdata={'Register.ZipCode': self.zip_code},
                    callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "Welcome!" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            return self.initialized()
        else:
            self.log("Error loggin in as guest")

    # def parse_item(self, response):
    #     # Scrape data from page
    #     print response

    def parse(self, response):
        for href in response.css("li.level-4 > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        items = response.xpath('//div[@class="id-productItems"]/div[contains(@class, "widget") and contains(@class, "id-productItem")]')
        for sel in items:
            try:
                tree = html.fromstring(sel.extract())
                json_data = tree.xpath('//script')[0].text
                data = json.loads(json_data)
                item = SafewayItem()
                item['item_id'] = data.get('Id')
                item['name'] = data.get('Description')
                item['price'] = data.get('Price')
                item['unit_price'] = data.get('PricePerSellingUnit')
                # item['image'] = sel.xpath('img').extract()
                item['category_link'] = response.url
                item['zip_code'] = self.zip_code
                yield item
            except Exception as e:
                print "Error"
                print sel
                print e
