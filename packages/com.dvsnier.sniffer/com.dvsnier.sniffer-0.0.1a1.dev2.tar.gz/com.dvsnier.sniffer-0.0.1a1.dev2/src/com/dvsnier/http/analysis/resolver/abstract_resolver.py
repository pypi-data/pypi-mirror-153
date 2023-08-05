# -*- coding:utf-8 -*-

from com.dvsnier.http.tool.iexecute import IExecute


class AbstractResolver(object):
    '''the abstract resolver class'''

    _beautiful_soup = None

    def __init__(self):
        super(AbstractResolver, self).__init__()

    def get_beautiful_soup(self):
        'get beautiful soup'
        return self._beautiful_soup

    def set_beautiful_soup(self, beautiful_soup, _on_callback=None):
        'set beautiful soup'
        # if self._beautiful_soup:
        #     logging.warning('the current it is {} that performs the assignment operation again.'.format('beautiful_soup'))
        self._beautiful_soup = beautiful_soup
        IExecute().execute(_on_callback, self._beautiful_soup)
        return self
