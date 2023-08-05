#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from enum import Enum
import logging


class _TupleOpCode(namedtuple('TupleOpCode', ['name', 'plot_symbol', 'default_logging_level'])):

    def __str__(self):
        return f'({self.plot_symbol} -> {self.name} (with default logging level: {self.default_logging_level}'


class OpCode(Enum):
    INSERT = _TupleOpCode('INSERT', '+', logging.INFO)
    UPDATE = _TupleOpCode('UPDATE', '.', logging.INFO)
    IGNORE = _TupleOpCode('IGNORE', '_', logging.INFO)
    ERROR = _TupleOpCode('ERROR', 'X', logging.ERROR)
    CONFLICT = _TupleOpCode('CONFLICT', '!', logging.ERROR)
    DELETE = _TupleOpCode('DELETE', '#', logging.INFO)
    SKIP = _TupleOpCode('SKIP', '/', logging.INFO)
    RETRY = _TupleOpCode('RETRY', 'R', logging.INFO)
    NO_CHANGE = _TupleOpCode('NO_CHANGE', '=', logging.DEBUG)
    SUCCESS = _TupleOpCode('SUCCESS', '$', logging.INFO)
    UNDEFINED = _TupleOpCode('UNDEFINED', '?', logging.WARN)

    def get_plot_symbol(self) -> str:
        return self.value.plot_symbol

    def get_name(self) -> str:
        return self.value.name

    def get_default_logging_level(self) -> int:
        return self.value.default_logging_level


class OpCounter:

    def __init__(self):
        self.counters = {}
        self._total = 0

    def inc(self, op_code: OpCode, inc: int = 1):
        self.counters[op_code] = self.counters.get(op_code, 0) + inc
        self._total += inc

    def total(self, compute: bool = False):
        if compute:
            total = 0
            for op_code in self.counters.keys():
                total += self.counters[op_code]
            self._total = total
        return self._total

    def __str__(self):
        s = ''
        for op_code, count in self.counters.items():
            s += f'\t{op_code.name:<10}: {count:4}'
        return s
