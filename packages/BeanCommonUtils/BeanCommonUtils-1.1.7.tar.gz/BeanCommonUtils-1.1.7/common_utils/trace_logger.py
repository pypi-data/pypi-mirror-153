# 每个日志文件的最大字节数
import logging
from logging.handlers import TimedRotatingFileHandler

from flask_log_request_id import RequestIDLogFilter

# 每个日志文件的最大字节数
MAX_BYTES = 1024 * 1024 * 1
# 最大日志文件备份数
BACKUP_COUNT = 10
# 默认格式化输出
DEFAULT_FORMATTER = """%(asctime)s - [%(filename)s line:%(lineno)s] - level=%(levelname)s \
- request_id=%(request_id)s - %(message)s"""


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


class TraceLogger:

    @classmethod
    def get_logger(cls, log_file_path, logger_name="flask_trace", level="INFO"):
        """
        :param log_file_path: 日志文件的绝对路径
        :param logger_name: 初始化logger的名字, 建议使用默认值
        :param level: 默认INFO, 建议使用默认值
        :return:
        """
        logger = logging.getLogger(logger_name)

        # 如果已经实例过一个相同名字的 logger，则不用再追加 handler
        if not logger.handlers:
            logger.setLevel(level=level)
            # midnight 表示每天凌晨自动切割文件
            time_file_handler = TimedRotatingFileHandler(
                filename=log_file_path, when="midnight", encoding="utf8", backupCount=BACKUP_COUNT)
            time_file_handler.suffix = "%Y-%m-%d_%H-%M-%S"
            formatter = OneLineExceptionFormatter(DEFAULT_FORMATTER)
            time_file_handler.setFormatter(formatter)
            time_file_handler.addFilter(RequestIDLogFilter())  # << Add request id contextual filter
            logger.addHandler(time_file_handler)
        return logger
