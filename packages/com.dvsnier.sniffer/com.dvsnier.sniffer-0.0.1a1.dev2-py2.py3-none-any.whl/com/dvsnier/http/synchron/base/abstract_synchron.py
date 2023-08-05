# -*- coding:utf-8 -*-

from com.dvsnier.http.synchron.base.isynchron import ISynchron


class AbstractSynchron(ISynchron, object):
    '''the abstract synchron class'''
    def __init__(self):
        super(AbstractSynchron, self).__init__()

    def template(self):
        'the template method'
        pass
