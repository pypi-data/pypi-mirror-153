import os
import logging
from core.logging_utils import LoggingUtils
from core import wmconstants
from core.dbclient import dbclient

class LibrariesClient(dbclient):
    def get_libraries_status_list(self):
        """ 
        Returns an array of json objects for library status
        """
        # fetch all libraries
        librariesList = self.get("/libraries/all-cluster-statuses", version='2.0').get('statuses', [])
        return librariesList

