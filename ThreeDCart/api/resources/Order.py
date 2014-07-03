import logging
import sys
log = logging.getLogger('Order')

class Order(object):
    can_enumerate = False
    
    fields = {
        'sku':{'cart_field':'ProductID','type':'string'},
        'inventory_level':{'cart_field':'Stock', 'type':'int'},
        'catalogid':{'cart_field':'CatalogID', 'type':'string'},
        'name':{'cart_field':'ProductName', 'type':'string'},
        'id':{'cart_field':'ProductID','type':'string'}
        }

    def __init__(self, connection, inventory_level=None, sku=None, id=None, name=None):
        self._connection = connection
        self.inventory_level = inventory_level
        self.sku = sku
        self.skus = []
        self.id = id
        self.name = name
        self.advOption = False


    def get(self, id):
        pass
        


    
        
