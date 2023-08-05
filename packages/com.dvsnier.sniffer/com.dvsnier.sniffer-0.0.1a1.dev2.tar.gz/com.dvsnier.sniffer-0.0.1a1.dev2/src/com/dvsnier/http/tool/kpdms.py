# -*- coding:utf-8 -*-

import datetime
import json
import os

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.directory.base_file import BaseFile
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.bbs.specimen.bbs_with_tianya import BbsWithTianYa
from com.dvsnier.http.tool.iexecute import IExecute
from com.dvsnier.http.util.file_utils import generate_file_name_only, get_extends_directory
from com.dvsnier.http.util.utils import task_sort_with_major_three


class KpmDs(object):
    '''the key-page mapping to standard data structure class'''

    __file_name = None

    def __init__(self):
        super(KpmDs, self).__init__()
        self.__bbs = BbsWithTianYa()

    def set_file_name(self, file_name):
        'the set single file name'
        self.__file_name = file_name
        return self

    def set_persistence(self, resource_persistence):
        # private property
        __common_object_model = AnalysisFactory.get_com()
        return __common_object_model.get_attribute().set_persistence(
            resource_persistence, _on_resource_persistence_callback=self._on_resource_persistence_callback)

    def set_quality(self, resource_quality):
        # private property
        __common_object_model = AnalysisFactory.get_com()
        return __common_object_model.get_attribute().set_quality(
            resource_quality, _on_resource_quality_callback=self._on_resource_quality_callback)

    def _callback_with_file_list_with_single(self):
        return [self.__file_name]

    def _callback_with_file_list_with_multiple(self):
        fmt = '%Y%m%d'
        bbs_name = 'bbs_{}'.format(datetime.datetime.now().strftime(fmt))
        output_dir_name = os.path.join(os.getcwd(), 'out', bbs_name)
        # private property
        __common_object_model = AnalysisFactory.get_com()
        return __common_object_model.get_http().get_file_list(output_dir_name)

    def _on_resource_persistence_callback(self, persistence):
        logging.debug('the set persistence task({}) has executed successfully.'.format(persistence))

    def _on_resource_quality_callback(self, quality):
        logging.debug('the set quality task({}) has executed successfully.'.format(quality))

    def local_to_json(self, flags, _on_item_callback=None, _on_callback=None):
        '''
            the local to json

            FLAGS: False: first pull , second translate otherwise True: one pull after another translate
        '''
        if flags:
            self.__local_to_json(self._callback_with_file_list_with_single,
                                 _on_item_callback=_on_item_callback,
                                 _on_callback=_on_callback)
        else:
            self.__local_to_json(self._callback_with_file_list_with_multiple,
                                 _on_item_callback=_on_item_callback,
                                 _on_callback=_on_callback)

    def __local_to_json(self, _obtain_file_list_with_name_only, _on_item_callback=None, _on_callback=None):
        # private property
        __common_object_model = AnalysisFactory.get_com()
        # private property
        __cfg = __common_object_model.get_cfg()
        # private property
        # __http = __common_object_model.get_http()
        # private property
        __model = __common_object_model.get_model()
        # private property
        # __resolver = __common_object_model.get_resolver()

        fmt = '%Y%m%d'
        bbs_name = None
        article_alias = __cfg.get('article-alias')
        if article_alias:
            bbs_name = 'bbs_{}_{}'.format(datetime.datetime.now().strftime(fmt), article_alias)
        else:
            bbs_name = 'bbs_{}'.format(datetime.datetime.now().strftime(fmt))
        output_dir_name = None
        # private property
        __ext_dir = get_extends_directory()
        if __ext_dir:
            output_dir_name = os.path.join(__ext_dir, bbs_name)
        else:
            output_dir_name = os.path.join(os.getcwd(), 'out', bbs_name)

        # set work region space
        base_file = BaseFile()
        base_file.set_work_region_space(os.getcwd())
        __common_object_model.get_brs().set_work_region_space(os.getcwd())

        file_list = _obtain_file_list_with_name_only()
        if file_list and isinstance(file_list, list):
            file_list.sort(key=task_sort_with_major_three)
        # logging.debug(json.dumps(file_list, ensure_ascii=False, indent=4))

        json_name = None
        if article_alias:
            json_name = 'json_{}_{}'.format(datetime.datetime.now().strftime(fmt), article_alias)
        else:
            json_name = 'json_{}'.format(datetime.datetime.now().strftime(fmt))
        dest_dir_name = None
        if __ext_dir:
            dest_dir_name = os.path.join(__ext_dir, json_name)
        else:
            dest_dir_name = os.path.join(os.getcwd(), 'out', json_name)

        for file in file_list:
            markup_file = os.path.join(output_dir_name, file)
            if markup_file and os.path.exists(markup_file):
                beautiful_soup = __model.beautiful_soup(markup_file, _on_callback=self._on_callback_with_beautiful_soup)
                # beautiful_soup = __resolver.beautiful_soup(markup_file, _on_callback=self._on_callback_with_beautiful_soup)
                bbs_introduce_dict = self.__bbs.get_bbs_plate(lambda: beautiful_soup)
                # logging.debug(json.dumps(bbs_introduce_dict, ensure_ascii=False, indent=4))
                if file and isinstance(file, str):
                    dest_file_name = None
                    if __ext_dir:
                        dest_file_name = generate_file_name_only(dest_dir_name,
                                                                 '{}.json'.format(file.split(r'.', maxsplit=1)[0]))
                    else:
                        dest_file_name = base_file.generate_file_name_only(
                            dest_dir_name, '{}.json'.format(file.split(r'.', maxsplit=1)[0]))
                    with open(dest_file_name, 'w') as f:
                        f.write(json.dumps(bbs_introduce_dict, ensure_ascii=False, indent=4))
                    IExecute().execute(_on_item_callback, file, dest_file_name)
            else:
                logging.error(
                    'The current markup file({}) does not exist, and then that is a fatal error and the subsequent process is interrupted.'
                    .format(markup_file))
        IExecute().execute(_on_callback)

    def _on_callback_with_beautiful_soup(self, beautiful_soup):
        if beautiful_soup:
            # private property
            __common_object_model = AnalysisFactory.get_com()
            __common_object_model.get_comment_model()._url = __common_object_model.get_http().get_url()
            logging.debug('the task({}) has executed successfully.'.format('_on_callback_with_beautiful_soup'))
            logging.debug('the current pile insertion parsing engine succeeded.')
