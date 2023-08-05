# -*- coding:utf-8 -*-

from com.dvsnier.http.dom.attribute.iattribute import IAttribute
from com.dvsnier.http.tool.iexecute import IExecute


class AbstractAttribute(IAttribute, object):
    '''the abstract attribute class'''

    __RESOURCE_PERSISTENCE = False  # False: resource not persistence to local otherwise True: resource ok
    __RESOURCE_QUALITY = False  # False: resource thumbnail quality otherwise True: resource original quality

    def __init__(self):
        super(AbstractAttribute, self).__init__()

    def get_persistence(self):
        'the get resource persistence'
        return self.__RESOURCE_PERSISTENCE

    def get_quality(self):
        'the get resource quality'
        return self.__RESOURCE_QUALITY

    def set_persistence(self, resource_persistence, _on_resource_persistence_callback=None):
        'the set resource persistence and the default value that is False: resource not persistence to local otherwise True: resource ok'
        self.__RESOURCE_PERSISTENCE = resource_persistence
        IExecute().execute(_on_resource_persistence_callback, self.__RESOURCE_PERSISTENCE)
        return self

    def set_quality(self, resource_quality, _on_resource_quality_callback=None):
        'the set resource quality and the default value that is False: resource thumbnail quality otherwise True: resource original quality'
        self.__RESOURCE_QUALITY = resource_quality
        IExecute().execute(_on_resource_quality_callback, self.__RESOURCE_QUALITY)
        return self
