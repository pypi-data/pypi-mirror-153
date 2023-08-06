import json
import unittest
import threading
from gadgethiServerUtils.authentication import *
from gadgethiServerUtils.file_basics import *
from gadgethiServerUtils.GadgethiAWSHandler import *

def handler_function(input_dict, **configs):
    return {"indicator":True, "message":input_dict}

def get_auth_headers(key, secret):
    a = GadgethiHMAC256Encryption(key,secret)
    return a.getGServerAuthHeaders()

class GAWSHandlerTests(unittest.TestCase):
    """
    Testing Strategy:
    
    * Constructor:
        - partition on handler function: No handler, custom handler
        - partition on authentication: With auth, without auth
    * handle
        - partition on payload types: GET, POST/json, POST/x-www-form-urlencode
    """
    def test_handler_function(self):
        configs = {
            "db_lock": threading.Lock()
        }
        # No handler
        handler = GadgetHiAWSHandler(**configs)
        event = {'body': None, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': '127.0.0.1:3000', 'Postman-Token': 'd556e82b-e73a-4458-bb48-e75279291909', 'User-Agent': 'PostmanRuntime/7.6.0', 'X-Forwarded-Port': '3000', 'X-Forwarded-Proto': 'http'}, 'httpMethod': 'GET', 'isBase64Encoded': False, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate'], 'Cache-Control': ['no-cache'], 'Connection': ['keep-alive'], 'Content-Type': ['application/x-www-form-urlencoded'], 'Host': ['127.0.0.1:3000'], 'Postman-Token': ['d556e82b-e73a-4458-bb48-e75279291909'], 'User-Agent': ['PostmanRuntime/7.6.0'], 'X-Forwarded-Port': ['3000'], 'X-Forwarded-Proto': ['http']}, 'multiValueQueryStringParameters': {'operation': ['add_all'], 'service': ['order']}, 'path': '/', 'pathParameters': None, 'queryStringParameters': {'operation': 'add_all', 'service': 'order'}, 'requestContext': {'accountId': '123456789012', 'apiId': '1234567890', 'domainName': '127.0.0.1:3000', 'extendedRequestId': None, 'httpMethod': 'GET', 'identity': {'accountId': None, 'apiKey': None, 'caller': None, 'cognitoAuthenticationProvider': None, 'cognitoAuthenticationType': None, 'cognitoIdentityPoolId': None, 'sourceIp': '127.0.0.1', 'user': None, 'userAgent': 'Custom User Agent String', 'userArn': None}, 'path': '/', 'protocol': 'HTTP/1.1', 'requestId': '34b0682d-a6db-4184-b924-3337c81082c9', 'requestTime': '05/Aug/2021:07:04:54 +0000', 'requestTimeEpoch': 1628147094, 'resourceId': '123456', 'resourcePath': '/', 'stage': 'Prod'}, 'resource': '/', 'stageVariables': None, 'version': '1.0'}        
        self.assertTrue(handler.handle(event, {}) == None)

        # Custom handler
        handler = GadgetHiAWSHandler(service_handler=handler_function, **configs)
        event = {'body': None, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': '127.0.0.1:3000', 'Postman-Token': 'd556e82b-e73a-4458-bb48-e75279291909', 'User-Agent': 'PostmanRuntime/7.6.0', 'X-Forwarded-Port': '3000', 'X-Forwarded-Proto': 'http'}, 'httpMethod': 'GET', 'isBase64Encoded': False, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate'], 'Cache-Control': ['no-cache'], 'Connection': ['keep-alive'], 'Content-Type': ['application/x-www-form-urlencoded'], 'Host': ['127.0.0.1:3000'], 'Postman-Token': ['d556e82b-e73a-4458-bb48-e75279291909'], 'User-Agent': ['PostmanRuntime/7.6.0'], 'X-Forwarded-Port': ['3000'], 'X-Forwarded-Proto': ['http']}, 'multiValueQueryStringParameters': {'operation': ['add_all'], 'service': ['order']}, 'path': '/', 'pathParameters': None, 'queryStringParameters': {'operation': 'add_all', 'service': 'order'}, 'requestContext': {'accountId': '123456789012', 'apiId': '1234567890', 'domainName': '127.0.0.1:3000', 'extendedRequestId': None, 'httpMethod': 'GET', 'identity': {'accountId': None, 'apiKey': None, 'caller': None, 'cognitoAuthenticationProvider': None, 'cognitoAuthenticationType': None, 'cognitoIdentityPoolId': None, 'sourceIp': '127.0.0.1', 'user': None, 'userAgent': 'Custom User Agent String', 'userArn': None}, 'path': '/', 'protocol': 'HTTP/1.1', 'requestId': '34b0682d-a6db-4184-b924-3337c81082c9', 'requestTime': '05/Aug/2021:07:04:54 +0000', 'requestTimeEpoch': 1628147094, 'resourceId': '123456', 'resourcePath': '/', 'stage': 'Prod'}, 'resource': '/', 'stageVariables': None, 'version': '1.0'}        
        self.assertTrue(handler.handle(event, {})["indicator"])

    def test_auth_function(self):
        # With authentication
        key, secret = "gh", "kkk"
        configs = {
            "gadgethi_secret": secret
        }
        handler = GadgetHiAWSHandler(service_handler=handler_function, authentication=True, **configs)
        event = {'body': '{\n\t"service": "order", \n\t"operation": "add_all"\n}', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Length': '49', 'Content-Type': 'application/json', 'Host': '127.0.0.1:3000', 'Postman-Token': '6aee7513-02a0-4189-86e4-571938e46ca8', 'User-Agent': 'PostmanRuntime/7.6.0', 'X-Forwarded-Port': '3000', 'X-Forwarded-Proto': 'http'}, 'httpMethod': 'POST', 'isBase64Encoded': False, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate'], 'Cache-Control': ['no-cache'], 'Connection': ['keep-alive'], 'Content-Length': ['49'], 'Content-Type': ['application/json'], 'Host': ['127.0.0.1:3000'], 'Postman-Token': ['6aee7513-02a0-4189-86e4-571938e46ca8'], 'User-Agent': ['PostmanRuntime/7.6.0'], 'X-Forwarded-Port': ['3000'], 'X-Forwarded-Proto': ['http']}, 'multiValueQueryStringParameters': None, 'path': '/', 'pathParameters': None, 'queryStringParameters': None, 'requestContext': {'accountId': '123456789012', 'apiId': '1234567890', 'domainName': '127.0.0.1:3000', 'extendedRequestId': None, 'httpMethod': 'POST', 'identity': {'accountId': None, 'apiKey': None, 'caller': None, 'cognitoAuthenticationProvider': None, 'cognitoAuthenticationType': None, 'cognitoIdentityPoolId': None, 'sourceIp': '127.0.0.1', 'user': None, 'userAgent': 'Custom User Agent String', 'userArn': None}, 'path': '/', 'protocol': 'HTTP/1.1', 'requestId': '34b0682d-a6db-4184-b924-3337c81082c9', 'requestTime': '05/Aug/2021:07:04:54 +0000', 'requestTimeEpoch': 1628147094, 'resourceId': '123456', 'resourcePath': '/', 'stage': 'Prod'}, 'resource': '/', 'stageVariables': None, 'version': '1.0'}
        event["headers"].update(get_auth_headers(key, secret))
        self.assertTrue(handler.handle(event, {})["indicator"])

        # Without authentication
        handler = GadgetHiAWSHandler(service_handler=handler_function, **configs)
        event = {'body': '{\n\t"service": "order", \n\t"operation": "add_all"\n}', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Length': '49', 'Content-Type': 'application/json', 'Host': '127.0.0.1:3000', 'Postman-Token': '6aee7513-02a0-4189-86e4-571938e46ca8', 'User-Agent': 'PostmanRuntime/7.6.0', 'X-Forwarded-Port': '3000', 'X-Forwarded-Proto': 'http'}, 'httpMethod': 'POST', 'isBase64Encoded': False, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate'], 'Cache-Control': ['no-cache'], 'Connection': ['keep-alive'], 'Content-Length': ['49'], 'Content-Type': ['application/json'], 'Host': ['127.0.0.1:3000'], 'Postman-Token': ['6aee7513-02a0-4189-86e4-571938e46ca8'], 'User-Agent': ['PostmanRuntime/7.6.0'], 'X-Forwarded-Port': ['3000'], 'X-Forwarded-Proto': ['http']}, 'multiValueQueryStringParameters': None, 'path': '/', 'pathParameters': None, 'queryStringParameters': None, 'requestContext': {'accountId': '123456789012', 'apiId': '1234567890', 'domainName': '127.0.0.1:3000', 'extendedRequestId': None, 'httpMethod': 'POST', 'identity': {'accountId': None, 'apiKey': None, 'caller': None, 'cognitoAuthenticationProvider': None, 'cognitoAuthenticationType': None, 'cognitoIdentityPoolId': None, 'sourceIp': '127.0.0.1', 'user': None, 'userAgent': 'Custom User Agent String', 'userArn': None}, 'path': '/', 'protocol': 'HTTP/1.1', 'requestId': '34b0682d-a6db-4184-b924-3337c81082c9', 'requestTime': '05/Aug/2021:07:04:54 +0000', 'requestTimeEpoch': 1628147094, 'resourceId': '123456', 'resourcePath': '/', 'stage': 'Prod'}, 'resource': '/', 'stageVariables': None, 'version': '1.0'}
        self.assertTrue(handler.handle(event, {})["indicator"])

    def test_payload_types(self):
        key, secret = "gh", "kkk"
        configs = {
            "gadgethi_secret": secret
        }
        handler = GadgetHiAWSHandler(service_handler=handler_function, authentication=True, **configs)
        # POST/json
        event = {'body': '{\n\t"service": "order", \n\t"operation": "add_all"\n}', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Length': '49', 'Content-Type': 'application/json', 'Host': '127.0.0.1:3000', 'Postman-Token': '6aee7513-02a0-4189-86e4-571938e46ca8', 'User-Agent': 'PostmanRuntime/7.6.0', 'X-Forwarded-Port': '3000', 'X-Forwarded-Proto': 'http'}, 'httpMethod': 'POST', 'isBase64Encoded': False, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate'], 'Cache-Control': ['no-cache'], 'Connection': ['keep-alive'], 'Content-Length': ['49'], 'Content-Type': ['application/json'], 'Host': ['127.0.0.1:3000'], 'Postman-Token': ['6aee7513-02a0-4189-86e4-571938e46ca8'], 'User-Agent': ['PostmanRuntime/7.6.0'], 'X-Forwarded-Port': ['3000'], 'X-Forwarded-Proto': ['http']}, 'multiValueQueryStringParameters': None, 'path': '/', 'pathParameters': None, 'queryStringParameters': None, 'requestContext': {'accountId': '123456789012', 'apiId': '1234567890', 'domainName': '127.0.0.1:3000', 'extendedRequestId': None, 'httpMethod': 'POST', 'identity': {'accountId': None, 'apiKey': None, 'caller': None, 'cognitoAuthenticationProvider': None, 'cognitoAuthenticationType': None, 'cognitoIdentityPoolId': None, 'sourceIp': '127.0.0.1', 'user': None, 'userAgent': 'Custom User Agent String', 'userArn': None}, 'path': '/', 'protocol': 'HTTP/1.1', 'requestId': '34b0682d-a6db-4184-b924-3337c81082c9', 'requestTime': '05/Aug/2021:07:04:54 +0000', 'requestTimeEpoch': 1628147094, 'resourceId': '123456', 'resourcePath': '/', 'stage': 'Prod'}, 'resource': '/', 'stageVariables': None, 'version': '1.0'}
        event["headers"].update(get_auth_headers(key, secret))
        self.assertTrue(handler.handle(event, {})["indicator"])
        self.assertEqual(handler.handle(event, {})["message"]["form"], {"service": "order", "operation":"add_all"})

        # POST/x-www-form-urlencode
        event = {'body': 'service=order&operation=add_all', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Length': '31', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': '127.0.0.1:3000', 'Postman-Token': '85e7465d-867b-4d42-858e-5ef91e7e33a3', 'User-Agent': 'PostmanRuntime/7.6.0', 'X-Forwarded-Port': '3000', 'X-Forwarded-Proto': 'http'}, 'httpMethod': 'POST', 'isBase64Encoded': False, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate'], 'Cache-Control': ['no-cache'], 'Connection': ['keep-alive'], 'Content-Length': ['31'], 'Content-Type': ['application/x-www-form-urlencoded'], 'Host': ['127.0.0.1:3000'], 'Postman-Token': ['85e7465d-867b-4d42-858e-5ef91e7e33a3'], 'User-Agent': ['PostmanRuntime/7.6.0'], 'X-Forwarded-Port': ['3000'], 'X-Forwarded-Proto': ['http']}, 'multiValueQueryStringParameters': None, 'path': '/', 'pathParameters': None, 'queryStringParameters': None, 'requestContext': {'accountId': '123456789012', 'apiId': '1234567890', 'domainName': '127.0.0.1:3000', 'extendedRequestId': None, 'httpMethod': 'POST', 'identity': {'accountId': None, 'apiKey': None, 'caller': None, 'cognitoAuthenticationProvider': None, 'cognitoAuthenticationType': None, 'cognitoIdentityPoolId': None, 'sourceIp': '127.0.0.1', 'user': None, 'userAgent': 'Custom User Agent String', 'userArn': None}, 'path': '/', 'protocol': 'HTTP/1.1', 'requestId': '34b0682d-a6db-4184-b924-3337c81082c9', 'requestTime': '05/Aug/2021:07:04:54 +0000', 'requestTimeEpoch': 1628147094, 'resourceId': '123456', 'resourcePath': '/', 'stage': 'Prod'}, 'resource': '/', 'stageVariables': None, 'version': '1.0'}
        event["headers"].update(get_auth_headers(key, secret))
        self.assertTrue(handler.handle(event, {})["indicator"])
        self.assertEqual(handler.handle(event, {})["message"]["form"], {"service": "order", "operation":"add_all"})

        # GET
        event = {'body': None, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': '127.0.0.1:3000', 'Postman-Token': 'd556e82b-e73a-4458-bb48-e75279291909', 'User-Agent': 'PostmanRuntime/7.6.0', 'X-Forwarded-Port': '3000', 'X-Forwarded-Proto': 'http'}, 'httpMethod': 'GET', 'isBase64Encoded': False, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate'], 'Cache-Control': ['no-cache'], 'Connection': ['keep-alive'], 'Content-Type': ['application/x-www-form-urlencoded'], 'Host': ['127.0.0.1:3000'], 'Postman-Token': ['d556e82b-e73a-4458-bb48-e75279291909'], 'User-Agent': ['PostmanRuntime/7.6.0'], 'X-Forwarded-Port': ['3000'], 'X-Forwarded-Proto': ['http']}, 'multiValueQueryStringParameters': {'operation': ['add_all'], 'service': ['order']}, 'path': '/', 'pathParameters': None, 'queryStringParameters': {'operation': 'add_all', 'service': 'order'}, 'requestContext': {'accountId': '123456789012', 'apiId': '1234567890', 'domainName': '127.0.0.1:3000', 'extendedRequestId': None, 'httpMethod': 'GET', 'identity': {'accountId': None, 'apiKey': None, 'caller': None, 'cognitoAuthenticationProvider': None, 'cognitoAuthenticationType': None, 'cognitoIdentityPoolId': None, 'sourceIp': '127.0.0.1', 'user': None, 'userAgent': 'Custom User Agent String', 'userArn': None}, 'path': '/', 'protocol': 'HTTP/1.1', 'requestId': '34b0682d-a6db-4184-b924-3337c81082c9', 'requestTime': '05/Aug/2021:07:04:54 +0000', 'requestTimeEpoch': 1628147094, 'resourceId': '123456', 'resourcePath': '/', 'stage': 'Prod'}, 'resource': '/', 'stageVariables': None, 'version': '1.0'}        
        event["headers"].update(get_auth_headers(key, secret))
        self.assertTrue(handler.handle(event, {})["indicator"])
        self.assertEqual(handler.handle(event, {})["message"]["values"], {"service": "order", "operation":"add_all"})

