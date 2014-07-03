from ThreeDCart.api.resources import ResourceObject
from ThreeDCart.api.lib.mapping import Mapping
from ThreeDCart.api.resources.Order import Order

import logging
log = logging.getLogger('Orders')

class Orders(ResourceObject):
    can_enumerate = True
    getOperation = "getOrder"
    countOperation = "getOrderCount"
    
    fields = {
        'sku':{'cart_field':'id','type':'string'},
        'id':{'cart_field':'id','type':'string'},
        'inventory_level':{'cart_field':'stock', 'type':'int'},
        'option_count':{'cart_field':'option_count', 'type':'int'},
        'name':{'cart_field':'name', 'type':'string'},
        'update':{'cart_field':'last_update', 'type':'string'},
        'catalogid':{'cart_field':'catalogid','type':'string'}
    }
    

    def get(self, id):
        return Product(connection=self._connection).get(id)

    def enumerate(self, batchSize=5, startNum=1, query={}): # batchSize=100 is max per batch
        resources = self._connection.get_orders(startNum, batchSize, query)
        if not isinstance(resources, list):
            resources = [resources]
        result = []
        
        for resource in resources:
            yield resource
        
        
        
        

    def count(self):
        if self.countOperation:
            try:
                result = int(self._connection.execute(self.countOperation).GetProductCountResponse.ProductQuantity)
                return result
            except:
                return None
        return None

