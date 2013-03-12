import sys
import logging
#from ThreeDCart.api.lib.mapping import Mapping
from ThreeDCart.api.lib.filters import FilterSet

log = logging.getLogger("3dcart.api")


class ResourceAccessor(object):
    """
    Provides methods that will create, get, and enumerate resourcesObjects.
    """
    
    def __init__(self, resource_name, connection, advConnection):
        """
        Constructor
        
        @param resource_name: The name of the resource being accessed.  There must be a
                              corresponding ResourceObject class
        @type resource_name: String
        @param connection: Connection to the bigCommerce SOAP API
        @type connection: {Connection}
        """
        self._parent = None
        self.__resource_name = resource_name
        self._connection = connection
        self._advConnection = advConnection
        
        try:
            mod = __import__('%s' % resource_name, globals(), locals(), [resource_name], -1)
            self._klass = getattr(mod, resource_name)(self._connection, self._advConnection)
        except:
            log.exception("ETRR")
            self._klass = ResourceObject(self._connection, self._advConnection)
            
    def enumerate(self, start=0, limit=0, query={}):
        """
        Enumerate resources
        
        @param start: The instance to start on
        @type start: int
        @param limit: The number of items to return - Set to 0 to return all items
        @type limit: int
        @param max_per_page: Number of items to return per request
        @type max_per_page: int
        @param query: not used, but included for compatibility
        @type query: dict
        """
        
        remaining = requested_items = limit if limit else sys.maxint
        batchSize = max(1, min(limit, 100)) # keep > 0 but less than 100
        startNum = max(0, start) # keep it positive
        
        
        # 3dCart is 1's based
        startNum += 1
        
        if self._klass.can_enumerate:
            while remaining > 0:
                batchSize = max(1, min(remaining, 100))
                try:
                    for res in self._klass.enumerate(batchSize=batchSize, startNum=startNum):
                        remaining -= 1
                        yield res
                except:
                    remaining = 0
                startNum += batchSize
        else:
            yield None

    def get(self, id):
        return self._klass.get(id)
        try:
            return self._klass.get(id)
        except:
            return None

    def update(self, *args, **kwargs):
        try:
            return self._klass.update(*args, **kwargs)
        except:
            return None

    def get_count(self):
        try:
            return self._klass.count()
        except Exception, e:
            return None


    def get_name(self):
        return self.__resource_name

    name = property(fget=get_name)

class ResourceObject(object):
    """
    The realized resource instance type.
    """
    can_enumerate = False   # can enumerate
    getOperation = None     # the "get" operation
    updateOperation = None  # the "update" operation - if None, cannot perform updates
    countOperation = None   # the "count" operation - if None, cannot count
    
    def __init__(self, connection, advConnection):
        self._connection = connection
        self._advConnection = advConnection

    def get(self, **kwargs):
        if self.getOperation:
            return self._connection.execute(self.getOperation, **kwargs)
        return None

    def enumerate(self, **kwargs):
        if self.getOperation:
            for item in self._connection.execute(self.getOperation, **kwargs):
                yield item
        else:
            yield None

    def count(self):
        if self.countOperation:
            return self._connection.execute(self.countOperation)
        return None

    def update(self, **kwargs):
        if self.updateOperation:
            return self._connection.execute(self.updateOperation, **kwargs)
        return None


