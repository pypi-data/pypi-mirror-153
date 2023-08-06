from logging.handlers import TimedRotatingFileHandler
import logging
from knifes import alarm


# critical级别日志报警
class TimedRotatingFileWithCriticalAlarmHandler(TimedRotatingFileHandler):
    def emit(self, record):
        super(TimedRotatingFileWithCriticalAlarmHandler, self).emit(record)
        if record.levelno == logging.CRITICAL:
            alarm.async_send_msg(record.getMessage())
