# -*- coding: utf-8 -*-

import logging
import sys

from monkey.crawler.op_codes import OpCode, OpCounter
from monkey.crawler.processor import Processor


class Crawler:

    def __init__(self, source_name: str, processor: Processor, offset: int = 0, max_retry: int = 0, reporter=None):
        self.logger = logging.getLogger(f'{self.__class__.__module__}.{self.__class__.__name__}')
        self.source_name = source_name
        self.offset = offset
        self.processor = processor
        self.retry_record_list = []
        self.retry_count = 0
        self.max_retry = max_retry
        self.reporter = ConsoleReporter() if reporter is None else reporter
        self.activity_logger = ActivityLogger('crawler')

    def crawl(self):
        """Crawl the entire data source"""
        self._crawl(self._get_records())

    def _crawl(self, records):
        """Crawl the provided records"""
        allow_retry = self.retry_count <= self.max_retry
        retry_accumulator = InMemoryAccumulator()
        if self.retry_count == 0:
            self.reporter.echo(self._get_start_message())
        self.reporter.pass_start(self.retry_count + 1, self.source_name)
        counter = OpCounter()
        with self.processor as processor:
            for record in records:
                self.reporter.line_head(counter)
                op_code = processor.process(record, allow_retry)
                counter.inc(op_code)
                self.reporter.plot(op_code)
                self.activity_logger.report(record, op_code)
                if op_code == OpCode.SKIP or op_code == OpCode.RETRY:
                    retry_accumulator.add(record)
        self.reporter.pass_end(self.retry_count + 1, self.source_name, self.processor.get_processing_duration())
        if len(retry_accumulator) > 0 and allow_retry:
            self._crawl(retry_accumulator)
        else:
            self.reporter.final_report(counter)

    def _get_records(self):
        """Returns an iterator on records"""
        # TODO: Check retry accumulator to get records from accumulator instead of original source
        raise NotImplementedError()

    def _get_start_message(self):
        return f'Starts crawling {self.source_name}'


class Accumulator:

    def __init__(self):
        pass

    def __iter__(self):
        raise NotImplementedError()


class InMemoryAccumulator:

    def __init__(self):
        super().__init__()
        self._list = []

    def __iter__(self):
        return self._list.__iter__()

    def add(self, elt):
        self._list.append(elt)

    def __len__(self):
        return len(self._list)


class ConsoleReporter:
    DEFAULT_MAX_COL = 100

    def __init__(self, out=sys.stdout, max_col: int = DEFAULT_MAX_COL, head_len: int = 6):
        self.out = out
        self.max_col: int = max_col
        self.plot_count: int = 0
        self.head_len: int = head_len

    def _println(self, *objects, sep=' '):
        self._print(*objects, sep=sep, end='\n', flush=False)

    def _print(self, *objects, sep=' ', end='', flush=True):
        print(*objects, sep=sep, end=end, file=self.out, flush=flush)

    def echo(self, message):
        self._println(message)

    def pass_start(self, idx, source_name):
        self._print(f'\n-- START PASS #{idx} ({source_name}) --')

    def pass_end(self, idx, source_name, duration):
        self._println(f'\n-- END PASS #{idx} ({source_name}) -- duration {duration:2f} ms')

    def final_report(self, counter: OpCounter):
        self._println(f'\nCrawling report: \n{counter}')

    def line_head(self, counter: OpCounter):
        if counter.total() % self.max_col == 0:
            self._print(f'\n{self.plot_count:<{self.head_len}}: ')
            self.plot_count += self.max_col

    def plot(self, op_code: OpCode):
        self._print(op_code.get_plot_symbol())

    def reset(self):
        self.plot_count = 0


class ActivityLogger:

    def __init__(self, base_name: str = None):
        logger_base_name = f'{self.__class__.__module__}.{self.__class__.__name__}' if base_name is None else base_name
        self.loggers = {}
        for op_code in OpCode:
            self.loggers[op_code] = logging.getLogger(f'{logger_base_name}.{op_code.name}')

    def report(self, record, op_code: OpCode, message: str = None):
        logger = self.loggers[op_code]
        extra = {
            'op_code': op_code.name,
            'record': record
        }
        msg = f'{op_code.name} - {record}' if message is None else message
        logger.log(op_code.get_default_logging_level(), msg, extra=extra)
