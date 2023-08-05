from knifes import times
from django.conf import settings
import requests
import threading
import logging
logger = logging.getLogger(__name__)


# 异步发送报警
def async_send_msg(msg):
    threading.Thread(target=send_work_wx_msg(msg)).start()


def send_work_wx_msg(msg):
    data = {
        'msgtype': 'text',
        'text': {
            'content': '{} [{}]'.format(msg, times.strftime())
        }
    }
    try:
        requests.post(settings.WORK_WX_ALARM_API, json=data, timeout=10, verify=False)
    except Exception:
        logger.exception('推送报警信息失败:{}'.format(msg))