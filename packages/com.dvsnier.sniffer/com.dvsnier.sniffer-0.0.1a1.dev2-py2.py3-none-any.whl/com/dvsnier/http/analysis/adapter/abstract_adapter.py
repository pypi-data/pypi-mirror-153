# -*- coding:utf-8 -*-

from com.dvsnier.http.analysis.adapter.idapter import IAdapter


class AbstractAdapter(IAdapter, object):
    '''the abstract dapter class'''
    def __init__(self):
        super(AbstractAdapter, self).__init__()
