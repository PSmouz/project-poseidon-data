"""Define here the models for your scraped items

See documentation in:
https://docs.scrapy.org/en/latest/topics/items.html
"""

import scrapy
import re
from itemloaders.processors import MapCompose, TakeFirst, Compose

# from ../../utils import extract_materials
from src.utils import extract_materials


def take_max(values):
    """

    Args:
        values:

    Returns:

    """
    non_none_values = [value for value in values if value is not None]
    return max(non_none_values) if non_none_values else None


class GymsharkItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    category_name = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split("/")[4]),
        output_processor=TakeFirst(),
    )
    collection_name = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    files = scrapy.Field()
    materials = scrapy.Field(
        input_processor=MapCompose(extract_materials),
    )
    sizes = scrapy.Field()
    color = scrapy.Field(
        input_processor=MapCompose(str.lower), output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(lambda x: float(x)),
        output_processor=lambda x: take_max(x),
    )


class OceansapartItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    category_name = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split("/")[-2]),
        output_processor=TakeFirst(),
    )
    images = scrapy.Field()
    materials = scrapy.Field(
        input_processor=MapCompose(extract_materials),
    )
    sizes = scrapy.Field(input_processor=Compose(lambda x: x[1:]))
    color = scrapy.Field(output_processor=TakeFirst())
    low_stock_remaining = scrapy.Field(output_processor=TakeFirst())
    in_stock = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field()
    price = scrapy.Field(
        # SurrealDB handles Price Object
        input_processor=MapCompose(lambda x: float(x.replace("\xa0", ""))),
        output_processor=TakeFirst(),
    )


class LoungeItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    )
    category_name = scrapy.Field(
        input_processor=MapCompose(
            lambda x: (
                x.split("/")[4].split("-")[0]
                if "-" in x.split("/")[4]
                else x.split("/")[4]
            )
        ),
        output_processor=TakeFirst(),
    )
    collection_name = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    reviews_number = scrapy.Field(
        input_processor=MapCompose(int), output_processor=TakeFirst()
    )
    images = scrapy.Field()
    materials = scrapy.Field(input_processor=MapCompose(extract_materials))
    sizes = scrapy.Field()
    color = scrapy.Field(
        input_processor=MapCompose(str.lower), output_processor=TakeFirst()
    )
    price = scrapy.Field(
        # SurrealDB handles Price Object
        input_processor=MapCompose(lambda x: float(x / 100.0)),
        output_processor=lambda x: take_max(x),
    )


class TeveoItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    )
    category_name = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split("/")[4].split("-")[1]),
        output_processor=TakeFirst(),
    )
    collection_name = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(
        input_processor=MapCompose(float), output_processor=TakeFirst()
    )
    reviews_number = scrapy.Field(
        input_processor=MapCompose(int), output_processor=TakeFirst()
    )
    images = scrapy.Field()
    materials = scrapy.Field(input_processor=MapCompose(extract_materials))
    sizes = scrapy.Field()
    color = scrapy.Field(
        input_processor=MapCompose(str.lower), output_processor=TakeFirst()
    )
    price = scrapy.Field(
        # SurrealDB handles Price Object
        input_processor=MapCompose(lambda x: float(x / 100.0)),
        output_processor=lambda x: take_max(x),
    )


class NVGTNItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    )
    category_name = scrapy.Field(
        input_processor=MapCompose(
            lambda x: (
                x.split("/")[4].split("-")[1]
                if "accessories" not in x
                else "underwear"
            )
        ),
        output_processor=TakeFirst(),
    )
    collection_name = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    materials = scrapy.Field(input_processor=MapCompose(extract_materials))
    sizes = scrapy.Field()
    color = scrapy.Field(
        input_processor=lambda x: next(
            (item.split("_")[0].lower() for item in x if "_color" in item),
            None,
        ),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        # SurrealDB handles Price Object
        input_processor=MapCompose(lambda x: float(x / 100.0)),
        output_processor=lambda x: take_max(x),
    )


class AlphaleteItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    )
    category_name = scrapy.Field(output_processor=TakeFirst())
    collection_name = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    materials = scrapy.Field(input_processor=MapCompose(extract_materials))
    sizes = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field(
        # SurrealDB handles Price Object
        input_processor=MapCompose(lambda x: float(x / 100.0)),
        output_processor=lambda x: take_max(x),
    )


class GKEliteItem(scrapy.Item):
    url = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split("?")[0]),
        output_processor=TakeFirst(),
    )
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    category_name = scrapy.Field(output_processor=TakeFirst())
    collection_name = scrapy.Field(output_processor=TakeFirst())
    # rating = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    materials = scrapy.Field(
        input_processor=MapCompose(extract_materials),
    )
    sizes = scrapy.Field()
    color = scrapy.Field(
        input_processor=MapCompose(str.lower), output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(lambda x: float(int(x)) / 100 if x else 0.0),
        output_processor=Compose(max),
    )


class SkimsItem(scrapy.Item):
    url = scrapy.Field(
        input_processor=MapCompose(lambda x: "https://skims.com/products/" + x),
        output_processor=TakeFirst(),
    )
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split(" | ")[0]),
        output_processor=TakeFirst(),
    )
    category_name = scrapy.Field(output_processor=TakeFirst())
    collection_name = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    status = scrapy.Field(output_processor=TakeFirst())
    type = scrapy.Field()
    materials = scrapy.Field(
        input_processor=MapCompose(extract_materials),
    )
    sizes = scrapy.Field()
    color = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(
        input_processor=MapCompose(lambda x: round(x, 2)),
        output_processor=Compose(max),
    )
