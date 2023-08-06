import json
import unittest
import threading
from gadgethiServerUtils.file_basics import *
from gadgethiServerUtils.GadgethiServer import *
from gadgethiServerUtils.GadgethiClient import *

def _initialize_order():
    """
    Init the database and create table.
    order_table -> log table
    """
    # , receipt text, taxID text, print_flag text, xml_flag text, RandomNumber text, staytime int, age text, gender text, ordertime int, payment_method text,
    # , isdelivery text, sales_item text, waittime int, buyer_address text, buyer_PersonInCharge text, buyer_TelephoneNumber text, buyer_FacsimileNumber text, buyer_EmailAddress text, buyer_CustomerNumber text, buyer_RoleRemark text, CheckNumber text, BuyerRemark text, MainRemark text, CustomsClearanceMark text, Category text, RelateNumber text, InvoiceType text, GroupMark text, DonateMark text, CarrierType text, CarrierId1 text, CarrierId2 text, PrintMark text,
    init_order = '''CREATE TABLE IF NOT EXISTS public.order_table (_id SERIAL PRIMARY KEY , 
    order_id text, order_no text, store_id text, serial_number text, username text, name1 text,
    name2 text, name3with4 text, stayortogo text, name5 text, amount int, price text, discount int, final_price int, total_price int, 
    payment_method text, receipt_number text, status text, promotion text,
    promotion_key text, order_time int, print_flag text, xml_flag text,
    comment1 text, comment2 text, comment3 text, comment4 text, comment5 text, 
    comment6 text, comment7 text, comment8 text, time int);'''
    executeSql(getDb(), init_order, None, db_operations.MODE_DB_NORMAL)

def _initialize_promotion():

    init_promotion = '''CREATE TABLE IF NOT EXISTS public.promotion_table (_id SERIAL PRIMARY KEY , 
    specific_promotion_key text, usage_amount int,promotion_key text, time int);'''
    executeSql(getDb(), init_promotion, None, db_operations.MODE_DB_NORMAL)

class GServerTests(unittest.TestCase):
    """
    Testing Strategy
    
    @ GServer
    - constructor:
        partition on table_list: length 0, >0
        partition on initialized_func_list: length 0, >0
        partition on desc: string length 0, >0
        partition on yaml_exccondition returns: all True, all False, some True some False
        partition on configs: empty dictionary, keys > 0
        partition on service_handler: Normal return true, normal return false, exception
        partition on config_path: file exists, file not exists
        partition on credential_path: file exists, file not exists
        partition on custom_event_handler: None, Normal return true, normal return false, exception
        partition on fetch_yaml_from_s3: True, False
        partition on authentication: True, False

    - handling:
        partition on HTTP types: GET, POST, OPTIONS, PUT
        partition on authentication: with auth header, without auth header
        partition on event handler type: custom event handler, gadgethi service handler
        partition on POST application types: json, urlencode, raw

    @GClient
    - constructor:
        partition on input kwargs: with '_http_url' string, without http_url string    

    - client_get:
        partition on key: key exists, key not exists
        partition on input_dict: empty, keys > 0, input_dict key type not string
        partition on timeout status: timeout, not timeout
        partition on gauth: True, False

    - client_post:
        partition on key: key exists, key not exists
        partition on input_dict: empty, keys > 0, input_dict key type not string
        partition on timeout status: timeout, not timeout
        partition on gauth: True, False
        partition on urlencode: True, False

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_server_instance(table_list = ["order_table", "promotion_table"],
          initialize_func_list=[_initialize_order, _initialize_promotion], 
          desc="GadgetHi Main", 
          yaml_exccondition=lambda: False, 
          configs={"dblock": 100}, 
          service_handler=None, 
          config_path=os.path.abspath(os.path.join(default_gserver_location, "config/config.yaml")),
          credential_path=os.path.abspath(os.path.join(default_gserver_location, "credentials.yaml")),
          authentication=True,
          custom_event_handler=lambda self, d, **kwargs: {"indicator":True, "message": "test success"},
          fetch_yaml_from_s3=False)

    def start_server_instance(self, **kwargs):
        """
        Run the actual threading test.
        Args:
            kwargs: all necessary kwargs for gadgethi server
        """
        server = GadgetHiServer(**kwargs)

        def start_and_init_server():
            """A helper function to start out server in a thread.
            This could be done as a lambda function, but this way we can
            perform other setup functions if necessary.
            """
            # Context manager to get rid of the unclosed warning
            with server as test_server:
                test_server.run()

        def shutdown_server():
            """
            function to shutdown the server. 
            """
            server.shutdown()

        self.server_thread = threading.Thread(target=start_and_init_server)
        self.shutdown_function = shutdown_server

        try:
            # Start the server
            self.server_thread.start()
        except Exception as e:
            print('Something went horribly wrong!', e)

    def test_http_authentication_header(self):
        client = GadgetHiClient(test_http_url="http://127.0.0.1:5050")

        self.assertTrue(json.loads(client.client_post("test_http_url", {"service": "order"}, gauth=True))["indicator"])
        self.assertTrue(json.loads(client.client_post("test_http_url", {"service": "order"}, gauth=True, urlencode=True))["indicator"])
        self.assertTrue(json.loads(client.client_post("test_http_url", {"service": "order"}, gauth=True, urlencode=True, 
            custom_headers={"custom_headers": "YAS!"}))["indicator"])

        self.assertTrue(json.loads(client.client_get("test_http_url", {"service": "order"}, gauth=True))["indicator"])
        self.assertTrue(json.loads(client.client_get("test_http_url", {"service": "order"}, gauth=True))["indicator"])
        self.assertTrue(json.loads(client.client_get("test_http_url", {"service": "order"}, gauth=True, 
            custom_headers={"custom_headers": "YAS!"}))["indicator"])

        self.shutdown_function()

