from ThreeDCart.api.resources import ResourceObject
from ThreeDCart.api.lib.mapping import Mapping
from ThreeDCart.api.resources.Product import Product

import logging
log = logging.getLogger('Products')

class Products(ResourceObject):
    can_enumerate = True
    getOperation = "getProduct"
    countOperation = "getProductCount"
    """
    fields = {
        'sku':{'cart_field':'ProductID','type':'string'},
        'inventory_level':{'cart_field':'Stock', 'type':'int'},
        'name':{'cart_field':'ProductName', 'type':'string'},
        'catalogid':{'cart_field':'CatalogID', 'type':'string'},
        'id':{'cart_field':'ProductID','type':'string'}
    }
    """
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
        products = self._connection.get_products(batchSize, startNum, query)
        if not isinstance(products, list):
            products = [products]
        result = []
        
        for product in products:
            product_ = Product(connection=self._connection)
            for k,v in self.fields.items():
                if v['type']=='int':
                    setattr(product_, k,int(getattr(product,v['cart_field'])))
                else:
                    setattr(product_, k, getattr(product,v['cart_field']))
            yield product_
        

    def count(self):
        if self.countOperation:
            try:
                result = int(self._connection.execute(self.countOperation).GetProductCountResponse.ProductQuantity)
                return result
            except:
                return None
        return None

