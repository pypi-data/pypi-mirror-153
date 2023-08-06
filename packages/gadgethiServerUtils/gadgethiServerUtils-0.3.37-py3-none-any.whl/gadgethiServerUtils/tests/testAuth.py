import unittest
from gadgethiServerUtils.time_basics import serverTime
from gadgethiServerUtils.authentication import GadgethiHMAC256Encryption, GadgethiHMAC256Verification

class AuthenticationTests(unittest.TestCase):
    """
    Testing Strategy:
    - GadgethiHMAC256Encryption
        * constructor
            - partition on key, secret length: 0, >0
        * hmac256_encryption
            - partition on message length: 0, >0
            - partition on mode: base64, hex
        * getGServerAuthHeaders
            - partition on key, secret length: 0, >0
        
    - GadgethiHMAC256Verification
        * constructor
            - partition on message length: 0, >0
        * hmac256_verification
            - partition on message, secret length: 0, >0
            - partition on mode: base64, hex
            - partition on return: same message, different message
        * gserver_authentication
            - partition on return: passed, time check failed, hmac256 failed
            - partition on message, secret length: 0, >0
            - partition on interval: 0, 30, >0 (except 30)
            - partition on checktime: 0, >0
    """

    # GadgethiHMAC256Encryption
    # ----------------------------
    def test_GadgethiHMAC256Encryption_instantiate_ok(self):
        gAuthEncryptor = GadgethiHMAC256Encryption("test-key", "test-secret")
        self.assertIsNotNone(gAuthEncryptor, "could not instantiate calculator")

    # covers 0 length string 
    def test_GadgethiHMAC256Encryption_zero_length(self):
        gAuthEncryptor = GadgethiHMAC256Encryption("", "")
        result = gAuthEncryptor.hmac256_encryption("test_message", mode="base64")
        self.assertEqual(result, "3d44g3tA+sZ6U96gde2bRz6NQ3hhUaUMjnYNRqpnvc8=", \
            "base64 case failed")

        result = gAuthEncryptor.hmac256_encryption("test_message", mode="hex")
        self.assertEqual(result, "ddde38837b40fac67a53dea075ed9b473e8d43786151a50c8e760d46aa67bdcf", \
            "hex case failed")

        header_dict = gAuthEncryptor.getGServerAuthHeaders()
        self.assertEqual(["Gadgethi-Key", "Hmac256-Result", "time"], list(header_dict.keys()), "Dictionary Keys Check")
        self.assertEqual(header_dict["Gadgethi-Key"], "", "Key Failed")

    # covers >0 length string, length 0 message
    def test_GadgethiHMAC256Encryption_other_length(self):
        gAuthEncryptor = GadgethiHMAC256Encryption("DDATESTBED001AA", "gadgethi")
        result = gAuthEncryptor.hmac256_encryption("test_message-test_message-test_message1500051546", mode="base64")
        self.assertEqual(result, "nSQ+zvPVEsRYOIKEEcQMq4d+LxUUGdR60eb5bZZmtsE=", \
            "base64 case failed")

        result = gAuthEncryptor.hmac256_encryption("", mode="hex")
        self.assertEqual(result, "76b4ad7dca6a86044c8f029c65d6d2f342bbf7c1b240b4a0cfa27e6a0589e9aa", \
            "hex case failed")

        header_dict = gAuthEncryptor.getGServerAuthHeaders()
        self.assertEqual(["Gadgethi-Key", "Hmac256-Result", "time"], list(header_dict.keys()), "Dictionary Keys Check")
        self.assertEqual(header_dict["Gadgethi-Key"], "DDATESTBED001AA", "Key Failed")


    # GadgethiHMAC256Verification
    # ----------------------------
    def test_GadgethiHMAC256Verification_instantiate_ok(self):
        verification = GadgethiHMAC256Verification("test-encrypted-message")
        self.assertIsNotNone(verification, "could not instantiate calculator")

    # covers 0 length secret 
    def test_GadgethiHMAC256Verification_zero_length(self):
        gAuthEncryptor = GadgethiHMAC256Encryption("", "")
        result = gAuthEncryptor.hmac256_encryption("", mode="base64")

        verification = GadgethiHMAC256Verification(result)
        self.assertTrue(verification.hmac256_verification("", ""), \
            "Empty Verification True")

        gserverAuth = verification.gserver_authentication("", serverTime(), "", 30)
        self.assertEqual(["indicator", "message"], list(gserverAuth.keys()), "Dictionary Keys Check")
        self.assertTrue(gserverAuth["indicator"],\
            "Gserver Header verification true")

        gserverAuth = verification.gserver_authentication("", 15000000, "", 0)
        self.assertEqual(["indicator", "message"], list(gserverAuth.keys()), "Dictionary Keys Check")
        self.assertFalse(gserverAuth["indicator"],\
            "Gserver Header verification failed due to time")

        verification = GadgethiHMAC256Verification("")
        self.assertFalse(verification.hmac256_verification("", ""), \
            "Empty Verification False")

        gserverAuth = verification.gserver_authentication("", serverTime(), "", 50)
        self.assertEqual(["indicator", "message"], list(gserverAuth.keys()), "Dictionary Keys Check")
        self.assertFalse(gserverAuth["indicator"],\
            "Gserver Header verification failed due to encryption")

        result = gAuthEncryptor.hmac256_encryption("secretmessage", mode="hex")
        verification = GadgethiHMAC256Verification(result)
        self.assertTrue(verification.hmac256_verification("", "secretmessage", mode="hex"), \
            ">0 message Verification True")

    # covers >0 length secret 
    def test_GadgethiHMAC256Verification_other_length(self):
        gAuthEncryptor = GadgethiHMAC256Encryption("keykeykey", "secretsecret123")
        result = gAuthEncryptor.hmac256_encryption("secretmessagesecretmessage123", mode="base64")

        verification = GadgethiHMAC256Verification(result)
        self.assertTrue(verification.hmac256_verification("secretsecret123", "secretmessagesecretmessage123"), \
            "Message Verification True")

        gserverAuth = verification.gserver_authentication("secretmessagesecretmessage123", serverTime(), "secretsecret123", 30)
        self.assertEqual(["indicator", "message"], list(gserverAuth.keys()), "Dictionary Keys Check")
        self.assertTrue(gserverAuth["indicator"],\
            "Gserver Header verification true (Message)")

        gserverAuth = verification.gserver_authentication("secretmessagesecretmessage123", 15000000, "secretsecret123", 0)
        self.assertEqual(["indicator", "message"], list(gserverAuth.keys()), "Dictionary Keys Check")
        self.assertFalse(gserverAuth["indicator"],\
            "Gserver Header verification failed due to time (Message)")

        