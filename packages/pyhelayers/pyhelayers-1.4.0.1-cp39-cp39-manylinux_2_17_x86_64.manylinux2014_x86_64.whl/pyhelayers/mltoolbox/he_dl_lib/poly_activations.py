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

# Import basic libraries
import numpy as np
import pandas as pd
from collections import OrderedDict

import torch
from torch.autograd import Variable
import torch.nn as nn
from torch.autograd import Function
from torch.nn.parameter import Parameter
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms  # import transformations to use for demo
from torch.autograd import Function
from pyhelayers.mltoolbox.he_dl_lib.my_logger import get_logger

logger = get_logger()

# simply define a square function
def square_activation(input):
    return input ** 2


def poly_activation_non_trainable(x):
    return 0.4439 * (x ** 4) - 0.7768 * (x ** 3) + 0.1401 * x + 0.1437 * (x ** 2)


tryout = 0
'''
Rounding the tensor with a specified precision
prec: number of digits to round off.
model_precision_phase: 'both', 'None', 'test'
'''


def round_noise_activation(x, prec, depth):
    # diff_to_round = torch.round(x * (10 ** prec)) / (10 ** prec) - x
    min_val = 0  # x.min()
    max_val = 1000  # x.max()
    norm_ratio = max_val - min_val
    scale = 2 ** (prec - depth) - 1
    rounded_number = torch.round(scale * (x - min_val) / norm_ratio) * norm_ratio / scale + min_val
    rounded_number = torch.clamp(rounded_number, -max_val, max_val)

    diff_to_round = (rounded_number - x).detach()
    # try:
    #     global tryout
    #
    #     if tryout % 100 == 0:
    #         print('rounding', x[0][0][0][0], (x+diff_to_round)[0][0][0][0])
    #     tryout += 1
    # except:
    #     pass
    return x + diff_to_round


def srelu_poly_activation(input):
    return 0.5 * input + 0.125 * (input ** 2) - 0.0052 * (input ** 4)  # 0.021 * (input ** 2) + 0.3 * input
    #  0.5 * input + 0.125 * (input ** 2) - 0.0052 * (input ** 4)  # for 4th degree


def iterative_sqrt(x, d=2):
    a = x
    b = x - 1

    for n in range(d):
        a = a * (1 - 0.5 * b)
        b = (b ** 2) * 0.25 * (b - 3)

    return a


def forward_iterative_relu(x):
    # return 0.5 * (input + iterative_sqrt(input ** 2, 2))
    # return 0.0625 * (-(x ** 3) - 2 * (x ** 2) + 15 * x + 4)

    # from michael's paper, implementing only f4(x)
    '''9th degree polynomial'''
    # sign_poly = (35. / 128.) * (x ** 9) - (180. / 128.) * (x ** 7) + (378. / 128.) * (x ** 5) - (420. / 128.) * (x ** 3) + (315. / 128.) * x
    '''7th degree'''
    # sign_poly = (-5./16.) * (x**7) + (21./16.) * (x ** 5) -(35./16.) * (x ** 3) + (35./16.) * x
    '''5th degree'''
    # sign_poly = (3./8.) * (x ** 5) -(10/8) * (x ** 3) + (35/16) * x
    '''3th degree'''
    sign_poly = -0.5 * (x ** 3) + 1.5 * x
    comp_x_0 = 0.5 * (sign_poly + 1)

    return x * comp_x_0


#
# def backward_iterative_relu(input):
#     return (input - 1)


# create a class wrapper from PyTorch nn.Module, so
# the function now can be easily used in models
class Square(nn.Module):
    '''
    Applies the Square function element-wise:
        Square(x) = x ** 2
    Shape:
        - Input: (N, *) where * means, any number of additional
          dimensions
        - Output: (N, *), same shape as the input
    '''

    def __init__(self):
        '''
        Init method.
        '''
        super().__init__()  # init the base class

    def forward(self, input):
        '''
        Forward pass of the function.
        '''
        return square_activation(input)  # simply apply already implemented Square


class TrainablePolyReLU(nn.Module):
    '''
    Implementation of soft ReLU activation with trainable params.
    Shape:
        - Input: (N, *) where * means, any number of additional
          dimensions
        - Output: (N, *), same shape as the input
    Parameters:
        - alpha, beta, gamma - trainable parameters
    References:
        - See related paper:
        https://arxiv.org/pdf/1602.01321.pdf
    Examples:
        >>> a1 = TrainablePolyReLU(256)
        >>> x = torch.randn(256)
        >>> x = a1(x)
    '''
    # is_trainable = True

    def __init__(self, coefficients_args=None, max_val=20, trainable=True):
        # def __init__(self, in_features, alpha=None, beta=None, gamma=None):
        '''
        Initialization.
        INPUT:
            - in_features: shape of the input
            - coefficients: trainable parameter. list
        '''
        super(TrainablePolyReLU, self).__init__()
        # if coefficients_scale is None:
        #     coefficients_scale = [0.1, 0.1, -0.001, 0.001]

        assert isinstance(coefficients_args, list)

        if isinstance(coefficients_args[0], list):
            self.coefficients_scale = coefficients_args[0]
            coefficients = coefficients_args[1]
        else:
            self.coefficients_scale = coefficients_args  # torch.tensor(coefficients_scale, requires_grad=False)
            coefficients = [1.] * len(coefficients_args)

        # self.coefficients_scale = torch.tensor(coefficients_scale, requires_grad=False)

        logger.debug(f'parameters: {coefficients_args}')

        # coefficients[0] = 1.
        self.coefficients = Parameter(torch.tensor(coefficients))  # create a tensor out of the coefficients

        self.coefficients.requires_grad = trainable

        self.coefficients_mask = coefficients_args
        # TODO - "self.range" is not used
        self.range = max_val

    def forward(self, x):
        '''
        Forward pass of the function.
        Applies the function to the input elementwise.
        '''
        # print(f'current coefficients:\n{self.coefficients.data}')
        # return 0.02 * (x ** 2) + self.coefficients[0] * x
        # return self.coefficients[0] * (x) + self.coefficients[1] * (x ** 2) + self.coefficients[2] * (x ** 3) + \
        #        self.coefficients[3] * (x ** 4) #+ self.coefficients[4] * (x ** 5) + self.coefficients[5] * (x ** 6)
        res = 0  # torch.zeros(1,1)
        # sum = torch.zeros_like(x)
        for i in range(len(self.coefficients_scale)):
            res += self.coefficients_scale[i] * self.coefficients[i] * (x ** (i + 1))

        # res = torch.clamp(res, -self.range, self.range)
        #
        # diff_to_drop = (res - x).detach()

        return res  # x + diff_to_drop

    def extra_repr(self):
        return 'coefs={}'.format(
            [t.item() for t in self.get_final_coefficients()])

    def get_final_coefficients(self):
        out = []
        for i in range(len(self.coefficients_scale)):
            out.append(self.coefficients_scale[i] * self.coefficients[i])
        return out


class ApproxReLU(nn.Module):
    '''
    Implementation of approximated relu, as suggested at: .
    Shape:
        - Input: (N, *) where * means, any number of additional
          dimensions
        - Output: (N, *), same shape as the input
    References:
        - See related paper:
        https://arxiv.org/pdf/1911.11377.pdf
    '''

    def __init__(self):
        super().__init__()

    def forward(self, x):
        '''
        Forward pass of the function.
        Applies the function to the input elementwise.
        '''
        return 0.000469841857369822 * (x**2) + 0.500000000000008 * x


# create a class wrapper from PyTorch nn.Module, so
# the function now can be easily used in models
class SReLU(nn.Module):
    '''
    Applies the srelu function element-wise:

    Shape:
        - Input: (N, *) where * means, any number of additional
          dimensions
        - Output: (N, *), same shape as the input
    '''

    def __init__(self):
        '''
        Init method.
        '''
        super().__init__()  # init the base class

    def forward(self, input):
        '''
        Forward pass of the function.
        '''
        return srelu_poly_activation(input)


class IterativeReLU(nn.Module):
    '''
    Applies the relu function iteratively:

    Shape:
        - Input: (N, *) where * means, any number of additional
          dimensions
        - Output: (N, *), same shape as the input
    '''

    def __init__(self):
        '''
        Init method.
        '''
        super().__init__()  # init the base class

    def forward(self, input):
        '''
        Forward pass of the function.
        '''
        return forward_iterative_relu(input)  # simply apply already implemented iterative_relu

    # def backward(self, input):
    #     return backward_iterative_relu(input)


class relu_20(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, input):
        return 20.0 * F.relu(input)


class relu_5(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, input):
        return 5.0 * F.relu(input)


class WeightedRelu(nn.Module):
    '''
    Applies the Square function element-wise:

    Shape:
        - Input: (N, *) where * means, any number of additional
          dimensions
        - Output: (N, *), same shape as the input
    '''
    def __init__(self, activation, ratio=0):
        super().__init__()  # init the base class
        self.ratio = ratio
        self.activation = activation

    def extra_repr(self):
        return 'ratio={}'.format(
            self.ratio)

    def forward(self, input):
        # print(f"{torch.flatten(input).shape},{torch.min(input)},{torch.max(input)},{torch.mean(input)},{torch.std(input)}")
        return (self.ratio) * self.activation(input) + (1 - self.ratio) * F.relu(input)


activation_functions_dict = {'relu': lambda x: nn.ReLU(),
                             '20_relu': lambda x: relu_20(),
                             'approx_relu': lambda x: ApproxReLU(),
                             'square': lambda x: Square(),
                             'poly_softplus': lambda x: SReLU(),
                             'trainable_2nd': lambda x: TrainablePolyReLU(x, trainable=True),
                             'trainable_2nd_shared': lambda x: TrainablePolyReLU(trainable=True),
                             'softplus': lambda x: nn.Softplus(),
                             'iterative_relu': lambda x: IterativeReLU(),
                             'non_trainable_poly': lambda x: TrainablePolyReLU(x, trainable=False),
                             'weighted_relu': lambda x, y: WeightedRelu(activation=x, ratio=y)
                             }

def get_activation_gen(activation_type: str, activation_args=None ):
    """Returns the activation function, that can be later used to generate the activation

    Args:
        activation_type (str): Activation name - one of the keys in the activation_functions_dict
        activation_args (Any, optional): Arguments to the activation, e.g coefficients. Defaults to None.

    Returns:
        lambda: A lambda function to generate an activation
    """
    activation_gen = lambda: activation_functions_dict[activation_type](activation_args)
    return activation_gen


# TODO - remove deprecated
def set_activation_layer(model, orig_layer_name, activation_type, ratio, activation_args=None):
    if 0 < ratio < 1:  # TODO: check ratio handling
        activation = activation_functions_dict[activation_type](activation_args)
        weighted_activation = activation_functions_dict['weighted_relu']( activation, ratio)
        setattr(model, orig_layer_name, weighted_activation )
    # elif ratio == 1:
    #     setattr(model, orig_layer_name, activation_functions_dict[activation_type], ratio, activation_args))
    else:  # ratio == 0 / 1
        setattr(model, orig_layer_name, activation_functions_dict[activation_type](activation_args))


def replace_relu_activation(model: nn.Module, activation_type='square', replace_all_at_once = False, ratio=0, activation_args=None):
    """Recursively replaces all relu module to a predefined module.

    Args:
        model (nn.Module): the input model
        activation_type (str, optional): Activation layer name. Defaults to 'square'.
        replace_all_at_once (bool, optional): Replace all at once. Defaults to False.
        ratio (int, optional): Replacement ratio. Defaults to 0.
        activation_args:  Arguments for the activation layer. Defaults to None.

    Returns:
        bool: True if a replacement was performed
    """
    was_relu = False

    for child_name, child in reversed(list(model.named_children())):
        if isinstance(child, nn.ReLU) or isinstance(child, WeightedRelu):
            # if ratio == 1:
            #     set_activation_layer(model, child_name, activation_type, ratio, activation_args)

            set_activation_layer(model, child_name, activation_type, ratio, activation_args)
            was_relu = True
            if not replace_all_at_once:
                return was_relu
        else:
            was_relu |= replace_relu_activation(child, activation_type, ratio, activation_args)
    return was_relu


# TODO - remove deprecated
def replace_relu_activation_for_layer(model, args, ratio, activation_args=None):
    """
    new_activation: Square/WeightedSquare()
    mode1: first/all_at_once
    mode2: non-smooth
    mode3: order

    what to change: only Relu
    Replaces the last non-changed relu activation layer
    :param model:
    :param args: from namespace
    :param activation_args: arguments for the activation layer
    :return:
    """
    if args.model in ['resnet18', 'mobilenet2', 'densenet169', 'alexnet']:
        model_root = model.module.cnn
        layers = list(dict(model_root.named_children()).keys())
    elif args.model.startswith("COVIDNet"):
        model_root = model.module.CovidNet
        layers = list(dict(model_root.named_children()).keys())
    else:
        raise KeyError(f'Unrecognized model name: {args.model}')

    model_changed = False
    for i in range(len(layers)-1, -1, -1):
    # for i in range(len(layers)):
        sub_model = eval(f'model_root.{layers[i]}')
        if layers[i] == 'relu':
            # sub_model = eval(f'model.module.{model_classname}')
            if isinstance(sub_model, nn.ReLU) or isinstance(sub_model, WeightedRelu):
                set_activation_layer(model_root, 'relu', args.activation_type, ratio, activation_args)
                relu_changed = True
        else:
            relu_changed = replace_relu_activation(sub_model, args.activation_type, args.replace_all_at_once, ratio, activation_args)
        if relu_changed:
            model_changed = True
        if relu_changed and not args.replace_all_at_once:
            return True

    return model_changed


def find_modules_by_type(model:nn.Module, m_types:list) -> list:
    """

    @param model: input model
    @param m_types: modules type to find
    @return: the list of (name, module) tuples satisfying the conditions
    """

    if not isinstance(m_types,list):
        m_types = [m_types]
    check_if_belong_to_types = lambda x: any([isinstance(x,m) for m in m_types])
    filt_modules = [(name,module) for name, module in model.named_modules() if check_if_belong_to_types(module)]
    return filt_modules


def get_module_by_name(model, name):

    """

    @param model: input model
    @param name: name of module string or list of name parts
    @return: the detected module
    """
    module = model
    if isinstance(name, str):
        name = name.split(".")

    for name_part in name:
        module = getattr(module,name_part)
    return module


def change_module(model:nn.Module, name:str, new_module:nn.Module):

    """

    @param model: input module
    @param name: full path for module to replace
    @param new_module: the new module name
    """
    if isinstance(name, str):
        name_parts = name.split(".")
    elif isinstance(name, list):
        name_parts = name
    else:
        raise Exception(f"Wrong input type {type(name)}")

    parent_module = get_module_by_name(model, name_parts[:-1])
    local_name = name_parts[-1]
    setattr(parent_module, local_name, new_module)


def _set_weighted_activation(model, name, activation, ratio):
    """
    @param model: input model
    @param name: module to be replaced
    @param activation: new activation
    @param ratio: ratio of new activation
    """
    w_activaton = WeightedRelu(activation, ratio=ratio)
    assert not isinstance(get_module_by_name(model,name), WeightedRelu), \
        "the module is already of type WeightedRelu"
    change_module(model, name, w_activaton)
    return w_activaton


def get_relu_activations(model):
    relu_activations = find_modules_by_type(model, [nn.ReLU])
    return relu_activations

def replace_relu_activations(model, activation_gen, replace_all_at_once = False) -> list:
    """
    @param model: input model
    @param activation_gen: function to generate activation
    @param replace_all_at_once: if true all activation should be replaced, otherwise only first
    @return the list of (name, activations) tuples of created activations
    """

    relu_activations = get_relu_activations(model)
    new_activations = []
    if len(relu_activations) == 0:
        return []
    if replace_all_at_once:
        for name, _ in relu_activations:
            new_activation = activation_gen()
            change_module(model, name, new_activation)
            new_activations.append((name,new_activation))
    else:
        index = -1
        name = relu_activations[index][0]
        new_activation = activation_gen()
        change_module(model, name, new_activation)
        new_activations.append((name, new_activation))
    return new_activations


def create_or_update_weighted_activations(model, activation_gen,
                                          change_index, change_ratio,
                                          replace_all_at_once)->(list, bool):

    """

    @param model: input model
    @param activation_gen: function to generate activation
    @param change_index: index of activation to be replaced or updated
    @param change_ratio: the ratio of new activation
    @param replace_all_at_once: if true all activation should be replaced, otherwise only first
    @return: list of (name, module) tuples of created activations and
            boolean indicating if the change_required index exceed the available list of  activations
    """
    activations_init = find_modules_by_type(model, [nn.ReLU, WeightedRelu])

    activations = []
    # to skip activations when ReLu is part of WeightedRelu
    for name, activation in activations_init:
        potential_parent_name = name.split(".")[:-1]
        potential_parent_module = get_module_by_name(model,potential_parent_name)
        if not isinstance(potential_parent_module,WeightedRelu):
            activations.append((name, activation))

    new_activations =[]
    is_missing = False

    if replace_all_at_once:
        # for replace_all_at_once by finishing the first cycle all activation should replaced with weight =1
        if change_index > 0:
            change_ratio = 1
            is_missing = True

        for name, activation in activations:
            if isinstance(activation, WeightedRelu):
                activation.ratio = change_ratio
            else:
                w_activaton = _set_weighted_activation(model,name,activation_gen(),ratio=change_ratio)
                new_activations.append((name, w_activaton))
    else:
        activations = activations[-1::-1]

        if change_index >= len(activations):
            is_missing = True
            # to make sure all previous activations are changed
            change_index = len(activations)
        else:
            target_name, target_activation = activations[change_index]
            if isinstance(target_activation, nn.ReLU):
                w_activaton = _set_weighted_activation(model, target_name, activation_gen(), ratio=change_ratio)
                new_activations.append((target_name, w_activaton))
            else:
                assert isinstance(target_activation, WeightedRelu)
                target_activation.ratio = change_ratio

        # validate/update all previous activations
        for _i in range(change_index):
            name, activation = activations[_i]
            if not isinstance(activations[_i][1], WeightedRelu):
                logger.debug(f"warning: previous activation[{_i}] {name} is not WeightedRelu ({activation}) - replacing with")
                w_activaton = _set_weighted_activation(model, name, activation_gen(), ratio=1.0)
                new_activations.append((name, w_activaton))
            elif activation.ratio < 1.0:
                logger.debug(f"warning: previous activation[{_i}] {name} ratio ({activation.ratio}) - replacing with ratio = 1.0")
                activation.ratio = 1.0

    return new_activations,is_missing
