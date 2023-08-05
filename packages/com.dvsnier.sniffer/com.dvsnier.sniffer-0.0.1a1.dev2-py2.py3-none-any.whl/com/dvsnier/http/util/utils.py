# -*- coding:utf-8 -*-

import datetime
import json
import os
import re
import traceback

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.directory.base_file import BaseFile
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.tool.iexecute import IExecute
from deprecated import deprecated


def task_sort_with_major_three(file_name):
    'only the sorting mode of file name is supported'
    if file_name and isinstance(file_name, str):
        file_split_list = file_name.split(r'_', maxsplit=4)
        if file_split_list[2]:
            return int(file_split_list[2])
    return 0


@deprecated(
    version='0.0.1.dev1',
    reason="You should use the from com.dvsnier.http.utils import task_sort_with_major_three method, that We will delete \
this method after extending 2-3 versions")
def task_sort_with_major_two(file_name_previous, file_name_next):
    '''
        only the sorting mode of file name is supported

        previous - next > 0, positive sequence
        previous - next = 0, invariant sequence
        previous - next < 0, reverse sequence
    '''
    if file_name_previous and isinstance(file_name_previous, str) and file_name_next and isinstance(
            file_name_next, str):
        previous_list = file_name_previous.split(r'_', maxsplit=4)
        next_list = file_name_next.split(r'_', maxsplit=4)
        if previous_list[2] and next_list[2]:
            return int(previous_list[2]) - int(next_list[2])
    return 0


REGION_INCLUSIVE_EXCLUSIVE = 0
REGION_EXCLUSIVE_INCLUSIVE = 1
REGION_EXCLUSIVE_EXCLUSIVE = 2
REGION_INCLUSIVE_INCLUSIVE = 3


def region(start, stop=0, step=1, flags=REGION_INCLUSIVE_EXCLUSIVE):
    '''
        start, stop[, step[,flags]]

        the region range:

            1. [m, n): REGION_INCLUSIVE_EXCLUSIVE = 0
            2. (m, n]: REGION_EXCLUSIVE_INCLUSIVE = 1
            3. (m, n): REGION_EXCLUSIVE_EXCLUSIVE = 2
            4. [m, n]: REGION_INCLUSIVE_INCLUSIVE = 3

            the default, range(n) = [0, n) equal region(n)
    '''
    value = range(0)
    if start > 0:
        if stop <= 0:  # range(n) = [0, start)
            value = range(start)
        else:
            if start < stop:
                if flags == REGION_INCLUSIVE_EXCLUSIVE:  # range(m, n) = [m, n)
                    value = range(start, stop, step)
                elif flags == REGION_EXCLUSIVE_INCLUSIVE:  # range(m, n) = (m, n]
                    value = range(start + 1, stop + 1, step)
                elif flags == REGION_EXCLUSIVE_EXCLUSIVE:  # range(m, n) = (m, n)
                    value = range(start + 1, stop, step)
                elif flags == REGION_INCLUSIVE_INCLUSIVE:  # range(m, n) = [m, n]
                    value = range(start, stop + 1, step)
                else:  # range(m, n) = [m, n)
                    value = range(start, stop)
            else:
                pass
    else:
        pass
    return value


def section(value, _on_callback=None):
    '''
        the section range:

        value: [m, n]|[m, n)|(m, n]|(m, n)
        the region range:

            1. [m, n): REGION_INCLUSIVE_EXCLUSIVE = 0
            2. (m, n]: REGION_EXCLUSIVE_INCLUSIVE = 1
            3. (m, n): REGION_EXCLUSIVE_EXCLUSIVE = 2
            4. [m, n]: REGION_INCLUSIVE_INCLUSIVE = 3
    '''
    ir_container = interval_range(value, _on_callback)
    return region(ir_container[0], ir_container[1], flags=ir_container[2])


def interval_range(value, _on_callback=None):
    '''
        the interval range:

        value: [m, n]|[m, n)|(m, n]|(m, n)
        the region range:

            1. [m, n): REGION_INCLUSIVE_EXCLUSIVE = 0
            2. (m, n]: REGION_EXCLUSIVE_INCLUSIVE = 1
            3. (m, n): REGION_EXCLUSIVE_EXCLUSIVE = 2
            4. [m, n]: REGION_INCLUSIVE_INCLUSIVE = 3
    '''
    page_start = 1
    page_stop = 0
    region_flags = 0
    pattern = re.compile(r'^[\[\(][\s]*\d+[\s]*,[\s]*\d+[\s]*[\]\)]$')
    if re.search(pattern, value):
        psam_match = re.search(r'^[\[\(]', value)
        psom_match = re.search(r'[\]\)]$', value)
        digital_list = re.findall(r'\d+', value)
        if psam_match and psom_match:
            psam_rmark = psam_match.group()
            psom_rmark = psom_match.group()
            if psam_rmark.strip() == '[':
                if psom_rmark.strip() == ']':
                    region_flags = REGION_INCLUSIVE_INCLUSIVE
                elif psom_rmark.strip() == ')':
                    region_flags = REGION_INCLUSIVE_EXCLUSIVE
                else:
                    raise ValueError('The current value({}) is an invalid parameter.'.format(value))
            elif psam_rmark.strip() == '(':
                if psom_rmark.strip() == ']':
                    region_flags = REGION_EXCLUSIVE_INCLUSIVE
                elif psom_rmark.strip() == ')':
                    region_flags = REGION_EXCLUSIVE_EXCLUSIVE
                else:
                    raise ValueError('The current value({}) is an invalid parameter.'.format(value))
            else:
                raise ValueError('The current value({}) is an invalid parameter.'.format(value))
            if digital_list:
                page_start = int(digital_list[0].strip())
                page_stop = int(digital_list[1].strip())
            else:
                raise ValueError('The current value({}) is an invalid parameter.'.format(value))
        else:
            raise ValueError('The current value({}) is an invalid parameter.'.format(value))
        pass
    else:
        raise ValueError('The current value({}) is an invalid parameter.'.format(value))
    if _on_callback:
        _on_callback(page_start, page_stop, region_flags)
    return [page_start, page_stop, region_flags]


def obtain_file_and_resolver(_on_callback=None):
    'the obtain file and resolver'
    fmt = '%Y%m%d'
    bbs_name = 'bbs_{}'.format(datetime.datetime.now().strftime(fmt))
    output_dir_name = os.path.join(os.getcwd(), 'out', bbs_name)
    # TEST SPENCIMEN
    # output_dir_name = os.path.join(os.getcwd(), 'out', 'bbs_20210812')

    # private property
    __common_object_model = AnalysisFactory.get_com()
    # private property
    __http = __common_object_model.get_http()
    # private property
    __model = __common_object_model.get_model()
    # private property
    # __resolver = __common_object_model.get_resolver()

    # set work region space
    base_file = BaseFile()
    base_file.set_work_region_space(os.getcwd())
    __common_object_model.get_brs().set_work_region_space(os.getcwd())

    file_list = __http.get_file_list(output_dir_name)
    # TEST SPENCIMEN
    # file_list = ['bbs_1_20210812_115726.html']
    # TEST SPENCIMEN
    # file_list = ['bbs_2_20210812_115938.html']
    if file_list and isinstance(file_list, list):
        file_list.sort(key=task_sort_with_major_three)
    # logging.debug(json.dumps(file_list, ensure_ascii=False, indent=4))

    beautiful_soup = __model.beautiful_soup(os.path.join(output_dir_name, file_list[0]),
                                            _on_callback=_on_callback_with_beautiful_soup)
    # beautiful_soup = __resolver.beautiful_soup(os.path.join(output_dir_name, file_list[0]), _on_callback=_on_callback_with_beautiful_soup)
    IExecute().execute(_on_callback)
    return beautiful_soup


def _on_callback_with_beautiful_soup(beautiful_soup):
    if beautiful_soup:
        # private property
        __common_object_model = AnalysisFactory.get_com()
        __common_object_model.get_comment_model()._url = __common_object_model.get_http().get_url()
        logging.debug('the task({}) has executed successfully.'.format('_on_callback_with_beautiful_soup'))
        logging.debug('the current pile insertion parsing engine succeeded.')


def output_exception_queue():
    'the output exception queue'
    # private property
    __common_object_model = AnalysisFactory.get_com()
    # private property
    __eoe = __common_object_model.get_eoe()
    if isinstance(__eoe, list) and len(__eoe) > 1:
        __eoe.pop(0)
        logging.warning('the current simple output exception queue, as shown below:')
        try:
            logging.error(json.dumps(__eoe, ensure_ascii=False, indent=4))
        except Exception as e:
            logging.exception(e)
            logging.exception(traceback.format_exc())
            logging.error(__eoe)
