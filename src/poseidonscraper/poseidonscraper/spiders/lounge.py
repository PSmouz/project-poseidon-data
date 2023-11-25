import scrapy
import uuid
import json
import requests
from scrapy.loader import ItemLoader
from poseidonscraper.items import LoungeItem

class LoungeSpider(scrapy.Spider):
    name = "lounge"
    allowed_domains = ["us.lounge.com","de.lounge.com"]
    start_urls = ["https://us.lounge.com"]
    api_url = 'https://j0t2nu3n49-dsn.algolia.net/1/indexes/*/queries'


    def __init__(self, categories=None, *args, **kwargs):
        super(LoungeSpider, self).__init__(*args, **kwargs)
        #TODO add country us/de

        ## Select Category from CL Argument
        if categories == None:
            categories = ["leggings", "underwear", "bodies", "lingerie"]
        else:
            categories = categories.split(',')
  
        category_paths = {
            "leggings": "leggings/",
            "underwear": "thongs-briefs/",
            "bodies": "bodysuits/",
            "lingerie": "intimate-sets/",
            "swim": "swim/"
        }

        self.start_urls = [f"https://us.lounge.com/collections/{category_paths[cat]}" for cat in categories]


    def start_requests(self):
        for url in self.start_urls:
            category = url.split('/')[-2]
            
            yield scrapy.Request(self.api_url, method='POST', headers=self.get_headers(), body=json.dumps(self.get_payload(category)), callback=self.parse_api_result, meta={'original_url': url})
        
            
    def parse_api_result(self, response): # Instead of parse_products
        # Attempt to parse the response body as JSON
        result = json.loads(response.text)
        # Handle the result as needed
        hits = result['results'][0]['hits']
        # Maps to relevant data only
        products = list(map(lambda x: x['handle'], hits))

        self.logger.info(f"Starting request for category: {response.meta['original_url']}")
        self.logger.info(f"Items: {len(products)}")
        for product in products:
            yield scrapy.Request(f"{response.meta['original_url']}products/{product}", callback=self.parse_item, meta={'original_url': response.meta['original_url']})


    def parse_item(self, response):
        content = response.xpath('//script[contains(@type, "application/json") and contains(@data-json, "product-page")]/text()').get()
        data = json.loads(content)
        product = data['product']

        image_urls = [image['src'] for image in product['images']]
        sizes = [{"size": size["title"], "quantity": size["inventory_quantity"]} for size in product['variants']]

        l = ItemLoader(item=LoungeItem(), response=response)
        l.add_value("url", response.url)
        l.add_value("id", str(uuid.uuid4()))
        l.add_value("name", product['title'])
        l.add_value("category_name", response.meta['original_url'])
        l.add_value("collection_name", 'None')
        l.add_value("rating", self.get_rating(product['id']))
        l.add_value("images", image_urls)
        l.add_value("materials", product['description'])
        l.add_value("sizes", sizes)
        l.add_value("color", product['color'])
        l.add_value("price", product['compare_at_price'])
        l.add_value("price", product['price'])
        yield l.load_item()
        

    def get_rating(self, product_id):
        #TODO NOT WORKING correctly yet
        url = 'https://stamped.io/api/widget/reviews'
        params = {
            'productId': product_id,
            'storeUrl': 'germanylounge.myshopify.com',
            'page': '1',
            'take': '24'
        }
        headers = {
            'authority': 'stamped.io',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,la;q=0.6,ar;q=0.5',
            'dnt': '1',
            'origin': 'null',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        data = requests.get(url, params=params, headers=headers).json()
        return {
            'rating': data['rating'] or 0.0,
            'reviews_number': data['total'] or 0
        }


    def get_headers(self):
        #TODO add country us/de
        return {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,la;q=0.6,ar;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://us.lounge.com',
            'Referer': 'https://us.lounge.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-algolia-api-key': 'd0e922fef7e538ca995a3f9fdc881124',
            'x-algolia-application-id': 'J0T2NU3N49'
        }


    def get_payload(self, category, num_items=9999):
        """
        Returns the payload for the Algolia API request.
        Number of items defaults to 9999 since we want to get all items (possibly at once) and at the moment
        I don't see a suffiecient way to get to the excat number of items with scrapy. But thank god
        Algolia delivers a error free response with all items they have. (has a limit of 1000 items per request.)
        """
        return {
            "requests": [
                {
                    "indexName": "en_us_products",
                    "query": "",
                    "params": f"getRankingInfo=true&distinct=true&facets=%5B%22*%22%5D&page=0&facetFilters=%5B%22collections%3A{category}%22%5D&hitsPerPage={num_items}&clickAnalytics=true"
                },
                {
                    "indexName": "en_us_products",
                    "query": "",
                    "params": f"getRankingInfo=true&distinct=true&facets=%5B%22*%22%5D&facetFilters=%5B%5B%22collections%3A{category}%22%5D%5D&page=0&hitsPerPage={num_items}&clickAnalytics=true"
                }
            ]
        }

     
def extract_product_info(hit):
        sizes = []
        # Extracting size-related information from the 'lounge' meta field
        # hit["meta"]["lounge"]["variant_availability"] # Alternative way to get the same data
        lounge_meta = hit.get('meta', {}).get('lounge', {})
        for variant_info in lounge_meta.get('variant_availability', []):
            size_info = {
                'size': variant_info['title'],
                'quantity': variant_info['inventory_quantity'],
            }
            sizes.append(size_info)

        return {
            'handle': hit['handle'],
            'price_original': hit['compare_at_price'],
            'sizes': sizes,
        }

