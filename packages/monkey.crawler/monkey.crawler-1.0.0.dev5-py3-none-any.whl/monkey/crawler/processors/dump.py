# -*- coding: utf-8 -*-

import csv
import datetime
import json

from monkey.crawler.op_codes import OpCode

from monkey.crawler.processor import Processor, Handler


class DumpProcessor(Processor):
    def __init__(self, source_name: str, file_path: str, encoding='utf-8', newline='', handlers: list[Handler] = None):
        super().__init__(source_name, handlers)
        self.file_path = file_path
        self.encoding = encoding
        self.newline = newline
        self.output_file = None

    def _enter(self):
        self.output_file = open(self.file_path, 'w', encoding=self.encoding, newline=self.newline)

    def _exit(self):
        self.output_file.close()


class DummyDumpProcessor(DumpProcessor):
    """A simple processor that dumps records into a text file, using the standard to string conversion."""

    def _process(self, record):
        self.output_file.write(str(record)+'\n')
        return OpCode.SUCCESS


class CSVDumpProcessor(DumpProcessor):
    """A processor that dumps records into a CSV file."""

    def __init__(self, source_name: str, file_path: str, encoding='utf-8', newline='', handlers: list[Handler] = None,
                 col_heads: list[str] = None, restval='', extrasaction: str = 'raise', dialect='excel'):
        super().__init__(source_name, file_path, encoding, newline, handlers)
        self.col_heads = col_heads
        self.restval = restval
        self.extrasaction = extrasaction
        self.dialect = dialect

    def _enter(self):
        super()._enter()
        self.writer = csv.DictWriter(self.output_file, self.col_heads, restval=self.restval,
                                     extrasaction=self.extrasaction, dialect=self.dialect)
        self.writer.writeheader()

    def _exit(self):
        super()._exit()

    def _process(self, record):
        self.writer.writerow(record)
        return OpCode.SUCCESS


class JSONDumpProcessor(DumpProcessor):
    """A processor that dumps records into a JSON file."""

    def __init__(self, source_name: str, file_path: str, encoding='utf-8', newline='', handlers: list[Handler] = None,
                 encoder: json.JSONEncoder = None):
        super().__init__(source_name, file_path, encoding, newline, handlers)
        # self.encoder = json.JSONEncoder() if encoder is None else encoder
        self.encoder = JSONEncoder() if encoder is None else encoder
        self.sep = ''

    def _enter(self):
        super()._enter()
        self.output_file.write(f'{{"{self.source_name}":[')

    def _exit(self):
        self.output_file.write(']}')
        self.sep = ''
        super()._exit()

    def _process(self, record):
        self.output_file.write(f'{self.sep}{self.encoder.encode(record)}')
        self.sep = ','
        return OpCode.SUCCESS


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)
