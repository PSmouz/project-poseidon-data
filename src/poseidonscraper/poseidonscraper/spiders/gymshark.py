import scrapy
import uuid
import json
from scrapy.loader import ItemLoader
from poseidonscraper.items import GymsharkItem

###
### Example Usage:
### scrapy crawl gymshark -a country=de -a categories=leggings,skorts -O data.json
### Countries: us/de , Categories: leggings,skorts,underwear,dresses
###https://de.gymshark.com/collections/all-in-one/womens

#TODO: ALL-IN-ONE in de für alles in us einzeln
#TODO: media.src nicht immer kann auch medias.videoSrc sein

class GymsharkSpider(scrapy.Spider):
    name = "gymshark"
    allowed_domains = ["www.gymshark.com","de.gymshark.com", "cdn.shopify.com"]

    def __init__(self, categories=None, *args, **kwargs):
        super(GymsharkSpider, self).__init__(*args, **kwargs)

        ## Select Region/Country from CL Argument
        if self.country == 'us':
            domain = self.allowed_domains[0]
        elif self.country == 'de':
            domain = self.allowed_domains[1]
        else:
            domain = self.allowed_domains[0]
        
        ## Select Category from CL Argument
        if categories == None:
            categories = ["leggings", "underwear", "dresses", "skorts", "all-in-one"]
        else:
            categories = categories.split(',')
        
        self.start_urls = [f"https://{domain}/collections/{cat}/womens" for cat in categories]

    def parse(self, response):
        products_amount = response.xpath('//*[@id="MainContent"]/section/div/div/span[2]/text()').get().split(' ')[0]
        products_url = response.url + "?viewAll=" + products_amount

        yield response.follow(products_url, callback=self.parse_products)

    def parse_products(self, response):
        products = response.xpath('//*[@id="MainContent"]/div[2]/section/div[1]/article')

        for product in products:
            item_url = product.css("a::attr(href)").extract_first()

            yield response.follow(item_url, callback=self.parse_item, meta={'original_url': response.url})

    def parse_item(self, response):
        content = response.xpath('//script[@id="__NEXT_DATA__" and @type="application/json"]/text()').get()
        data = json.loads(content)
        product = data['props']['pageProps']['productData']['product']
        
        image_urls = [image['src'] for image in product['media']]
        sizes = list(map(lambda x: {'size': x['size'], 'quantity': int(x['inventoryQuantity'])}, product['availableSizes']))
        rating = {
            "rating": float(product['rating']['average']),
            "reviews_number": int(product['rating']['count'])
        }

        l = ItemLoader(item=GymsharkItem(), response=response)
        l.add_value("url", response.url)
        l.add_value("id", str(uuid.uuid4()))
        l.add_value("name", product['title'])
        l.add_value("category_name", response.meta['original_url'])
        l.add_value("collection_name", product['handle'].split("-")[-1])
        l.add_value("rating", rating)
        l.add_value("images", image_urls)
        l.add_value("materials", product['description'])
        l.add_value("sizes", sizes)
        l.add_value("color", product['colour'])
        l.add_value("price", product['price'])
        l.add_value("price", product['compareAtPrice'])

        yield l.load_item()
