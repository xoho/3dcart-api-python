STORE_URL = "3dcart store url"# found in Settings->General->Store Settings (towards the bottom) or at top right of admin page
STORE_TOKEN = "the API User key" #found in Settings->General->Module Settings
STORE_USER = "BogusUserId" # is not used by 3dCart but is included here for compatibility with other libraries

try:
    import dev_settings
    STORE_URL = dev_settings.STORE_URL
    STORE_TOKEN = dev_settings.STORE_TOKEN
    STORE_USER = dev_settings.STORE_USER
except:
    pass

import sys
import logging
from pprint import pprint
from ThreeDCart.api import ApiClient

logging.basicConfig(level=logging.DEBUG, 
                    stream=sys.stdout,
                    format='%(asctime)s %(levelname)-8s[%(name)s] %(message)s',
                    datefmt='%m/%d %H:%M:%S')
log = logging.getLogger("main")

if __name__ == "__main__":
    log.debug("HOST %s" % (STORE_URL))
    api = ApiClient(STORE_URL, STORE_TOKEN, STORE_USER)

    all_tests = ['inventory','product_count','all_products','limited_products','update_inventory','get_product','inventory_products','update_product_inventory','add_five_to_all']
    #tests = ['update_inventory','inventory_products']
    #tests = ['update_product_inventory']
    #tests = ['inventory']
    tests = ['get_2_products','add_five_to_all']
    #tests = all_tests

    sku = 'APPLE-BLUE'
    id = 8

    test = "inventory"
    if test in tests:
        log.debug('')
        log.debug('running %s...' % test)

        # Get inventory for a product
        log.debug('Product inventory for %s: %s' % (id, api.Product.get(id).inventory_level ))


    test = "product_count"
    if test in tests:
        log.debug('')
        log.debug('running %s...' % test)
        # Get count of products
        log.debug("Count of products for this store:%s" % api.Products.get_count())

    test = "all_products"
    if test in tests:
        log.debug('')
        log.debug('running %s...' % test)
        # Get Products
        log.debug('Getting all products...')
        for product in api.Products.enumerate():
            log.debug("Product: name: %s, sku: %s, id: %s, inventory_level: %s" % (product.name, product.sku, product.id, product.inventory_level))


    test = "limited_products"
    if test in tests:
        log.debug('')
        log.debug('running %s...' % test)
        # Get a limited set of products
        log.debug('Getting limited set of products...')
        for product in api.Products.enumerate(start=0, limit=2):
            log.debug("Product: %s" % product.sku)


    test = "get_2_products"
    if test in tests:
        log.debug('')
        log.debug('running %s...' % test)
        # Get a product
        id_ = sku
        log.debug('Get product %s' % id_)
        product = api.Products.get(id_)
        log.debug('Product: name: %s, sku: %s, id:%s, inventory_level:%s' % (product.name, product.sku, product.id, product.inventory_level))
        id_ = 'PUREFIF'
        log.debug('Get product %s' % id_)
        product = api.Products.get(id_)
        log.debug('Product: name: %s, sku: %s, id:%s, inventory_level:%s' % (product.name, product.sku, product.id, product.inventory_level))



    test = "get_product"
    if test in tests:
        log.debug('')
        log.debug('running %s...' % test)
        # Get a product
        log.debug('Get product %s' % id)
        product = api.Products.get(id)
        log.debug('Product: name: %s, sku: %s, id:%s, inventory_level:%s' % (product.name, product.sku, product.id, product.inventory_level))

    test = "update_product_inventory"
    if test in tests:
        log.debug('')
        log.debug('running %s...' % test)
        # Update's one product inventory
        log.debug('Get product %s' % id)
        product = api.Products.get(id)
        log.debug('Product: sku: %s, id:%s, start inventory_level:%s' % (product.sku, product.id, product.inventory_level))
        product.inventory_level += 5
        product.save()
        log.debug('Product: sku: %s, id:%s, added inventory_level:%s' % (product.sku, product.id, product.inventory_level))
        product.inventory_level -= 7
        product.save()
        log.debug('Product: sku: %s, id:%s, subtracted inventory_level:%s' % (product.sku, product.id, product.inventory_level))



    test = "update_inventory"
    if test in tests:
        log.debug('')
        log.debug('running %s...' % test)
        # Update inventory
        # uses the ProductInventory object -
        log.debug('Starting inventory level for %s: %s' % (sku, api.ProductInventory.get(sku)))
        qty=33
        api.ProductInventory.update(sku, qty)
        log.debug('New inventory level for %s (adding %s): %s' % (sku, qty, api.ProductInventory.get(sku)))
        api.ProductInventory.update(id=sku, quantity=-qty)
        log.debug('New inventory level for %s (subtracting %s): %s' % (sku, qty, api.ProductInventory.get(sku)))



    test = "inventory_products"
    if test in tests:
        log.debug('')
        log.debug('running %s...' % test)
        # Gets the invnentories for the list of products
        for product in api.Products.enumerate():
            log.debug('Product %s has %s items' % (product.sku, api.ProductInventory.get(product.sku)))


    test = "add_five_to_all"
    if test in tests:
        log.debug('')
        log.debug('running %s...' % test)
        # Gets the invnentories for the list of products
        for product in api.Products.enumerate():
            log.debug('Product: sku: %s, id: %s, inventory_level: %s (original)' % (product.sku, product.id, product.inventory_level))
            product.inventory_level += 5
            product.save()

        for product in api.Products.enumerate():
            log.debug('Product: sku: %s, id: %s, inventory_level: %s (final)' % (product.sku, product.id, product.inventory_level))
