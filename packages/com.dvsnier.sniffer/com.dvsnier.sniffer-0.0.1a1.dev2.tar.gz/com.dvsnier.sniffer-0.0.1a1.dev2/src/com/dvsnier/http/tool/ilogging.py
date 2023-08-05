# -*- coding:utf-8 -*-

import os

from com.dvsnier.config.journal.compat_logging import logging


class ILogging(object):
    '''the Template class'''
    def __init__(self):
        super(ILogging, self).__init__()

    def set_logging(self, _on_callback=None):
        '''
            the set method

            the default set params that is above:

            {
                'output_dir_name': 'http',
                'file_name': 'log',
                'level': logging.DEBUG
            }
        '''
        # kwargs = {'output_dir_name': 'http', 'file_name': 'log', 'level': logging.DEBUG}
        # if _on_callback:
        #     kwargs = _on_callback()
        # deprecated
        # config(kwargs)
        logging.set_kw_output_dir_name(os.path.join(os.getcwd(), 'out',
                                                    'dvs-http')).set_kw_file_name('log').set_kw_level(
                                                        logging.DEBUG).set_logging_name('dvs-http').build()
