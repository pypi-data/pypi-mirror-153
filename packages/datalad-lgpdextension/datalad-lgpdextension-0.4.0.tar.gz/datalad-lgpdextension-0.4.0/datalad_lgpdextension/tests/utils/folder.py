import unittest
import pandas as pd
import numpy as np
from datalad_lgpdextension.utils.folder import Folder

class TestFolder(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        unittest.TestCase.__init__(self,*args,**kwargs)
        self.path = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/settings_base.json"
    def test_current(self):
        res = Folder.getcurrent()
        self.assertIsNotNone(res)
    def test_update_value(self):
        res = Folder().updatevalue({"obj":{"name":"test"},"key":"name","value":"test1"})
        self.assertTrue(res["name"] == "test1")
    def test_read(self):
        res = Folder(self.path).read()
        self.assertIsNotNone(res)
    def test_save(self):
        fld = Folder(self.path)
        content = fld.read()
        res = fld.save(content)
        self.assertTrue(res == True)
    def test_exists(self):
        fld = Folder(self.path)
        res = fld.exists()
        self.assertTrue(res == True)