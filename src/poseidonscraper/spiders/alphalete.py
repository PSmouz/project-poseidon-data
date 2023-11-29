"""Alphalete spider

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
    - skirts

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
from scrapy.http import Request
from scrapy.loader import ItemLoader

from ..items import AlphaleteItem


class AlphaleteSpider(scrapy.Spider):
    name = "alphalete"
    allowed_domains = [
        "alphaleteathletics.com",
        "premium-alphalete.mybcapps.com",
    ]

    def __init__(self, categories=None, country="us", *args, **kwargs):
        super(AlphaleteSpider, self).__init__(*args, **kwargs)

        # Select Category from CL Argument
        if categories is None:
            categories = ["leggings", "underwear", "skirts"]
        else:
            categories = categories.split(",")

        categories_map = {
            "leggings": "leggings/",
            "underwear": "underwear/",
            "skirts": "dresses-skirts/",
        }

        self.start_urls = [
            f"https://{self.allowed_domains[0]}/collections/womens"
            f"-{categories_map[cat]}"
            for cat in categories
        ]

    def parse(self, response):
        """

        Args:
            response:
        """
        scope = response.url.split("/")[-2].replace("womens-", "")
        scope_map = {
            "leggings": "436180492",
            "underwear": "68415258742",
            "dresses-skirts": "289912881336",
        }

        pattern = r"collection_count:\s*(\d+)"
        matches = re.search(pattern, response.text)
        products_amount = matches.group(1)

        for i in range(math.ceil(int(products_amount) / 50)):
            products_url = (
                f"https://premium-alphalete.mybcapps.com/bc-sf-filter"
                f"/filter?shop=alphaleteathletics.myshopify.com&limit="
                f"50&product_available=false&variant_available=false"
                f"&build_filter_tree=true&check_cache=true&pg="
                f"collection_page&event_type=collection&page="
                f"{str(i + 1)}&sort="
                f"manual&collection_scope={scope_map[scope]}"
            )

            yield Request(products_url, callback=self.parse_products)

    def parse_products(self, response):
        """

        Args:
            response:
        """
        products = json.loads(response.text)["products"]

        for product in products:
            item_url = (
                f"https://alphaleteathletics.com/search?view=json&type"
                f"=product&sort_by=created-descending&q=title%3A"
                f"{product['title'].replace(' ', '%20')}"
                f"%20AND%20product_type%3A"
                f"{product['product_type'].replace(' ', '%20')}"
            )
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
        product = json.loads(response.text)[0]

        name, color = self.parse_title(product["title"])
        url = f"https://{self.allowed_domains[0]}/products/{product['handle']}"

        sizes = [
            {"size": size["title"], "quantity": size["inventory_quantity"]}
            for size in product["variants"]
        ]

        loader = ItemLoader(item=AlphaleteItem(), response=response)
        loader.add_value("url", url)
        loader.add_value("id", str(uuid.uuid4()))
        loader.add_value("name", name)
        loader.add_value("category_name", self.get_category(name))
        loader.add_value("collection_name", self.get_collection(name))
        loader.add_value(
            "images", ["https:" + image for image in product["images"]]
        )
        loader.add_value("materials", product["description"])
        loader.add_value("sizes", sizes)
        loader.add_value("color", color)
        loader.add_value("price", product["price"])
        loader.add_value("price", product["compare_at_price"])

        yield loader.load_item()

    @staticmethod
    def parse_title(title):
        """

        Args:
            title:
        """
        title = title.split("-")
        name = title[0].strip().replace("Legging", "Leggings")
        color = title[1].strip().lower()

        if "/" in color:
            color = [item.strip() for item in color.split("/")]

        return name, color

    @staticmethod
    def get_collection(title):
        """

        Args:
            title:
        """
        collection_map = {
            "amplify": "Seamless",
            "ozone": "Seamless",
            "aura": "Aura",
            "surface": "Surface",
            "alphalux": "Alphalux",
            "pulse": "Pulse",
            "ultrasoft": "Ultrasoft",
            "varsity": "Varsity",
        }

        for key in collection_map.keys():
            if key in title.lower():
                return collection_map[key]

    @staticmethod
    def get_category(title):
        """

        Args:
            title:
        """
        collection_map = {
            "legging": "leggings",
            "skirt": "skirts",
            "thong": "underwear",
            "bralette": "underwear",
        }

        for key in collection_map.keys():
            if key in title.lower():
                return collection_map[key]
