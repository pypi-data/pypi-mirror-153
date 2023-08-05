# -*- coding: utf-8 -*-
# TODO: Field validation against min, max, expression evaluation

import re
from monkey.crawler.op_codes import OpCode
from monkey.crawler.processor import Handler, InputError


class ValidationError(InputError):

    def __init__(self, record_info, violations):
        details = '\n\t'.join(violations)
        super().__init__(record_info, f'Validation errors:{details}')
        self.violations = violations


class Validator:
    """Operates validation on value"""

    def validate(self, record: dict, field_name: str):
        """Executes the value validation
        :param record: the record to validate
        :param field_name: the name of the field to validate
        :return: a violation description or None if validation passes
        """
        raise NotImplemented()


class FieldFilter(Handler):
    """Checks if specified fields verify specific conditions"""

    def __init__(self, field_names: set[str], validator: Validator, on_violation: OpCode = None):
        """Initializes the handler.
        :param field_names: the names of the fields that will be validated
        :param validator: the validator used to execute the validation
        :param on_violation: the operation code to return if validation failed. If None, a validation violation
        will raise a ValidationError.
        """
        super().__init__()
        self.field_names = field_names
        self.validator = validator
        self.onf_violation_op_code = on_violation

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the validation check on target fields from the provided record.
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation
        :return: the provided record
        :return: the provided operation code
        :raise ValidationError: if any validation failed unless if an on_violation op code has been provided.
        """
        violations = []
        for field_name in self.field_names:
            violation = self.validator.validate(record, field_name)
            if violation:
                violations.append(violation)
        if len(violations):
            if self.onf_violation_op_code:
                return record, self.onf_violation_op_code
            else:
                raise ValidationError(record, violations)
        else:
            return record, op_code


class RequiredValidator(Validator):

    def __init__(self, accept_empty: bool = True):
        """Initializes the handler.
        :param accept_empty: indicates if empty value are accepted or not
        """
        super().__init__()
        self.accept_empty = accept_empty

    def validate(self, record: dict, field_name: str):
        """Executes the value validation
        :param record: the record to validate
        :param field_name: the name of the field to validate
        :return: a violation description or None if validation passes
        """
        violation = None
        try:
            value = record.get(field_name)
            if not (self.accept_empty or bool(value)):
                violation = f'Required field \'{field_name}\' is empty.'
        except KeyError:
            violation = f'Required field \'{field_name}\' is missing.'
        return violation


class RequiredFieldFilter(FieldFilter):
    """Checks if required fields are provided and if they are not empty."""

    def __init__(self, field_names: set[str], accept_empty: bool = True, on_violation: OpCode = None):
        """Initializes the handler.
        :param field_names: the names of the fields that will be validated
        :param accept_empty: indicates if empty value are accepted or not
        :param on_violation: the operation code to return if validation failed. If None, a validation violation
        will raise a ValidationError.
        """
        super().__init__(field_names, RequiredValidator(accept_empty), on_violation)


class ValueListChecker(Validator):

    def __init__(self, values: set, exclusion: bool = False):
        """Initializes the handler.
        :param values: the values against which fields will be tested
        :param exclusion: indicates if the provided value list is an exclusion list (black list) or a inclusion list
        (white list)
        """
        super().__init__()
        self.values = values
        self.exclusion = exclusion

    def validate(self, record: dict, field_name: str):
        """Executes the value validation
        :param record: the record to validate
        :param field_name: the name of the field to validate
        :return: a violation description or None if validation passes
        """
        violation = None
        try:
            val = record[field_name]
            if val in self.values:
                violation = f'\'{val}\' is forbidden for field \'{field_name}\'.' if self.exclusion else None
            else:
                violation = f'\'{val}\' is not accepted for field \'{field_name}\'.' if not self.exclusion else None
        except KeyError:
            pass
        return violation


class ValueListFilter(FieldFilter):
    """Filters records on field values.
    """

    def __init__(self, field_names: set[str], values: set, exclusion: bool = False, on_violation: OpCode = None):
        """Initializes the handler.
        :param field_names: the names of the fields that will be validated
        :param values: the values against which fields will be tested
        :param exclusion: indicates if the provided value list is an exclusion list (black list) or a inclusion list
        (white list)
        :param on_violation: the operation code to return if validation failed. If None, a validation violation
        will raise a ValidationError.
        """
        super().__init__(field_names, ValueListChecker(values, exclusion), on_violation)


class SubstringValidator(Validator):

    def __init__(self, values: set, capture_regex: str = '(?P<capture>.*)',
                 capture_group_name: str = 'capture', exclusion: bool = False, ):
        """Initializes the handler.
        :param values: the values against which fields will be tested
        :param capture_regex: the regular expression used to capture substring
        :param capture_group_name: the name of the group to capture
        :param exclusion: indicates if the provided value list is an exclusion list (black list) or a inclusion list
        (white list)
        """
        super().__init__()
        self.values = values
        self.capture_regex = capture_regex
        self.capture_group_name = capture_group_name
        self.exclusion = exclusion

    def validate(self, record: dict, field_name: str):
        """Executes the value validation
        :param record: the record to validate
        :param field_name: the name of the field to validate
        :return: a violation description or None if validation passes
        """
        violation = None
        try:
            val = record[field_name]
            match = re.match(self.capture_regex, val)
            matching_val = match.group(self.capture_group_name)
            if matching_val in self.values:
                violation = f'\'{matching_val}\' is forbidden within field \'{field_name}\'.' if self.exclusion \
                    else None
            else:
                violation = f'\'{val}\' does not contain any accepted values for field \'{field_name}\'.' if not \
                    self.exclusion else None
        except KeyError:
            pass
        return violation


class SubstringFilter(FieldFilter):
    """Filters records on the specified text field value.
    """

    def __init__(self, field_names: set[str], values: set, capture_regex: str = '(?P<capture>.*)',
                 capture_group_name: str = 'capture', exclusion: bool = False,
                 on_violation: OpCode = None):
        """Initializes the handler.
        :param field_names: the names of the fields that will be validated
        :param values: the values against which fields will be tested
        :param capture_regex: the regular expression used to capture substring
        :param capture_group_name: the name of the group to capture
        :param exclusion: indicates if the provided value list is an exclusion list (black list) or a inclusion list
        (white list)
        :param on_violation: the operation code to return if validation failed. If None, a validation violation
        will raise a ValidationError.
        """
        super().__init__(field_names, SubstringValidator(values, capture_regex, capture_group_name, exclusion),
                         on_violation)


class TailingTextValidator(Validator):

    def __init__(self, values: set, exclusion: bool = False, ):
        """Initializes the handler.
        :param values: the values against which fields will be tested
        :param capture_regex: the regular expression used to capture substring
        :param capture_group_name: the name of the group to capture
        :param exclusion: indicates if the provided value list is an exclusion list (black list) or a inclusion list
        (white list)
        """
        super().__init__()
        self.values = values
        self.exclusion = exclusion

    def validate(self, record: dict, field_name: str):
        """Executes the value validation
        :param record: the record to validate
        :param field_name: the name of the field to validate
        :return: a violation description or None if validation passes
        """
        violation = None
        try:
            val = record[field_name]
            match = None
            for trail in self.values:
                if val.endswith(trail):
                    match = trail
                    if self.exclusion:
                        violation = f'\'{match}\' is forbidden as text trail in field \'{field_name}\'.'
                    else:
                        break
            if match is None and not self.exclusion:
                violation = f'\'{val}\' is not accepted because it does not match any accepted text trail for field' \
                            f' \'{field_name}\'.'
        except KeyError:
            pass
        return violation


class TrailingTextFilter(FieldFilter):
    """Filters records on fields whose the value ends with one of the accepted value.
    """

    def __init__(self, field_names: set[str], values: set, exclusion: bool = False, on_violation: OpCode = None):
        """Initializes the handler.
        :param field_names: the names of the fields that will be validated
        :param values: the values against which fields will be tested
        :param exclusion: indicates if the provided value list is an exclusion list (black list) or a inclusion list
        (white list)
        :param on_violation: the operation code to return if validation failed. If None, a validation violation
        will raise a ValidationError.
        """
        super().__init__(field_names, TailingTextValidator(values, exclusion), on_violation)


class BooleanFlagValidator(Validator):

    def __init__(self, accepted_value: bool = True, ):
        """Initializes the handler.
              :param accepted_value: the values against which fields will be tested
        """
        super().__init__()
        self.accepted_value = accepted_value

    def validate(self, record: dict, field_name: str):
        """Executes the value validation
        :param record: the record to validate
        :param field_name: the name of the field to validate
        :return: a violation description or None if validation passes
        """
        violation = None
        try:
            val = record[field_name]
            if not (val is self.accepted_value):
                violation = f'\'{val}\' is not accepted for field \'{field_name}\'.'
        except KeyError:

            pass
        return violation


class BooleanFlagFilter(FieldFilter):
    """Filters records on fields whose contains boolean flag.
    """

    def __init__(self, field_names: set[str], accepted_value: bool = True, on_violation: OpCode = None):
        """Initializes the handler.
        :param field_names: the names of the fields that will be validated
        :param accepted_value: the values against which fields will be tested
        :param on_violation: the operation code to return if validation failed. If None, a validation violation
        will raise a ValidationError.
        """
        super().__init__(field_names, BooleanFlagValidator(accepted_value), on_violation)
