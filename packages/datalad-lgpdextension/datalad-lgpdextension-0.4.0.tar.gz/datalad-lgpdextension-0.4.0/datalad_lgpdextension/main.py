import logging
from datalad_lgpdextension.utils.dataframe import Dataframe
from datalad_lgpdextension.writers.dataframe import Dataframe as dfutils
from datalad_lgpdextension.utils.folder import Folder
from datalad_lgpdextension.runner.actions import Actions
from datalad_lgpdextension.utils.generate_config import GenerateConfig
from datalad_lgpdextension.utils.folder import Folder

lgr = logging.getLogger('datalad.lgpdextension.lgpd_extension.writers.dataframe')

class Main:
    def __init__(self,createfile,filename=""):
        self.filename = filename
        self.createfile = createfile
    def update_file(self,settings):
        defauld_field = "Added the '{{FIELD}} field'. YOU NEED TO CONFIGURE THE '{{FIELD}} FIELD' FROM SETTINGS JSON."
        if not settings.get("ofuscation",None):
            msg = defauld_field.replace("{{FIELD}}","OFUSCATION")
            lgr.info(msg)
            settings["ofuscation"] = GenerateConfig().addExampleOfuscation()
        if not settings.get("tokenization",None):
            msg = defauld_field.replace("{{FIELD}}","TOKENIZATION")
            lgr.info(msg)
            settings["tokenization"] = GenerateConfig().addExampleTokenization()
        if not settings.get("file",None):
            msg = defauld_field.replace("{{FIELD}}","FILE")
            lgr.info(msg)
            settings["file"] = GenerateConfig().addExampleFile()
        if not settings.get("columns",None):
            msg = defauld_field.replace("{{FIELD}}","COLUMNS")
            lgr.info(msg)
            settings["columns"] = GenerateConfig().addExampleColumn()
        Folder(self.filename).save(settings)
        return settings
    def run(self):
        if self.createfile:
            if not self.filename:
                self.filename = f"{Folder().getcurrent()}/_settings.json"
            self.update_file(dict())
            return 4
        elif not Folder(self.filename).exists():
            return 1
        else:
            fld = Folder(self.filename)
            settings = self.update_file(fld.read())
        dataframe = dfutils().read(settings)
        for colname,value in settings["columns"].items():
            if value.get("enable",None) == "true":
                Actions(colname,settings,dataframe,self.filename).run(value["actions"])
        return 0