# -*- coding: utf-8 -*-

from monkey.crawler.handlers.transform import FieldTransformer, StrFormatter, DatetimeFormatter


class FieldStrFormatter(FieldTransformer):
    """Formats specified field value using a format spec
    See: 'Format Specification Mini-Language <https://docs.python.org/3/library/string.html#formatspec>'_
    """

    def __init__(self, field_name: str, format_spec: str = '', result_field_name: str = None):
        """Initializes the handler.
        :param field_name: the name of the field whose value will be formatted
        :param format_spec: the format specification. If not specified, the format operation behave as a simple string
        conversion.
        :param result_field_name: the name ot the field where the formatted value will be store. If not specified, the
        origin field value will be replaced.
        """
        super().__init__({field_name}, StrFormatter(format_spec),
                         {field_name: field_name if result_field_name is None else result_field_name})


class FieldDatetimeFormatter(FieldTransformer):
    """Converts the string value of the specified field into datetime object.
    See: 'Format codes <https://docs.python.org/fr/3/library/datetime.html?highlight=datetime#strftime-strptime-behavior>'_
    """

    def __init__(self, field_name: str, format_spec: str = 'YYYY-MM-DDTHH:MM:SS', result_field_name: str = None):
        """Initializes the handler.
        :param field_name: the name of the field whose value will be formatted
        :param format_spec: the format specification.
        :param result_field_name: the name ot the field where the datetime object will be store. If not specified, the
        origin field value will be replaced.
        """
        super().__init__({field_name}, DatetimeFormatter(format_spec),
                         {field_name: field_name if result_field_name is None else result_field_name})
