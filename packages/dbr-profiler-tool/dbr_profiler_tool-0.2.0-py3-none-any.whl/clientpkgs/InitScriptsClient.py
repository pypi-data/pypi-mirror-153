import os
import logging
from core.logging_utils import LoggingUtils
from core import wmconstants
from core.dbclient import dbclient

class InitScriptsClient(dbclient):
    def get_allglobalinitscripts_list(self):
        """ 
        Returns an array of json objects for global init sccripts. 
        """
        # fetch all init scripts
        globallist = self.get("/global-init-scripts", version='2.0').get('scripts', [])
        return globallist


