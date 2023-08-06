import copy

"""
Holds the required configs
for several use cases. 
"""
class GServerConfigs:
    """
    Immutable configs object that stores
    all the default config keys and values
    of basic use case. 
    """
    basic_configs = {
        # The info of the main server
        "server_address": "127.0.0.1",
        "server_port": "5050",

        "log_file_path": "/opt/doday/LOG_FILES/",
        "program_header": "gadgethi-default-server-",

        "server_api_path": "yamls/server_api.yaml",
        "allowed_ip": ["*"],

        "database_name": "gadgethi-database-001",
        "local_database_ini_path": "~/.gserver/database.ini"
    }

    doday_configs = {
        # The info of the websocket server which the main server connects
        "websocket_ip": "127.0.0.1",
        "websocket_port": 9001,
        "websocket_mode": "client",
        # Business Hour
        "opening_time": "10:00",
        "closing_time": "23:50",

        "order_invoice_bucket": "doday-order-invoice",
        "order_invoice_url_header": "https://doday-order-invoice.s3-ap-southeast-1.amazonaws.com/",
        
        # Special hours
        "special_hours":
        [{
            "type": "by-days",
            "arg": [1, []], # [days (monday =1, sunday = 7), index of that day of the month, 
            # e.g. 1st and 3rd monday]
            "hours": {
              "opening_time": "11:30",
              "closing_time": "21:00"
            }
          },
          # just an example, not doing anything now. 
          # by dates have higher priority so need to be later in the list
          {
            "type": "by-dates",
            "arg": [], # [1st of that month]
            "hours": {
              "opening_time": "XX", # write "XX" if not in business that day
              "closing_time": "XX"
            }
          }],
    }

    aws_configs = {
        "s3_bucket_name": "gadgethi-bucket001",
        "fetch_s3_files": ["database_ini/database.ini", "doday_yamls/*"],
        "local_s3_locations": ["~/.gserver/database.ini", "yamls/*"]
    }

    credential_configs = {
        "gadgethi_key": "test",
        "gadgethi_secret": "SECRET"
    }

    def __init__(self, doday_flag=False, aws_flag=True):
        """
        @params doday_flag: attach doday related server configs
        @params aws_flag: attach aws yaml fetch related configs
        """
        configs = {}
        configs.update(self.basic_configs)

        if doday_flag:
            configs.update(self.doday_configs)

        if aws_flag:
            configs.update(self.aws_configs)

        # Use super class to set attributes to bypass
        # the immutable properties. 
        for key in configs.keys():
            super(GServerConfigs, self).__setattr__(key, configs[key])

    def __setattr__(self, key, value):
        """Prevent modification of attributes."""
        raise AttributeError('GServerConfigs cannot be modified')

    @classmethod
    def check_current_configs_match_reqs(cls, current_cfgs):
        """
        This is the class method function to check
        whether the input configs matches minimal requirement
        -> at least the basic requirements
        @returns status, newly_produced_dict_that_matches_req:
        status indicates current_cfgs matches or not. 
        """
        check_dict = copy.deepcopy(cls.basic_configs)
        check_dict.update(cls.aws_configs)
        input_defensive_copy = copy.deepcopy(current_cfgs)
        if set(check_dict.keys()).issubset(set(current_cfgs.keys())):
            return True, input_defensive_copy

        new_return_dict = copy.deepcopy(check_dict)
        new_return_dict.update(input_defensive_copy)
        return False, new_return_dict


