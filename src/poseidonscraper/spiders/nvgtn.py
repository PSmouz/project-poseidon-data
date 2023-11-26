"""NVGTN spider

This spider crawls the gymshark.com website and extracts the following
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

Categories (default all):
    - leggings
    - underwear
    - dresses
    - skorts
    - all-in-one

Country (default de):
    - de
    - us

Example Usage:
    scrapy crawl gymshark -a country=de -a categories=leggings,skorts

"""
import json
import re
import math
import uuid

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from ..items import NVGTNItem


class NVGTNSpider(scrapy.Spider):
    name = "nvgtn"
    allowed_domains = ["nvgtn.com"]

    def __init__(self, categories=None, country="us", *args, **kwargs):
        super(NVGTNSpider, self).__init__(*args, **kwargs)

        # Select Category from CL Argument
        if categories is None:
            categories = [
                "leggings",
                "underwear",
            ]
        else:
            categories = categories.split(",")

        categories_map = {
            "leggings": "fitness-leggings/",
            "underwear": "accessories/",
        }

        self.start_urls = [
            f"https://nvgtn.com/collections/{categories_map[cat]}"
            for cat in categories
        ]

    def parse(self, response):
        """

        Args:
            response:
        """
        pattern = r"collection_count:\s*(\d+)"
        matches = re.search(pattern, response.text)
        products_amount = matches.group(1)

        for i in range(math.ceil(int(products_amount) / 16)):
            products_url = response.url + "?page=" + str(i + 1)

            yield response.follow(products_url, callback=self.parse_products)

    def parse_products(self, response):
        """

        Args:
            response:
        """
        products = response.xpath(
            '//div[contains(@class, "product-card")]/a/@href'
        ).extract()

        for product in products:
            item_url = (
                "https://"
                + self.allowed_domains[0]
                + "/products/"
                + product.split("/")[-1]
                + ".js"
            )  # Gets Json directly

            yield Request(
                item_url,
                callback=self.parse_item,
                meta={"original_url": response.url},
            )

    def parse_item(self, response):
        """

        Args:
            response:
        """
        product = json.loads(response.text)
        # name, color, collection = self.parse_title(product["title"])
        loader = ItemLoader(item=NVGTNItem(), response=response)
        loader.add_value("url", response.meta["original_url"])
        loader.add_value("id", str(uuid.uuid4()))
        loader.add_value("name", product["title"])
        loader.add_value("category_name", response.meta["original_url"])
        loader.add_value(
            "collection_name", self.get_collection(product["title"])
        )
        loader.add_value(
            "images", ["https:" + image for image in product["images"]]
        )
        loader.add_value("materials", product["description"])
        loader.add_value(
            "sizes", [size["title"] for size in product["variants"]]
        )
        loader.add_value("color", product["tags"])
        loader.add_value("price", product["price"])
        loader.add_value("price", product["compare_at_price"])

        yield loader.load_item()

    @staticmethod
    def get_collection(title):
        """

        Args:
            title:
        """
        collection_map = {
            "contour": "NVGTN Contour",
            "curve": "Curve Seamless",
            "scrunch": "Scrunch Seamless",
            "solid": "Solid Seamless",
            "camo": "Camo Seamless",
            "snakeskin": "Wild Thing Seamless",
            "zebra": "Wild Thing Seamless",
            "leopard": "Wild Thing Seamless",
            "signature": "Signature 2.0",
        }

        for key in collection_map.keys():
            if key in title.lower():
                return collection_map[key]
