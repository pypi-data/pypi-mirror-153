# -*- coding:utf-8 -*-

from bs4.element import Tag
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.analysis.model.abstract_model import AbstractModel


class PublisherModel(AbstractModel, object):
    '''the publisher model class'''
    def __init__(self):
        super(PublisherModel, self).__init__()

    def get_main_item(self, tag, **kwargs):
        '''
            get main item

            the `kwargs` parameter is defined as follows:

            {
                "attrs": {
                    "attr_name": "class",
                    "author_name": "_host",
                    "author_id": "_hostid",
                    "author_time": "replytime"
                },
                "select": "div#alt_reply a.reportme.a-link",
                "child":{
                    "name":"div",
                    "attrs":{
                        "class": "bbs-content clearfix"
                    }
                }
            }
        '''
        element_item = dict()
        if isinstance(tag, Tag) and kwargs:
            kwargs_attrs = kwargs.get('attrs', dict())
            attr_name = kwargs_attrs.get('attr_name', str())
            if attr_name and tag.has_attr(attr_name):
                div_bbs_item = tag
                if div_bbs_item and isinstance(div_bbs_item, Tag):
                    author_name = kwargs_attrs.get('author_name', str())
                    author_id = kwargs_attrs.get('author_id', str())
                    author_time = kwargs_attrs.get('author_time', str())
                    element_item['author_name'] = div_bbs_item.get(author_name)
                    element_item['author_id'] = div_bbs_item.get(author_id)
                    kwargs_select = kwargs.get('select', str())
                    div_alt_reply_a_result_set = div_bbs_item.select(kwargs_select)
                    if div_alt_reply_a_result_set:
                        for index, reply_item in enumerate(div_alt_reply_a_result_set):
                            if reply_item and isinstance(reply_item, Tag):
                                if index == 0:
                                    element_item['author_time'] = reply_item.get(author_time)
                                else:
                                    break
                kwargs_child = kwargs.get('child', dict())
                kwargs_child_name = kwargs_child.get('name', dict())
                kwargs_child_attrs = kwargs_child.get('attrs', dict())
                div_bbs_content = tag.findChild(name=kwargs_child_name, attrs=kwargs_child_attrs)
                if div_bbs_content and isinstance(div_bbs_content, Tag):
                    # private property
                    __common_object_model = AnalysisFactory.get_com()
                    element_item['author_content_set'] = __common_object_model.get_content().bbs_content_set(div_bbs_content)
                element_item['index'] = 0
                element_item['sequence'] = ''
                element_item['type'] = 1
        return element_item
