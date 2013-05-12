"""
Connection Module

Handles put and get operations to the ThreeDCart SOAP API
"""
import logging
from datetime import datetime, timedelta
from suds.client import Client
 
log = logging.getLogger("3dCart.conn")

base_url  = 'http://api.3dcart.com/cart.asmx?WSDL'
adv_base_url = 'http://api.3dcart.com/cart_advanced.asmx?wsdl'



class Connection(object):
    """
    Handles client calls
    """
    def __init__(self, store_url, token):
        self.store_url = store_url
        self.token = token
        self.__client = Client(base_url)
        self.__sql_client = Client(adv_base_url)
        
        
    def execute_sql(self, query):
        """
        Executes the command and returns the results
        """
        result = {}
        log.debug('Executing runQuery')
        try:
            op = getattr(self.__sql_client.service, 'runQuery')
        except Exception, e:
            log.exception(e.message)
            raise Exception("No command named 'runQuery' (Error: %s)." % (e.message))

        try:
            log.debug("Query %s" % query)
            result = op(storeUrl=self.store_url, userKey=self.token, sqlStatement=query).runQueryResponse

        except Exception, e:
            log.exception(e.message)
            raise Exception("Could not get results for command named 'runQuery' (Error: %s)." % (e.message))

        return result



    def execute(self, operation, **kwargs):
        """
        Executes the command and returns the results
        """
        result = {}
        log.debug('Executing operation %s...' % operation)
        try:
            op = getattr(self.__client.service, operation)
        except Exception, e:
            log.exception(e.message)
            raise Exception("No command named '%s' (Error: %s)." % (operation, e.message))

        try:
            log.debug('kwargs: %s' % kwargs)
            result = op(storeUrl=self.store_url, userKey=self.token, **kwargs)

        except Exception, e:
            log.exception(e.message)
            raise Exception("Could not get results for command named '%s' (Error: %s)." % (operation, e.message))
        return result
    
    

    def get_db_type(self):
        """
        Run a bogus query and check the DB Type based on the error message generated
        """
        log.info("Discovering 3dCart DB Type")
        result = self.execute_sql("Select Top 1 id from xxxxxxxxxxx")
        description = result.Error.Description
        log.info("Message '%s'" % description)
        
        if description.find("Microsoft") > 0:
            return "Access"
        else:
            return "SQL"
            


class Adapter(object):
    
    def __init__(self, connection):
        log.info("Using %s" % self.__class__.__name__)
        self._connection = connection
        self._timezone = self.get_timezone()
        
    def transport(self):
        return self._connection    
    
    def get_timezone(self):
        result = self._connection.execute_sql("SELECT varvalue FROM store_settings2 WHERE varname Like 'time_zone'")
        tz = int(result.runQueryRecord.varvalue)
        log.info("Server Timezone is %d" % tz)
        return tz
    
    
    def get_product(self, id):
        try:
            return self._connection.execute("getProduct", batchSize=1, startNum=1, productId=id).GetProductDetailsResponse.Product
        except:
            log.exception("Unable to get product %s" % id)
            raise
        
    
    def get_products(self, start, limit, query={}):
        pass
    
    
    def get_subproducts(self, id):
        query = "SELECT * FROM options_Advanced WHERE ProductID=%s" % id
        result = self._connection.execute_sql(query)
        try:
            return result.runQueryRecord
        except:
            #log.error("Error in %s" % query)
            #log.error("Response %s" % result)
            return []
    
        
    def get_subproduct(self, id, sku):
        query = "SELECT * FROM options_Advanced WHERE ProductID=%s AND AO_Sufix='%s'" % (id, sku)
        result = self._connection.execute_sql(query)
        try:
            return result.runQueryRecord
        except:
            #log.error("Error in %s" % query)
            #log.error("Response %s" % result)
            return None
        
    def update_stock_option(self, sku, qty):
        query = "UPDATE options_Advanced SET AO_Stock=%s WHERE AO_Sufix='%s'" % (qty, sku)
        result = self._connection.execute_sql(query)
        try:
            return result.runQueryRecord
        except:
            #log.error("Error in %s" % query)
            #log.error("Response %s" % result)
            return None

    def update_product(self, id, qty, replace=False):
        return self._connection.execute('updateProductInventory', productId=id, quantity=qty, replaceStock=replace).UpdateInventoryResponse.NewInventory



class SQLAdapter(Adapter):
    
    def get_products(self, limit, start, query={}):
        
        where = ""
        format = "%m/%d/%Y %H:%M:%S"
        if query.has_key("last_update") and query["last_update"]:
            local_time = query["last_update"] + timedelta(hours=self._timezone)
            log.info("Datetime UTC %s - Local: %s" % (query["last_update"].strftime(format), local_time.strftime(format)))
            where = "last_update > '%s'" % (local_time.strftime(format))
        
        # Get product count
        count_query = "SELECT Count(*) as count FROM products %s" % ("where %s" % where if where else "")
        result = self._connection.execute_sql(count_query)
        count = int(result.runQueryRecord.count)
        
        log.info("Count %d - first %d" % (count, (start) ))
        if count < (start):
            raise EOFError
                      
        query = """SELECT Top %d * 
                    From (select count(options_Advanced.AO_Sufix) as option_count, ROW_NUMBER() OVER (ORDER BY products.id) rn, products.id, last_update, stock, name, catalogid FROM products 
                    left join options_Advanced on products.catalogid = options_Advanced.ProductID group by products.id, stock, catalogid, last_update, name) t 
                    where rn > %d and %s""" % (limit, start - 1, where)
        log.debug("Query: %s" % query)
        
        result = self._connection.execute_sql(query)
        return result.runQueryRecord
        
        
        
        
class AccessAdapter(Adapter):
        
    def get_products(self, limit, start, query={}):
        
        where = ""
        format = "%m/%d/%Y %H:%M:%S"
        if query.has_key("last_update") and query["last_update"]:
            local_time = query["last_update"] + timedelta(hours=self._timezone)
            log.info("Datetime UTC %s - Local: %s" % (query["last_update"].strftime(format), local_time.strftime(format)))
            where = "Where last_update > #%s#" % (local_time.strftime(format))
        
        # Get product count
        count_query = "SELECT Count(*) as items FROM products %s" % (where)
        result = self._connection.execute_sql(count_query)
        count = int(result.runQueryRecord.items)
        
        log.info("Count %d - first %d" % (count, (start) ))
        if count < (start):
            raise EOFError
        
        query = """Select top %d count(options_Advanced.AO_Sufix) as option_count, tbl.id, last_update, stock, name, catalogid 
                      From [Select Top %d * from products %s order by products.id DESC;]. as tbl 
                      left join options_Advanced on tbl.catalogid = options_Advanced.ProductID
                      group by products.id, stock, catalogid, last_update, name 
                      order by products.id""" % (limit, count - start + 1, where)
        log.debug("Query: %s" % query)
        
        result = self._connection.execute_sql(query)
        return result.runQueryRecord
        



def Connect(store_url, token):
    """
    Connection class manages the connection to the ThreeDCart SOAP API.
    """
    log.debug("Getting connection")
    connection = Connection(store_url, token)
    if connection.get_db_type() == "Access":
        return AccessAdapter(connection)
    else:
        return SQLAdapter(connection)
        
 