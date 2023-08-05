# -*- coding:utf-8 -*-

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.analysis.adapter.abstract_adapter import AbstractAdapter
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.analysis.model.comment_model import CommentModel
from com.dvsnier.http.analysis.model.meta_model import MetaModel
from com.dvsnier.http.analysis.model.node_model import NodeModel
from com.dvsnier.http.analysis.model.publisher_model import PublisherModel
from com.dvsnier.http.analysis.model.respondent_model import RespondentModel
from com.dvsnier.http.analysis.resolver.simple_resolver import SimpleResolver
from com.dvsnier.http.analysis.rma.irma import IRma
from com.dvsnier.http.tool.iexecute import IExecute


class AbstractRma(IRma, object):
    '''the abstract rma class'''

    # protected property
    _adapter = None
    # protected property
    _model = None
    # protected property
    _resolver = None

    def __init__(self):
        super(AbstractRma, self).__init__()
        self._adapter = AbstractAdapter()
        self._model = NodeModel()
        self._meta_model = MetaModel()
        self._publisher_model = PublisherModel()
        self._respondent_model = RespondentModel()
        self._comment_model = CommentModel()
        self._resolver = SimpleResolver()
        # private property
        self.__common_object_model = AnalysisFactory.get_com()
        # self.__common_object_model.set_adapter(self._adapter,
        #                                        lambda it: logging.debug('the {} object configured successfully.'.format('adapter')))
        self.__common_object_model.set_model(
            self._model, lambda it: logging.debug('the {} object configured successfully.'.format('model')))
        self.__common_object_model.set_meta_model(
            self._meta_model, lambda it: logging.debug('the {} object configured successfully.'.format('meta_model')))
        self.__common_object_model.set_publisher_model(
            self._publisher_model,
            lambda it: logging.debug('the {} object configured successfully.'.format('publisher_model')))
        self.__common_object_model.set_respondent_model(
            self._respondent_model,
            lambda it: logging.debug('the {} object configured successfully.'.format('respondent_model')))
        self.__common_object_model.set_comment_model(
            self._comment_model,
            lambda it: logging.debug('the {} object configured successfully.'.format('comment_model')))
        self.__common_object_model.set_resolver(
            self._resolver, lambda it: logging.debug('the {} object configured successfully.'.format('resolver')))

    def get_adapter(self):
        'the get adapter instance'
        if not self._adapter:
            raise KeyError(
                'The current value({}) is invalid and illegal, and then please reset the value'.format('adapter'))
        return self._adapter

    def get_comment_model(self):
        'the get comment model instance'
        if not self._comment_model:
            raise KeyError(
                'The current value({}) is invalid and illegal, and then please reset the value'.format('comment_model'))
        return self._comment_model

    def get_model(self):
        'the get model instance'
        if not self._model:
            raise KeyError(
                'The current value({}) is invalid and illegal, and then please reset the value'.format('model'))
        return self._model

    def get_meta_model(self):
        'the get meta model instance'
        if not self._meta_model:
            raise KeyError(
                'The current value({}) is invalid and illegal, and then please reset the value'.format('meta_model'))
        return self._meta_model

    def get_publisher_model(self):
        'the get publisher model instance'
        if not self._publisher_model:
            raise KeyError('The current value({}) is invalid and illegal, and then please reset the value'.format(
                'publisher_model'))
        return self._publisher_model

    def get_respondent_model(self):
        'the get respondent model instance'
        if not self._respondent_model:
            raise KeyError('The current value({}) is invalid and illegal, and then please reset the value'.format(
                'respondent_model'))
        return self._respondent_model

    def get_resolver(self):
        'the get resolver instance'
        if not self._resolver:
            raise KeyError(
                'The current value({}) is invalid and illegal, and then please reset the value'.format('resolver'))
        return self._resolver

    def set_adapter(self, adapter, _on_adapter_callback=None):
        'the set adapter object'
        self._adapter = adapter
        IExecute().execute(_on_adapter_callback, self._adapter)
        return self

    def set_comment_model(self, comment_model, _on_comment_model_callback=None):
        'the set comment model object'
        self._comment_model = comment_model
        IExecute().execute(_on_comment_model_callback, self._comment_model)
        return self

    def set_model(self, model, _on_model_callback=None):
        'the set model object'
        self._model = model
        IExecute().execute(_on_model_callback, self._model)
        return self

    def set_meta_model(self, meta_model, _on_meta_model_callback=None):
        'the set meta model object'
        self._meta_model = meta_model
        IExecute().execute(_on_meta_model_callback, self._meta_model)
        return self

    def set_publisher_model(self, publisher_model, _on_publisher_model_callback=None):
        'the set publisher model object'
        self._publisher_model = publisher_model
        IExecute().execute(_on_publisher_model_callback, self._publisher_model)
        return self

    def set_respondent_model(self, respondent_model, _on_respondent_model_callback=None):
        'the set respondent model object'
        self._respondent_model = respondent_model
        IExecute().execute(_on_respondent_model_callback, self._respondent_model)
        return self

    def set_resolver(self, resolver, _on_resolver_callback=None):
        'the set resolver object'
        self._resolver = resolver
        IExecute().execute(_on_resolver_callback, self._resolver)
        return self
