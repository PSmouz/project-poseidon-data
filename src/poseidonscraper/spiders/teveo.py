"""Teveo Spider

This spider is used to crawl the teveo.com website for products.

Categories:
    - leggings
    - underwear

Example Usage:
    scrapy crawl teveo -a -a categories=leggings,underwear
"""

import json
import math
import re
import uuid

import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from ..items import TeveoItem


class TeveoSpider(scrapy.Spider):
    name = "teveo"
    allowed_domains = ["teveo.com"]
    collections = [
        "Candy",
        "Charming",
        "College",
        "Elegant",
        "Everyday",
        "Evolution",
        "Focus",
        "Lounge",
        "Originals",
        "Ribbed",
        "Sensation",
        "Signature",
        "Statement",
        "Tie Dye",
        "Timeless",
        "True",
        "V-Shape",
    ]

    def __init__(self, categories=None, *args, **kwargs):
        super(TeveoSpider, self).__init__(*args, **kwargs)

        # Select Category from CL Argument
        if categories is None:
            categories = ["leggings", "underwear"]
        else:
            categories = categories.split(",")

        category_paths = {
            "leggings": "hosen-leggings/",
            "underwear": "sport-unterwaesche/",
        }

        self.start_urls = [
            f"https://teveo.com/collections/{category_paths[cat]}"
            for cat in categories
        ]

    def parse(self, response):
        """

        Args:
            response:
        """
        products_amount = response.xpath(
            '//*[@id="ProductGridContainer"]/div/div[3]/@data-total-products'
        ).get()

        for i in range(math.ceil(int(products_amount) / 60)):
            products_url = response.url + "?page=" + str(i + 1)

            yield response.follow(products_url, callback=self.parse_products)

    def parse_products(self, response):
        """

        Args:
            response:
        """
        products = response.xpath(
            '//span[contains(@class, "card-information__text")]/a/@href'
        ).extract()

        for product in products[:1]:
            item_url = (
                "https://" + self.allowed_domains[0] + product + ".js"
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

        name, color, collection = self.parse_title(product["title"])

        loader = ItemLoader(item=TeveoItem(), response=response)
        loader.add_value("url", response.url.split(".js")[0])
        loader.add_value("id", str(uuid.uuid4()))
        loader.add_value("name", name)
        loader.add_value("category_name", response.meta["original_url"])
        loader.add_value("collection_name", collection)
        loader.add_value("images", [image["src"] for image in product["media"]])
        loader.add_value("materials", product["description"])
        loader.add_value(
            "sizes", [size["title"] for size in product["variants"]]
        )
        loader.add_value("color", color)
        loader.add_value("price", product["price"])
        loader.add_value("price", product["compare_at_price"])

        yield loader.load_item()

    def parse_title(self, title: str) -> tuple[str, str, str]:
        """

        Args:
            title: The title string ot the project. Mostly of the form:
                "Collection Product Name \"Color\""

        Returns:
            A tuple containing the name, color and collection of the product.
        """
        collection = next((c for c in self.collections if c in title), None)
        # Check if collection is not None before using replace
        if collection:
            title = title.replace(collection, "").strip()
        # Define a regular expression pattern to capture text inside double
        # quotes
        pattern = re.compile(r'"(?P<color>[^"]+)"')
        # Use the findall method to find all occurrences of the pattern in
        # the title
        matches = pattern.findall(title)
        # Extract color and name based on the matches
        color = matches[0] if matches else None
        name = pattern.sub("", title).strip()

        return name, color, collection
