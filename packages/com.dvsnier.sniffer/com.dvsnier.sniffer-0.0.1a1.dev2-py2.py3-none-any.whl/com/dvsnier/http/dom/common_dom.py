# -*- coding:utf-8 -*-

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.dom.idom import IDom
from com.dvsnier.http.tool.iexecute import IExecute


class CommonDom(IDom, object):
    '''
        the common dom class

        The parameter data structure is described below:

        {
            "attribute": object,
            "brs": object,
            "cfg": object,
            "content": object,
            "comment_model": object,
            "debug": object,
            "eoe": object,
            "http": object,
            "model": object,
            "meta_model": object,
            "publisher_model": object,
            "resolver": object,
            "respondent_model": object
        }
    '''

    # protected property
    # _debug = True
    # protected property
    _debug = False

    def __init__(self):
        super(CommonDom, self).__init__()
        self.common_object = dict()

    def get_attribute(self):
        'the get attribute instance'
        attribute = self.common_object.get('attribute')
        if self._debug:
            if not attribute:
                logging.warning(
                    'The current value({}) is invalid and illegal, and then please reset the value'.format('attribute'))
        return attribute

    def get_brs(self):
        'the get brs instance'
        brs = self.common_object.get('brs')
        if self._debug:
            if not brs:
                logging.warning(
                    'The current value({}) is invalid and illegal, and then please reset the value'.format('brs'))
        return brs

    def get_cfg(self):
        'the get cfg instance'
        cfg = self.common_object.get('cfg')
        if self._debug:
            if not cfg:
                logging.warning(
                    'The current value({}) is invalid and illegal, and then please reset the value'.format('cfg'))
        return cfg

    def get_content(self):
        'the get content instance'
        content = self.common_object.get('content')
        if self._debug:
            if not content:
                logging.warning(
                    'The current value({}) is invalid and illegal, and then please reset the value'.format('content'))
        return content

    def get_comment_model(self):
        'the get comment model instance'
        comment_model = self.common_object.get('comment_model')
        if self._debug:
            if not comment_model:
                logging.warning('The current value({}) is invalid and illegal, and then please reset the value'.format(
                    'comment_model'))
        return comment_model

    def get_debug(self):
        'the get debug instance'
        debug = self.common_object.get('debug')
        if self._debug:
            if not debug:
                logging.warning(
                    'The current value({}) is invalid and illegal, and then please reset the value'.format('debug'))
        return debug

    def get_eoe(self):
        'the get eoe instance'
        eoe = self.common_object.get('eoe')
        if self._debug:
            if not eoe:
                logging.warning(
                    'The current value({}) is invalid and illegal, and then please reset the value'.format('eoe'))
        return eoe

    def get_http(self):
        'the get http instance'
        http = self.common_object.get('http')
        if self._debug:
            if not http:
                logging.warning(
                    'The current value({}) is invalid and illegal, and then please reset the value'.format('http'))
        return http

    def get_model(self):
        'the get model instance'
        model = self.common_object.get('model')
        if self._debug:
            if not model:
                logging.warning(
                    'The current value({}) is invalid and illegal, and then please reset the value'.format('model'))
        return model

    def get_meta_model(self):
        'the get meta model instance'
        meta_model = self.common_object.get('meta_model')
        if self._debug:
            if not meta_model:
                logging.warning('The current value({}) is invalid and illegal, and then please reset the value'.format(
                    'meta_model'))
        return meta_model

    def get_publisher_model(self):
        'the get publisher model instance'
        publisher_model = self.common_object.get('publisher_model')
        if self._debug:
            if not publisher_model:
                logging.warning('The current value({}) is invalid and illegal, and then please reset the value'.format(
                    'publisher_model'))
        return publisher_model

    def get_resolver(self):
        'the get resolver instance'
        resolver = self.common_object.get('resolver')
        if self._debug:
            if not resolver:
                logging.warning(
                    'The current value({}) is invalid and illegal, and then please reset the value'.format('resolver'))
        return resolver

    def get_respondent_model(self):
        'the get respondent model instance'
        respondent_model = self.common_object.get('respondent_model')
        if self._debug:
            if not respondent_model:
                logging.warning('The current value({}) is invalid and illegal, and then please reset the value'.format(
                    'respondent_model'))
        return respondent_model

    def set_attribute(self, attribute, _on_attribute_callback=None):
        'the set attribute object'
        self.common_object['attribute'] = attribute
        IExecute().invoked(_on_attribute_callback, self.get_attribute())
        return self

    def set_brs(self, brs, _on_brs_callback=None):
        'the set brs object'
        self.common_object['brs'] = brs
        IExecute().invoked(_on_brs_callback, self.get_brs())
        return self

    def set_cfg(self, cfg, _on_cfg_callback=None):
        'the set cfg object'
        self.common_object['cfg'] = cfg
        IExecute().invoked(_on_cfg_callback, self.get_cfg())
        return self

    def set_content(self, content, _on_content_callback=None):
        'the set content object'
        self.common_object['content'] = content
        IExecute().invoked(_on_content_callback, self.get_content())
        return self

    def set_comment_model(self, comment_model, _on_comment_model_callback=None):
        'the set comment model object'
        self.common_object['comment_model'] = comment_model
        IExecute().invoked(_on_comment_model_callback, self.get_comment_model())
        return self

    def set_debug(self, debug, _on_debug_callback=None):
        'the set debug object'
        self.common_object['debug'] = debug
        IExecute().invoked(_on_debug_callback, self.get_debug())
        return self

    def set_eoe(self, eoe, _on_eoe_callback=None):
        'the set eoe object'
        self.common_object['eoe'] = eoe
        IExecute().invoked(_on_eoe_callback, self.get_eoe())
        return self

    def set_http(self, http, _on_http_callback=None):
        'the set http object'
        self.common_object['http'] = http
        IExecute().invoked(_on_http_callback, self.get_http())
        return self

    def set_model(self, model, _on_model_callback=None):
        'the set model object'
        self.common_object['model'] = model
        IExecute().invoked(_on_model_callback, self.get_model())
        return self

    def set_meta_model(self, meta_model, _on_meta_model_callback=None):
        'the set meta model object'
        self.common_object['meta_model'] = meta_model
        IExecute().invoked(_on_meta_model_callback, self.get_meta_model())
        return self

    def set_publisher_model(self, publisher_model, _on_publisher_model_callback=None):
        'the set publisher model object'
        self.common_object['publisher_model'] = publisher_model
        IExecute().invoked(_on_publisher_model_callback, self.get_publisher_model())
        return self

    def set_resolver(self, resolver, _on_resolver_callback=None):
        'the set resolver object'
        self.common_object['resolver'] = resolver
        IExecute().invoked(_on_resolver_callback, self.get_resolver())
        return self

    def set_respondent_model(self, respondent_model, _on_respondent_model_callback=None):
        'the set respondent model object'
        self.common_object['respondent_model'] = respondent_model
        IExecute().invoked(_on_respondent_model_callback, self.get_respondent_model())
        return self
