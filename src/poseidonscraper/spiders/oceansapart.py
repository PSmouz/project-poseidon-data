import re
import uuid

import requests
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

# from src.poseidonscraper.poseidonscraper.items import OceansapartItem


###
### Example Usage:
### scrapy crawl oceansapart -a categories=leggings -O oceansapart_en-de_11_20_2023.json
### Categories: leggings,skorts,underwear,dresses
###


class OceansapartSpider(scrapy.Spider):
    name = "oceansapart"
    allowed_domains = ["www.oceansapart.com", "cdn.oceansapart.com"]
    color_map = {}

    #
    # Control the logging level for Selenium and urllib3 to make console more
    # readable.
    #
    # Set the logging level for the Selenium remote_connection logger to ERROR
    # logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)
    # Set the logging level for urllib3.connectionpool logger to WARNING
    # logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

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
        # Get the color map from the CSS file
        self.get_color_map()

        for url in self.start_urls:
            yield Request(
                url,
                callback=self.parse_products,
                dont_filter=True,
                meta={"original_url": url},
            )

    def parse_products(self, response):
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
        color_code = (
            response.xpath(
                "string(//*[contains(@class, "
                "'oa-bubble--active')]/span//@class)"
            )
            .get()
            .split(" ")[1]
        )

        # id = re.search(r'postid-(\d+)', response.xpath('//body/@class').get()).group(1)
        # product = requests.get(f"https://www.oceansapart.com/de/wp-json/wc/store/v1/products/{id}").json()
        # image_urls = [image['src'] for image in product['images']]
        # sizes = [size['attributes'][0]['value'] for size in product['variations']].reverse()

        l = ItemLoader(item=OceansapartItem(), response=response)
        l.add_value("url", response.url)
        l.add_value("id", str(uuid.uuid4()))
        l.add_xpath(
            "name", "/html/body/main/main/section/article/div[1]/h1/text()"
        )
        l.add_value("category_name", response.meta["original_url"])
        l.add_xpath(
            "images",
            '//*[@id="productDetailsCarousel"]//*[not(contains(@class, '
            '"tns-slide-cloned"))]/@href',
        )
        l.add_xpath(
            "materials",
            "/html/body/main/main/section/article/div[4]/div[2]/div/ul",
        )
        l.add_xpath(
            "sizes",
            "/html/body/main/main/section/article/form/div["
            "1]/select/option/text()",
        )
        l.add_xpath(
            "color_name",
            "/html/body/main/main/section/article/div[1]/h1/span/text()",
        )
        l.add_value("color_value", self.color_map[color_code])
        l.add_xpath(
            "price",
            "/html/body/main/main/section/article/div[2]/p/span/bdi/text()",
        )
        l.add_xpath(
            "price",
            "/html/body/main/main/section/article/div[2]/p/del/span/bdi/text()",
        )  # Sale Price
        # l.add_xpath("name", '/html/body/main/main/section/article/div[
        # 1]/h1/text()') l.add_value("category_name", response.meta[
        # 'original_url']) l.add_value("images", image_urls) l.add_value(
        # "materials", product['description']) l.add_value("sizes", sizes)
        # l.add_xpath("color_name",
        # '/html/body/main/main/section/article/div[1]/h1/span/text()')
        # l.add_value("color_value", self.color_map[color_code]) l.add_value(
        # "price", product['prices']['price']) l.add_value("price", product[
        # 'prices']['sale_price'])
        yield l.load_item()

    def get_color_map(self):
        url = (
            "https://cdn.oceansapart.com/de/wp-content/plugins/oceansapart"
            "-extensions/includes/color-bubbles/css/colors.css?ver=3.112.0"
        )
        css = requests.get(url).text
        self.color_map = parse_css_colors(css)


def parse_css_colors(css):
    # Define a regular expression pattern
    pattern = (
        r"\.([\w-]+)(?:,\s*([\w-]+))?\s*{\s*background-color\s*:\s*#(["
        r"0-9a-fA-F]+)(?:\s*;\s*)?}"
    )
    # Find all matches using the pattern
    matches = re.findall(pattern, css)
    # Create a dictionary to store the parsed data
    parsed_data = {}
    # Process each match and populate the dictionary
    for match in matches:
        selector1, selector2, background_color = match
        selector1 = selector1.strip()
        selector2 = selector2.strip() if selector2 else None
        background_color = background_color.strip()

        # Handle multiple selectors
        if selector2:
            selectors = [selector1, selector2]
        else:
            selectors = [selector1]

        for selector in selectors:
            # Update the parsed_data dictionary
            parsed_data[selector] = "#" + background_color

    return parsed_data
