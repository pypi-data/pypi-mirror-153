# -*- coding:utf-8 -*-

from com.dvsnier.http.synchron.generator.igenerator import IGenerator


class AbstractGenerator(IGenerator, object):
    '''the abstract generator class'''
    def __init__(self):
        super(AbstractGenerator, self).__init__()
