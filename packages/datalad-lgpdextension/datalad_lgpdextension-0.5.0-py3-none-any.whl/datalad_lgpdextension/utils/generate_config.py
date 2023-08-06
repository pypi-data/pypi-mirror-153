from datalad_lgpdextension.utils.folder import Folder
class GenerateConfig:
    def __init__(self,path=None):
        self.path = path
    def run(self,path):
        self.path = Folder().getcurrent()
        pass
    def checkIsNull(self,object,key,value):
        if object.get(key,None):
            object[key] = value
        return object
    def addExampleColumn(self):
        settings = {}
        column = {}
        column["enable"] = "true | false"
        column["actions"] = "tokenization | ofuscation | anonymization"
        column["operations"] = {
            "upper | lower | toInt | toFloat | toNumeric | toPrice | toDate | rangeNumeric | encrypt | decrypt": "'toPrice'->('BR'='{:.,2f}' | 'US'='{:,.2f}' | ANY) | 'toDate'->('BR'='%d/%m/%y' | 'US'='%m/%d/%y' | 'CN'='%y/%m/%d' | ANY) | 'json'->{'masculino':0,'feminino':1} | 'rangeNumeric'->{'0-2':0,'3-5':1}"
        }
        settings["NewColumn"] = column
        return settings
    def addExampleTokenization(self):
        settings = {}
        settings["publicKey"] = ""
        return settings
    def addExampleOfuscation(self):
        settings = {}
        settings["publicKey"] = ""
        settings["privateKey"] = ""
        return settings
    def addExampleFile(self):
        settings = {
        "format": "parquet | csv",
        "separator": "; , | ",
        "names": [],
        "header": "0 | None",
        "path": f"{self.path}/filename.parquet"
        }
        return settings
    

