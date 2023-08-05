# -*- coding:utf-8 -*-

import os
import sys
import time
from typing import Any

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.dom.common_dom import CommonDom
from datetime import datetime
from hashlib import md5


class AnalysisFactory(object):
    '''the analysis factory class'''

    # public property
    kw = dict()

    def __init__(self):
        super(AnalysisFactory, self).__init__()
        # self.kw = dict()

    @classmethod
    def obtain(cls):
        uuid = AnalysisFactory.get_uuid()
        if uuid in cls.kw.keys():
            logging.info('the current instance uuid({}) has skipped.'.format(uuid))
        else:
            logging.info('the current instance uuid({}) produced and running is successfully.'.format(uuid))
            cls.kw[uuid] = CommonDom()
        return cls

    @classmethod
    def create_tianya_analysis(cls, _on_callback):
        'the create tianya analysis'
        # packings = AbstractPackings()
        # packings.execute(_on_callback)
        # return packings
        #
        # 1. bugfixs circular import question
        #
        return _on_callback()

    @classmethod
    def get_com(cls, _on_callback=None):  # type: (Any) -> CommonDom
        'get the common object model that simply as com, and the granularity is valid only for the current process'
        uuid = cls.get_uuid()
        common_object_model = cls.kw.get(uuid)
        if not common_object_model:
            if _on_callback:
                common_object_model = _on_callback(uuid)
            else:
                raise KeyError('the uuid common object model of the current process is invalid. please reset it')
        return common_object_model

    @classmethod
    def get_special_com(cls, uuid, _on_callback=None):  # type: (str, Any) -> CommonDom
        'get the special common object model that simply as com, and the granularity is valid only for the current process'
        if uuid:
            common_object_model = cls.kw.get(uuid)
            if not common_object_model:
                if _on_callback:
                    common_object_model = _on_callback(uuid)
                else:
                    raise KeyError('the uuid common object model of the current process is invalid. please reset it')
            return common_object_model
        else:
            return cls.get_com(_on_callback)

    @classmethod
    def get_special_uuid(cls, name):
        'get the special uuid'
        uuid = None
        if not name:
            if sys.version_info.major == 3 and sys.version_info.minor >= 3:
                uuid = md5(str(datetime.timestamp(datetime.now())).encode('utf-8')).hexdigest()
            else:
                uuid = md5(str(time.time()).encode('utf-8')).hexdigest()
            logging.info('the currently preparing to automatically generate uuid that value is {}.'.format(uuid))
        else:
            uuid = md5(str(name + ':' + str(os.getpid())).encode('utf-8')).hexdigest()
        return uuid

    @classmethod
    def get_uuid(cls):
        'the get anonymous uuid'
        return cls.get_special_uuid(name='anonymous')
