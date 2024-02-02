"""GKElite Spider

This spider crawls the gkelite.com website and extracts the following
information from the product pages:

- Product Name
- Product Category
- Product Collection
- Product Rating
- Product Images
- Product Materials
- Product Sizes
- Product Color
- Product Price


Example Usage:
    scrapy crawl gkelite

"""

import json
import uuid

import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from ..items import GKEliteItem


class GKEliteSpider(scrapy.Spider):
    name = "gkelite"
    allowed_domains = [
        "gkelite.com",
        "eucs19.ksearchnet.com",
        "gkelite.azureedge.net",
    ]

    def __init__(self, *args, **kwargs):
        super(GKEliteSpider, self).__init__(*args, **kwargs)

        self.start_urls = [
            f"https://{self.allowed_domains[0]}/collections/jade-carey"
        ]

    def parse(self, response):
        """

        Args:
            response:
        """
        products_url = (
            "https://eucs19.ksearchnet.com/cloud-search/n-search"
            "/search?ticket=klevu-158558306829411932"
            "&analyticsApiKey=klevu-158558306829411932"
            "&showOutOfStockProducts=true&fetchMinMaxPrice=true"
            "&noOfResults=52&visibility=catalog&category"
            "=KLEVU_PRODUCT%20Jade%20Carey&responseType=json"
        )

        yield Request(products_url, callback=self.parse_products)

    def parse_products(self, response):
        """

        Args:
            response:
        """
        products = json.loads(response.text)["result"]
        product_ids = set()

        for product in products:
            # The general url format is https://www.gkelite.com/products/e4906.
            # While the last split accounts for .../e4906-sales-rep.
            product_ids.add(product["url"].split("/")[-1].split("-")[0])

        for product_id in list(product_ids):
            yield Request(
                f"https://www.{self.allowed_domains[0]}/products/"
                f"{product_id}?view=json",
                callback=self.parse_item,
            )

    def parse_item(self, response):
        """

        Args:
            response:
        """
        product = json.loads(response.text)
        variant = list(product["colors"].values())[0]

        sizes = list(variant["sizes"].keys())

        loader = ItemLoader(item=GKEliteItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_value("id", str(uuid.uuid4()))
        loader.add_value("name", product["productMeta"]["title"])
        loader.add_value("category_name", "bodysuits")
        loader.add_value("collection_name", "Jade Carey")
        loader.add_value("images", variant["images"])
        loader.add_value("materials", product["productMeta"]["description"])
        loader.add_value("sizes", sizes)
        loader.add_value("color", variant["cpqColor"])
        loader.add_value("price", product["productMeta"]["price"])
        loader.add_value("price", product["productMeta"]["compare_at_price"])

        yield loader.load_item()
