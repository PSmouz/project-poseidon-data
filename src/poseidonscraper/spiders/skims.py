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

from ..items import SkimsItem


class SkimsSpider(scrapy.Spider):
    name = "skims"
    allowed_domains = ["skims.com", "hfqi0zm0.apicdn.sanity.io"]
    # Muss so, da url Request sonst nicht funktioniert
    collections = [
        '"fits-everybody"',
        '"cotton"',
        '"seamless-sculpt"',
        '"soft-lounge"',
        '"naked"',
        '"cotton-fleece"',
        '"boyfriend"',
        '"soft-smoothing-seamless"',
        '"cozy"',
        '"wireless-form"',
        '"swim"',
        '"weightless"',
        '"essential-bodysuits"',
        '"core-control"',
        '"no-show"',
        '"sheer-sculpt"',
        '"barely-there"',
        '"ultra-fine-mesh"',
        # Limited
        '"everyday-sculpt"',
        '"skims-ultimate-bra"',
        '"skims-body"',
        '"stretch-satin"',
        '"skims-first-layers"',
        # Legacies
        '"faux-leather"',
        '"skims-velvet"',
        '"skims-for-team-usa"',
        '"after-hours"',
        '"logo-velour"',
        '"velour"',
        '"lace-up"',
        '"teddy"',
        '"woven-shine"',
        '"shine-foundations"',
        '"free-cut"',
        '"logo-mesh"',
        '"jelly-sheer"',
        '"skims-romance"',
        '"skims-hotel"',
        '"warp-knit-lace"',
        '"shades-of-grey"',
        '"skims-disco"',
        '"swarovski-x-skims"',
    ]
    categories = [
        '"shapewear"',
        '"bodysuits"',
        '"bras"',
        '"panties"',
        '"underwear"',
        '"leggings-pants"',
        '"skirts"',
    ]

    def __init__(self, categories=None, *args, **kwargs):
        super(SkimsSpider, self).__init__(*args, **kwargs)

        # # Select Category from CL Argument
        # if categories is None:
        #     categories = [
        #         "leggings",
        #         "underwear",
        #         "dresses",
        #         "skorts",
        #         "all-in-one",
        #     ]
        # else:
        #     categories = categories.split(",")

        self.start_urls = ["https://skims.com"]

    def parse(self, response):
        """
        Args:
            response:
        """
        # Set your query parameters

        # Define your GraphQL query
        graphql_query = r"""
            {
                "query": "*[_type == 'collection' && collectionStore.slug.current == $collection][0] {\"products\": *[ _type == \"product\" && _id in ^.collectionStore.products[]._ref && (store.tags match \"Config: Master\" && \"Config: Master\" in string::split(store.tags, \", \") ) ]{defined(store.vendor) => { \"vendor\": store.vendor },defined(detail.fabric) => { \"material\": detail.fabric }, siblings { colorsList, colorsSeasonal, colorsSeasonalAutomated}, defined(store.productType) => { \"productType\": store.productType }, defined(store.options[1].values) => { \"sizes\": store.options[1]{values} }, defined(store.title) => { \"title\": store.title }, defined(store.slug.current) => { \"url\": store.slug.current }, defined(store.priceRange.maxVariantPrice) => { \"price\": store.priceRange.maxVariantPrice },  defined(store.status) => { \"status\": store.status }, defined(store.productType) => { \"type\": store.productType } }}"
            }
        """

        # Choose between categories or collections array
        for collection in self.collections:
            # Send the POST request
            yield scrapy.Request(
                url=f"https://hfqi0zm0.apicdn.sanity.io/v2021-10-21/data/query/"
                f"production?$collection={collection}",
                method="POST",
                headers={"Content-Type": "application/json"},
                body=json.dumps(json.loads(graphql_query)),
                callback=self.parse_result,
            )

    def parse_result(self, response):
        """
        Args:
            response:
        """
        # Attempt to parse the response body as JSON
        result = json.loads(response.text)["result"]
        # Handle the result as needed
        if not result:
            print(f"No result found for {response.url}")
            return

        products = result["products"]

        for product in products:

            color_map = self.map_colors(product["siblings"])
            url = product["url"]
            colors = [
                color.lower().replace(" ", "-")
                for sublist in color_map.values()
                for color in sublist
            ]

            # Find the color in the URL
            color_in_url = next(
                (color for color in colors if color in url), None
            )

            # If a color is found in the URL, concatenate it with each color
            # from the combined array
            if color_in_url:
                urls_with_color = [
                    url.replace(color_in_url, color) for color in colors
                ]

            query = (
                '{"query": "*[_type == \'product\' && (store.slug.current in '
                + str(urls_with_color)
                + ")] {defined(store.images) => {'images': "
                'store.images[]{src}}}"}'
            )

            yield scrapy.Request(
                url=f"https://hfqi0zm0.apicdn.sanity.io/v2021-10-21/data/query/"
                f"production",
                method="POST",
                headers={"Content-Type": "application/json"},
                body=json.dumps(json.loads(query)),
                meta={"product": product, "color": color_map},
                callback=self.parse_item,
            )

    def parse_item(self, response):
        """
        Args:
            response:
        """
        product = response.meta["product"]
        result = json.loads(response.text)

        image_urls = [
            image["src"]
            for item in result["result"]
            for image in item["images"]
        ]

        loader = ItemLoader(item=SkimsItem(), response=response)
        loader.add_value("url", product["url"])
        loader.add_value("id", str(uuid.uuid4()))
        loader.add_value("name", product["title"])
        loader.add_value("category_name", "")
        loader.add_value("collection_name", product["vendor"])
        loader.add_value("images", image_urls)
        loader.add_value("materials", product["material"])
        loader.add_value("sizes", product["sizes"]["values"])
        loader.add_value("color", response.meta["color"])
        loader.add_value("price", product["price"])
        loader.add_value("status", product["status"])
        loader.add_value("type", product["type"])
        loader.add_value("type", product["productType"])

        yield loader.load_item()

    @staticmethod
    def map_colors(input_colors):
        """
        Args:
            input_colors:
        """

        colors_list = (
            input_colors["colorsList"].lower().split(", ")
            if input_colors["colorsList"]
            else []
        )
        colors_seasonal = (
            input_colors["colorsSeasonal"].lower().split(", ")
            if input_colors["colorsSeasonal"]
            else []
        )
        colors_seasonal_automated = (
            input_colors["colorsSeasonalAutomated"].lower().split(", ")
            if input_colors["colorsSeasonalAutomated"]
            else []
        )

        seasonal_colors = list(set(colors_seasonal + colors_seasonal_automated))

        return {"classic": colors_list, "seasonal": seasonal_colors}
