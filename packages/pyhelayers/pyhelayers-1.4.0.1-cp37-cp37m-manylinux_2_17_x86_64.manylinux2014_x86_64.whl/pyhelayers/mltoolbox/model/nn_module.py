'''
MIT License

Copyright (c) 2020 International Business Machines

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from torch import tensor
import torch.nn as nn
import pyhelayers.mltoolbox.he_dl_lib.poly_activations as poly_activations

class nn_module(nn.Module):
    def __init__(self):
            super(nn_module, self).__init__()


    def set_max_pooling_to_avg(self):
        """ Replaces each max-pooling by an average-pooling 
        """
        maxpool_activations = poly_activations.find_modules_by_type(self.cnn, nn.MaxPool2d)

        for i, (name, module) in enumerate(maxpool_activations):
            target_pooling = nn.AvgPool2d(module.kernel_size, module.stride, module.padding,
                                          ceil_mode=module.ceil_mode)
            poly_activations.change_module(self.cnn, name, target_pooling)


    def add_batch_norm_after_conv(self):
        """Adds batch normalization after each convolutional layer
        """
        conv_activations = poly_activations.find_modules_by_type(self.cnn, nn.Conv2d)

        for i, (name, module) in enumerate(conv_activations):
            conv_with_bn = nn.Sequential(nn.Conv2d(module.in_channels, module.out_channels,
                                                                   module.kernel_size, module.stride,
                                                                   module.padding),
                                                                   nn.BatchNorm2d(module.out_channels))
            poly_activations.change_module(self.cnn, name, conv_with_bn)


    def add_batch_norm_before_conv(self):
        """Adds batch normalization before each convolutional layer, except for the first one
        """
        conv_activations = poly_activations.find_modules_by_type(self.cnn, nn.Conv2d)

        for i, (name, module) in enumerate(conv_activations):
            if i > 0:
                conv_with_bn = nn.Sequential(nn.BatchNorm2d(module.in_channels), nn.Conv2d(module.in_channels,
                                                                                           module.out_channels,
                                                                                           module.kernel_size,
                                                                                           module.stride,
                                                                                           module.padding))
                poly_activations.change_module(self.cnn, name, conv_with_bn)



    class bn_info:
        """Defines a layer data element for adding batch normalization after a layer
        """
        def __init__(self, after_layer_name: str, channels: int):
            """
            Args:
                after_layer_name (str): Name of the layer, after which the batch normalization should be added
                channels (int): batch normalization channels
            """
            self.after_layer_name = after_layer_name
            self.channels = channels


    # adds bn after pooling.
    def addBatchNormAfterActivation(self, bn_info):
        """Adds batch normalization after specific layers, specified by the user

        Args:
            bn_info (list[bn_info]): list of layers after which batch normalization should be added
        """
        for info in bn_info:
            module = poly_activations.get_module_by_name(self.cnn, info.after_layer_name)
            poly_activations.change_module(self.cnn, info.after_layer_name,
                                           nn.Sequential(module, nn.BatchNorm2d(info.channels)))




    @staticmethod
    def get_pooling_by_type(type):
        dict = {
            'avg': nn.AvgPool2d,
            'max': nn.MaxPool2d
        }
        return dict[type]

    def make_fhe_friendly(self, add_bn: bool, pooling_type: str = 'max', bn_list=None):
        """Applies changes to the given model towards making it FHE-Friendly. This is the first step. The model may still contain Relu activations after the call to this function.

        Args:
            add_bn (bool): If True batch normalization will be added
            pooling_type (str, optional): Required pooling type: 'avg' or 'max'. Average pooling is considered FHE-Friendly, Max is not. Defaults to 'max'.
            bn_list (list[bn_info], optional): If not None - the batch normalization will be added after the specified layers, if None the batch normalization will be added after each convolutional layer . Defaults to None.
        """
        if add_bn:
            if bn_list:
                self.addBatchNormAfterActivation(bn_list)
            else:
                self.add_batch_norm_after_conv()

        if not pooling_type == 'max':
            self.set_max_pooling_to_avg()

    def assertSize(self, x: tensor):
        """Asserts the required image size for the model

        Args:
            x (tensor): data tensor

        Raises:
            Exception: Please resize the images to the matching size
        """
        inputSize=f'{x.shape[2]}*{x.shape[3]}'
        if (inputSize!=self.INPUT_SIZE):
            raise Exception (f' Model expects images of size {self.INPUT_SIZE}. Please resize the images to the matching size')
        
    def post_process_activations(self):
        """Replaces each WeightedRelu activation in the given model, by the WeightedRelu.activation:
        
        Example: 
            WeightedRelu( ratio=1.0
                (activation): TrainablePolyReLU(coefs=[0.09679805487394333, 0.13760216534137726]))

            will be replaced by the plain

            TrainablePolyReLU(coefs=[0.09679805487394333, 0.13760216534137726])
        """
        activations = poly_activations.find_modules_by_type(self.cnn, poly_activations.WeightedRelu)
        for name, module in activations:
            poly_activations.change_module(self.cnn, name, module.activation)