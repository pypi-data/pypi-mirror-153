import unittest
import logging
import pandas as pd
from datalad_lgpdextension.crypto.rsa import Rsa

class TestRsa(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        unittest.TestCase.__init__(self,*args,**kwargs)
    def test_ofuscation(self):
        settings = {"publicKey":None,"privateKey":None}
        res = Rsa().ofuscation(settings)
        result = res["publicKey"] and res["privateKey"]
        self.assertTrue(result != None)
    def test_tokenization(self):
        settings = {"publicKey":{},"privateKey":{}}
        res = Rsa().tokenization(settings)
        self.assertTrue(res != None)
    def test_encrypt(self):
        text = "test123"
        res = Rsa().encrypt(text)
        self.assertTrue(res == False)
    def test_encrypt_rsa(self):
        text = "text123"
        rsa = Rsa()
        rsa.setpublickey()
        res = rsa.encrypt(text)
        self.assertTrue(res != text)
    def test_decrypt(self):
        text = "test123"
        res = Rsa().decrypt(text)
        self.assertTrue(res == False)
    def test_decrypt_rsa(self):
        text = "test123"
        rsa = Rsa()
        rsa.setkeys()
        text_encrypt = rsa.encrypt(text)
        res = rsa.decrypt(text_encrypt)
        self.assertTrue(res == text)
    def test_generate(self):
        pubKey,priKey = Rsa().generate()
        res = pubKey != None and priKey != None
        self.assertTrue(res != None)
    def test_setpublickey(self):
        rsa = Rsa()
        rsa.setpublickey()
        pubKey= rsa.publickey
        self.assertTrue(pubKey != None)
    def test_setkeys(self):
        rsa = Rsa()
        rsa.setkeys()
        pubKey = rsa.publickey
        priKey = rsa.privatekey
        res = pubKey != None and priKey != None
        self.assertTrue(res != None)