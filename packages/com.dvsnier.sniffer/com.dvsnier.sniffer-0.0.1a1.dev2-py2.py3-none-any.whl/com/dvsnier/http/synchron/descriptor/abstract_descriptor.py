# -*- coding:utf-8 -*-

from com.dvsnier.http.synchron.descriptor.idescriptor import IDescriptor


class AbstractDescriptor(IDescriptor, object):
    '''the abstract descriptor class'''
    def __init__(self):
        super(AbstractDescriptor, self).__init__()
