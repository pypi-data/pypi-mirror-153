import logging
import rsa
from datalad_lgpdextension.utils.folder import Folder

lgr = logging.getLogger('datalad.lgpdextension.lgpd_extension.runner.operations')

class Rsa:
    def __init__(self):
        self.publicKey = None
        self.privateKey = None
    def ofuscation(self,settings):
        lgr.info("ofuscation to " + str(settings))
        if not settings.get("publicKey",None) or not settings.get("privateKey",None):
            self.setkeys()
        elif settings.get("publicKey",None) and settings.get("privateKey",None):
            pub = settings["publicKey"]
            pri = settings["privateKey"]
            self.publicKey = rsa.PublicKey(pub["n"],pub["e"])
            self.privateKey = rsa.PrivateKey(pri["n"],pri["e"],pri["d"],pri["p"],pri["q"])
        settings = self.updatefile(settings,"publicKey",{"n":self.publicKey.n,"e":self.publicKey.e})
        settings = self.updatefile(settings,"privateKey",{"n":self.privateKey.n,"e":self.privateKey.e,"d":self.privateKey.d,"p":self.privatekey.p,"q":self.privateKey.q})
        return settings
    def tokenization(self,settings):
        lgr.info("tokenization to " + str(settings))
        if not settings.get("publicKey",None):
            self.setpublickey()
        elif settings.get("publicKey",None):
            pub = settings["publicKey"]
            self.publicKey = rsa.PublicKey(pub["n"],pub["e"])
        settings = self.updatefile(settings,"publicKey",{"n":self.publicKey.n,"e":self.publicKey.e})
        return settings
    def encrypt(self,text):
        lgr.info("encrypt to " + str(text))
        if self.publicKey:
            return rsa.encrypt(text.encode(),self.publicKey)
        return False
    def decrypt(self,text):
        lgr.info("decrypt to " + str(text))
        if self.privateKey:
            return rsa.decrypt(text, self.privateKey).decode()
        return False
    def generate(self):
        lgr.info("generate keys")
        publicKey,privateKey = rsa.newkeys(512)
        return publicKey,privateKey
    def setpublickey(self):
        lgr.info("setpublickey key")
        self.publicKey,_ = self.generate()
    def setkeys(self):
        lgr.info("setkeys keys")
        self.publicKey,self.privateKey = self.generate()
    def updatefile(self,settings,key,value):
        lgr.info("updatefile to " + str(settings))
        return Folder().updatevalue({"obj":settings,"key":key,"value":value})
    @property
    def publickey(self):
        return self.publicKey
    @property
    def privatekey(self):
        return self.privateKey