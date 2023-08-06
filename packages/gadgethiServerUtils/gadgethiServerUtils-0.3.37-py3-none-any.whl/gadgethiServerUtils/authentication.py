import datetime
from gadgethiServerUtils.time_basics import *
from Cryptodome.Hash import SHA256, HMAC
from base64 import b64decode, b64encode

def HMAC256_digest(secret,message,mode='base64'):
    """
    This is the main HMAC256 digest function
    to encrypt the input message with 
    the secret and turn it to hex digest. 
    (or other modes)
    """
    if type(secret) != bytes:
        secret = secret.encode()
    h = HMAC.new(secret, digestmod=SHA256)
    if message != bytes:
        message = message.encode()
    h.update(message)
    if mode != 'base64':
        return h.hexdigest()
    else:
        b64 = b64encode(bytes.fromhex(h.hexdigest())).decode()
        return b64

"""
Performs gadgethi HMAC256 
Encryption. 
"""
class GadgethiHMAC256Encryption():
    """
    Methods:
        * hmac256_encryption: general encryption function
            for encrypting message to hmac256
        * getGServerAuthHeaders: This is specifically for gserver
            authentication headers and prepare the header
            for http POST and GET. 
    """
    def __init__(self, key, secret):
        """
        @params key: string
        @params secret: string
        """
        self.key = str(key) 
        self.secret = str(secret)

    def hmac256_encryption(self, message, mode="base64"):
        """
        This is the general function to 
        encrypt a message with hmac256
        """
        encryption_result = HMAC256_digest(self.secret, message, mode=mode)
        return encryption_result

    def getGServerAuthHeaders(self):
        """
        This is the function to obtain the
        gServer Authentication header fields
        """
        current_time = int(serverTime())
        auth_dict = {}
        auth_dict['Gadgethi-Key'] = self.key
        auth_dict['Hmac256-Result'] = self.hmac256_encryption(self.key+str(current_time))
        auth_dict['time'] = str(current_time)
        return auth_dict

"""
Performs gadgethi HMAC256 
verification. 
"""
class GadgethiHMAC256Verification():
    """
    Methods:
        * hmac256_verification: general verification function
            for testing data integrity
        * gserver_authentication: This is specifically for gserver
            authentication and checked the time/hmac256 header message
            to see if the data is corrupted. 
    """
    def __init__(self, encrypted_message):
        """
        - Input:
            The encrypted message that you want
        to verified
        """
        self.encrypted_message = encrypted_message

    def hmac256_verification(self, secret, message, mode="base64"):
        """
        This is the raw hmac256 verification
        function. Returns true if the encrypted message
        equals the message after applying hmac256. 
        """
        encryption_result = HMAC256_digest(secret, message, mode=mode)
        return encryption_result == self.encrypted_message

    def gserver_authentication(self, message, check_time, secret, interval=30):
        """
        This is the verfication function
        for gserver http handler. 
        - Input:
            * message: the message to be verified. 
            * check_time: the current time given by the client
        """
        if self.hmac256_verification(secret, message) and \
            is_time_between(serverTime() - interval, serverTime() + interval, check_time):
            return {"indicator":True,"message":"Verification Passed"}
        else:
            return {"indicator":False,"message":"HMAC256 Verification Failed or Timeout Reached! \
                 Current time for server is: "+serverTime(TimeMode.STRING)}

if __name__ == "__main__":
    g = GadgethiAuthenticationStandardEncryption("nanshanddctablet", "gadgethi")
    print(HMAC256_digest(g.secret,g.key+"1619644177"))