import logging
from datalad_lgpdextension.utils.dataframe import Dataframe

lgr = logging.getLogger('datalad.lgpdextension.lgpd_extension.runner.operations')

class Operations:
    def __init__(self, dataframe:Dataframe):
        setattr(Operations, 'dataframe', dataframe)
    def run(self, settings):
        lgr.info("run to " + str(settings))
        operations = [x for x in settings.keys()]
        for op in operations:
            self.select(op,settings[op])
    def select(self,operation,value):
        lgr.info("select to " + operation)
        if operation == "upper":
            self.dataframe.upper(),
        elif operation == "lower":
            self.dataframe.lower(),
        elif operation == "toInt":
            self.dataframe.toInt(),
        elif operation == "toFloat":
            self.dataframe.toFloat(),
        elif operation == "toNumeric":
            self.dataframe.toNumeric(),
        elif operation == "toPrice":
            self.dataframe.toPrice(value),
        elif operation == "toDate":
            self.dataframe.toDate(value),
        elif operation == "json":
            self.dataframe.json(),
        elif operation == "rangeNumeric":
            self.dataframe.rangeNumeric(value)
        elif operation == "encrypt":
            self.dataframe.encrypt()
        elif operation == "decrypt":
            self.dataframe.decrypt()
        elif operation == "toString":
            self.dataframe.toString()
    @property
    def dataframe(self):
        return self.dataframe