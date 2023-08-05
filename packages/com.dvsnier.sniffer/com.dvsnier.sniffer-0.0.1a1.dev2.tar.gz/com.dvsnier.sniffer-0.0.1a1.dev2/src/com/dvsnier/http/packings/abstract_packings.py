# -*- coding:utf-8 -*-

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.analysis.rma.abstract_rma import AbstractRma
from com.dvsnier.http.base.abstract_http import AbstractHttp
from com.dvsnier.http.dom.abstract_dom import AbstractDom
from com.dvsnier.http.tool.idebug import IDebug
from com.dvsnier.http.tool.iexecute import IExecute


class AbstractPackings(object):
    '''the abstract packings class'''

    # protected property
    _dom = None
    # protected property
    _rma = None

    def __init__(self):
        super(AbstractPackings, self).__init__()
        self.execute(lambda: logging.debug('the current create object({}) is ready to be created.'.format('packings')))

    def execute(self, _on_callback=None):
        'the execute task'
        # private property
        __common_object_model = AnalysisFactory.get_com()
        if __common_object_model.get_debug():
            logging.debug('the current instance({}) has ready that had skipped.'.format('debug'))
        else:
            __common_object_model.set_debug(
                IDebug(), lambda it: logging.debug('the {} object configured successfully.'.format('debug')))
        if __common_object_model.get_eoe():
            logging.debug('the current instance({}) has ready that had skipped.'.format('eoe'))
        else:
            eoe = list()
            eoe.append('PLACEHOLDER')
            __common_object_model.set_eoe(
                eoe, lambda it: logging.debug('the {} object configured successfully.'.format('eoe')))
        if __common_object_model.get_http():
            logging.debug('the current instance({}) has ready that had skipped.'.format('http'))
            logging.debug('the current instance({}) has ready that had skipped.'.format('brs'))
        else:
            http = AbstractHttp()
            __common_object_model.set_http(
                http, lambda it: logging.debug('the {} object configured successfully.'.format('http')))
            __common_object_model.set_brs(
                http.brs, lambda it: logging.debug('the {} object configured successfully.'.format('brs')))

        if self._dom:
            logging.debug('the current instance({}) has ready that had skipped.'.format('dom'))
        else:
            self._dom = AbstractDom()
        if self._rma:
            logging.debug('the current instance({}) has ready that had skipped.'.format('rma'))
        else:
            self._rma = AbstractRma()
        IExecute().execute(_on_callback)
        return self

    def get_dom(self):
        'the get dom instance'
        if not self._dom:
            raise KeyError(
                'The current value({}) is invalid and illegal, and then please reset the value'.format('dom'))
        return self._dom

    def get_rma(self):
        'the get rma instance'
        if not self._rma:
            raise KeyError(
                'The current value({}) is invalid and illegal, and then please reset the value'.format('rma'))
        return self._rma

    def set_dom(self, dom, _on_dom_callback=None):
        'the set dom object'
        self._dom = dom
        if _on_dom_callback:
            _on_dom_callback(self._dom)
        return self

    def set_rma(self, rma, _on_rma_callback=None):
        'the set rma object'
        self._rma = rma
        if _on_rma_callback:
            _on_rma_callback(self._rma)
        return self
