# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from itemloaders.processors import MapCompose, TakeFirst, Compose	


class PoseidonscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



    

def extract_materials_german(value):
    # Regex pattern to match percentage and material
    pattern = re.compile(r'(\d{1,3}%)\s*([\w\s]+?)(?=(?:\s*,|\s*und|\s*<|\s*(?:\d{1,3}%|$)))')
    # Extract matches from the value
    matches = pattern.findall(value)
    result = [f"{percentage} {material.lower()}" for percentage, material in matches]
    return result

def take_max(values):
    non_none_values = [value for value in values if value is not None]
    return max(non_none_values) if non_none_values else None

class GymsharkItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    category_name = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split("/")[4]),
        output_processor=TakeFirst())
    collection_name = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    materials = scrapy.Field(
        input_processor=MapCompose(extract_materials),
    )
    sizes = scrapy.Field()
    color = scrapy.Field(
        input_processor=MapCompose(str.lower),
        output_processor=TakeFirst()
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
        output_processor=TakeFirst())
    images = scrapy.Field()
    materials = scrapy.Field(
        input_processor=MapCompose(extract_materials),
    )
    sizes = scrapy.Field(input_processor=Compose(lambda x: x[1:]))
    color_name = scrapy.Field(
        input_processor=MapCompose(str.lower),
        output_processor=TakeFirst()
    )
    color_value= scrapy.Field(
        input_processor=MapCompose(str.lower),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        # SurrealDB handles Price Object
        input_processor=MapCompose(lambda x: float(x.replace('\xa0', ''))),
        output_processor=TakeFirst(),
    ) 

class LoungeItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst())
    category_name = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split("/")[4].split("-")[0] if '-' in x.split("/")[4] else x.split("/")[4]), # TODO: Fix this
        output_processor=TakeFirst())
    collection_name = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(
        input_processor=MapCompose(float),
        output_processor=TakeFirst()
    )
    reviews_number = scrapy.Field(
        input_processor=MapCompose(int),
        output_processor=TakeFirst()
    )
    images = scrapy.Field()
    materials = scrapy.Field(
        input_processor=MapCompose(extract_materials)
    )
    sizes = scrapy.Field()
    color = scrapy.Field(
        input_processor=MapCompose(str.lower),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        # SurrealDB handles Price Object
        input_processor=MapCompose(lambda x: float(x / 100.0)),
        output_processor=lambda x: take_max(x)
    )

class TeveoItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst())
    category_name = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split("/")[-2].split("-")[1]),
        output_processor=TakeFirst())
    collection_name = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(
        input_processor=MapCompose(float),
        output_processor=TakeFirst()
    )
    reviews_number = scrapy.Field(
        input_processor=MapCompose(int),
        output_processor=TakeFirst()
    )
    images = scrapy.Field()
    materials = scrapy.Field(
        input_processor=MapCompose(extract_materials)
    )
    sizes = scrapy.Field()
    color = scrapy.Field(
        input_processor=MapCompose(str.lower),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        # SurrealDB handles Price Object
        input_processor=MapCompose(lambda x: float(x / 100.0)),
        output_processor=lambda x: take_max(x)
    )