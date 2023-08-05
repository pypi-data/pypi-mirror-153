# -*- coding:utf-8 -*-

import datetime
import random
import requests
import time
import traceback

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.tool.ilogging import ILogging
from requests import codes, ConnectTimeout, ReadTimeout, Timeout


class IHttp(object):
    '''the ihttp class'''

    _COUNT = 0
    _MAX_COUNT = 3

    def __init__(self):
        super(IHttp, self).__init__()

    def set_logging(self, _on_callback=None):
        self.logging = ILogging()
        self.logging.set_logging(_on_callback)

    def get(self, url, timeout=60, _on_callback=None):
        '''
            the get requtst that reply to response object
            '_content', 'status_code', 'headers', 'url', 'history','encoding', 'reason', 'cookies', 'elapsed', 'request'
        '''
        headers = None
        response = None
        UA = 'User-Agent'
        try:
            if _on_callback:
                headers = _on_callback()
                response = requests.get(url, headers=headers, timeout=timeout)
            else:
                # private property
                __common_object_model = AnalysisFactory.get_com()
                if __common_object_model.get_cfg() and __common_object_model.get_cfg().get(UA):
                    headers = {UA: __common_object_model.get_cfg().get(UA)}
                    response = requests.get(url, headers=headers, timeout=timeout)
                else:
                    response = requests.get(url, timeout=timeout)
        except (ConnectTimeout, ReadTimeout, Timeout) as e:
            # private property
            __common_object_model = AnalysisFactory.get_com()
            __common_object_model.get_eoe().append({
                'id': url,
                'emsg': str(e),
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            # logging.exception(e)
            logging.exception('the current tracked information: {}'.format(traceback.format_exc()))
            if self._COUNT < self._MAX_COUNT:
                self._COUNT += 1
                random_value = self._COUNT * self._MAX_COUNT + random.random()
                logging.warning(
                    'the current request timed out, sleep that is {:.3f}s and soon afterwards start {}th request...'.
                    format(random_value, self._COUNT))
                time.sleep(random_value)
                response = self.get(url, timeout, _on_callback)
            else:
                self._COUNT = 0
        else:
            if response.status_code != codes.ok:
                # private property
                __common_object_model = AnalysisFactory.get_com()
                __common_object_model.get_eoe().append({
                    'id':
                    url,
                    'emsg':
                    'the current error code that is {}'.format(response.status_code),
                    'timestamp':
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                if self._COUNT < self._MAX_COUNT:
                    self._COUNT += 1
                    random_value = self._COUNT * self._MAX_COUNT + random.random()
                    logging.warning(
                        'the current request timed out, sleep that is {:.3f}s and soon afterwards start {}th request...'
                        .format(random_value, self._COUNT))
                    time.sleep(random_value)
                    response = self.get(url, timeout, _on_callback)
                else:
                    self._COUNT = 0
        return response
