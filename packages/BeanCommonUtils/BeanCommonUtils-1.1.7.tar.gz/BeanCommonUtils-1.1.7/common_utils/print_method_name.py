from common_utils.new_log import NewLog


class PrintMethodName:

    log = NewLog(__name__)
    logger = log.get_log()

    def __call__(self, func):
        def wrapper(*args, **kw):
            self.logger.debug("begin call method %s ====================" % func.__name__)
            result = func(*args, **kw)
            return result
        return wrapper
