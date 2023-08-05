# -*- coding:utf-8 -*-

import datetime
import os
import traceback

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.directory.base_file import BaseFile
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.base.ihttp import IHttp
from com.dvsnier.http.tool.iexecute import IExecute
from com.dvsnier.http.util.file_utils import generate_complex_or_fmt_file_name, get_extends_directory
from requests import ConnectionError, HTTPError, RequestException


class AbstractHttp(IHttp, object):
    '''the abstract http class'''

    url = None

    def __init__(self):
        super(AbstractHttp, self).__init__()
        self.brs = BaseFile(strategy_mode=True)

    def get_default_region_space(self):
        'the get default region space by brs'
        return self.brs

    def get_file_list(self, dir_name):
        'the get file list only with specifically direcotry'
        file_list = []
        if dir_name and os.path.exists(dir_name) and os.path.isdir(dir_name):
            dir_or_file_list = os.listdir(dir_name)
            for file in dir_or_file_list:
                if os.path.isfile(os.path.join(dir_name, file)):
                    file_list.append(file)
                elif os.path.isdir(os.path.join(dir_name, file)):
                    continue
                else:
                    continue
        else:
            logging.error('the currently given directory name is an invalid or illegal parameter')
        return file_list

    def get_url(self):
        'the get url'
        return self.url

    def set_url(self, url, _on_callback=None):
        'the set url'
        self.url = url
        IExecute().execute(_on_callback, self.get_url())
        return self

    def set_work_region_space(self, work_region_space, _on_callback=None):
        'the set work region space'
        self.get_default_region_space().set_work_region_space(work_region_space)
        IExecute().execute(_on_callback, self.get_default_region_space().get_work_region_space())
        return self

    # private property
    def __write_to_file(self, url, file_name, features='html.parser'):
        try:
            response = self.get(url)
            if response:
                # logging.debug(response.headers['Content-Type'])
                if self.brs and file_name:
                    if not self.brs:
                        self.brs.set_work_region_space(os.getcwd())
                    with open(file_name, 'w') as f:
                        # private property
                        __common_object_model = AnalysisFactory.get_com()
                        soup = __common_object_model.get_resolver().bs(response.content, features)
                        if soup:
                            prettify = __common_object_model.get_resolver().prettify(soup)
                            if prettify:
                                f.write(prettify)
        except (ConnectionError, HTTPError, RequestException) as e:
            # private property
            __common_object_model = AnalysisFactory.get_com()
            __common_object_model.get_eoe().append({
                'id': url,
                'emsg': str(e),
                'file_name': file_name,
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            logging.exception(e)
            logging.exception('the current tracked information: {}'.format(traceback.format_exc()))

    def write_to_file_with_multiple(self, url, file_prefix, file_suffix, output_dir_name='http', index=None):
        'the write to file multiple times'
        file_name = None
        if self.brs:
            if not output_dir_name:
                output_dir_name = file_suffix
            # private property
            __ext_dir = get_extends_directory()
            if __ext_dir:
                output_dir_name = os.path.join(__ext_dir, output_dir_name)
                if index:
                    file_name = generate_complex_or_fmt_file_name(output_dir_name,
                                                                  '{}_{}.{}'.format(file_prefix, index, file_suffix))
                else:
                    file_name = generate_complex_or_fmt_file_name(output_dir_name,
                                                                  '{}.{}'.format(file_prefix, file_suffix))
            else:
                if index:
                    file_name = self.brs.generate_complex_or_fmt_file_name(
                        output_dir_name, '{}_{}.{}'.format(file_prefix, index, file_suffix))
                else:
                    file_name = self.brs.generate_complex_or_fmt_file_name(output_dir_name,
                                                                           '{}.{}'.format(file_prefix, file_suffix))
            if url:
                logging.warning('the file name currently written is {}'.format(file_name))
                self.__write_to_file(url, file_name)
            else:
                logging.error('The current {} parameter is illegal'.format(url))
                raise KeyError('The current {} parameter is illegal'.format(url))
        return file_name
