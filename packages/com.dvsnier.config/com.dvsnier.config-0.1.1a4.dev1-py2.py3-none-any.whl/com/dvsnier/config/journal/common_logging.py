# -*- coding:utf-8 -*-
# STRICT MODE

import logging
import os
import time

from com.dvsnier.config.base.iconf import IConf
from typing import Any, Dict, List, Literal, Optional, Union


class Logging(IConf, object):
    '''the logging class'''

    CRITICAL = 50  # type: Literal[50]
    FATAL = CRITICAL  # type: Literal[50]
    ERROR = 40  # type: Literal[40]
    WARNING = 30  # type: Literal[30]
    WARN = WARNING  # type: Literal[30]
    INFO = 20  # type: Literal[20]
    DEBUG = 10  # type: Literal[10]
    NOTSET = 0  # type: Literal[0]

    LOGGING_OUT_DIRECTORY_NAME = 'output_dir_name'  # type: Literal['output_dir_name']
    LOGGING_FILE_NAME = 'file_name'  # type: Literal['file_name']
    LOGGING_LEVEL = 'level'  # type: Literal['level']

    def __init__(self):
        super(Logging, self).__init__()
        # protected property
        self._logging_name = None  # type: Optional[str]
        # protected property
        self._fully_qualified_file_name = None  # type: Optional[str]
        # protected property
        self._fully_qualified_error_name = None  # type: Optional[str]
        # protected property
        self._kwargs = {
            self.LOGGING_OUT_DIRECTORY_NAME: '',
            # the never forget the original intention
            self.LOGGING_FILE_NAME: 'tnftoi',
            self.LOGGING_LEVEL: logging.WARNING,
        }  # type: Dict[str, Union[str, int]]
        # the recorder engine object
        self._logging_logger = None  # type: logging.Logger
        # the formatter engine object
        self._logging_formatter = None  # type: logging.Formatter
        # the console handle engine object
        self._logging_console_handler = None  # type: Optional[logging.StreamHandler]
        # the general file handle engine object
        self._logging_file_handler = None  # type: Optional[logging.FileHandler]
        # the error file handle engine object
        self._logging_error_handler = None  # type: Optional[logging.FileHandler]

    def kwargs(self, kwargs):  # type: (Dict[str, Union[str, int]]) -> Logging
        '''
            the logging config info:
                config(**kwargs={output_dir_name=\' \', file_name=\' \', level=logging.WARNING})

            the level value range:
                - CRITICAL = 50
                - FATAL = CRITICAL
                - ERROR = 40
                - WARNING = 30
                - WARN = WARNING
                - INFO = 20
                - DEBUG = 10
                - NOTSET = 0

            the article link reference:

                1. https://peps.python.org/pep-0282/
                2. https://docs.python.org/zh-cn/2.7/howto/logging.html#logging-basic-tutorial
                3. https://docs.python.org/zh-cn/2.7/howto/logging.html#logging-advanced-tutorial
                4. https://docs.python.org/zh-cn/2.7/howto/logging-cookbook.html#logging-cookbook
                5. https://docs.python.org/zh-cn/2.7/library/logging.html
        '''
        if kwargs:
            if kwargs.get(self.LOGGING_OUT_DIRECTORY_NAME) is None or isinstance(
                    kwargs.get(self.LOGGING_OUT_DIRECTORY_NAME), str) and len(
                        str(kwargs.get(self.LOGGING_OUT_DIRECTORY_NAME)).strip()) == 0:
                raise KeyError('the current kwargs([{}]: {} ) that is illegal.'.format(
                    self.LOGGING_OUT_DIRECTORY_NAME, kwargs.get(self.LOGGING_OUT_DIRECTORY_NAME)))
            if kwargs.get(self.LOGGING_FILE_NAME) is None or isinstance(kwargs.get(
                    self.LOGGING_FILE_NAME), str) and len(str(kwargs.get(self.LOGGING_FILE_NAME)).strip()) == 0:
                raise KeyError('the current kwargs([{}]: {} ) that is illegal.'.format(
                    self.LOGGING_FILE_NAME, kwargs.get(self.LOGGING_FILE_NAME)))
            if kwargs.get(self.LOGGING_LEVEL) is not None:
                __logging_level = kwargs.get(self.LOGGING_LEVEL)
                if __logging_level and isinstance(__logging_level, int):
                    if int(__logging_level) < logging.NOTSET:
                        raise KeyError('the current kwargs([{}]: {} ) that is illegal.'.format(
                            self.LOGGING_LEVEL, kwargs.get(self.LOGGING_LEVEL)))
                    elif __logging_level == logging.NOTSET:
                        kwargs[self.LOGGING_LEVEL] = logging.WARNING
                    else:
                        # nothing to do
                        pass
            elif kwargs.get(self.LOGGING_LEVEL) is None:
                kwargs[self.LOGGING_LEVEL] = logging.WARNING
            else:
                # nothing to do
                pass
            self._kwargs = kwargs
        else:
            raise KeyError('the current kwargs is illegal.')
        return self

    def build(self, console_only=True, file_record=True, error_record=True):  # type (bool, bool, bool) -> None
        ''' the build program '''
        if not console_only and not file_record and not error_record:
            return
        else:
            self.obtain_logger()  # type: logging.Logger
            if self._logging_logger:
                self._logging_logger.setLevel(self.get_kw_level())
            if console_only:
                self.set_logging_console(level=self.get_kw_level())
            if file_record:
                self.set_logging_file(level=self.get_kw_level())
                self._logging_logger.info('this current generic file is {}'.format(self._fully_qualified_file_name))
            if error_record:
                self.set_logging_error()
                self._logging_logger.info('this current error file is {}'.format(self._fully_qualified_error_name))

    def generic_logging_file_prefix(self, file_prefix, error_mark=False):  # type: (str, bool) -> str
        ''' the generic logging file preix '''
        if error_mark:
            return "error_{}_{}.log".format(file_prefix, int(time.time()))
        else:
            return "{}_{}.log".format(file_prefix, int(time.time()))

    def obtain_logger(self, logging_name=None):  # type: (Optional[str]) -> logging.Logger
        ''' the obtain logger '''
        if self._logging_logger:
            return self._logging_logger
        else:
            self.set_logging_name(logging_name)
            if self.get_logging_name():
                self._logging_logger = logging.getLogger(self.get_logging_name())
            return self._logging_logger

    # @HIDE
    def set_logger(self, logger):  # type (logging.Logger) -> Logging
        ''' the set logger '''
        if logger:
            self._logging_logger = logger
        return self

    def get_kw_output_dir_name(self):  # type: () -> str
        ''' the get kw output directory name '''
        # After consideration, I don't agree with the path policy given by the program by default
        # when the user doesn't specify the parameters
        logging_out_directory_name = self._kwargs.get(self.LOGGING_OUT_DIRECTORY_NAME, '')
        if not isinstance(logging_out_directory_name, str):
            logging_out_directory_name = str(logging_out_directory_name)
        return logging_out_directory_name

    def set_kw_output_dir_name(self, output_dir_name):  # type: (Optional[str]) -> Logging
        ''' the set kw output directory name, note that relative paths are currently not supported '''
        if output_dir_name:
            self._kwargs[self.LOGGING_OUT_DIRECTORY_NAME] = output_dir_name
        return self

    def get_kw_file_name(self):  # type: () -> str
        ''' the get kw file name '''
        logging_file_name = self._kwargs.get(self.LOGGING_FILE_NAME, '')
        if not isinstance(logging_file_name, str):
            logging_file_name = str(logging_file_name)
        return logging_file_name

    def set_kw_file_name(self, file_name):  # type: (str) -> Logging
        ''' the set kw file name '''
        if file_name:
            self._kwargs[self.LOGGING_FILE_NAME] = file_name
        return self

    def get_kw_level(self):  # type: () -> int
        ''' the get kw level '''
        logging_level = self._kwargs.get(self.LOGGING_LEVEL, logging.WARNING)
        if not isinstance(logging_level, int):
            logging_level = int(logging_level)
        return logging_level

    def set_kw_level(self, level):  # type: (int) -> Logging
        ''' the set kw level '''
        self._kwargs[self.LOGGING_LEVEL] = level
        return self

    def get_logging_name(self):  # type: () -> Optional[str]
        ''' the get logging name '''
        if not self._logging_name:
            self.set_logging_name()
        return self._logging_name

    def set_logging_name(self, logging_name=None):  # type: (Optional[str]) -> Logging
        ''' the get logging name that default value is root '''
        if logging_name:
            self._logging_name = logging_name
        else:
            self._logging_name = 'root'
        return self

    def get_logging_formatter(self):  # type: () -> logging.Formatter
        ''' the get logging formatter '''
        if not self._logging_formatter:
            self.set_logging_formatter()
        return self._logging_formatter

    def set_logging_formatter(self,
                              logging_formatter=None,
                              format_style=logging.WARNING):  # type: (Optional[str], int) -> Logging
        '''
            the get logging formatter

            the following format information may be required:

                0. '[%(asctime)s][%(levelname)8s] --- %(message)s'
                1. '[%(asctime)s][%(name)15s][%(levelname)8s] --- [%(filename)s:%(lineno)s] --- %(message)s'
        '''
        if logging_formatter:
            self._logging_formatter = logging.Formatter(logging_formatter)
        else:
            if format_style == logging.DEBUG:
                self._logging_formatter = logging.Formatter(
                    '[%(asctime)s][%(name)15s][%(levelname)8s] --- [%(filename)s:%(lineno)s] --- %(message)s')
            else:
                self._logging_formatter = logging.Formatter('[%(asctime)s][%(levelname)8s] --- %(message)s')
        return self

    def set_logging_console(self, level=logging.DEBUG):  # type: (int) -> Logging
        ''' the set console output logging '''
        self._logging_console_handler = logging.StreamHandler()
        if level < logging.NOTSET or level > logging.CRITICAL:
            level = logging.WARNING
        self._logging_console_handler.setLevel(level)
        self._logging_console_handler.setFormatter(self.get_logging_formatter())
        if self._logging_logger:
            self._logging_logger.addHandler(self._logging_console_handler)
        return self

    def set_logging_file(self,
                         filename=None,
                         mode='a',
                         encoding='utf-8',
                         level=logging.DEBUG):  # type: (Optional[str], str, str, int) -> Logging
        ''' the set file output logging '''
        if filename:
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        else:
            if not os.path.exists(self.get_kw_output_dir_name()):
                os.makedirs(self.get_kw_output_dir_name())
            filename = os.path.join(self.get_kw_output_dir_name(),
                                    self.generic_logging_file_prefix(self.get_kw_file_name()))
        self._fully_qualified_file_name = filename
        self._logging_file_handler = logging.FileHandler(filename, mode, encoding)
        if level < logging.NOTSET or level > logging.CRITICAL:
            level = logging.WARNING
        self._logging_file_handler.setLevel(level)
        self._logging_file_handler.setFormatter(self.get_logging_formatter())
        if self._logging_logger:
            self._logging_logger.addHandler(self._logging_file_handler)
        return self

    def set_logging_error(self,
                          filename=None,
                          mode='a',
                          encoding='utf-8',
                          level=logging.ERROR):  # type: (Optional[str], str, str, int) -> Logging
        ''' the set error output logging '''
        if filename:
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        else:
            if not os.path.exists(self.get_kw_output_dir_name()):
                os.makedirs(self.get_kw_output_dir_name())
            filename = os.path.join(self.get_kw_output_dir_name(),
                                    self.generic_logging_file_prefix(self.get_kw_file_name(), error_mark=True))
        self._fully_qualified_error_name = filename
        self._logging_error_handler = logging.FileHandler(filename, mode, encoding)
        if level < logging.NOTSET or level > logging.CRITICAL:
            level = logging.WARNING
        self._logging_error_handler.setLevel(level)
        self._logging_error_handler.setFormatter(self.get_logging_formatter())
        if self._logging_logger:
            self._logging_logger.addHandler(self._logging_error_handler)
        return self

    def debug(self, msg, *args, **kwargs):  # type: (Optional[str], List, Any) -> None
        # **kwargs typye is
        # Union[None, bool, Union[Tuple[type, BaseException, Optional[TracebackType]], Tuple[None, None, None]]]
        if self._logging_logger:
            self.obtain_logger()
        self._logging_logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):  # type: (Optional[str], List, Any) -> None
        if self._logging_logger:
            self.obtain_logger()
        self._logging_logger.info(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):  # type: (int, Optional[str], List, Any) -> None
        if self._logging_logger:
            self.obtain_logger()
        self._logging_logger.log(level, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):  # type: (Optional[str], List, Any) -> None
        if self._logging_logger:
            self.obtain_logger()
        self._logging_logger.warning(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):  # type: (Optional[str], List, Any) -> None
        if self._logging_logger:
            self.obtain_logger()
        self._logging_logger.warn(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):  # type: (Optional[str], List, Any) -> None
        if self._logging_logger:
            self.obtain_logger()
        self._logging_logger.exception(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):  # type: (Optional[str], List, Any) -> None
        if self._logging_logger:
            self.obtain_logger()
        self._logging_logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):  # type: (Optional[str], List, Any) -> None
        if self._logging_logger:
            self.obtain_logger()
        self._logging_logger.critical(msg, *args, **kwargs)
