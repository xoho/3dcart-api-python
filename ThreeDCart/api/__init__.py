import os
import sys
import base64
import logging

from ThreeDCart.api.lib.connection import Connect
from resources import ResourceAccessor

log = logging.getLogger("3dCart.apiClient")


class ApiClient(object):
    
    def __init__(self, host, token, user_id): # user_id is ignored - provided only for library compatibility
        self._connection = Connect(host, token)

    @property
    def connection(self):
        return self._connection
    
    def get_url_registry(self):
        return self._connection.meta_data()
    
      
    def __getattr__(self, attrname):
        try:
            return ResourceAccessor(attrname, self._connection)
        except:
            raise AttributeError
        raise AttributeError
            
