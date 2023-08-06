import unittest
import pandas as pd
from datalad_lgpdextension.writers.csv import Csv
from datalad_lgpdextension.utils.folder import Folder
class TestCsv(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        unittest.TestCase.__init__(self,*args,**kwargs)
        self.path = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/test_"
        self.settings_w_header = {"file":{"format":"csv","separator":";","names":["Name", "Age"],"header":"None","path":self.path+"w_header.csv"}}
        self.settings_w_names = {"file":{"format":"csv","separator":";","names":[],"header":0,"path":self.path+"w_names.csv"}}
        self.settings = {"file":{"format":"csv","separator":";","names":[],"header":0,"path":self.path+"settings.csv"}}
        self.dataframe = {'Name': ['Tom', 'Joseph', 'Krish', 'John'], 'Age': [20, 21, 19, 18]}  
    def test_read_header(self):
        res = Csv(self.settings_w_header["file"]).read()
        self.assertTrue(isinstance(res,pd.DataFrame))
    def test_read_names(self):
        res = Csv(self.settings_w_names["file"]).read()
        self.assertTrue(isinstance(res,pd.DataFrame))
    def test_read(self):
        res = Csv(self.settings["file"]).read()
        self.assertTrue(isinstance(res,pd.DataFrame))
    def test_write_header(self):
        df = pd.DataFrame(self.dataframe)
        res = Csv(self.settings_w_header["file"]).write(df)
        self.assertEqual(res,None)
    def test_write_names(self):
        df = pd.DataFrame(self.dataframe)
        res = Csv(self.settings_w_names["file"]).write(df)
        self.assertEqual(res,None)
    def test_write(self):
        df = pd.DataFrame(self.dataframe)
        res = Csv(self.settings["file"]).write(df)
        self.assertEqual(res,None)