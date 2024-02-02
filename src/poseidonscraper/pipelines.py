# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
from scrapy.utils.python import to_bytes


class PoseidonscraperPipeline:
    def process_item(self, item, spider):
        return item


class PoseidonscraperImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{image_guid}.png"


class PoseidonscraperFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        file_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{file_guid}.mp4"
