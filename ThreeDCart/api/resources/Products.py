from ThreeDCart.api.resources import ResourceObject
from ThreeDCart.api.lib.mapping import Mapping
from ThreeDCart.api.resources.Product import Product

import logging
log = logging.getLogger('Products')

class Products(ResourceObject):
    can_enumerate = True
    getOperation = "getProduct"
    countOperation = "getProductCount"
    fields = {
        'sku':{'cart_field':'ProductID','type':'string'},
        'inventory_level':{'cart_field':'Stock', 'type':'int'},
        'id':{'cart_field':'CatalogID','type':'string'}
    }

    def get(self, id):
        return Product(connection=self._connection).get(id)

    def enumerate(self, batchSize=100, startNum=1): # batchSize=100 is max per batch
        if self.getOperation:
            try:

                products = self._connection.execute(self.getOperation, startNum=startNum, batchSize=batchSize).GetProductDetailsResponse.Product
                result = []
                for product in products:
                    product_ = Product(connection=self._connection)
                    for k,v in self.fields.items():
                        if v['type']=='int':
                            setattr(product_, k,int(getattr(product,v['cart_field'])))
                        else:
                            setattr(product_, k, getattr(product,v['cart_field']))
                    result.append(product_)

                return result
            except Exception, e:
                log.exception(e.message)
        return None

    def count(self):
        if self.countOperation:
            try:
                result = int(self._connection.execute(self.countOperation).GetProductCountResponse.ProductQuantity)
                return result
            except:
                return None
        return None

