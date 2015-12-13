import json
import time


class JsonWriterPipeline(object):

    def __init__(self):
        time_str = time.strftime("%m-%d-%Y_%H-%M-%S")
        self.file = open('products/data/items_{0}.json'.format(time_str), 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item
