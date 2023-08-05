# -*- coding:utf-8 -*-

import datetime
import json
import random
from time import sleep
import traceback

from bs4.element import Tag
from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.analysis.model.abstract_model import AbstractModel
from requests import Response, codes
from requests import ConnectionError, HTTPError, RequestException


class CommentModel(AbstractModel, object):
    '''the comment model class'''
    def __init__(self):
        super(CommentModel, self).__init__()

    def get_article_id_with_comments_params(self):
        'the obtain comments params.articleId with url'
        params_article_id = ''
        if self._response and isinstance(self._response, Response):
            url = self._response.url
            if url and isinstance(url, str):
                urls = url.split('-')
                if urls and len(urls):
                    params_article_id = urls[2]
        elif self._url:
            url = self._url
            if url and isinstance(url, str):
                urls = url.split('-')
                if urls and len(urls):
                    params_article_id = urls[2]
        else:
            raise NameError(
                'the Illegal operation. Please execute the get() or set_url() request before using this method')
        return params_article_id

    def get_article_serial_number(self):
        'the obtain serial number with url'
        article_serial_number = ''
        if self._response and isinstance(self._response, Response):
            url = self._response.url
            if url and isinstance(url, str):
                urls = url.split('-')
                if urls and len(urls):
                    if urls[3]:
                        article_serial_number = urls[3].split('.', maxsplit=1)[0]
        elif self._url:
            url = self._url
            if url and isinstance(url, str):
                urls = url.split('-')
                if urls and len(urls):
                    if urls[3]:
                        article_serial_number = urls[3].split('.', maxsplit=1)[0]
        else:
            raise NameError(
                'the Illegal operation. Please execute the get() or set_url() request before using this method')
        return article_serial_number

    def get_item_with_comments_params(self):
        'the obtain comments params.item with url'
        params_item = ''
        if self._response and isinstance(self._response, Response):
            url = self._response.url
            if url and isinstance(url, str):
                urls = url.split('-')
                if urls and len(urls):
                    params_item = urls[1]
        elif self._url:
            url = self._url
            if url and isinstance(url, str):
                urls = url.split('-')
                if urls and len(urls):
                    params_item = urls[1]
        else:
            raise NameError(
                'the Illegal operation. Please execute the get() or set_url() request before using this method')
        return params_item

    def get_subordinate_reply_item(self, tag, **kwargs):
        '''
            get subordinate reply item

            the `kwargs` parameter is defined as follows:

            {
                "select": "div.atl-con-bd.clearfix div.item-reply-view div.ir-list li",
                "li_item": {
                    "select": "div.atl-con-bd.clearfix div.bbs-content",
                    "attrs": {
                        "comment_key_with_union_id": "id",
                        "comment_key_with_union_rid": "_rid",
                        "comment_name": "_username",
                        "comment_id": "_userid",
                        "comment_time": "_replytime",
                        "comment_content": {
                            "select": "span.ir-content"
                        }
                    },
                    "more_comment": {
                    }
                },
            }

            the `more_comment` parameter is defined that please refer to CommentModel#__get_more_comments()

        '''
        element_nodes = []
        kwargs_select = kwargs.get('select', str())
        li_result_set = tag.select(kwargs_select)
        if li_result_set:
            kwargs_li_item = kwargs.get('li_item', dict())
            for index_item, li_item in enumerate(li_result_set):  # the first comment page data
                if li_item and isinstance(li_item, Tag):
                    element_item = dict()
                    kwargs_li_item_select = kwargs_li_item.get('select', str())
                    div_bbs_content_result_set = li_item.select(kwargs_li_item_select)
                    if div_bbs_content_result_set:
                        for index, div_bbs_content in enumerate(div_bbs_content_result_set):
                            if div_bbs_content and isinstance(div_bbs_content, Tag):
                                element_item['author_content'] = div_bbs_content.text.strip()
                    kwargs_li_item_attrs = kwargs_li_item.get('attrs', dict())
                    kwargs_li_item_comment_key_with_union_id = kwargs_li_item_attrs.get(
                        'comment_key_with_union_id', str())
                    kwargs_li_item_comment_key_with_union_rid = kwargs_li_item_attrs.get(
                        'comment_key_with_union_rid', str())
                    kwargs_li_item_comment_name = kwargs_li_item_attrs.get('comment_name', str())
                    kwargs_li_item_comment_id = kwargs_li_item_attrs.get('comment_id', str())
                    kwargs_li_item_comment_time = kwargs_li_item_attrs.get('comment_time', str())
                    element_item['comment_key_with_union_id'] = li_item.get(
                        kwargs_li_item_comment_key_with_union_id)  # union primary key
                    element_item['comment_key_with_union_rid'] = li_item.get(
                        kwargs_li_item_comment_key_with_union_rid)  # union primary key
                    element_item['comment_name'] = li_item.get(kwargs_li_item_comment_name)
                    element_item['comment_id'] = li_item.get(kwargs_li_item_comment_id)
                    element_item['comment_time'] = li_item.get(kwargs_li_item_comment_time)
                    kwargs_li_item_comment_content = kwargs_li_item_attrs.get('comment_content', dict())
                    kwargs_li_item_comment_content_select = kwargs_li_item_comment_content.get('select', str())
                    span_result_set = li_item.select(kwargs_li_item_comment_content_select)  # comment content
                    if span_result_set:
                        for index, span_item in enumerate(span_result_set):
                            if span_item and isinstance(span_item, Tag):
                                a_result_set = span_item.select("a")
                                if a_result_set:
                                    for index, a_item in enumerate(a_result_set):
                                        if a_item and isinstance(a_item, Tag):
                                            element_item['reply_name'] = a_item.text.strip()
                                            if span_item.i and isinstance(span_item.i, Tag):
                                                span_item.i.unwrap()
                                            comment_content_value = span_item.text.strip()
                                            if comment_content_value.find('：') >= 0:
                                                element_item['comment_content'] = span_item.text.strip().split(
                                                    r'：', maxsplit=1)[1]
                                            else:
                                                element_item['comment_content'] = span_item.text.strip()
                                            element_item['type'] = 4
                                else:
                                    element_item['comment_content'] = span_item.text.strip()
                                    element_item['type'] = 3
                    element_item['index'] = index_item
                    element_nodes.append(element_item)
            kwargs_li_item_more_comment = kwargs_li_item.get('more_comment', dict())
            element_nodes.extend(self.__get_more_comments(
                tag, len(element_nodes), **kwargs_li_item_more_comment))  # the more comment page data list
        return element_nodes

    def __get_more_comments(self, tag, length, features='html.parser', **kwargs):
        '''
            get more comments

            the `kwargs` parameter is defined as follows:

            {
                "reply": {
                    "select": "div.atl-con-bd.clearfix div.atl-reply",
                    "attrs": {
                        "id": "id"
                    }
                },
                "select": "div.atl-con-bd.clearfix div.item-reply-view div.ir-action div.ir-page",
                "attrs": {
                    "comment_index": "_index",
                    "comment_page_count": "_pagecount",
                    "comment_key_with_union_id": "id",
                    "comment_key_with_union_rid": "_rid",
                    "comment_name": "author_name",
                    "comment_id": "author_id",
                    "comment_time": "comment_time",
                    "comment_content": "content"
                }
            }
        '''
        element_nodes = []
        reply_id = None
        kwargs_reply = kwargs.get('reply', dict())
        kwargs_reply_select = kwargs_reply.get('select', str())
        reply_result_set = tag.select(kwargs_reply_select)
        if reply_result_set and len(reply_result_set) > 0:
            rid_item = reply_result_set[0]
            if isinstance(rid_item, Tag):
                kwargs_reply_attrs = kwargs_reply.get('attrs', dict())
                kwargs_reply_attrs_id = kwargs_reply_attrs.get('id', str())
                rid_original = rid_item.get(kwargs_reply_attrs_id)
                if rid_original and isinstance(rid_original, str):
                    rid_lists = rid_original.split('_')
                    if rid_lists and len(rid_lists) > 1:
                        reply_id = rid_lists[1]
        page_size = length
        kwargs_select = kwargs.get('select', str())
        more_comments_result_set = tag.select(kwargs_select)
        if more_comments_result_set and len(more_comments_result_set) > 0 and reply_id:
            more_comments_result = more_comments_result_set[0]
            if more_comments_result and isinstance(more_comments_result, Tag):
                kwargs_attrs = kwargs.get('attrs', dict())
                kwargs_attrs_comment_index = kwargs_attrs.get('comment_index', str())
                kwargs_attrs_comment_page_count = kwargs_attrs.get('comment_page_count', str())
                current_index = more_comments_result.get(kwargs_attrs_comment_index)
                page_count = more_comments_result.get(kwargs_attrs_comment_page_count)
                if isinstance(current_index, str) and isinstance(page_count, str):
                    if int(current_index) < int(page_count):
                        logging.debug('')
                        logging.debug('There are {} pages of comment data in total.'.format(page_count))
                        for i in range(int(current_index) + 1, int(page_count) + 1):  # range[m, n)
                            logging.debug('the start requesting {} page data...'.format(i))
                            response_with_dict = self.get_comment_lists(replyId=int(reply_id), pageNum=i)
                            if response_with_dict and isinstance(response_with_dict, dict):
                                comment_lists = response_with_dict.get('data')
                                if comment_lists and len(comment_lists) > 0:
                                    for index, comment_item in enumerate(comment_lists):
                                        element_item = dict()
                                        kwargs_comment_key_with_union_id = kwargs_attrs.get(
                                            'comment_key_with_union_id', str())
                                        # kwargs_comment_key_with_union_rid = kwargs_attrs.get('comment_key_with_union_rid', str())
                                        kwargs_comment_name = kwargs_attrs.get('comment_name', str())
                                        kwargs_comment_id = kwargs_attrs.get('comment_id', str())
                                        kwargs_comment_time = kwargs_attrs.get('comment_time', str())
                                        kwargs_comment_content = kwargs_attrs.get('comment_content', str())
                                        element_item['comment_key_with_union_id'] = 'itemreply-{}'.format(
                                            comment_item.get(kwargs_comment_key_with_union_id))  # union primary key
                                        element_item['comment_key_with_union_rid'] = comment_item.get(
                                            kwargs_comment_key_with_union_id)  # union primary key
                                        element_item['comment_name'] = comment_item.get(kwargs_comment_name)
                                        element_item['comment_id'] = comment_item.get(kwargs_comment_id)
                                        element_item['comment_time'] = comment_item.get(kwargs_comment_time)
                                        content = comment_item.get(kwargs_comment_content)
                                        if content and isinstance(content, str):
                                            # private property
                                            __common_object_model = AnalysisFactory.get_com()
                                            beautifulSoup = __common_object_model.get_resolver().bs(content, features)
                                            a = beautifulSoup.find('a')
                                            if a and isinstance(a, Tag):
                                                element_item['reply_name'] = a.extract().text
                                                comment_content_value = beautifulSoup.get_text()
                                                if comment_content_value.find('：') >= 0:
                                                    element_item['comment_content'] = comment_content_value.strip(
                                                    ).split(r'：', maxsplit=1)[1]
                                                else:
                                                    element_item['comment_content'] = comment_content_value.strip()
                                                element_item['type'] = 4
                                            else:
                                                element_item['comment_content'] = content.strip()
                                                element_item['type'] = 3
                                        else:
                                            element_item['comment_content'] = ''
                                            element_item['type'] = 3
                                        if length > 0 and length - 1 > 0:
                                            if len(element_nodes) >= page_size:  # the more page
                                                element_item['index'] = length + len(element_nodes)
                                            else:  # the second page
                                                element_item['index'] = length + index
                                        else:
                                            for j in range(3):
                                                logging.error(
                                                    'When there is no data on the first page of the comment, the paging comment request interface should not be called, which is an illegal operation'
                                                )
                                        if element_item:
                                            element_nodes.append(element_item)
                            logging.debug('the ended request {} page data.'.format(i))
                            # the request the network interface and temporarily sleep the random number (0,1)s
                            # to prevent being hacked by the server and this situation can be seen everywhere.
                            # We should try to personify the request
                            random_value = float('{:.3f}'.format(random.random()))
                            sleep(random_value)
                            logging.debug('the current sleep that is {:.3f}s'.format(random_value))
        return element_nodes

    def get_comment_lists(self, replyId, pageNum, timeout=600):
        '''
            the obtain comment list

            the response data structure:
            {
                "success":"1",
                "code":"1",
                "message":"",
                "data":[
                    {
                        "author_name":"",
                        "comment_time":"2018-09-05 11:17:43.533",
                        "id":"2150",
                        "author_id":"1309",
                        "content":"..."
                    }
                ]
            }
        '''
        response_with_dict = None
        api = 'http://bbs.tianya.cn/api'
        method = 'bbs.api.getCommentList'
        url = '{}?method={}&params.item={}&params.articleId={}&params.replyId={}&params.pageNum={}'.format(
            api, method, self.get_item_with_comments_params(), self.get_article_id_with_comments_params(), replyId,
            pageNum)
        if not (replyId and isinstance(replyId, int)):
            raise ValueError('the {} parameter is illegal'.format(replyId))
        if not (pageNum and isinstance(pageNum, int)):
            raise ValueError('the {} parameter is illegal'.format(pageNum))
        # private property
        __common_object_model = AnalysisFactory.get_com()
        try:
            __response = __common_object_model.get_http().get(url, timeout=timeout)
            # logging.debug('the current request url that is {}'.format(url))
            if __response and __response.status_code == codes.ok:
                content = __response.content
                if content:
                    response_with_dict = json.loads(content)
        except (ConnectionError, HTTPError, RequestException) as e:
            __common_object_model.get_eoe().append({
                'id': url,
                'emsg': str(e),
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            logging.exception(e)
            logging.exception('the current tracked information: {}'.format(traceback.format_exc()))
        return response_with_dict
