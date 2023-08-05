# -*- coding:utf-8 -*-

from bs4.element import Tag
from com.dvsnier.http.analysis.model.abstract_model import AbstractModel


class MetaModel(AbstractModel, object):
    '''the meta model class'''
    def __init__(self):
        super(MetaModel, self).__init__()

    def get_meta_data(self, beautifulSoup, select):
        'get meta data'
        element_item = dict()
        js_meta_result_set = beautifulSoup.select(select)
        if js_meta_result_set:
            for index, meta_item in enumerate(js_meta_result_set):
                if meta_item and isinstance(meta_item, Tag):
                    element_item['_host'] = meta_item.get('_host')
                    element_item['js_activityurl'] = meta_item.get('js_activityurl')
                    element_item['js_activityuserid'] = meta_item.get('js_activityuserid')
                    element_item['js_activityusername'] = meta_item.get('js_activityusername')
                    element_item['js_activityusername_gbk'] = meta_item.get('js_activityusername_gbk')
                    element_item['js_appid'] = meta_item.get('js_appid')
                    element_item['js_blockid'] = meta_item.get('js_blockid')
                    element_item['js_blockname'] = meta_item.get('js_blockname')
                    element_item['js_blockname_gbk'] = meta_item.get('js_blockname_gbk')
                    element_item['js_clickcount'] = meta_item.get('js_clickcount')
                    element_item['js_grade'] = meta_item.get('js_grade')
                    element_item['js_pageurl'] = meta_item.get('js_pageurl')
                    element_item['js_postid'] = meta_item.get('js_postid')
                    element_item['js_posttime'] = meta_item.get('js_posttime')
                    element_item['js_powerreply'] = meta_item.get('js_powerreply')
                    element_item['js_replycount'] = meta_item.get('js_replycount')
                    element_item['js_replytime'] = meta_item.get('js_replytime')
                    element_item['js_title'] = meta_item.get('js_title')
                    element_item['js_title_gbk'] = meta_item.get('js_title_gbk')
                    element_item['support_ds_version'] = '0.0.1'
                else:
                    continue
        return element_item
