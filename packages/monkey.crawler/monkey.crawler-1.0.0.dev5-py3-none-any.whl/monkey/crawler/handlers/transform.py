# -*- coding: utf-8 -*-
import re
import unicodedata
from datetime import datetime
from monkey.crawler.processor import Handler, ProcessingError
from monkey.crawler.op_codes import OpCode


class Transformer:
    """Operates transformation on value"""

    def transform(self, value):
        """Executes the value transformation"""
        raise NotImplemented()


class FieldTransformer(Handler):
    """Transforms the specified field value using a transformer
    """

    def __init__(self, field_names: set[str], transformer: Transformer, result_field_mapping: dict = None,
                 fail_on_missing_field: bool = False):
        """Initializes the handler
        :param field_names: the names of the fields hose value will be transformed
        :param transformer: the transformer
        :param result_field_mapping: a field name mapping for transformed value storage. If no mapping specified, the
         field original value will be replaced.
         :param fail_on_missing_field: If false missing field will not raise any error and the handler will just skip
         the field (no transformation attempt)
        """
        super().__init__()
        self.field_names = field_names
        self.transformer = transformer
        self.result_field_mapping = {} if result_field_mapping is None else result_field_mapping
        self.fail_on_missing_field = fail_on_missing_field

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the transformation and store the new value in the specified target field
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation.
        :return: a copy of the provided record that contains the formatted value in the target field
        :return: the provided operation code
        """
        rec = record.copy()
        for field_name in self.field_names:
            try:
                val = self.transformer.transform(record[field_name])
                result_field_name = self.result_field_mapping.get(field_name, field_name)
                rec[result_field_name] = val
            except KeyError as e:
                if self.fail_on_missing_field:
                    raise ProcessingError(record, f'Record does not contain any field named \'{field_name}\'', e)
            except Exception as e:
                raise ProcessingError(record, f'Failed to handle transformation ({type(self.transformer).__name__}) : '
                                              f'{e}', e)
        return rec, op_code


class StrFormatter(Transformer):
    """Formats the specified value using a format spec
    See: 'Format Specification Mini-Language <https://docs.python.org/3/library/string.html#formatspec>'_
    """

    def __init__(self, format_spec: str = ''):
        """Initializes the transformer
       :param format_spec: the format specification. If not specified, the format operation behave as a simple string
        conversion.
        """
        super().__init__()
        self.format_spec = format_spec

    def transform(self, value):
        """Performs the format operation
        :param value: the value to format
        :return: the formatted value
        """
        if value is not None:
            return format(value, self.format_spec)
        else:
            return None


class DatetimeFormatter(Transformer):
    """Converts the string value of the specified field into datetime object.
    See: 'Format codes
    <https://docs.python.org/fr/3/library/datetime.html?highlight=datetime#strftime-strptime-behavior>'_
    """

    def __init__(self, format_spec: str = 'YYYY-MM-DDTHH:MM:SS'):
        """Initializes the transformer
        :param format_spec: the format specification. If not specified, the format operation applies ISO 8601 format
        'YYYY-MM-DDTHH:MM:SS'.
        """
        super().__init__()
        self.format_spec = format_spec

    def transform(self, value):
        """Performs the format operation
        :param value: the value to format
        :return: the formatted value
        """
        if value is not None:
            return datetime.strptime(value, self.format_spec)
        else:
            return None


class E164Formatter(Transformer):
    """Converts specified field value as a string representation of a phone number in E.164 format
    """

    def __init__(self, default_country_code: int = None):
        """Initializes the transformer
        :param default_country_code: the country code (dial code) to use by default if provided value does not represent
        an international phone number
        """
        super().__init__()
        self.default_country_code = default_country_code

    def transform(self, value):
        """Formats the value into E164 representation
        :param value: the value to format
        :return: the formatted value
        """
        if value is not None:
            # Remove separators
            phone_num = re.sub(r'[- .]', '', value)
            if phone_num.startswith('00'):
                phone_num = phone_num.replace('00', '+', 1)
            # else:
            # TODO: Check if value starts with '+'
            return phone_num
        else:
            return None


class ListReducer(Transformer):
    """If provided value is multivalued, the transformer reduces it to its first value or a default value if field
    contains an empty list.
    """

    def __init__(self, default_value=None):
        """Initializes the transformer.
        :param default_value: the default value to use if provided value is an empty list
        """
        super().__init__()
        self.default_value = default_value

    def transform(self, value):
        """Performs the reduction
        :param value: the value to reduce
        :return: a single value
        """
        val = value
        if val is not None:
            if isinstance(val, list):
                if len(val) > 0:
                    val = val[0]
                else:
                    val = self.default_value
        return val


class UppercaseFormatter(Transformer):
    """Formats the specified text value in uppercase"""

    def transform(self, value):
        """Performs the format operation
        :param value: the value to format
        :return: the formatted value
        """
        if isinstance(value, str):
            return value.upper()
        else:
            return None


class LowercaseFormatter(Transformer):
    """Formats the specified text value in uppercase"""

    def transform(self, value):
        """Performs the format operation
        :param value: the value to format
        :return: the formatted value
        """
        if isinstance(value, str):
            return value.lower()
        else:
            return None


class DiacriticsRemover(Transformer):
    """Remove diacritic symbols from string"""

    def __init__(self):
        """Initializes the transformer
        """
        super().__init__()

    def transform(self, value):
        """Performs the format operation
        :param value: the value to format
        :return: the formatted value
        """
        if value is not None:
            return ''.join(c for c in unicodedata.normalize('NFC', value)
                           if unicodedata.category(c) != 'Mn')
        else:
            return None


class TextReplacer(Transformer):
    """Replace any text matching the specified pattern
    See: https://docs.python.org/fr/3/library/re.html?#re.sub
    """

    def __init__(self, pattern, repl, count=0):
        """Initializes the transformer
       :param pattern:
       :param repl:
       :param count:
        """
        super().__init__()
        self.pattern = pattern
        self.repl = repl
        self.count = count

    def transform(self, value):
        """Performs the format operation
        :param value: the value to format
        :return: the formatted value
        """
        if value is not None:
            return re.sub(self.pattern, self.repl, value, self.count)
        else:
            return None
