"""
Connection Module

Handles put and get operations to the ThreeDCart SOAP API
"""
import logging
from suds.client import Client
 
log = logging.getLogger("3dCart.conn")
try:
    import settings
except:
    pass


class Connection():
    """
    Connection class manages the connection to the ThreeDCart SOAP API.
    """
    
    def __init__(self, service_url, store_url, token):
        """
        Constructor
        """
        self.service_url = service_url
        self.store_url = store_url
        self.token = token
        self.__client = Client(self.service_url)

    def meta_data(self):
        """
        Return a string representation of available services
        """
        return self.__client.service.__dict__

    def execute(self, operation, **kwargs):
        """
        Executes the command and returns the results
        """
        result = {}
        log.debug('Executing operation %s...' % operation)
        try:
            op = getattr(self.__client.service, operation)
        except Exception, e:
            log.exception(e.message)
            raise Exception("No command named '%s' (Error: %s)." % (operation, e.message))

        try:
            log.debug('kwargs: %s' % kwargs)
            result = op(storeUrl=self.store_url, userKey=self.token, **kwargs)

        except Exception, e:
            log.exception(e.message)
            raise Exception("Could not get results for command named '%s' (Error: %s)." % (operation, e.message))


        return result

    def __repr__(self):
        return "Connection %s" % self.service_url
