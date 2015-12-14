import json
import time
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class JsonWriterPipeline(object):

    def __init__(self):
        time_str = time.strftime("%m-%d-%Y_%H-%M-%S")
        self.file = open('{0}/products/products/data/items_{1}.json'.format(PROJECT_ROOT, time_str), 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item
