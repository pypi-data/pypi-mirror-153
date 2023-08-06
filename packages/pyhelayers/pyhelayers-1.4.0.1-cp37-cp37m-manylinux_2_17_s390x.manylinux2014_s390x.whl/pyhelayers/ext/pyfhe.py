#
# OCO Source Materials
# 5737-A56
# © Copyright IBM Corp. 2017
#
# The source code for this program is not published or other-wise divested
# of its trade secrets, irrespective of what has been deposited with the
# U.S. Copyright Office.
#

import pyhelayers
import os
import json
from enum import Enum


class MODEL_ARCH(Enum):
    LR = 1
    NN = 2


class PYFHE(object):
    __requirements_setters = {"security": "set_security_level",
                              "integerPartPrecision": "set_integer_part_precision",
                              "fractPartPrecision": "set_fractional_part_precision",
                              "batchSize": "set_batch_size",
                              "modelEncrypted": "set_model_encrypted",
                              "nofixedBatchSize": "set_no_fixed_batch_size",
                              "optTarget": "set_optimization_target",
                              "exhaustiveSearch": "set_exhaustive_search",
                              "maxBatchMemory": "set_max_batch_memory",
                              "maxClientInferenceCpuTime": "set_max_client_inference_cpu_time",
                              "maxClientInferenceMemory": "set_max_client_inference_memory",
                              "maxPredictCpuTime": "set_max_predict_cpu_time",
                              "maxOutputMemory": "set_max_output_memory",
                              "maxModelMemory": "set_max_model_memory",
                              "maxInputMemory": "set_max_input_memory",
                              "maxInitModelCpuTime": "set_max_init_model_cpu_time",
                              "maxContextMemory": "set_max_context_memory",
                              "maxDecryptOutputCpuTime": "set_max_decrypt_output_cpu_time",
                              "maxEncryptInputCpuTime": "set_max_encrypt_input_cpu_time",
                              "maxInferenceCpuTime": "set_max_inference_cpu_time",
                              "maxInferenceMemory": "set_max_inference_memory"
                              }

    def __init__(self, model_architecture, requirements=None, model_file=None, weights_file=None):
        if not isinstance(model_architecture, MODEL_ARCH):
            raise TypeError(
                "The model_architecture parameter should be [MODEL_ARCH.LR | MODEL_ARCH.NN]")

        self.__model_architecture = model_architecture
        if model_file:
            assert(os.path.isfile(model_file))
        if weights_file:
            assert(os.path.isfile(weights_file))
        self.__plain = self.__init_plain(model_file, weights_file)
        self.__init_default_context()
        self.__profile = None
        self.__enc_model = None

        try:
            if os.path.isfile(requirements):
                with open(requirements, 'r') as f:
                    config = json.loads(f.read())
                    self.__requirements = config["optimizer_requirements"]
            else:
                raise FileNotFoundError
        except TypeError:
            self.__requirements = requirements
        print(f"User model architecture is {self.__model_architecture}")
        print(f"User requirements are {self.__requirements}")

    def encrypt_model(self):
        profile = self.get_profile()

        if self.__model_architecture == MODEL_ARCH.NN:
            self.__enc_model = pyhelayers.NeuralNet(self.__client_context)
            self.__enc_model.encode_encrypt(self.__plain, profile)
            print('Encrypted NN model ready')
        else:
            self.__enc_model = pyhelayers.LogisticRegression(
                self.__client_context)
            self.__enc_model.encode_encrypt(self.__plain, profile)
            print('Encrypted LR model ready')

        return self.__enc_model

    def encrypt_input(self, plain_samples):
        res = self.get_encrypted_model().encode_encrypt_input(plain_samples)
        print('Prediction data samples has been encrypted')
        return res

    def decrypt_output(self, client_predictions):
        if isinstance(client_predictions, pyhelayers.CTileTensor):
            predictions = client_predictions
        else:
            predictions = pyhelayers.CTileTensor(self.__client_context)
            predictions.load_from_buffer(client_predictions)

        res = self.get_encrypted_model().decrypt_decode_output(predictions)
        print('Prediction results have been decrypted')
        return res

    def init_context(self):
        if self.__profile is None:
            self.__init_profile()

        self.__client_context.init(self.__profile.requirement)
        print('Context ready')

    def __init_default_context(self):
        self.__client_context = pyhelayers.DefaultContext()

    def __init_plain(self, model_file, weights_file):
        if self.__model_architecture == MODEL_ARCH.NN:
            plain = pyhelayers.NeuralNetPlain()
            if model_file:
                plain.init_arch_from_json_file(model_file)
            if weights_file:
                plain.init_weights_from_hdf5_file(weights_file)
            print('NN model loaded into the library')
        else:
            plain = pyhelayers.LogisticRegressionPlain()
            if model_file:
                plain.init_from_json_file(model_file)
            print('LR model loaded into the library')

        return plain

    def __init_profile(self):
        optimizer = pyhelayers.HeProfileOptimizer(
            self.__plain, self.__client_context)

        [getattr(optimizer.get_requirements(), PYFHE.__requirements_setters[req])(self.__requirements[req])
         for req in self.__requirements.keys() if req in PYFHE.__requirements_setters]
        print("Optimizer ready")

        self.__profile = optimizer.get_optimized_profile(False)
        print("Profile ready")

    def get_profile(self):
        if self.__profile is None:
            self.__init_profile()
        return self.__profile

    def get_encrypted_model(self):
        return self.__enc_model if self.__enc_model else self.encrypt_model()

    def init_context_from_buffer(self, context_buffer, secret_key=None):
        self.__init_default_context()
        self.__client_context.load_from_buffer(context_buffer)
        if secret_key:
            self.__client_context.load_secret_key(secret_key)

    def encrypted_model_from_buffer(self, model_buffer):
        if self.__model_architecture == MODEL_ARCH.NN:
            self.__enc_model = pyhelayers.NeuralNet(self.__client_context)
            self.__enc_model.load_from_buffer(model_buffer)
        else:
            self.__enc_model = pyhelayers.LogisticRegression(
                self.__client_context)
            self.__enc_model.load_from_buffer(model_buffer)

        return self.__enc_model

    def get_context(self, secret_key=None):
        if secret_key is None:
            return self.__client_context
        elif secret_key == False:
            return self.__client_context.save_to_buffer()
        else:
            return self.__client_context.save_to_buffer(), self.__client_context.save_secret_key()

    def predict(self, enc_samples):
        prediction = None

        if isinstance(enc_samples, pyhelayers.CTileTensor):
            prediction = self.get_encrypted_model().predict(enc_samples)
        else:
            samples = pyhelayers.CTileTensor(self.__client_context)
            samples.load_from_buffer(enc_samples)
            prediction = self.get_encrypted_model().predict(samples)

        print('Prediction results ready')
        return prediction
