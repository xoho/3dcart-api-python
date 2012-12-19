import logging
log = logging.getLogger('Product')

class Product(object):
    can_enumerate = False
    getOperation = "getProduct"
    updateOperation = "updateProductInventory"

    fields = {
        'sku':{'cart_field':'ProductID','type':'string'},
        'inventory_level':{'cart_field':'Stock', 'type':'int'},
        'name':{'cart_field':'ProductName', 'type':'string'},
        'id':{'cart_field':'CatalogID','type':'string'}
        }

    def __init__(self, connection, inventory_level=None, sku=None, id=None, name=None):
        self._connection = connection
        self.inventory_level = inventory_level
        self.sku = sku
        self.skus = []
        self.id = id
        self.name = name

    def get(self, id):

        if self.getOperation:
            try:
                product = self._connection.execute(self.getOperation, batchSize=1, startNum=1, catalogId=id).GetProductDetailsResponse.Product
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

