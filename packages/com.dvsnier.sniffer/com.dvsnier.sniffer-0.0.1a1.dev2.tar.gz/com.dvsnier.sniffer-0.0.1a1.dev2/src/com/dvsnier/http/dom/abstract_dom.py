# -*- coding:utf-8 -*-

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.dom.attribute.abstract_attribute import AbstractAttribute
from com.dvsnier.http.dom.content.abstract_bbs_content import AbstractBbsContent
from com.dvsnier.http.dom.idom import IDom
from com.dvsnier.http.tool.iexecute import IExecute


class AbstractDom(IDom, object):
    '''the abstract dom class'''

    # protected property
    _attribute = None
    # protected property
    _content = None

    def __init__(self):
        super(AbstractDom, self).__init__()
        self._attribute = AbstractAttribute()
        self._content = AbstractBbsContent()
        # private property
        self.__common_object_model = AnalysisFactory.get_com()
        self.__common_object_model.set_attribute(
            self._attribute, lambda it: logging.debug('the {} object configured successfully.'.format('attribute')))
        self.__common_object_model.set_content(
            self._content, lambda it: logging.debug('the {} object configured successfully.'.format('content')))

    def get_attribute(self):
        'the get attribute instance'
        if not self._attribute:
            raise KeyError(
                'The current value({}) is invalid and illegal, and then please reset the value'.format('attribute'))
        return self._attribute

    def get_content(self):
        'the get content instance'
        if not self._content:
            raise KeyError(
                'The current value({}) is invalid and illegal, and then please reset the value'.format('content'))
        return self._content

    def set_attribute(self, attribute, _on_attribute_callback=None):
        'the set attribute object'
        self._attribute = attribute
        IExecute().execute(_on_attribute_callback, self._attribute)
        return self

    def set_content(self, content, _on_content_callback=None):
        'the set content object'
        self._content = content
        IExecute().execute(_on_content_callback, self._content)
        return self
