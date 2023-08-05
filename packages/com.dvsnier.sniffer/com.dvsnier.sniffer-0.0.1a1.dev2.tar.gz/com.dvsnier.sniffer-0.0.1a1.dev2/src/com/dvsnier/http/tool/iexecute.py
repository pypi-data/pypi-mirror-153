# -*- coding:utf-8 -*-


class IExecute(object):
    '''the execute class'''
    def __init__(self):
        super(IExecute, self).__init__()

    def execute(self, _on_callback=None, *args):
        'the initiative execute task'
        if _on_callback:
            if args:
                _on_callback(*args)
            else:
                _on_callback()

    def invoked(self, _on_callback=None, *args):
        'the passivity invoked task'
        if _on_callback:
            if args:
                _on_callback(*args)
            else:
                _on_callback()
