# -*- coding: utf-8 -*-

from monkey.crawler.op_codes import OpCode
from monkey.crawler.processor import Handler


class FieldCalculator(Handler):
    """Evaluates an expression and store the result in the specified field.
    Expression may use record fields using 'record' to refer the provided record. For example expression, expression
    '(record[\'first_name\']+record[\'last_name\']).upper()' will compute the concatenation of fields 'first_name' and
    'last_name' then convert into uppercase.
    """

    def __init__(self, expr: str, result_field_name: str):
        """Initializes the handler.
        :param expr: the expression that will be evaluated.
        :param result_field_name: the name of the field that will store the calculated value.
        """
        super().__init__()
        self.expr = expr
        self.result_field_name = result_field_name

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the evaluation of the expression and store the formatted value in the specified target field.
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation
        :return: a copy of the provided record that contains the evaluated value in the target field
        :return: the provided operation code
        """
        rec = record.copy()
        rec[self.result_field_name] = eval(self.expr)
        return rec, op_code


class FlagCalculator(FieldCalculator):
    """Evaluates an expression as a boolean and store the result in the specified field. The handler can update the
    operation code depending on the expression evaluation result.
    """

    def __init__(self, expr: str, result_field_name: str = None, if_true_op_code: OpCode = None,
                 if_false_op_code: OpCode = None):
        """Initializes the handler.
        :param expr: the expression that will be evaluated.
        :param result_field_name: the name of the field that will store the calculated value.
        :param if_true_op_code: the operation code to return if the expression is evaluated to True
        :param if_false_op_code: the operation code to return if the expression is evaluated to False
        """
        super().__init__(expr, result_field_name)
        self.if_true_op_code = if_true_op_code
        self.if_false_op_code = if_false_op_code

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the evaluation of the expression and store the formatted value in the specified target field.
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation
        :return: a copy of the provided record that contains the evaluated value in the target field
        :return: the operation code depending on the expression evaluation
        """
        rec = record.copy()
        flag_val = eval(self.expr)
        if flag_val:
            op_code = op_code if self.if_true_op_code is None else self.if_true_op_code
        else:
            op_code = op_code if self.if_false_op_code is None else self.if_false_op_code
        if self.result_field_name is not None:
            rec[self.result_field_name] = flag_val
        return rec, op_code
