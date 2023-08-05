# -*- coding:utf-8 -*-

from com.dvsnier.http.bbs.specimen.tianya.api_tianya import API_TianYa


class API_InternalTianYa(API_TianYa, object):
    '''the internal tianya interface define class'''
    def __init__(self):
        super(API_InternalTianYa, self).__init__()

    # @HIDE
    def get_title(self):
        'the get title method'
        # NotImplemented
        pass

    # @HIDE
    def get_author(self):
        'the get author method'
        # NotImplemented
        pass

    # @HIDE
    def get_author_introduce(self):
        'the get author introduce method'
        # NotImplemented
        pass
