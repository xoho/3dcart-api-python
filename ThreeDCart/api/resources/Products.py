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
        'name':{'cart_field':'ProductName', 'type':'string'},
        'id':{'cart_field':'ProductID','type':'string'}
    }

    def get(self, id):
        return Product(connection=self._connection, advConnection=self._advConnection).get(id)

    def enumerate(self, batchSize=100, startNum=1): # batchSize=100 is max per batch
        if self.getOperation:
            try:
                products = self._connection.execute(self.getOperation, startNum=startNum, batchSize=batchSize).GetProductDetailsResponse.Product
                result = []
                for product in products:
                    if len(product.Options)>0:
                        # We have options
                        for option in self._advConnection.execute('runQuery',sqlStatement="SELECT * FROM options_Advanced WHERE ProductID=%s" % product.CatalogID).runQueryResponse.runQueryRecord:
                            option_product = Product(connection=self._connection, advConnection=self._advConnection)
                            option_product.id = option.AO_Sufix
                            option_product.sku = option_product.id
                            option_product.name = option.AO_Name
                            option_product.inventory_level = option.AO_Stock
                            option_product.advOption = True
                            result.append(option_product)

                    product_ = Product(connection=self._connection, advConnection=self._advConnection)
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

