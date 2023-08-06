#
# OCO Source Materials
# 5737-A56
# © Copyright IBM Corp. 2017
#
# The source code for this program is not published or other-wise divested
# of its trade secrets, irrespective of what has been deposited with the
# U.S. Copyright Office.
#

try:
    from .pyfhemlimpl import KerasNNRequest, SKLearnLRRequest
    from .replace import replace
except ImportError:
    from .pyfhecommon import AbstractMLComputationRequest, SKLearnConfigHandler, KerasMLConfigHandler

from .pyfhe import PYFHE as pyfhe, MODEL_ARCH
