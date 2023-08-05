# -*- coding:utf-8 -*-

from com.dvsnier.http.synchron.upk.iupk import IUpk


class AbstractUpk(IUpk, object):
    '''the abstract union primary key class'''
    def __init__(self):
        super(AbstractUpk, self).__init__()
