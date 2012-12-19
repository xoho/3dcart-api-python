import logging
log = logging.getLogger('Product')

class Product(object):
    can_enumerate = False
    getOperation = "getProduct"
    updateOperation = "updateProductInventory"

    fields = {
        'sku':{'cart_field':'ProductID','type':'string'},
        'inventory_level':{'cart_field':'Stock', 'type':'int'},
        'id':{'cart_field':'ProductID','type':'string'}
        }

    def __init__(self, connection, inventory_level=None, sku=None, id=None):
        self._connection = connection
        self.inventory_level = inventory_level
        self.sku = sku
        self.skus = []
        self.id = id

    def get(self, productId):
        self.productId = productId
        if self.getOperation:
            try:
                product = self._connection.execute(self.getOperation, productId=productId, batchSize=1, startNum=1).GetProductDetailsResponse.Product
            except Exception, e:
                log.exception(e.message)
                return None

            for k,v in self.fields.items():
                if v['type']=='int':
                    setattr(self, k,int(getattr(product,v['cart_field'])))
                else:
                    setattr(self, k, getattr(product,v['cart_field']))

            return self

        return None

    def save(self):
        # Saves the product inventory
        if not self.sku:
            log.error('No sku was found for this product.')
            return None
        result = self._connection.execute(self.updateOperation, productId=self.sku, quantity=self.inventory_level, replaceStock=True).UpdateInventoryResponse.NewInventory
        self.inventory_level = int(result)

        return result

