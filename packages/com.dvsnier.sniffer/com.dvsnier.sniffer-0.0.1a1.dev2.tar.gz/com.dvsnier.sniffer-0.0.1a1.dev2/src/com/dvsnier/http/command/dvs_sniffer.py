# -*- coding:utf-8 -*-

import argparse
import datetime
import json
import os
import random
import re
import sys
import tempfile
import time

from com.dvsnier.config.cfg.configuration import Configuration
from com.dvsnier.config.journal.compat_logging import logging
from com.dvsnier.http import DEBUGGER, ENVIRONMENT_VARIABLE_CONFIGURATION, VERSIONS
from com.dvsnier.http.analysis.analysis_factory import AnalysisFactory
from com.dvsnier.http.tool.ilogging import ILogging
from com.dvsnier.http.tool.kpdms import KpmDs
from com.dvsnier.http.tool.network import Network
from com.dvsnier.http.util.utils import REGION_EXCLUSIVE_EXCLUSIVE, REGION_EXCLUSIVE_INCLUSIVE
from com.dvsnier.http.util.utils import REGION_INCLUSIVE_EXCLUSIVE, REGION_INCLUSIVE_INCLUSIVE
from com.dvsnier.http.util.utils import interval_range, region


class Crawler_Bbs_TianYa(object):
    '''the crawler bbs tianya class'''

    # private property
    __flag = True  # False: first pull , second translate True: one pull after another translate
    # protected property
    _page_start = 1
    # protected property
    _page_stop = 0
    # protected property
    _region_flags = REGION_INCLUSIVE_EXCLUSIVE

    def __init__(self, args):
        super(Crawler_Bbs_TianYa, self).__init__()
        # ILogging().set_logging()
        self.__args = args
        self.__network = Network()
        self.__network.set_work_region_space(os.getcwd())
        self.__pmds = KpmDs()
        # self.__pmds.set_persistence(True)
        # self.__pmds.set_quality(True)

    def run(self):
        'the run method'
        if self.__flag:
            logging.warning('the scheme with {} that is currently adopted.'.format('one pull after another translate'))
        else:
            logging.warning('the scheme with {} that is currently adopted.'.format('first pull then second translate'))
        self.__network.pull_bbs_to_local(self._on_callback)
        if not self.__flag:
            random_value = 1.0 + random.random()
            time.sleep(random_value)
            logging.debug('the current task(translate_bbs_local_to_json) sleep that is {:.3f}s'.format(random_value))
            self.__pmds.local_to_json(self.__flag)

    def set_range(self, page_start, page_stop=0, flag=REGION_INCLUSIVE_EXCLUSIVE):
        'set range'
        self._page_start = page_start
        self._page_stop = page_stop
        self._region_flags = flag
        return self

    def set_flag(self, flag):
        'set flag then False: first pull , second translate True: one pull after another translate'
        self.__flag = flag
        return self

    def _on_callback(self, urls):
        if self.__args:
            pf = None
            region_with_cli_mask = None
            if self.__args.region_mask == 'REGION_INCLUSIVE_EXCLUSIVE':
                pf = REGION_INCLUSIVE_EXCLUSIVE
                region_with_cli_mask = '[{},{})'.format(self._page_start, self._page_stop)
            elif self.__args.region_mask == 'REGION_EXCLUSIVE_INCLUSIVE':
                pf = REGION_EXCLUSIVE_INCLUSIVE
                region_with_cli_mask = '({},{}]'.format(self._page_start, self._page_stop)
            elif self.__args.region_mask == 'REGION_EXCLUSIVE_EXCLUSIVE':
                pf = REGION_EXCLUSIVE_EXCLUSIVE
                region_with_cli_mask = '({},{})'.format(self._page_start, self._page_stop)
            elif self.__args.region_mask == 'REGION_INCLUSIVE_INCLUSIVE':
                pf = REGION_INCLUSIVE_INCLUSIVE
                region_with_cli_mask = '[{},{}]'.format(self._page_start, self._page_stop)
            else:
                pf = REGION_INCLUSIVE_EXCLUSIVE
                region_with_cli_mask = '[{},{})'.format(self._page_start, self._page_stop)
            cfg = {
                'sn-url-prefix': [
                    self.__args.url[1],
                ],
                'article-alias': self.__args.article_alias,
                'page-start': self.__args.region_start,
                'page-stop': self.__args.region_end,
                'page-flag': pf,
                'region': '{}'.format(region_with_cli_mask),
                'article-multi-media-persistence': self.__args.article_multi_media_persistence,
                'article-multi-media-quality': self.__args.article_multi_media_quality,
                'article-flag': self.__flag,
                'output-directory': self.__args.destination_directory,
                'output-uuid-encryptor': self.__args.destination_uuid_encryptor,
                'User-Agent': self.__args.user_agent,
            }
            # private property
            __common_object_model = AnalysisFactory.get_com()
            __common_object_model.set_cfg(
                cfg, lambda it: logging.debug('the {} object configured successfully.'.format('cfg')))
            sn_url_prefix = cfg.get('sn-url-prefix')
            article_alias = cfg.get('article-alias')
            if self._page_start <= 1 and self._page_stop <= 0:  # NO DEFAULT CONFIGURATION REGION
                page_start = cfg.get('page-start', int())
                page_stop = cfg.get('page-stop', int())
                region_flags = cfg.get('page-flag', int())
                page_region = cfg.get('region', str())
                if page_start == 0 and page_stop == 0 and region_flags == 0:
                    ir = interval_range(page_region)
                    if ir:
                        page_start = ir[0]
                        page_stop = ir[1]
                        region_flags = ir[2]
                if isinstance(page_start, int) and isinstance(page_stop, int) and isinstance(region_flags, int):
                    self.set_range(page_start, page_stop, region_flags)
                persistence = cfg.get('article-multi-media-persistence', False)
                if persistence:
                    self.__pmds.set_persistence(persistence)
                quality = cfg.get('article-multi-media-quality', False)
                if quality:
                    self.__pmds.set_quality(quality)
                article_flag = cfg.get('article-flag', True)
                if not article_flag:
                    self.set_flag(article_flag)
            if sn_url_prefix and isinstance(sn_url_prefix, list):
                for url_prefix in sn_url_prefix:
                    for i in region(self._page_start, self._page_stop, flags=self._region_flags):
                        index = i
                        if self._page_stop <= 0:
                            index = i + 1
                        else:
                            index = i
                        url = url_prefix.format(index)
                        urls.append(url)
                        # fmt = '%Y%m%d_%H%M%S'
                        fmt = '%Y%m%d'
                        output_dir_name = None
                        if article_alias:
                            output_dir_name = 'bbs_{}_{}'.format(datetime.datetime.now().strftime(fmt), article_alias)
                        else:
                            output_dir_name = 'bbs_{}'.format(datetime.datetime.now().strftime(fmt))
                        file_name = self.__network.write_to_file_with_multiple(url,
                                                                               'bbs',
                                                                               'html',
                                                                               output_dir_name=output_dir_name,
                                                                               index=index)
                        # random_value = 500 + random.random() * 100 + random.random() * 1000
                        random_value = 1.0 + random.random()
                        time.sleep(random_value)
                        logging.debug('the current task union-id({}) sleep that is {:.3f}s'.format(url, random_value))
                        if self.__flag and file_name:
                            self._on_callback_with_ps(os.path.basename(file_name))

    def _on_callback_with_ps(self, file_name_only):
        self.__pmds.set_file_name(file_name_only).local_to_json(
            self.__flag,
            _on_item_callback=lambda args0, args1: logging.debug('the task({} -> {}) has executed successfully.'.format(
                args0, args1)),
            _on_callback=lambda: logging.debug('the task({}) has executed successfully.'.format('local to json')))


def __onDestinationDirectoryCallback():
    dvs_dd = None
    user = os.path.expanduser('~')
    dvs_rc = os.path.join(user, ENVIRONMENT_VARIABLE_CONFIGURATION)
    if os.path.exists(dvs_rc):
        dvs_cfg = Configuration().obtain_config(dvs_rc)
        dvs_dd = dvs_cfg.get('dvs-default-output-directory', tempfile.mkdtemp(prefix='dvs-sniffer-'))
        logging.info('the currently found user({}) environment variable definition configuration file.'.format(user))
    return dvs_dd


def execute(args=None):
    '''
        the execute command

        it is that reference link:

            1. https://docs.python.org/zh-cn/3/library/argparse.html
            2. https://docs.python.org/zh-cn/2/library/argparse.html
    '''
    if args is None:
        args = sys.argv[1:]
    ILogging().set_logging()
    parser = argparse.ArgumentParser(
        prog='dvs-sniffer',
        description="""

    this is a dvs network sniffer execution program.

    the sniffer destination url format must conform to the following continuous URLs:

        eg:

            1. http://bbs.xxx.cn/list-xyz-1.shtml
            2. http://bbs.xxx.cn/list-xyz-2.shtml
            3. http://bbs.xxx.cn/list-xyz-3.shtml
            4. ...
            5. http://bbs.xxx.cn/list-xyz-{}.shtml
        """,
        epilog='the copyright belongs to DovSnier that reserve the right of final interpretation.\n',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version=VERSIONS, help='the show version and exit.')
    parser.add_argument(
        'url',
        action='store',
        nargs=1,
        type=str,
        metavar='sn-url',
        # dest='url',
        help='the sniffer destination url.')
    parser.add_argument('-dd',
                        '--destination_directory',
                        action='store',
                        nargs='?',
                        const=tempfile.mkdtemp(prefix='dvs-sniffer-'),
                        default=__onDestinationDirectoryCallback(),
                        type=str,
                        metavar='destination-directory',
                        dest='destination_directory',
                        help='the sniffer destination directory.')
    parser.add_argument(
        '-amp',
        '--article-multi-media-persistence',
        action='store_false',
        default=True,
        dest='article_multi_media_persistence',
        help='if True: multi media resources are stored locally, otherwise they are not, and the default value is True.'
    )
    parser.add_argument(
        '-amq',
        '--article-multi-media-quality',
        action='store_true',
        default=False,
        dest='article_multi_media_quality',
        help='if True: multi media resources are high quality, otherwise they are not, and the default value is False.')
    parser.add_argument('-a2',
                        '--article-alias',
                        action='store',
                        nargs='?',
                        const=datetime.datetime.now().strftime('article_%H%M_%S'),
                        default=datetime.datetime.now().strftime('article_%H%M_%S'),
                        type=str,
                        metavar='article-alias',
                        dest='article_alias',
                        help='a short text article alias of the sniffer to be.')
    parser.add_argument('-ad',
                        '--article-describe',
                        action='store',
                        nargs='?',
                        const='',
                        default='',
                        type=str,
                        metavar='article-describe',
                        dest='article_describe',
                        help='a short text article description of the sniffer to be.')
    parser.add_argument('-af',
                        '--article-flag',
                        action='store_false',
                        default=True,
                        dest='article_flag',
                        help='''
        if False: first pull, second translate True: one pull after another translate, and the default value is True.
            ''')
    parser.add_argument('-rs',
                        '--region-start',
                        action='store',
                        nargs='?',
                        const=0,
                        default=0,
                        type=int,
                        metavar='region-start',
                        dest='region_start',
                        help='a briefly describe the range start to be sniffed mathematically.')
    parser.add_argument('-re',
                        '--region-end',
                        action='store',
                        nargs='?',
                        const=1,
                        default=1,
                        type=int,
                        metavar='region-end',
                        dest='region_end',
                        help='a briefly describe the range end to be sniffed mathematically.')
    parser.add_argument('-rm',
                        '--region-mask',
                        action='store',
                        nargs='?',
                        const='REGION_INCLUSIVE_EXCLUSIVE',
                        default='REGION_INCLUSIVE_EXCLUSIVE',
                        choices=[
                            'REGION_INCLUSIVE_EXCLUSIVE',
                            'REGION_EXCLUSIVE_INCLUSIVE',
                            'REGION_EXCLUSIVE_EXCLUSIVE',
                            'REGION_INCLUSIVE_INCLUSIVE',
                        ],
                        type=str,
                        metavar='region-mask',
                        dest='region_mask',
                        help='''
        The olfactory spatial range of the sniffer can only be the following values:

            REGION_INCLUSIVE_EXCLUSIVE = 0,
            REGION_EXCLUSIVE_INCLUSIVE = 1,
            REGION_EXCLUSIVE_EXCLUSIVE = 2,
            REGION_INCLUSIVE_INCLUSIVE = 3,
            and the default value is REGION_INCLUSIVE_EXCLUSIVE.
        ''')
    parser.add_argument(
        '-due',
        '--destination-uuid-encryptor',
        action='store_false',
        # nargs=1,
        default=True,
        # type=bool,
        # metavar='destination-uuid-encryptor',
        dest='destination_uuid_encryptor',
        help='the sniffer destination uuid encryptor, and the default value is True.')
    parser.add_argument(
        '-ua',
        '--user-agent',
        action='store',
        nargs='?',
        const='User-Agent: ' +
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        default='User-Agent: ' +
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        type=str,
        metavar='User-Agent',
        dest='user_agent',
        help='''
        the user agent flag of set sniffer for default network access, which is the macintosh system identifier by default.
        ''')
    args = parser.parse_args(args)
    run(args)


def run(args):
    ''' the run script command '''
    if args:
        if args.url and '{}' not in args.url[0]:
            pattern = re.compile(r'\-\d+')
            url_match = re.search(pattern, args.url[0])
            if not url_match:
                logging.error('the note: the currently provided link({}) does not meet the format requirements.'.format(
                    args.url[0]))
            value = args.url[0][0:args.url[0].rfind('-')] + '-{}' + args.url[0][args.url[0].rfind('.'):]
            args.url.append(value)
    if DEBUGGER:
        # print('vars(args): {}'.format(vars(args)))
        logging.warning('the current config(args): {}'.format(json.dumps(vars(args), indent=4)))
    Crawler_Bbs_TianYa(args=args).set_flag(args.article_flag).run()


if __name__ == "__main__":
    '''the main function entry'''
    execute()
