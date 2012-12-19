from ThreeDCart.api.resources import ResourceObject
import logging
log = logging.getLogger('ProductInventory')

class ProductInventory(ResourceObject):
    can_enumerate = False
    getOperation = "getProductInventory"
    updateOperation = "updateProductInventory"

    def get(self, id):
        if self.getOperation:
            try:
                return int(self._connection.execute(self.getOperation, productId=id).GetInventoryResponse.Inventory)
            except:
                return None
        return None

    def update(self, *args, **kwargs):
        if self.updateOperation:
            if len(args)>0:
                kwargs.update({'productId':args[0]})
            if len(args)>1:
                kwargs.update({'quantity':args[1]})
            if len(args)>2:
                kwargs.update({'replaceStock':args[2]})

            if kwargs.has_key('id'):
                kwargs.update({'productId':kwargs['id']})

            if not kwargs.has_key('replaceStock'):
                kwargs.update({'replaceStock':False})

            valid_keys = ['productId','quantity','replaceStock']
            for key in kwargs.keys():
                if not key in valid_keys:
                    del(kwargs[key])

            try:
                result = int(self._connection.execute(self.updateOperation, **kwargs).UpdateInventoryResponse.NewInventory)
                return result
            except:
                return None
