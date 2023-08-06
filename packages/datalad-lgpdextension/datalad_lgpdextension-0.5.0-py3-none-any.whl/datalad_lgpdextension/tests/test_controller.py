import unittest   
from datalad_lgpdextension.tests.crypto.rsa import TestRsa
from datalad_lgpdextension.tests.runner.actions import TestActions
from datalad_lgpdextension.tests.runner.operations import TestOperations
from datalad_lgpdextension.tests.utils.dataframe import TestDataframe as TestDataframeUtils
from datalad_lgpdextension.tests.utils.folder import TestFolder 
from datalad_lgpdextension.tests.writers.csv import TestCsv
from datalad_lgpdextension.tests.writers.dataframe import TestDataframe
from datalad_lgpdextension.tests.writers.parquet import TestParquet
def create_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestCsv)
    test_suite.addTest(TestActions)
    test_suite.addTest(TestRsa)
    test_suite.addTest(TestDataframe)
    test_suite.addTest(TestOperations)
    test_suite.addTest(TestFolder)
    test_suite.addTest(TestParquet)
    test_suite.addTest(TestDataframeUtils)
    return test_suite

if __name__ == '__main__':
   suite = create_suite()
   runner=unittest.TextTestRunner()
   runner.run(suite)