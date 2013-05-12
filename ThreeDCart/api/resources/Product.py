import logging
import sys
log = logging.getLogger('Product')

class Product(object):
    can_enumerate = False
    getOperation = "getProduct"
    updateOperation = "updateProductInventory"

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
        try:
            product = self._connection.get_product(id)
            # Set the options
            if product:
                for k,v in self.fields.items():
                    log.debug('%s = %s' % (v['cart_field'], getattr(product,v['cart_field'])))
                    if v['type']=='int':
                        setattr(self, k,int(getattr(product,v['cart_field'])))
                    else:
                        setattr(self, k, getattr(product,v['cart_field']))
                setattr(self, "option_count", len(product.Options))
    
            return self
        except:
            log.error("Error getting product %s" % id)
        return None


    def sub_products(self):
        if self.option_count:
             for option in self._connection.get_subproducts(self.catalogid):
                 option_product = Product(connection=self._connection)
                 option_product.catalogid = self.catalogid
                 option_product.id = self.id
                 option_product.sku = option.AO_Sufix
                 option_product.name = option.AO_Name
                 option_product.inventory_level = int(option.AO_Stock)
                 option_product.advOption = True
                 yield option_product
         
        
    def get_subproduct(self, sku):
        product = self._connection.get_subproduct(self.catalogid, sku)
        if product:
            option_product = Product(connection=self._connection)
            option_product.catalogid = self.catalogid
            option_product.id = self.id
            option_product.sku = product.AO_Sufix
            option_product.name = product.AO_Name
            option_product.inventory_level = int(product.AO_Stock)
            option_product.advOption = True
            return option_product
        else:
            return None         
                 
    def save(self):
        # Saves the product inventory
        if not self.sku:
            return None

        if self.advOption:
            #parent = self._advConnection.execute("runQuery", sqlStatement="SELECT * FROM options_Advanced WHERE AO_Sufix='%s'" % (self.id)).runQueryResponse.runQueryRecord
            #parent_sku = self._advConnection.execute("runQuery", sqlStatement="SELECT * FROM products WHERE catalogId=%s" % (parent.ProductID)).runQueryResponse.runQueryRecord
            
            #old_adv = self._advConnection.execute('runQuery',sqlStatement="SELECT AO_Stock FROM options_Advanced WHERE AO_Sufix='%s'" % self.id).runQueryResponse.runQueryRecord
            old_adv = self.get_subproduct(self.sku)
            
            delta = self.inventory_level - int(old_adv.inventory_level)
            log.info("Delta %d" % delta)
            self._connection.update_stock_option(self.sku, self.inventory_level)
            self._connection.update_product(self.id, delta)
            result = self.inventory_level
            
        else:
            result = self._connection.update_product(self.sku, self.inventory_level, replace=True)
        self.inventory_level = int(result)

        return result

    
        
