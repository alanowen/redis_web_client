import socket
import getpass
from logging import Logger, getLoggerClass, LogRecord, getLogger


class RedisLogger(getLoggerClass()):

    def __init__(self):
        super(RedisLogger, self).__init__(name='redis')


class RedisLogRecord(LogRecord):
    
    def __init__(self, name, level, pathname, lineno,
                 msg, args, exc_info, func=None, sinfo=None, **kwargs):
        super(RedisLogRecord, self).__init__(name, level, pathname, lineno,
                                             msg, args, exc_info, func, sinfo, **kwargs)

        self.hostname = socket.gethostname()
