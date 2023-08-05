# -*- coding:utf-8 -*-

import os
import time

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.synchron.base.abstract_synchron import AbstractSynchron
from com.dvsnier.http.tool.iexecute import IExecute


class ObjectNotationSynchron(AbstractSynchron, object):
    '''the object notation synchron class'''
    def __init__(self):
        super(ObjectNotationSynchron, self).__init__()

    def swap(self, lf, rf, _on_callback=None, *union_primary_key):
        'the swap method'
        start = time.time()
        if os.path.exists(lf) and os.path.exists(rf):
            pass
        end = time.time()
        logging.info('the execute task union-id({}) has completed, that total time consumed {:.3f} seconds '.format(
            '', end - start))
        IExecute().execute(_on_callback)
        pass
