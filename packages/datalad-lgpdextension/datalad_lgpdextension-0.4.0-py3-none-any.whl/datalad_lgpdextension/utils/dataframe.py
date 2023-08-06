import logging
import pandas as pd
from datalad_lgpdextension.crypto.rsa import Rsa

lgr = logging.getLogger('datalad.lgpdextension.lgpd_extension.utils.dataframe')

class Dataframe:
    def __init__(self, dataframe,rsa,colname):
        self.cryptoObj = rsa
        setattr(Dataframe, 'dataframe', dataframe)
        self.colname = colname
        self.date_format = {"BR":"%d/%m/%y","US":"%m/%d/%y","CN":"%y/%m/%d"}
        self.price_format = {"BR":"{:.,2f}","US":"{:,.2f}"}
    def encrypt(self):
        lgr.info("Encrypt to " + self.colname)
        self.dataframe[self.colname] = self.dataframe[self.colname].apply(self.cryptoObj.encrypt)
    def decrypt(self):
        lgr.info("Decrypt to " + self.colname)
        self.dataframe[self.colname] = self.dataframe[self.colname].apply(self.cryptoObj.decrypt)    
    def upper(self):
        lgr.info("Upper to " + self.colname)
        self.dataframe[self.colname] = self.dataframe[self.colname].str.upper()
    def lower(self):
        lgr.info("Lower to " + self.colname)
        self.dataframe[self.colname] = self.dataframe[self.colname].str.lower()
    def toInt(self):
        lgr.info("toInt to " + self.colname)
        self.dataframe[self.colname] = self.dataframe[self.colname].astype(int)
    def toFloat(self):
        lgr.info("toFloat to " + self.colname)
        self.dataframe[self.colname] = self.dataframe[self.colname].astype(float)
    def toNumeric(self):
        lgr.info("toNumeric to " + self.colname)
        self.dataframe[self.colname] = pd.to_numeric(self.dataframe[self.colname])
    def toPrice(self,value):
        lgr.info("toPrice to " + self.colname + " - format to " + value)
        self.dataframe[self.colname] = self.dataframe[self.colname].map(self.price_format.get(value,value).format)
    def toDate(self,value):
        lgr.info("toDate to " + self.colname + " - format to " + value)
        self.dataframe[self.colname] = pd.to_datetime(self.dataframe[self.colname],format=self.date_format.get(value,value))
    def toString(self):
        lgr.info("toString to " + self.colname)
        self.dataframe[self.colname] = self.dataframe[self.colname].astype(str)
    def json(self,text):
        lgr.info("json to " + self.colname + " - " + str(text))
        self.toString()
        self.dataframe[self.colname] = self.dataframe[self.colname].map(text)
    def rangeNumeric(self,text):
        lgr.info("range_numeric to " + self.colname + " - " + str(text))   
        values = {}
        for i in list(text.keys()):
            value = text[i]
            key = i.split("-")
            nums = [str(i) for i in range(int(key[0]),int(key[1])+1)]
            for j in nums:
                values[j] = pd.to_numeric(value)
        self.json(values)
    @property
    def dataframe(self):
        return self.dataframe