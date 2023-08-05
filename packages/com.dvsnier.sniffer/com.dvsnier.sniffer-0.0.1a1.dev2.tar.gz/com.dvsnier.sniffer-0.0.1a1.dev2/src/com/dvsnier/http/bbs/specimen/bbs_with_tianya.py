# -*- coding:utf-8 -*-

from com.dvsnier.http.bbs.specimen.tianya.api_tianya import API_TianYa
from com.dvsnier.http.bbs.specimen.tianya.tianya_adapter import TianYaAdapter


class BbsWithTianYa(API_TianYa, object):
    '''
        the bbs with tianya class

        The steps are as follows:

            1. the configure container objects that use factory
    '''
    def __init__(self):
        super(BbsWithTianYa, self).__init__()
        self.adapter = TianYaAdapter()

    def get_bbs_plate(self, _on_callback=None):
        return self.adapter.get_bbs_plate(_on_callback)
