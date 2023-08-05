# -*- coding: utf-8 -*-

import logging
import time

from monkey.crawler.op_codes import OpCode


class RecoverableError(Exception):

    def __init__(self, message='Recoverable error', cause=None):
        self.message = message
        self.cause = cause


class InputError(Exception):

    def __init__(self, record_info, explanation='', cause=None):
        self.message = f'Bad input for record: {record_info} -> {explanation}'
        self.record_info = record_info
        self.cause = cause


class ProcessingError(Exception):
    def __init__(self, record_info, explanation='', cause=None):
        self.message = f'{explanation} -> {cause}\n\t{record_info}'
        self.record_info = record_info
        self.cause = cause


class Handler:
    """Supports misc operation to prepare record for processing.  This may include validation, formatting, projection
    (reduction), enrichment, flattening, transformation, calculation, etc."""

    def __init__(self):
        self.logger = logging.getLogger(f'{self.__class__.__module__}.{self.__class__.__name__}')

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs an operation on the supplied record in preparation for processing.
        :param record: the record to handle
        :param op_code: the operation code computed by any previous operation
        :return: a new record resulting of the operation run
        :return: a computed operation code that can influence the global processing of the record
        """
        raise NotImplemented()


class Processor:
    def __init__(self, source_name: str, handlers: list[Handler] = None):
        self.logger = logging.getLogger(f'{self.__class__.__module__}.{self.__class__.__name__}')
        self.source_name = source_name
        self.handlers = [] if handlers is None else handlers
        self._start_time = 0
        self._end_time = 0

    def __enter__(self):
        self._end_time = 0
        self._start_time = time.time()
        self._enter()
        return self

    def _enter(self):
        raise NotImplementedError()

    def __exit__(self, *args):
        self._end_time = time.time()
        self._exit()
        return False

    def _exit(self):
        raise NotImplementedError()

    def process(self, record, allow_retry=False):
        try:
            rec, op_code = self._prepare(record)
            if op_code not in (OpCode.IGNORE, OpCode.SKIP, OpCode.ERROR):
                op_code = self._process(rec)
        except RecoverableError as e:
            self.logger.error(f'{self.source_name} - RECOVERABLE ERROR - {e.message}')
            if allow_retry:
                op_code = OpCode.RETRY
            else:
                op_code = OpCode.ERROR
        except InputError as e:
            self.logger.error(f'{self.source_name} - INPUT ERROR - {e.message}')
            op_code = OpCode.ERROR
        except ProcessingError as e:
            self.logger.error(f'{self.source_name} - PROCESSING ERROR - {e.message}')
            op_code = OpCode.ERROR
        except Exception as e:
            self.logger.error(f'{self.source_name} - UNEXPECTED ERROR - {e}')
            op_code = OpCode.ERROR
        self.logger.log(op_code.get_default_logging_level(), f'{self.source_name} - {op_code.get_name()} - {record}')
        return op_code

    def _prepare(self, record):
        rec = record
        op_code = None
        for handler in self.handlers:
            handler: Handler
            try:
                rec, op_code = handler.handle(rec, op_code)
                if rec is None:
                    break
            except ProcessingError as e:
                raise e
            except Exception as e:
                raise ProcessingError(record, f'{type(handler).__name__} failed to handle record', e)
        return rec, op_code

    def _process(self, record):
        """Actual processing of a handled objet
        :param record: The record object to process
        :return: The executed operation code
        """
        raise NotImplemented()

    def get_processing_duration(self):
        if self._start_time > 0:
            if self._end_time > 0:
                return self._end_time - self._start_time
            else:
                return time.time() - self._start_time
        else:
            return 0
