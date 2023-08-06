#
# OCO Source Materials
# 5737-A56
# © Copyright IBM Corp. 2017
#
# The source code for this program is not published or other-wise divested
# of its trade secrets, irrespective of what has been deposited with the
# U.S. Copyright Office.
#

from ..pyfhecommon import AbstractMLComputationRequest, SKLearnConfigHandler, KerasMLConfigHandler
from ..pyfhe import MODEL_ARCH


class SKLearnLRRequest(AbstractMLComputationRequest):
    def __init__(self, model, requirements={}):
        with SKLearnConfigHandler(model) as config:
            AbstractMLComputationRequest.__init__(
                self, MODEL_ARCH.LR, config.get_model(), None, requirements)

    def _AbstractMLComputationRequest__predict(self, enc_model, enc_samples):
        return enc_model.predict(enc_samples)


class KerasNNRequest(AbstractMLComputationRequest):
    def __init__(self, model, requirements={}):
        with KerasMLConfigHandler(model) as config:
            AbstractMLComputationRequest.__init__(
                self, MODEL_ARCH.NN, config.get_model(), config.get_weights(), requirements)

    def _AbstractMLComputationRequest__predict(self, enc_model, enc_samples):
        return enc_model.predict(enc_samples)
