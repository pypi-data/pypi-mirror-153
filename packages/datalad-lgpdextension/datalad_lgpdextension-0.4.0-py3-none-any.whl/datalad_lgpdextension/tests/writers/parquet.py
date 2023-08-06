import unittest
import pandas as pd
from datalad_lgpdextension.writers.parquet import Parquet
from datalad_lgpdextension.utils.folder import Folder
class TestParquet(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        unittest.TestCase.__init__(self,*args,**kwargs)
        self.settings_w_names = {"file":{"format":"parquet","separator":"","names":["Name", "Age"],"header":"None","path":f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/test_exists_parquet.parquet"}}
        self.settings = {"file":{"format":"parquet","separator":"","names":[],"header":"None","path":f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/test_exists_parquet.parquet"}}
        self.dataframe = {'Name': ['Tom', 'Joseph', 'Krish', 'John'], 'Age': [20, 21, 19, 18], 'Price': [1.4,2.4,3.5,1.9], 'DateBorn': ['2022-03-03','2022-06-03','2022-04-12','2022-03-21']}
    def test_read_header(self):
        res = Parquet(self.settings_w_names["file"]).read()
        self.assertTrue(isinstance(res,pd.DataFrame))
    def test_read(self):
        res = Parquet(self.settings["file"]).read()
        self.assertTrue(isinstance(res,pd.DataFrame))
    def test_write_names(self):
        df = pd.DataFrame(self.dataframe)
        res = Parquet(self.settings_w_names["file"]).write(df)
        self.assertIsNone(res)
    def test_write(self):
        df = pd.DataFrame(self.dataframe)
        res = Parquet(self.settings["file"]).write(df)
        self.assertIsNone(res)