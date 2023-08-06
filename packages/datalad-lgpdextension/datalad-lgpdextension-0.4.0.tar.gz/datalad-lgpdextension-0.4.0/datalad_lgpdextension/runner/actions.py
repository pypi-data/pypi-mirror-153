import pandas as pd
import logging
from datalad_lgpdextension.utils.dataframe import Dataframe as dfoperations
from datalad_lgpdextension.crypto.rsa import Rsa
from datalad_lgpdextension.writers.dataframe import Dataframe as dfutils
from datalad_lgpdextension.runner.operations import Operations
from datalad_lgpdextension.utils.folder import Folder
lgr = logging.getLogger('datalad.lgpdextension.lgpd_extension.runner.actions')

class Actions:
    def __init__(self,colname,settings,df,filepath):
        self.colname = colname
        setattr(Actions, 'dataframe', df)
        setattr(Actions, 'settings', settings)
        self.colsettings = settings["columns"][colname]
        self.filepath = filepath
    def run(self, action):
        lgr.info("run to " + str(action))
        if action == "tokenization":
            self.tokenization()
        elif action == "ofuscation":
            self.ofuscation()
        elif action == "anonymization":
            self.anonymization()
    def execute(self,rsa):
        lgr.info("execute to " + str(rsa))
        dfobj = dfoperations(self.dataframe,rsa,self.colname)
        opobj = Operations(dfobj)
        opobj.run(self.colsettings["operations"])
        dfutils().write(opobj.dataframe.dataframe,self.settings)
        Folder(self.filepath).save(self.settings)
    def tokenization(self):
        lgr.info("tokenization action")
        rsa = Rsa()
        self.settings["tokenization"] = rsa.tokenization(self.settings.get("tokenization",{}))
        self.execute(rsa)
    def ofuscation(self):
        lgr.info("ofuscation action")
        rsa = Rsa()
        self.settings["ofuscation"] = rsa.ofuscation(self.settings.get("ofuscation",{}))
        self.execute(rsa)
    def anonymization(self):
        lgr.info("anonymization action")
        dfobj = dfoperations(self.dataframe,None,self.colname)
        opobj = Operations(dfobj)
        opobj.run(self.colsettings["operations"])
        dfutils().write(self.dataframe,self.settings)
        Folder(self.filepath).save(self.settings)
    @property
    def settings(self):
        return self.settings
    def settings_set(self, value):
        self.settings = value
    @property
    def dataframe(self):
        return self.dataframe