# -*- coding:utf-8 -*-

import base64
from datetime import datetime
import io
import os
import PIL
import re
import traceback

from bs4.element import NavigableString, Tag
from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.dom.content.ibbscontent import IBbsContent
from com.dvsnier.http.util.file_utils import generate_file_name_only, get_extends_directory, mk_output_dir
from requests import ConnectionError, HTTPError, RequestException
from PIL import Image, ImageFile


class AbstractBbsContent(IBbsContent, object):
    '''the abstract bbs content class'''
    def __init__(self):
        super(AbstractBbsContent, self).__init__()

    def bbs_content_set(self, div_bbs_content):
        # deprecated
        # element_item['author_content'] = div_bbs_content.get_text().strip()
        element_item_set = []
        for index, item_with_bbs_content in enumerate(div_bbs_content.children):
            if item_with_bbs_content and isinstance(item_with_bbs_content, NavigableString):
                element_item_set.extend(self.__bbs_content_with_navigable_string(index, item_with_bbs_content))
            elif item_with_bbs_content and isinstance(item_with_bbs_content, Tag):
                element_item_set.extend(self.__bbs_content_with_tag(index, item_with_bbs_content))
            else:
                # continue
                element_item_set.extend(self.__bbs_content_with_illegal(index, item_with_bbs_content))
        return element_item_set

    def __bbs_content_with_navigable_string(self, *element_item):
        element_item_set = []
        if element_item:
            index = element_item[0]
            item_with_bbs_content = element_item[1]

            element_content_item = dict()
            element_content_item['index'] = index
            if item_with_bbs_content and isinstance(item_with_bbs_content, NavigableString):
                element_content_item['type'] = 1
                element_content_item['resource_content'] = item_with_bbs_content.strip()
                element_item_set.append(element_content_item)
        return element_item_set

    def __bbs_content_with_tag(self, *element_item):
        element_item_set = []
        if element_item:
            index = element_item[0]
            item_with_bbs_content = element_item[1]

            if item_with_bbs_content.name == 'br':
                element_item_set.extend(self.__bbs_content_with_tag_dot_br(index, item_with_bbs_content))
            elif item_with_bbs_content.name == 'img':
                element_item_set.extend(self.__bbs_content_with_tag_dot_img(index, item_with_bbs_content))
            elif item_with_bbs_content.name == 'a':
                element_item_set.extend(self.__bbs_content_with_tag_dot_a(index, item_with_bbs_content))
            elif item_with_bbs_content.name == 'span':
                element_item_set.extend(self.__bbs_content_with_tag_dot_span(index, item_with_bbs_content))
            else:
                element_content_item = dict()
                element_content_item['index'] = index
                element_content_item['type'] = 0
                element_item_set.append(element_content_item)
                logging.error(
                    'the current parse bbs content node({}) error that contains property values that have not been processed.'
                    .format(item_with_bbs_content))
        return element_item_set

    def __bbs_content_with_tag_dot_br(self, *element_item):
        element_item_set = []
        if element_item:
            index = element_item[0]
            item_with_bbs_content = element_item[1]

            element_content_item = dict()
            element_content_item['index'] = index
            if item_with_bbs_content and isinstance(item_with_bbs_content, Tag):
                element_content_item['type'] = 1
                element_content_item['resource_content'] = '\n'
                element_item_set.append(element_content_item)
        return element_item_set

    def __bbs_content_with_tag_dot_img(self, *element_item):
        element_item_set = []
        if element_item:
            index = element_item[0]
            item_with_bbs_content = element_item[1]

            element_content_item = dict()
            element_content_item['index'] = index
            if item_with_bbs_content and isinstance(item_with_bbs_content, Tag):
                element_content_item['type'] = 3
                element_content_item['resource_url_original'] = item_with_bbs_content.get('original')
                element_content_item['resource_url_thumbnail'] = item_with_bbs_content.get('src')
                url = None
                # private property
                __common_object_model = AnalysisFactory.get_com()
                if __common_object_model.get_attribute().get_quality():
                    url = element_content_item['resource_url_original']
                else:
                    url = element_content_item['resource_url_thumbnail']
                try:
                    response = __common_object_model.get_http().get(url, timeout=600)  # url data to str(base64)
                    if response:
                        resource_bytes = io.BytesIO(response.content).read()
                        element_content_item['resource_base64'] = str(base64.b64encode(resource_bytes),
                                                                      encoding='utf-8')
                except (ConnectionError, HTTPError, RequestException) as e:
                    element_content_item['resource_base64'] = ''
                    element_content_item['anchor_mark'] = 'N'
                    # private property
                    __common_object_model = AnalysisFactory.get_com()
                    __common_object_model.get_eoe().append({
                        'id': url,
                        'emsg': str(e),
                        'element': element_content_item,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    logging.exception(e)
                    logging.exception('the current tracked information: {}'.format(traceback.format_exc()))
                self.__bbs_content_with_tag_dot_img_persistence_to_locality(element_content_item)
                element_item_set.append(element_content_item)
        return element_item_set

    def __bbs_content_with_tag_dot_img_persistence_to_locality(self, element_content_item):
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        # private property
        __common_object_model = AnalysisFactory.get_com()
        if __common_object_model.get_attribute().get_persistence():  # the persistence
            fmt = '%Y%m%d'
            article_alias = __common_object_model.get_cfg().get('article-alias')
            # private property
            __ext_dir = get_extends_directory()
            multi_media_name = None
            if article_alias:
                if __ext_dir:
                    multi_media_name = 'multi_media_{}_{}'.format(datetime.now().strftime(fmt), article_alias)
                else:
                    multi_media_name = 'bbs_{}_{}'.format(datetime.now().strftime(fmt), article_alias)
            else:
                multi_media_name = 'multi_media_{}'.format(datetime.now().strftime(fmt))
            crs = __common_object_model.get_brs().get_current_region_space()
            if crs:
                persistence_url = element_content_item['resource_url_original']
                output_dir_name = ''
                if __ext_dir:
                    output_dir_name = mk_output_dir(os.path.join(__ext_dir, multi_media_name))
                else:
                    output_dir_name = __common_object_model.get_brs().mk_output_dir(
                        os.path.join('image', multi_media_name))
                if persistence_url and isinstance(persistence_url, str):
                    pattern = re.compile(r'[a-zA-Z]{3,4}')
                    match = re.search(pattern, persistence_url.split(r'.')[-1])
                    if match and match.string:
                        img_suffix = match.string
                        img_name = 'img_{}_{}.{}'.format(
                            __common_object_model.get_comment_model().get_article_serial_number(),
                            int(datetime.timestamp(datetime.now())), img_suffix)
                        file_name = ''
                        if __ext_dir:
                            file_name = generate_file_name_only(output_dir_name, img_name)
                        else:
                            file_name = __common_object_model.get_brs().generate_file_name_only(
                                output_dir_name, img_name)
                        # logging.debug('the current img path that is {}'.format(file_name))
                        try:
                            persistence_response = __common_object_model.get_http().get(
                                persistence_url, timeout=600)  # url data to persistence
                            if persistence_response:
                                try:
                                    resource_bytes = io.BytesIO(persistence_response.content)
                                    resource_with_image = Image.open(resource_bytes)
                                    if resource_with_image:
                                        #
                                        # PIL 图片模式(https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html):
                                        # 1             1 位像素，黑和白，存成8位的像素
                                        # L             8 位像素，黑白
                                        # P             8 位像素，使用调色板映射到任何其他模式
                                        # RGB           3×8 位像素，真彩
                                        # RGBA          4×8 位像素，真彩+透明通道
                                        # CMYK          4×8 位像素，颜色隔离
                                        # YCbCr         3×8 位像素，彩色视频格式
                                        # I             32 位整型像素
                                        # F             32 位浮点型像素
                                        if img_suffix.lower() == 'jpg' or img_suffix.lower() == 'jpeg':
                                            resource_with_image.convert('RGB').save(file_name, quality=100)
                                        elif img_suffix.lower() == 'gif':
                                            resource_with_image.save(file_name, save_all=True)
                                        else:
                                            resource_with_image.save(file_name, quality=100)
                                except (FileNotFoundError, PIL.UnidentifiedImageError, ValueError, TypeError,
                                        KeyError) as e:
                                    # private property
                                    __common_object_model = AnalysisFactory.get_com()
                                    __common_object_model.get_eoe().append({
                                        'id':
                                        persistence_url,
                                        'emsg':
                                        str(e),
                                        'element':
                                        element_content_item,
                                        'timestamp':
                                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    })
                                    logging.exception(e)
                                    logging.exception('the current tracked information: {}'.format(
                                        traceback.format_exc()))
                                else:
                                    if __common_object_model.get_debug().is_debug():
                                        logging.debug(
                                            'the current persistent image data({}) succeeded.'.format(file_name))
                        except (ConnectionError, HTTPError, RequestException) as e:
                            # private property
                            __common_object_model = AnalysisFactory.get_com()
                            __common_object_model.get_eoe().append({
                                'id':
                                persistence_url,
                                'emsg':
                                str(e),
                                'element':
                                element_content_item,
                                'timestamp':
                                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            logging.exception(e)
                            logging.exception('the current tracked information: {}'.format(traceback.format_exc()))

    def __bbs_content_with_tag_dot_a(self, *element_item):
        element_item_set = []
        if element_item:
            index = element_item[0]
            item_with_bbs_content = element_item[1]

            element_content_item = dict()
            element_content_item['index'] = index
            element_content_item, item_with_bbs_content
            if item_with_bbs_content and isinstance(item_with_bbs_content, Tag):
                href = item_with_bbs_content.get('href')
                if href:
                    if href == 'javascript:void(0);':
                        element_content_item['type'] = 1
                        element_content_item['resource_content'] = item_with_bbs_content.get_text().strip()
                    else:
                        element_content_item['type'] = 2
                        element_content_item['resource_content'] = item_with_bbs_content.get_text().strip()
                        element_content_item['resource_href'] = href
                    element_item_set.append(element_content_item)
        return element_item_set

    def __bbs_content_with_tag_dot_span(self, *element_item):
        element_item_set = []
        if element_item:
            index = element_item[0]
            item_with_bbs_content = element_item[1]

            element_content_item = dict()
            element_content_item['index'] = index
            if item_with_bbs_content and isinstance(item_with_bbs_content, Tag):
                span_dot_img_result_set = item_with_bbs_content.select('span img')
                if span_dot_img_result_set:
                    for index, item_with_img in enumerate(span_dot_img_result_set):
                        element_item_set.extend(self.__bbs_content_with_tag_dot_img(element_content_item,
                                                                                    item_with_img))
                else:
                    element_content_item['type'] = 1
                    element_content_item['resource_content'] = item_with_bbs_content.get_text().strip()
                    element_item_set.append(element_content_item)
        return element_item_set

    def __bbs_content_with_illegal(self, *element_item):
        element_item_set = []
        if element_item:
            index = element_item[0]
            item_with_bbs_content = element_item[1]

            # element_content_item = dict()
            # element_content_item['additional_type'] = "0: 数据(脏), 1: 文本, 2: 链接, 3: 图片, 4: 视频, 5: 音频, 6: 附件",
            # element_content_item['anchor_mark'] = "N: 数据(脏), U: 数据未追踪(Untracked), A: 新数据(Added, Staged), M: 数据有修改(Modified), +M: 数据有修改(Modified, Staged), C: 数据有冲突(Conflict), D: 数据被删除(Deleted)",
            # element_content_item['index'] = index
            # element_content_item['type'] = "0: 数据(脏), 1: 文本, 2: 链接, 3: 图片, 4: 视频, 5: 音频, 6: 附件",
            # element_content_item['resource_base64'] = "3: 图片, 4: 视频(不建议), 5: 音频(不建议), 6: 附件(不推荐)",
            # element_content_item['resource_content'] = "1: 文本, 2: 链接",
            # element_content_item['resource_href'] = "2: 链接",
            # element_content_item['resource_url_thumbnail'] = "3: 图片, 4: 视频, 5: 音频, 6: 附件",
            # element_content_item['resource_url_small'] = "3: 图片, 4: 视频, 5: 音频, 6: 附件",
            # element_content_item['resource_url_middle'] = "3: 图片, 4: 视频, 5: 音频, 6: 附件",
            # element_content_item['resource_url_large'] = "3: 图片, 4: 视频, 5: 音频, 6: 附件",
            # element_content_item['resource_url_original'] = "3: 图片, 4: 视频, 5: 音频, 6: 附件",
            element_content_item = dict()
            element_content_item['index'] = index
            element_content_item['type'] = 0
            element_item_set.append(element_content_item)
            logging.error(
                'the current parse bbs content node({}) error that contains property values that have not been processed.'
                .format(item_with_bbs_content.text))
        return element_item_set
