# -*- coding:utf-8 -*-

from bs4.element import Tag
from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.analysis.model.imodel import IModel
from com.dvsnier.http.tool.iexecute import IExecute


class AbstractModel(IModel, object):
    '''the abstract model class'''

    # protected property
    _url = None  # only support for private domain requests is provided
    # protected property
    _response = None  # only support for private domain requests is provided

    def __init__(self):
        super(AbstractModel, self).__init__()

    # extends SimpleResolver
    def beautiful_soup(self,
                       file,
                       find={
                           "name": "div",
                           "attrs": {
                               "class": "atl-menu clearfix js-bbs-act"
                           }
                       },
                       key='js_pageurl',
                       features='html.parser',
                       flag=None,
                       _on_callback=None):
        'the bbs beautiful soup by read file'
        # private property
        __common_object_model = AnalysisFactory.get_com()
        # beautifulSoup = __common_object_model.get_resolver().beautiful_soup(file, features=features, flag=flag, _on_callback=_on_callback)
        beautifulSoup = __common_object_model.get_resolver().beautiful_soup(file, features=features, flag=flag)
        if beautifulSoup:
            div = beautifulSoup.find(name=find.get('name', str()), attrs=find.get('attrs', dict()))
            if div and isinstance(div, Tag):
                js_pageurl = div.get(key)
                if js_pageurl:
                    self._url = js_pageurl  # synchronize url data
                    __common_object_model.get_http().set_url(
                        js_pageurl, lambda it: logging.debug(
                            'the url object({}) with the current article link that has configured successfully.'.format(
                                js_pageurl)))
                else:
                    logging.warning('the url object with the current article link that has configured unsuccessfully.')
            else:
                logging.warning('the url object with the current article link that has configured unsuccessfully.')
        IExecute().execute(_on_callback, self._url)
        return beautifulSoup

    # extends IHttp
    def get(self, url, timeout=60):
        'the request url'
        self._url = url
        # private property
        __common_object_model = AnalysisFactory.get_com()
        self._response = __common_object_model.get_http().get(url, timeout=timeout)
        return self._response
