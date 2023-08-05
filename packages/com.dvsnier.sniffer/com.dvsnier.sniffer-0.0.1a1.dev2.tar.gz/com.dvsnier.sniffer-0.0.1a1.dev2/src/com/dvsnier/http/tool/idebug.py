# -*- coding:utf-8 -*-


class IDebug(object):
    '''the attribute class'''

    __DEBUG = False

    def __init__(self):
        super(IDebug, self).__init__()

    def is_debug(self):
        'the has inner debug'
        return self.__DEBUG

    def set_debug(self, debug, _on_debug_callback=None):
        'the set inner debug'
        self.__DEBUG = debug
        if _on_debug_callback:
            _on_debug_callback(self.__DEBUG)
        return self


DEBUG = IDebug()
