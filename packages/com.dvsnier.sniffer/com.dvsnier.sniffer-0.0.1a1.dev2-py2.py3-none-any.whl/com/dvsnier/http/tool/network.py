# -*- coding:utf-8 -*-

import time

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.base.abstract_http import AbstractHttp
from com.dvsnier.http.tool.iexecute import IExecute
from com.dvsnier.http.util.utils import output_exception_queue


class Network(AbstractHttp, object):
    '''the network class'''
    def __init__(self):
        super(Network, self).__init__()

    def pull_bbs_to_local(self, _on_callback):
        'the pull bbs to local method'
        start = time.time()
        urls = []
        IExecute().invoked(_on_callback, urls)
        end = time.time()
        # if urls:
        #     logging.debug(json.dumps(urls, ensure_ascii=False, indent=4))
        logging.info(
            'the execute task(pull_bbs_to_local) has completed, that total time consumed {:.3f} seconds '.format(end -
                                                                                                                 start))
        output_exception_queue()
