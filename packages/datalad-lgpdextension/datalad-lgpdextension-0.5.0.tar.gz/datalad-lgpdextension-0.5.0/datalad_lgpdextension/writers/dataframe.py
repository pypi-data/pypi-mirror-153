import logging
import pandas as pd
from datalad_lgpdextension.writers.csv import Csv
from datalad_lgpdextension.writers.parquet import Parquet

lgr = logging.getLogger('datalad.lgpdextension.lgpd_extension.writers.dataframe')

class Dataframe:
    def read(self, settings):
        lgr.info("Reading path to " + str(settings["file"].get("format",'None')))
        if settings["file"].get("format",None) == "csv":
            return Csv(settings["file"]).read()
        elif settings["file"].get("format",None) == "parquet":
            return Parquet(settings["file"]).read()
        return None
    def write(self, dataframe, settings):
        lgr.info("Writing dataframe to " + str(settings.get("format",'None')))
        if settings["file"].get("format",None) == "csv":
            return Csv(settings["file"]).write(dataframe)
        elif settings["file"].get("format",None) == "parquet":
            return Parquet(settings["file"]).write(dataframe)
        return None