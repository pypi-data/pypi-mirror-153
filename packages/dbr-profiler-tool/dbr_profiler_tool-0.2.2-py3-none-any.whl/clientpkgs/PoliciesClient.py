import os
import logging
from core.logging_utils import LoggingUtils
from core import wmconstants
from core.dbclient import dbclient

class PoliciesClient(dbclient):
    def get_policies_list(self):
        """ 
        Returns an array of json objects for policies
        """
        # fetch all policies
        poolsList = self.get("/policies/clusters/list", version='2.0').get('policies', [])
        return poolsList


