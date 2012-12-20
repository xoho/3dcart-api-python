import logging

# Debug logging settings
logging.getLogger().setLevel(logging.DEBUG)
#for func in ['ProductInventory','Products']:
#    logging.getLogger(func).setLevel(logging.DEBUG)

# Error only logging settings
for func in [
    #'Product',
    '3dCart.conn',
    'suds.client',
    'suds.transport.http',
    'suds.mx.literal',
    'suds.mx.core',
    'suds.xsd.schema',
    'suds.metrics',
    'suds.xsd.sxbase',
    'suds.xsd.query',
    'suds.wsdl',
    'suds.xsd.sxbasic',
    'suds.resolver',
    'suds.umx.typed'
    ]:
    logging.getLogger(func).setLevel(logging.ERROR)
