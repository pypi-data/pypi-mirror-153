import unittest
import pandas as pd
import numpy as np
from datalad_lgpdextension.utils.dataframe import Dataframe
from datalad_lgpdextension.crypto.rsa import Rsa

class TestDataframe(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        unittest.TestCase.__init__(self,*args,**kwargs)
        self.dataframe = {'Name': ['Tom', 'Joseph', 'Krish', 'John'], 'Age': [20, 21, 19, 18], 'Price': [1.4,2.4,3.5,1.9], 'DateBorn': ['2022-03-03','2022-06-03','2022-04-12','2022-03-21']}
        self.colname = "Name"
        self.colnamenum = "Age"
        self.colnameprice = "Price"
        self.colnameborn = "DateBorn"
    def test_encrypt(self):
        rsa = Rsa()
        rsa.setpublickey()
        df = pd.DataFrame(self.dataframe).head(1)
        name = df.get(self.colname).iloc[0]
        dfutils = Dataframe(df,rsa,self.colname)
        dfutils.encrypt()
        name_crypto = dfutils.dataframe.get(self.colname).iloc[0]
        self.assertNotEqual(name,str(name_crypto))
    def test_decrypt(self):
        rsa = Rsa()
        rsa.setkeys()
        df = pd.DataFrame(self.dataframe).head(1)
        name = df.get(self.colname).iloc[0]
        dfutils = Dataframe(df,rsa,self.colname)
        dfutils.encrypt()
        dfutils.decrypt()
        name_w_crypto = dfutils.dataframe.get(self.colname).iloc[0]
        self.assertEqual(name,name_w_crypto)
    def test_upper(self):
        df = pd.DataFrame(self.dataframe)
        name = df.get(self.colname).iloc[0]
        dfutils = Dataframe(df,None,self.colname)
        dfutils.upper()
        name = str(dfutils.dataframe.get(self.colname).iloc[0])
        self.assertTrue(name.isupper())
    def test_lower(self):
        df = pd.DataFrame(self.dataframe)
        name = df.get(self.colname).iloc[0]
        dfutils = Dataframe(df,None,self.colname)
        dfutils.lower()
        name = str(dfutils.dataframe.get(self.colname).iloc[0])
        self.assertTrue(name.islower())
    def test_toint(self):
        df = pd.DataFrame(self.dataframe)
        dfutils = Dataframe(df,None,self.colnamenum)
        dfutils.toInt()
        type = dfutils.dataframe.get(self.colnamenum).dtypes
        self.assertTrue(type == np.int32)
    def test_tofloat(self):
        df = pd.DataFrame(self.dataframe)
        dfutils = Dataframe(df,None,self.colnamenum)
        dfutils.toFloat()
        type = dfutils.dataframe.get(self.colnamenum).dtypes
        self.assertTrue(type == np.float64)
    def test_tonumeric(self):
        df = pd.DataFrame(self.dataframe)
        dfutils = Dataframe(df,None,self.colnamenum)
        dfutils.toNumeric()
        type = dfutils.dataframe.get(self.colnamenum).dtypes
        self.assertTrue(type == np.int64)
    def test_toformatfloat(self):
        df = pd.DataFrame(self.dataframe)
        dfutils = Dataframe(df,None,self.colnameprice)
        dfutils.toFormatFloat("US")
        type = dfutils.dataframe.get(self.colnameprice).dtypes
        self.assertTrue(type == np.object0)
    def test_todate(self):
        df = pd.DataFrame(self.dataframe)
        dfutils = Dataframe(df,None,self.colnameborn)
        dfutils.toDate("%Y-%m-%d")
        type = dfutils.dataframe.get(self.colnameborn).dtypes
        self.assertTrue(type == np.dtype('datetime64[ns]'))
    def test_tostring(self):
        df = pd.DataFrame(self.dataframe)
        dfutils = Dataframe(df,None,self.colnamenum)
        dfutils.toString()
        type = dfutils.dataframe.get(self.colnamenum).dtypes
        self.assertTrue(type == np.object0)
    def test_range_numeric(self):
        df = pd.DataFrame(self.dataframe)
        dfutils = Dataframe(df,None,self.colnamenum)
        dfutils.rangeNumeric({'0-18': 0, '19-25': 1, '26-60': 2, '61-130': 3})
        type = dfutils.dataframe.get(self.colnamenum).dtypes
        self.assertTrue(type == np.int64)