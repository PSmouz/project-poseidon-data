"""GymShark spider

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
import uuid

import scrapy
from scrapy.loader import ItemLoader

from ..items import GymsharkItem


# TODO: ALL-IN-ONE in de für alles in us einzeln
# TODO: media.src nicht immer kann auch medias.videoSrc sein


class GymsharkSpider(scrapy.Spider):
    name = "gymshark"
    allowed_domains = ["www.gymshark.com", "de.gymshark.com", "cdn.shopify.com"]

    def __init__(self, categories=None, country="de", *args, **kwargs):
        super(GymsharkSpider, self).__init__(*args, **kwargs)

        # Select Category from CL Argument
        if categories is None:
            categories = [
                "leggings",
                "underwear",
                "dresses",
                "skorts",
                "all-in-one",
            ]
        else:
            categories = categories.split(",")

        country_map = {
            "us": self.allowed_domains[0],
            "de": self.allowed_domains[1],
        }

        self.start_urls = [
            f"https://{country_map[country]}/collections/{cat}/womens"
            for cat in categories
        ]

    def parse(self, response):
        """

        Args:
            response:
        """
        products_amount = (
            response.xpath(
                '//*[@id="MainContent"]/section/div/div/span[2]/text()'
            )
            .get()
            .split(" ")[0]
        )
        products_url = response.url + "?viewAll=" + products_amount

        yield response.follow(products_url, callback=self.parse_products)

    def parse_products(self, response):
        """

        Args:
            response:
        """
        products = response.xpath(
            '//*[@id="MainContent"]/div[2]/section/div[1]/article'
        )

        for product in products:
            item_url = product.css("a::attr(href)").extract_first()

            yield response.follow(
                item_url,
                callback=self.parse_item,
                meta={"original_url": response.url},
            )

    def parse_item(self, response):
        """

        Args:
            response:
        """
        content = response.xpath(
            '//script[@id="__NEXT_DATA__" and @type="application/json"]/text()'
        ).get()
        data = json.loads(content)
        product = data["props"]["pageProps"]["productData"]["product"]

        image_urls = [image["src"] for image in product["media"]]
        sizes = list(
            map(
                lambda x: {
                    "size": x["size"],
                    "quantity": int(x["inventoryQuantity"]),
                },
                product["availableSizes"],
            )
        )
        rating = {
            "rating": float(product["rating"]["average"]),
            "reviews_number": int(product["rating"]["count"]),
        }

        loader = ItemLoader(item=GymsharkItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_value("id", str(uuid.uuid4()))
        loader.add_value("name", product["title"])
        loader.add_value("category_name", response.meta["original_url"])
        loader.add_value("collection_name", product["handle"].split("-")[-1])
        loader.add_value("rating", rating)
        loader.add_value("images", image_urls)
        loader.add_value("materials", product["description"])
        loader.add_value("sizes", sizes)
        loader.add_value("color", product["colour"])
        loader.add_value("price", product["price"])
        loader.add_value("price", product["compareAtPrice"])

        yield loader.load_item()
