# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from com.dvsnier.http.analysis.resolver.abstract_resolver import AbstractResolver


class SimpleResolver(AbstractResolver, object):
    '''the simple resolver class'''
    def __init__(self):
        super(SimpleResolver, self).__init__()

    def beautiful_soup(self, file, features='html.parser', flag=None, _on_callback=None):
        'the beautiful soup by file read or parse'
        beautifulSoup = None
        with open(file, 'r') as f:
            if flag == -1:
                diagnose(f.read())
            beautifulSoup = BeautifulSoup(f, features=features)
        self.set_beautiful_soup(beautifulSoup, _on_callback)
        return beautifulSoup

    def bs(self, markup, features='html.parser', _on_callback=None):
        'the beautiful soup'
        beautiful_soup = None
        if markup:
            beautiful_soup = BeautifulSoup(markup, features)
        self.set_beautiful_soup(beautiful_soup, _on_callback)
        return beautiful_soup

    def prettify(self, beautiful_soup):
        'the prettify'
        prettify = None
        if beautiful_soup:
            prettify = beautiful_soup.prettify()
        return prettify
