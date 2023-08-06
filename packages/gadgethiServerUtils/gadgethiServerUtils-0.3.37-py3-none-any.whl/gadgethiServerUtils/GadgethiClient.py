import os
import requests
from gadgethiServerUtils.file_basics import *
from gadgethiServerUtils.authentication import *
from gadgethiServerUtils._exceptions import *
from gadgethiServerUtils.time_basics import timeout

"""
Represents the client class to send
HTTP requests. Including gadgethi
authentication function. 
"""
class GadgetHiClient:
    
    def __init__(self, custom_credentials_loc=os.path.abspath(os.path.join(default_gserver_location, "credentials.yaml")), 
        http_timeout=None, **configs):
        """
        @kwargs: if _http_url in kwargs, 
            get that key and set it to the
            attribute. 
        """
        self.credentials = read_config_yaml(custom_credentials_loc)

        for key in configs:
            if "_http_url" in key:
                setattr(self, key, configs[key])

    def __getitem__(self, key):
        return getattr(self, key)
    
    @gexception
    @timeout(10)
    def client_get(self, key, input_dict, gauth=False, custom_headers={}):
        """
        This is the main function to send out HTTP GET. 
        @params key: the key of the url stored in the ADT
        @params input_dict: the input dictionary of the data that is 
            going to send
        @params gauth: whether we should enable gadgethi authentication, 
            adding auth headers to the HTTP packets
        @params custom_headers: custom headers to send, default empty. 
        """
        get_query = self[key]

        # assign query list
        query_list = ["?"]
        for key in input_dict:
            query_list.extend([str(key), "=", input_dict[key], "&"])

        # concatenate together
        get_query += "".join(query_list[:-1])

        if gauth:
            # authentication
            a = GadgethiHMAC256Encryption(self.credentials['gadgethi_key'],self.credentials['gadgethi_secret'])
            auth_header = a.getGServerAuthHeaders()
            headers = custom_headers
            headers.update(auth_header)
            r = requests.get(get_query,headers=headers)
        else:
            r = requests.get(get_query,headers=custom_headers)
        response = r.text 
        return response

    @gexception
    @timeout(10)
    def client_post(self, key, input_dict,gauth=False,urlencode=False, 
        custom_headers={}):
        """
        This is the main function to send out HTTP POST. 
        @params key: the key of the url stored in the ADT
        @params input_dict: the input dictionary of the data that is 
            going to send
        @params gauth: whether we should enable gadgethi authentication, 
            adding auth headers to the HTTP packets
        @params urlencode: This defines the application type of the POST content. 
            If True -> www-urlencode, default False -> json
        @params custom_headers: custom headers to send, default empty. 
        """
        post_query = self[key]

        if gauth:
            # authentication
            a = GadgethiHMAC256Encryption(self.credentials['gadgethi_key'],self.credentials['gadgethi_secret'])
            auth_header = a.getGServerAuthHeaders()
            headers = custom_headers
            headers.update(auth_header)

            if urlencode:
                r = requests.post(post_query, data=input_dict,headers=headers)
            else:
                r = requests.post(post_query, json=input_dict,headers=headers)
            response = r.text           
        else:

            if urlencode:
                r = requests.post(post_query, data=input_dict,headers=custom_headers)
            else:
                r = requests.post(post_query, json=input_dict,headers=custom_headers)
            response = r.text

        return response

    @gexception
    @timeout(10)
    def client_put(self, key, input_dict, custom_headers={}):
        """
        This is the main function to send out HTTP PUT. 
        @params key: the key of the url stored in the ADT
        @params input_dict: the input dictionary of the data that is 
            going to send
        @params gauth: whether we should enable gadgethi authentication, 
            adding auth headers to the HTTP packets
        @params custom_headers: custom headers to send, default empty. 
        """
        put_query = self[key]

        r = requests.put(put_query, data=input_dict,headers=custom_headers)
        response = r.text
        return response

    def client_post_without_timeout(self, key, input_dict):
        """
        This is the auxiliary function to send out http post
        without a timeout declaration. It is usually for local
        development and no authentication is needed. 
        Not recommended for production or public facing
        applications. 
        """
        post_query = self[key]
        r = requests.post(post_query, data=input_dict)
        response = r.text
        return response

