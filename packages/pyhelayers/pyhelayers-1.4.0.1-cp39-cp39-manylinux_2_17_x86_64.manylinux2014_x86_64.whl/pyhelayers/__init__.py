#
# OCO Source Materials
# 5737-A56
# © Copyright IBM Corp. 2017
#
# The source code for this program is not published or other-wise divested
# of its trade secrets, irrespective of what has been deposited with the
# U.S. Copyright Office.
#

from .libs.pyhelayers import *
import os
if 'HELAYERS_RESOURCES_DIR' not in os.environ:
    os.environ['HELAYERS_RESOURCES_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)) , "resources")
