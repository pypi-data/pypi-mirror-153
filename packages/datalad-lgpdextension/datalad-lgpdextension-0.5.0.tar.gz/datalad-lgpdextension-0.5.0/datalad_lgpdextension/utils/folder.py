import os
import sys
import shutil
import json
import logging

lgr = logging.getLogger('datalad.lgpdextension.lgpd_extension.utils.folder')

class Folder:
    def __init__(self, path=None):
        self.path = path
    @classmethod
    def getcurrent(self):
        return os.getcwd()
    @classmethod
    def updatevalue(self,element):
        js = element["obj"]
        js[element["key"]] = element["value"]
        return js
    def read(self):
        content = ""
        with open(self.path, 'r') as openfile:
            content = json.load(openfile)
        return content
    def save(self,settings):
        output = json.dumps(settings, indent = 4)
        with open(self.path, "w") as file:
            file.write(output)
        return True
    def exists(self):
        return os.path.exists(self.path)
    def copy(self,sourcepath,destpath):
        shutil.copyfile(sourcepath,destpath)