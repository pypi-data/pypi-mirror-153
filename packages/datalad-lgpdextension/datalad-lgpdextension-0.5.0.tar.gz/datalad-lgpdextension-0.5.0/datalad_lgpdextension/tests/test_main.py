import unittest
from datalad_lgpdextension.main import Main
from datalad_lgpdextension.utils.folder import Folder
class TestMain(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        unittest.TestCase.__init__(self,*args,**kwargs)
        self.filepath = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/settings_base.json"
    def test_run(self):
        path = f"{Folder().getcurrent()}/datalad_lgpdextension/tests/resources/"
        Folder().copy(path+"test_exists_copy.parquet",path+"test_exists.parquet")
        res = Main(self.filepath).run()
        self.assertTrue(res)