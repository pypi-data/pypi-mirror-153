# -*- coding: utf-8 -*-

from monkey.crawler.op_codes import OpCode
from monkey.crawler.processor import Handler


class FieldProjector(Handler):
    """Operates a field projection"""

    def __init__(self, field_names: set[str]):
        """Initializes the handler.
        :param field_names: the names of the fields that will be projected
        """
        super().__init__()
        self.field_names = field_names

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the projection.
        :param record: the record
        :param op_code: the operation code computed by any previous operation
        :return: a new record only containing the projected fields
        :return: the provided operation code
        """
        # rec = dict(filter(lambda elem: elem[0] in self.field_names, record.items()))
        rec = {}
        for field_name in self.field_names:
            rec[field_name] = record[field_name]
        return rec, op_code


class FieldMapper(Handler):
    """Operates a field projection and a field name mapping."""

    def __init__(self, field_map: dict):
        """Initializes the handler.
        :param field_map: the mapping between original names and new names.
        """
        super().__init__()
        self.field_map: dict = field_map

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the projection and field name mapping.
        :param record: the record
        :param op_code: the operation code computed by any previous operation
        :return: a new record only containing the projected fields with the new field names
        :return: the provided operation code
        """
        rec = {}
        for original_name, new_name in self.field_map.items():
            rec[new_name] = record[original_name]
        return rec, op_code
