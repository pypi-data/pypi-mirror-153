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

from pyhelayers.mltoolbox.he_dl_lib.my_logger import get_logger
from pyhelayers.mltoolbox.model.alexnet_fhe import alexnet_fhe
from pyhelayers.mltoolbox.model.lenet5 import Lenet5
from pyhelayers.mltoolbox.model.squeezenetchet import SqueezeNetCHET
from pyhelayers.mltoolbox.model.squeezenet import SqueezeNet1_0_FHE, SqueezeNet1_1_FHE
logger = get_logger()


def get_model(classes:int, model: str, pooling_type: str, add_bn: bool):
    """Returns the required model, based on model name

    Args:
        classes (int): number of classes
        model (str): model name
        pooling_type (str): 'max' | 'avg'
        add_bn (bool): True if batch normalization should be automatically added to the model

    Returns:
        nn.Module: The required model
    """
    if model == 'alexnet':
        return alexnet_fhe(classes, pooling_type, add_bn)
    elif model == 'lenet5':
        return Lenet5(classes)
    elif model == 'squeezenet_CHET':
        return SqueezeNetCHET(num_classes=classes)
    elif model == 'squeezenet1_0':
        return SqueezeNet1_0_FHE(classes, pooling_type, add_bn)
    elif model == 'squeezenet1_1':
        return SqueezeNet1_1_FHE(classes, pooling_type, add_bn)
    else:
        logger.error(f"Unsupported model name {model}")
        return None
    
def get_model_by_name(args):
    """Returns one of the predefined models, by the user configuration

    Args:
        args (Arguments): user arguments

    Raises:
        NameError: "Model doesn't exist"

    Returns:
        nn.Module: The required model
    """
    if args.model in ['lenet5', 'alexnet', 'squeezenet_CHET','squeezenet1_0','squeezenet1_1']:
        return get_model(args.classes, args.model, args.pooling_type, args.change_bn_or_add)
    else:
        raise NameError(f"Model name: {args.model} doesn't exist.")
