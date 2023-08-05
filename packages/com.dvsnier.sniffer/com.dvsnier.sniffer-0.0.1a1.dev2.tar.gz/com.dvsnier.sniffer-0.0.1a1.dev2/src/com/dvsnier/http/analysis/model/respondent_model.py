# -*- coding:utf-8 -*-

from bs4.element import Tag
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.analysis.model.abstract_model import AbstractModel


class RespondentModel(AbstractModel, object):
    '''the respondent model class'''
    def __init__(self):
        super(RespondentModel, self).__init__()

    def get_subordinate_item(self, tag, **kwargs):
        '''
            get subordinate item

            the `kwargs` parameter is defined as follows:

            {
                "attrs": {
                    "author_name": "_host",
                    "author_id": "_hostid",
                    "author_time": "js_restime"
                },
                "select": "div:not(.host-item).atl-item",
                "child":{
                    "select": "div.atl-con-bd.clearfix div.bbs-content",
                    "reply_key":"replyid",
                    "sequence":"id"
                },
                "subordinate_reply_item": {
                }
            }

            the `subordinate_reply_item` parameter is defined that please refer to CommentModel#get_subordinate_reply_item()
        '''
        element_nodes = []
        kwargs_select = kwargs.get('select', str())
        # https://www.w3school.com.cn/cssref/css_selectors.asp
        div_result_set = tag.select(kwargs_select)
        if div_result_set:
            kwargs_subordinate_reply_item = kwargs.get('subordinate_reply_item', dict())
            for index_item, div_item in enumerate(div_result_set):
                if div_item and isinstance(div_item, Tag):
                    element_item = dict()
                    kwargs_attrs = kwargs.get('attrs', dict())
                    author_name = kwargs_attrs.get('author_name', str())
                    author_id = kwargs_attrs.get('author_id', str())
                    author_time = kwargs_attrs.get('author_time', str())
                    element_item['author_name'] = div_item.get(author_name)
                    element_item['author_id'] = div_item.get(author_id)
                    element_item['author_time'] = div_item.get(author_time)
                    kwargs_child = kwargs.get('child', dict())
                    kwargs_child_select = kwargs_child.get('select', str())
                    div_bbs_content_result_set = div_item.select(kwargs_child_select)
                    # private property
                    __common_object_model = AnalysisFactory.get_com()
                    if div_bbs_content_result_set:
                        for index, div_bbs_content in enumerate(div_bbs_content_result_set):
                            if div_bbs_content and isinstance(div_bbs_content, Tag):
                                element_item['author_content_set'] = __common_object_model.get_content().bbs_content_set(div_bbs_content)
                    subordinate_reply_list = __common_object_model.get_comment_model().get_subordinate_reply_item(
                        div_item, **kwargs_subordinate_reply_item)
                    if subordinate_reply_list and len(subordinate_reply_list):
                        element_item['item'] = subordinate_reply_list
                    element_item['index'] = index_item + 1
                    kwargs_child_reply_key = kwargs_child.get('reply_key', str())
                    element_item['reply_key'] = div_item.get(kwargs_child_reply_key)  # primary key
                    kwargs_child_sequence = kwargs_child.get('sequence', str())
                    element_item['sequence'] = '{} 楼'.format(div_item.get(kwargs_child_sequence))
                    element_item['type'] = 2
                    element_nodes.append(element_item)
        return element_nodes
