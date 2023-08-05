# -*- coding:utf-8 -*-

import datetime
from hashlib import md5
import os

from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory


def get_extends_directory():
    'get extended directory'
    output_dir_name = None
    # private property
    __common_object_model = AnalysisFactory.get_com()
    # private property
    __cfg = __common_object_model.get_cfg()
    if __cfg:
        output_dir_name = __cfg.get('output-directory', str())
        if output_dir_name:
            __output_dir_root_name = __cfg.get('output-directory-path', str())
            if not __output_dir_root_name:
                fmt = '%Y%m%d_%H%M%S'
                __output_uuid_encryptor = __cfg.get('output-uuid-encryptor', False)
                if __output_uuid_encryptor:
                    __output_dir_root_name = os.path.join(
                        output_dir_name,
                        md5(str(datetime.datetime.now().strftime(fmt)).encode('utf-8')).hexdigest())
                else:
                    __output_dir_root_name = os.path.join(output_dir_name, datetime.datetime.now().strftime(fmt))
                __cfg.update({'output-directory-path': __output_dir_root_name})
                # mk_dir(output_dir_root_name)
                logging.warning('the output directory with absolute path prefix currently written is {}\\...'.format(
                    __output_dir_root_name))
            output_dir_name = __output_dir_root_name
    else:
        raise ValueError('the {} object had not configured unsuccessfully.'.format('cfg'))
    return output_dir_name


def mk_dir(output_dir_name):
    'the make dir '
    output_dir = output_dir_name
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def mk_output_dir(output_dir_name, output_default_super_dir_name=None, flag=True):
    'the mk output dir'
    output_dir = ''
    if flag:
        if output_default_super_dir_name:
            output_dir = mk_dir(os.path.join(output_dir_name, output_default_super_dir_name))
        else:
            output_dir = mk_dir(output_dir_name)
    else:
        if output_dir_name and os.path.exists(output_dir_name):
            if output_default_super_dir_name:
                output_dir = mk_dir(os.path.join(output_dir_name, output_default_super_dir_name))
        elif not os.path.exists(output_dir_name):
            output_dir = mk_dir(output_dir_name)
        else:
            raise ValueError('the directory name({}) is invaild.'.format('output_dir_name'))
    return output_dir


def generate_file_name_only(output_dir_name, file_name):
    'the generate file name only'
    output_dir = mk_dir(output_dir_name)
    return os.path.join(output_dir, file_name)


def generate_complex_or_fmt_file_name(output_dir_name, file_name, fmt='%Y%m%d_%H%M%S'):
    'the generate out complex or fmt file name'
    output_dir = mk_output_dir(output_dir_name)
    if file_name is None or len(file_name.strip()) == 0:
        raise ValueError('the file name is invaild.')
    file_name = file_name.strip()
    if '.' in file_name:
        rdot_index = file_name.rfind('.')
        if rdot_index > 0:
            file_name = str("%s_%s%s" %
                            (file_name[0:rdot_index], datetime.datetime.now().strftime(fmt), file_name[rdot_index:]))
    else:
        file_name = str("%s_%s" % (file_name, datetime.datetime.now().strftime(fmt)))
    return os.path.join(output_dir, file_name)
