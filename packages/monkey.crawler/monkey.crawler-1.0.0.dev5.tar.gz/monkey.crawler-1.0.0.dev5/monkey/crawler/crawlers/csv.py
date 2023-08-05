# -*- coding: utf-8 -*-

import csv

from monkey.crawler.crawler import Crawler
from monkey.crawler.processor import Processor


class CSVCrawler(Crawler):

    def __init__(self, source_name: str, processor: Processor, source_file: str, offset: int = 1, max_retry: int = 0,
                 source_encoding=None, col_heads: list[str] = None, dialect='excel'):
        super().__init__(source_name, processor, offset, max_retry)
        self.csv_file = source_file
        self.encoding = source_encoding
        self.dialect = dialect
        self.col_heads = col_heads[:]

    def _get_records(self):
        # with open(self.csv_file, encoding=self.encoding) as source:
        # See: https://docs.python.org/fr/3/library/csv.html#csv.DictReader
        # See: https://docs.python.org/fr/3/library/csv.html#csv.reader
        # See: https://docs.python.org/fr/3/library/csv.html#csv-fmt-params
        source = open(self.csv_file, encoding=self.encoding)
        reader = csv.DictReader(source, fieldnames=self.col_heads, dialect=self.dialect)
        for i in range(self.offset):
            reader.__next__()
        return reader

    def _get_start_message(self):
        return f'Crawling {self.source_name} from {self.csv_file} file.'
