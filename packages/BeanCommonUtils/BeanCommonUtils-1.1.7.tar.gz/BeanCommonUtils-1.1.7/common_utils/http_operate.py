# -*- coding: UTF-8 -*-

import requests
import time
from common_utils.new_log import NewLog


class HttpOperate:

    log = NewLog(__name__)
    logger = log.get_log()
    interval_time = 0.5
    session = requests.Session()

    @classmethod
    def http_get(cls, url, headers, params=None, **kwargs):
        response = cls.session.get(url=url, headers=headers, params=params, **kwargs)
        time.sleep(cls.interval_time)
        return response.text, response.status_code

    @classmethod
    def http_post(cls, url, headers, params=None, data=None,  **kwargs):
        response = cls.session.post(url=url, headers=headers, params=params, data=data, **kwargs)
        time.sleep(cls.interval_time)
        return response.text, response.status_code

    @classmethod
    def http_put(cls, url, headers, data=None, **kwargs):
        response = cls.session.put(url=url, headers=headers, data=data, **kwargs)
        time.sleep(cls.interval_time)
        return response.text, response.status_code

    @classmethod
    def http_delete(cls, url, headers, **kwargs):
        response = cls.session.delete(url=url, headers=headers, **kwargs)
        time.sleep(cls.interval_time)
        return response.text, response.status_code
