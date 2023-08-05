# -*- coding:utf-8 -*-

import json
import time

from com.dvsnier.config.cfg.configuration import Configuration
from com.dvsnier.config.journal.compat_logging import logging


class IConfig(object):
    '''the iconfig class'''

    cfg = None

    def __init__(self):
        super(IConfig, self).__init__()

    def config(self, config):
        'the resolve local configuration list'
        parsing_configuration_start = time.time()
        self.cfg = Configuration().obtain_config(config)
        logging.debug('the current config is {}'.format(json.dumps(self.cfg, indent=4, ensure_ascii=False)))
        parsing_configuration_end = time.time()
        logging.info('the parsing configuration file complete, that total time consumed {:.3f} seconds '.format(
            parsing_configuration_end - parsing_configuration_start))
        return self.cfg
