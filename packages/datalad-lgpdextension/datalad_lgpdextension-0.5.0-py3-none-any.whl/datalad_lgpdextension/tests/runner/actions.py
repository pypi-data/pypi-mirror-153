import unittest
import pandas as pd
from datalad_lgpdextension.runner.actions import Actions
from datalad_lgpdextension.utils.folder import Folder
from datalad_lgpdextension.utils.dataframe import Dataframe
class TestActions(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        unittest.TestCase.__init__(self,*args,**kwargs)
        self.df = {'Name': ['Tom', 'Joseph', 'Krish', 'John'], 'Age': [20, 21, 19, 18],"DateBorn":["2020-01-02","2020-04-02","2021-01-02","2022-01-02"]}  
        self.operations = {"upper": "true"}
        self.filepath = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/settings_base.json"
        self.settings = Folder(self.filepath).read()
    def test_tokenization(self):
        dfa = pd.DataFrame(self.df)
        path = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/test_tokenization.parquet"
        self.settings["file"]["path"] = path
        self.filepath = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/settings_base_tokenization.json"
        act = Actions("Name",self.settings,dfa,self.filepath)
        act.tokenization()
        res = act.dataframe
        self.assertTrue(isinstance(res,pd.DataFrame))
    def test_ofuscation(self):
        dfa = pd.DataFrame(self.df)
        path = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/test_ofuscation.parquet"
        self.settings["file"]["path"] = path
        self.filepath = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/settings_base_ofuscation.json"
        act = Actions("DateBorn",self.settings,dfa,self.filepath)
        act.ofuscation()
        res = act.dataframe
        self.assertTrue(isinstance(res,pd.DataFrame))
    def test_anonymization(self):
        dfa = pd.DataFrame(self.df)
        path = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/test_anonymization.parquet"
        self.settings["file"]["path"] = path
        self.filepath = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/settings_base_anonymization.json"
        act = Actions("Age",self.settings,dfa,self.filepath)
        act.anonymization()
        res = act.dataframe
        self.assertTrue(isinstance(res,pd.DataFrame))