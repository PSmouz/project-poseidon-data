"""Oceansapart Spider

This spider crawls the oceansapart.com website and extracts the following
information from the product pages:

- Product Name
- Product Category
- Product Images
- Product Materials
- Product Sizes
- Product Color (Name, Value)
- Product Price

Categories (default all):
    - leggings
    - skorts
    - underwear
    - dresses

Example Usage:
    scrapy crawl oceansapart -a categories=leggings
"""
import re
import uuid

import requests
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from ..items import OceansapartItem
from ...utils import parse_css_colors, color_map


class OceansapartSpider(scrapy.Spider):
    name = "oceansapart"
    allowed_domains = ["www.oceansapart.com", "cdn.oceansapart.com"]
    color_map = {}

    def __init__(self, categories=None, *args, **kwargs):
        super(OceansapartSpider, self).__init__(*args, **kwargs)
        # Select Category from CL Argument
        if categories is None:
            categories = ["leggings", "underwear", "bodies", "skorts"]
        else:
            categories = categories.split(",")

        category_paths = {
            "leggings": "bottoms/leggings/",
            "underwear": "underwear/panties/",
            "bodies": "underwear/body-underwear/",
            "skorts": "bottoms/shorts-skirts/",
        }

        self.start_urls = [
            (
                f"https://www.oceansapart.com/en/product-category/"
                f"{category_paths[cat]}"
            )
            for cat in categories
        ]

    def start_requests(self):
        """Placeholder"""
        self.get_color_map()

        for url in self.start_urls:
            yield Request(
                url,
                callback=self.parse_products,
                dont_filter=True,
                meta={"original_url": url},
            )

    def parse_products(self, response):
        """

        Args:
            response:
        """
        products = response.css(".card__details::attr(href)").extract()

        for item_url in products:
            yield response.follow(
                item_url,
                callback=self.parse_item,
                meta={"original_url": response.meta["original_url"]},
            )

        # Extract the next page link
        next_page = response.css(".next::attr(href)").extract_first()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_products,
                meta={"original_url": response.meta["original_url"]},
            )

    def parse_item(self, response):
        """

        Args:
            response:
        """
        color_code = (
            response.xpath(
                "string(//*[contains(@class, "
                "'oa-bubble--active')]/span//@class)"
            )
            .get()
            .split(" ")[1]
        )

        loader = ItemLoader(item=OceansapartItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_value("id", str(uuid.uuid4()))
        loader.add_xpath(
            "name", "/html/body/main/main/section/article/div[1]/h1/text()"
        )
        loader.add_value("category_name", response.meta["original_url"])
        loader.add_xpath(
            "images",
            '//*[@id="productDetailsCarousel"]//*[not(contains(@class, '
            '"tns-slide-cloned"))]/@href',
        )
        loader.add_xpath(
            "materials",
            "/html/body/main/main/section/article/div[4]/div[2]/div/ul",
        )
        loader.add_xpath(
            "sizes",
            "/html/body/main/main/section/article/form/div["
            "1]/select/option/text()",
        )
        loader.add_value(
            "color",
            {
                "name": response.xpath(
                    "/html/body/main/main/section/article/div[1]/h1/span/text()"
                )
                .get()
                .lower(),
                "value": self.color_map[color_code],
            },
        )
        loader.add_xpath(
            "price",
            "/html/body/main/main/section/article/div[2]/p/span/bdi/text()",
        )
        loader.add_xpath(
            "price",
            "/html/body/main/main/section/article/div[2]/p/del/span/bdi/text()",
        )  # Sale Price

        yield loader.load_item()

    def get_color_map(self):
        """Requests a css file for color map."""
        # TODO: Fix regex
        # url = (
        #     "https://cdn.oceansapart.com/de/wp-content/plugins/oceansapart"
        #     "-extensions/includes/color-bubbles/css/colors.css?ver=3.112.0"
        # )
        # css = requests.get(url).text
        # self.color_map = parse_css_colors(css)
        self.color_map = color_map.copy()


# JSON Alternative:
# id = re.search(r'postid-(\d+)', response.xpath('//body/@class').get(
# )).group(1) product = requests.get(
# f"https://www.oceansapart.com/de/wp-json/wc/store/v1/products/{id}").json()
# image_urls = [image['src'] for image in product['images']] sizes = [size[
# 'attributes'][0]['value'] for size in product['variations']].reverse()

# l.add_xpath("name", '/html/body/main/main/section/article/div[
# 1]/h1/text()') l.add_value("category_name", response.meta[
# 'original_url']) l.add_value("images", image_urls) l.add_value(
# "materials", product['description']) l.add_value("sizes", sizes)
# l.add_xpath("color_name",
# '/html/body/main/main/section/article/div[1]/h1/span/text()')
# l.add_value("color_value", self.color_map[color_code]) l.add_value(
# "price", product['prices']['price']) l.add_value("price", product[
# 'prices']['sale_price'])
