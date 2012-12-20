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
        'id':{'cart_field':'ProductID','type':'string'}
        }

    def __init__(self, connection, advConnection, inventory_level=None, sku=None, id=None, name=None):
        self._connection = connection
        self._advConnection = advConnection
        self.inventory_level = inventory_level
        self.sku = sku
        self.skus = []
        self.id = id
        self.name = name
        self.advOption = False

    def get(self, id):

        if self.getOperation:
            try:
                product = self._connection.execute(self.getOperation, batchSize=1, startNum=1, productId=id).GetProductDetailsResponse.Product
            except Exception, e:
                # Check to see if this is an adv option product
                product = None
                try:
                    option = self._advConnection.execute('runQuery',sqlStatement='SELECT * FROM options_Advanced WHERE AO_Sufix="%s"' % id).runQueryResponse.runQueryRecord
                    log.debug('adv option product')
                    self.id = str(option.AO_Sufix)
                    self.sku = self.id
                    self.name = str(option.AO_Name)
                    self.inventory_level = int(option.AO_Stock)
                    self.advOption = True
                except Exception, e:
                    log.exception(e.message)
                    return None

            if product:
                for k,v in self.fields.items():
                    log.debug('%s = %s' % (v['cart_field'], getattr(product,v['cart_field'])))
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

        if self.advOption:
            result = self._advConnection.execute("runQuery", sqlStatement="UPDATE options_Advanced SET AO_Stock=%s WHERE AO_Sufix='%s'" % (self.inventory_level, self.id))
            log.debug('adv save results:')
            log.debug(result)
            log.debug(dir(result))
            result = self.inventory_level
        else:
            result = self._connection.execute(self.updateOperation, productId=self.sku, quantity=self.inventory_level, replaceStock=True).UpdateInventoryResponse.NewInventory

        self.inventory_level = int(result)

        return result

