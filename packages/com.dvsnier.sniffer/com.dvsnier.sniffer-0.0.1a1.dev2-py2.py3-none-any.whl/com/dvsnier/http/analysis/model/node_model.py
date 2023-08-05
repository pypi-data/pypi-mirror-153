# -*- coding:utf-8 -*-

from datetime import datetime
from typing import Iterable

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.analysis.model.abstract_model import AbstractModel


class NodeModel(AbstractModel, object):
    '''the node model class'''
    def __init__(self):
        super(NodeModel, self).__init__()

    def get_title(self, beautifulSoup, select):
        'the get title method'
        title = None
        if beautifulSoup and isinstance(beautifulSoup, BeautifulSoup) and select:
            title_result_set = beautifulSoup.select(select)
            if title_result_set:
                for index, title in enumerate(title_result_set):
                    if title and isinstance(title, Tag):
                        title = title.string
                        if isinstance(title, str):
                            title = title.strip()
        else:
            logging.error('the current {} parameter is invalid'.format(beautifulSoup))
        return title

    def get_author(self, beautifulSoup, find, child):
        'the get author method'
        author = ''
        author_introduce = self.get_author_introduce(beautifulSoup, find, child)
        if author_introduce:
            author = author_introduce[0]
        return author

    def get_author_introduce(self, beautifulSoup, find_parent, find_child):
        'the get author introduce method'
        author_introduce = []
        if beautifulSoup and isinstance(beautifulSoup, BeautifulSoup) and find_parent and isinstance(
                find_parent, dict) and find_child and isinstance(find_child, dict):
            div = beautifulSoup.find(name=find_parent.get('name'), attrs=find_parent.get('attrs'))
            if div and isinstance(div, Tag):
                div = div.findChild(name=find_child.get('name'), attrs=find_child.get('attrs'))
                if div and isinstance(div, Tag) and isinstance(div.children, Iterable):
                    for span in div.children:
                        if isinstance(span, Tag):
                            for index, element in enumerate(span.children):
                                element_value = None
                                if isinstance(element, NavigableString):
                                    element_value = element.strip()
                                    if element_value:
                                        # logging.debug(element_value)
                                        author_introduce.append(element_value)
                                    else:
                                        continue
                                elif isinstance(element, Tag):
                                    element_value = element.text.strip()
                                    # logging.debug(element_value)
                                    if index == 1:
                                        element_value = author_introduce[0] + element.text.strip()
                                        author_introduce.clear()
                                        author_introduce.append(element_value)
                                else:
                                    continue
        else:
            logging.error('the current {} parameter is invalid'.format(beautifulSoup))
        return author_introduce

    def get_element_node(self, beautifulSoup, **kwargs):
        '''
            The data structure is defined as follows:

            {
                "article_name": "...",
                "article_author": "...",
                "article_time": "...",
                "article_click": 1,
                "article_reply": 1,
                "article_capture_count": 1,
                "article_capture_last_time": "...",
                "article_link": "...",
                "article_online": 1,
                "article_version_name": "v0.0.1",
                "article_version_code": 1,
                "item": [

                ]
                "meta_data": {
                    "_host": "12345678",
                    "js_activityurl": "http://bbs.tianya.cn/post-xxx-1.shtml,
                    "js_activityuserid": "12345678",
                    "js_activityusername": "...",
                    "js_activityusername_gbk": "...",
                    "js_appid": "bbs",
                    "js_blockid": "worldlook",
                    "js_blockname": "...",
                    "js_blockname_gbk": "...",
                    "js_clickcount": "2449379",
                    "js_grade": "0,
                    "js_pageurl": "...",
                    "js_postid": "1915123,
                    "js_posttime": "1577084902000",
                    "js_powerreply": "0",
                    "js_replycount": "11218,
                    "js_replytime": "2021-08-04 13:46:37.0,
                    "js_title": "...,
                    "js_title_gbk": "...
                }
                "support_ds_version": "0.0.1|~0.0.x|^0.x.0|*x.0.0",
                "system_time": " ",
                "system_timestamp": 0
            }

            The `item` node data structure is defined as follows:

            {
                "author_name": "发布",
                "author_id": "",
                "author_time": "",
                # "author_content": "...",
                "author_content_set": [

                ],

                "comment_key_with_union_id": "it is union primary key",
                "comment_key_with_union_rid": "it is union primary key",
                "comment_name": "评论",
                "comment_id": "",
                "comment_time": "",
                # "comment_content": "...",
                "comment_content_set": [

                ],

                "item": {

                },
                "index": 0,

                "reply_key": "it is primary key",
                "reply_name": "回复",
                "reply_id": "",
                "reply_time": "",
                # "reply_content": "...",
                "reply_content_set": [

                ],

                "sequence": "1 楼",

                "type": "1: 发布, 2: 回复, 3: 评论, 4: 回复评论(评论的评论)"
            }

            The `author_content_set` and `comment_content_set` and `reply_content_set` node data structure is defined as follows:

            {
                "additional_type": "0: 数据(脏), 1: 文本, 2: 链接, 3: 图片, 4: 视频, 5: 音频, 6: 附件",
                "anchor_mark": "N: 数据(脏), U: 数据未追踪(Untracked), A: 新数据(Added, Staged), M: 数据有修改(Modified), +M: 数据有修改(Modified, Staged), C: 数据有冲突(Conflict), D: 数据被删除(Deleted)",
                "index": 0,
                "type": "0: 数据(脏), 1: 文本, 2: 链接, 3: 图片, 4: 视频, 5: 音频, 6: 附件",
                "resource_base64": "3: 图片, 4: 视频(不建议), 5: 音频(不建议), 6: 附件(不推荐)",
                "resource_content": "1: 文本, 2: 链接",
                "resource_href": "2: 链接",
                "resource_url_thumbnail": "3: 图片, 4: 视频, 5: 音频, 6: 附件",
                "resource_url_small": "3: 图片, 4: 视频, 5: 音频, 6: 附件",
                "resource_url_middle": "3: 图片, 4: 视频, 5: 音频, 6: 附件",
                "resource_url_large": "3: 图片, 4: 视频, 5: 音频, 6: 附件",
                "resource_url_original": "3: 图片, 4: 视频, 5: 音频, 6: 附件",
            }

            the `kwargs` parameter is defined as follows:

            {
                "title": {
                    "select": "div#post_head.atl-head > h1.atl-title > span.s_title > span"
                },
                "author_or_introduce": {
                    "find":{
                        "name": "div",
                        "attrs": {
                            "class": "atl-menu clearfix js-bbs-act"
                        }
                    },
                    "child": {
                        "name": "div",
                        "attrs": {
                            "class": "atl-info"
                        }
                    }
                },
                "meta": {
                    "select": "div.atl-menu.clearfix.js-bbs-act"
                },
                "system": {
                    "article": {
                        "article_link": "js_pageurl"
                    }
                },
                "publisher": {

                },
                "respondent": {

                },
                "present": {
                    "find":{
                        "name": "div",
                        "attrs": {
                            "class": "atl-main"
                        },
                        "find_child": {
                            "name": "div",
                            "attrs": {
                                "class": "atl-item host-item"
                            }
                        }
                    }
                }
            }

            the `publisher` parameter is defined that please refer to PublisherModel#get_main_item()

            the `respondent` parameter is defined that please refer to RespondentModel#get_subordinate_item()

        '''
        element_node = dict()
        if beautifulSoup and kwargs:
            kwargs_title = kwargs.get('title', dict())
            title_title_select = kwargs_title.get('select', str())
            element_node['article_name'] = self.get_title(beautifulSoup, title_title_select)
            kwargs_author_or_introduce = kwargs.get('author_or_introduce', dict())
            find_parent = kwargs_author_or_introduce.get('find', dict())  # kwargs_author_or_introduce_find
            find_child = kwargs_author_or_introduce.get('child', dict())  # kwargs_author_or_introduce_child
            author_introduce = self.get_author_introduce(beautifulSoup, find_parent, find_child)
            if author_introduce:
                element_node['article_author'] = author_introduce[0].split(r'：')[1]
                element_node['article_time'] = author_introduce[1].split(r'：')[1]
                element_node['article_click'] = author_introduce[2].split(r'：')[1]
                element_node['article_reply'] = author_introduce[3].split(r'：')[1]
            element_node['article_capture_count'] = 1
            element_node['article_capture_last_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            element_node['article_link'] = None
            element_node['article_online'] = 1
            element_node['article_version_name'] = 'v0.0.1'
            element_node['article_version_code'] = 1
            element_node['system_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            element_node['system_timestamp'] = datetime.now().timestamp()
            element_node['item'] = []
            kwargs_present = kwargs.get('present', dict())
            kwargs_present_find = kwargs_present.get('find', dict())
            kwargs_present_find_name = kwargs_present_find.get('name', str())
            kwargs_present_find_attrs = kwargs_present_find.get('attrs', dict())
            div = beautifulSoup.find(name=kwargs_present_find_name, attrs=kwargs_present_find_attrs)
            # private property
            __common_object_model = AnalysisFactory.get_com()
            if div and isinstance(div, Tag):
                kwargs_present_find_child = kwargs_present_find.get('find_child', dict())
                kwargs_present_find_child_name = kwargs_present_find_child.get('name', str())
                kwargs_present_find_child_attrs = kwargs_present_find_child.get('attrs', dict())
                main_item = div.findChild(name=kwargs_present_find_child_name,
                                          attrs=kwargs_present_find_child_attrs)  # main item
                if main_item and isinstance(main_item, Tag):
                    kwargs_publisher = kwargs.get('publisher', dict())
                    element_node['item'].append(__common_object_model.get_publisher_model().get_main_item(
                        main_item, **kwargs_publisher))
            kwargs_respondent = kwargs.get('respondent', dict())
            element_node['item'].extend(__common_object_model.get_respondent_model().get_subordinate_item(
                div, **kwargs_respondent))  # subordinate item
            # private property
            __common_object_model = AnalysisFactory.get_com()
            # private property
            __metamodel = __common_object_model.get_meta_model()
            kwargs_meta = kwargs.get('meta', dict())
            meta_select = kwargs_meta.get('select', str())
            element_node['meta_data'] = __metamodel.get_meta_data(beautifulSoup, meta_select)
            kwargs_system = kwargs.get('system', dict())
            kwargs_system_article = kwargs_system.get('article', dict())
            article_link_url = kwargs_system_article.get('article_link', str())
            element_node['article_link'] = element_node['meta_data'].get(article_link_url)
        else:
            logging.error('the current {} parameter is invalid'.format(beautifulSoup))
        # if element_node:
        #     logging.debug(json.dumps(element_node, ensure_ascii=False, indent=4))
        return element_node
