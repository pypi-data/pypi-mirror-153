# -*- coding:utf-8 -*-

from com.dvsnier.http.synchron.enregistor.ienregistor import IEnregistor


class AbstractEnregistor(IEnregistor, object):
    '''the abstract enregistor class'''
    def __init__(self):
        super(AbstractEnregistor, self).__init__()
