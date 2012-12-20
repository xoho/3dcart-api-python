import os
import sys
import base64
import logging

from ThreeDCart.api.lib.connection import Connection
from resources import ResourceAccessor

log = logging.getLogger("3dCart.apiClient")


class ApiClient(object):
    base_url  = 'http://api.3dcart.com/cart.asmx?WSDL'
    adv_base_url = 'http://api.3dcart.com/cart_advanced.asmx?wsdl'
    
    def __init__(self, host, token, user_id): # user_id is ignored - provided only for library compatibility
        self._connection = Connection(self.base_url, host, token)
        self._advConnection = Connection(self.adv_base_url, host, token)

    def connection(self):
        pass
    
    def get_url_registry(self):
        return self._connection.meta_data()
        
    def __getattr__(self, attrname):
        try:
            return ResourceAccessor(attrname, self._connection, self._advConnection)
        except:
            raise AttributeError
        raise AttributeError
            