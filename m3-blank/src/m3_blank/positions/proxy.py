# coding: utf-8
u""" Module description. 
"""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

# 3rdparty
from django.db import models

# Recordpack
from recordpack.provider import BaseProxy

#------------------------------------------------------------------------------
# Proxies
#------------------------------------------------------------------------------

class PositionListProxy(BaseProxy):
    def load(self, root):
        self.from_root()
