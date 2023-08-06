# -*- coding: UTF-8 -*-

from common_utils.new_log import NewLog


class LogDecorator:

    log = NewLog(__name__)
    logger = log.get_log()

    def __call__(self, func):
        def wrapper(*args, **kw):
            self.logger.debug("call method %s ===============" % func.__name__)
            self.logger.debug("method [%s] input args: [%s],  kw: [%s]" % (func.__name__, args, kw))
            result = func(*args, **kw)
            self.logger.debug("method [%s] response: [%s]" % (func.__name__, result))
            return result
        return wrapper
