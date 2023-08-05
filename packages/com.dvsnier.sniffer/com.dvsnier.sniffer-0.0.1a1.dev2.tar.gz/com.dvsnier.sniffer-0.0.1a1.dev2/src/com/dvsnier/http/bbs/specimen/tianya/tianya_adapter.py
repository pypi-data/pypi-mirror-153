# -*- coding:utf-8 -*-

import json
import time

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.analysis.adapter.abstract_adapter import AbstractAdapter
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.bbs.specimen.tianya.api_internal_tianya import API_InternalTianYa
from com.dvsnier.http.config.bbs_plate_with_ty import get_json_with_tianya
from com.dvsnier.http.packings.abstract_packings import AbstractPackings
from com.dvsnier.http.util.utils import obtain_file_and_resolver


class TianYaAdapter(AbstractAdapter, API_InternalTianYa, object):
    '''the tianya adapter class'''
    def __init__(self):
        super(TianYaAdapter, self).__init__()
        logging.warning('the start preparing to instantiate {} object...'.format('packings'))
        self.packings = TianYaAdapter.build()
        logging.info('the {} object configured successfully.'.format('packings'))

    @classmethod
    def build(cls):
        packings = AnalysisFactory.obtain().create_tianya_analysis(lambda: AbstractPackings())
        return packings

    def get_title(self):
        'the get title method'
        super(TianYaAdapter, self).get_title()
        title = None
        select = 'div#post_head.atl-head > h1.atl-title > span.s_title > span'
        # private property
        __common_object_model = AnalysisFactory.get_com()
        if __common_object_model.get_model():
            beautiful_soup = __common_object_model.get_resolver().get_beautiful_soup()
            if beautiful_soup:
                title = __common_object_model.get_model().get_title(beautiful_soup, select)
            else:
                raise ValueError(
                    'the current {} object is invalid, and maybe you had needed that use AbstractModel#beautiful_soup() to AbstractResolver#set_beautiful_soup().'
                    .format('beautiful_soup'))
        return title

    def get_author(self):
        'the get author method'
        author = ''
        find = {"name": "div", "attrs": {'class': "atl-menu clearfix js-bbs-act"}}
        child = {"name": "div", "attrs": {'class': "atl-info"}}
        if find and child:
            # private property
            __common_object_model = AnalysisFactory.get_com()
            if __common_object_model.get_model():
                beautiful_soup = __common_object_model.get_resolver().get_beautiful_soup()
                if beautiful_soup:
                    author = __common_object_model.get_model().get_author(beautiful_soup, find, child)
                else:
                    raise ValueError(
                        'the current {} object is invalid, and maybe you had needed that use AbstractModel#beautiful_soup() to AbstractResolver#set_beautiful_soup().'
                        .format('beautiful_soup'))
        return author

    def get_author_introduce(self):
        'the get author introduce method'
        super(TianYaAdapter, self).get_author_introduce()
        author_introduce = []
        find = {"name": "div", "attrs": {'class': "atl-menu clearfix js-bbs-act"}}
        child = {"name": "div", "attrs": {'class': "atl-info"}}
        if find and child:
            # private property
            __common_object_model = AnalysisFactory.get_com()
            if __common_object_model.get_model():
                beautiful_soup = __common_object_model.get_resolver().get_beautiful_soup()
                if beautiful_soup:
                    author_introduce.extend(__common_object_model.get_model().get_author_introduce(
                        beautiful_soup, find, child))
                else:
                    raise ValueError(
                        'the current {} object is invalid, and maybe you had needed that use AbstractModel#beautiful_soup() to AbstractResolver#set_beautiful_soup().'
                        .format('beautiful_soup'))
        return author_introduce

    def get_bbs_plate(self, _on_callback=None):
        '''
            the get bbs plate method
        '''
        super(TianYaAdapter, self).get_bbs_plate()
        start = time.time()
        element_node = None
        beautiful_soup = None
        if _on_callback:
            beautiful_soup = _on_callback()
        else:
            beautiful_soup = obtain_file_and_resolver()
        # private property
        __common_object_model = AnalysisFactory.get_com()
        kwargs = json.loads(get_json_with_tianya())
        element_node = __common_object_model.get_model().get_element_node(beautiful_soup, **kwargs)
        end = time.time()
        logging.info('the execute task union-id({}) has completed, that total time consumed {:.3f} seconds '.format(
            AnalysisFactory.get_com().get_http().get_url(), end - start))
        return element_node
