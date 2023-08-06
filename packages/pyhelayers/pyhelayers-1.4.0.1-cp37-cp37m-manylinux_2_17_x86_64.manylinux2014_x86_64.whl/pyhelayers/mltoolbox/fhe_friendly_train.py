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

import os
os.environ["LOG_LEVEL"]="DEBUG" #DEBUG,INFO,WARNING,ERROR,FATAL,CRITICAL
import numpy as np
import torch
from torch.optim.lr_scheduler import ReduceLROnPlateau
import pyhelayers.mltoolbox.he_dl_lib.poly_activations as poly_activations
from pyhelayers.mltoolbox.utils.util import get_optimizer
from pyhelayers.mltoolbox.he_dl_lib.my_logger import get_logger


logger = get_logger()


def calc_relu_ratio(start_epoch: int, epoch: int, change_round: int):
    """Calculates the required ratio of the new activation in the smooth replacement strategy, based on current epoch

    Args:
        start_epoch (int): number of epoch when the replacement started
        epoch (int): current epoch number
        change_round (int): number of epochs for full replacement

    Returns:
        int: change index (relevant only for args.replace_all_at_once=False, when on each change_round a single activation is replaced, for args.replace_all_at_once=True the only possible change_index is 0 )
        float: ratio
        
    """
    change_progress = float(epoch - start_epoch) / change_round
    change_index = int(change_progress)
    change_ratio = change_progress - change_index

    return change_index, change_ratio



def init_distillation_model(args):
    """Loads the distillation model, if it was specified in user arguments

    Args:
        args (Arguments): user arguments
    """
    if args.distillation_path:
        logger.info(f"Loading distillation model from {args.distillation_path}")
        
        chk_point = {}
        if args.cuda:
            chk_point = torch.load(os.path.join(args.distillation_path))
        else:
            chk_point = torch.load(os.path.join(args.distillation_path), map_location=torch.device('cpu'))

        args.distillation_model = chk_point['model']
    else:
        args.distillation_model = None



def set_seed(args):
    """Impose reproducibility

    Args:
        args (Arguments): user arguments
    """
    seed = args.seed
    torch.manual_seed(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)

    if args.cuda:
        torch.cuda.manual_seed_all(seed)


def init(args):
    if args.cuda:
        logger.info("Visible gpu devices: " + os.environ["CUDA_VISIBLE_DEVICES"])

    # coefficients scale for trainable poly activation
    assert isinstance(args.coeffs_scale, list)
    logger.info(f"loaded coeffs_scale is {args.coeffs_scale}")

    init_distillation_model(args)

    # set seed for  reproducibility
    set_seed(args)


def replace_all_activations(model, activation_gen, args):
    """Replaces relu activations in a non-smooth manner, either all at once or one by one

    Args:
        model(nn.Module) : Input model
        activation_gen (lambda): A lambda fumction to generate the required activation
        args (Arguments): user arguments

    Raises:
        Exception: There are no ReLU activations to replace - check configuration and the model

    Returns:
        ReduceLROnPlateau: Handles reduction of learning rate when a metric has stopped improving
        torch.optim: optimizer
        bool: Number of epochs to wait before next change
        bool: True if no more Relu activations remained in the model
    """
    new_activations = poly_activations.replace_relu_activations(model, activation_gen, args.replace_all_at_once)
    
    if len(new_activations) == 0: #if no replacement was performed 
        raise Exception("There are no ReLU activations to replace - check configuration and the model")

    if args.cuda:
        model = model.cuda()
    logger.info(model)
    logger.info(f"restart optimizer and scheduler for activation {new_activations}")
    optimizer = get_optimizer(args, model)
    scheduler = ReduceLROnPlateau(optimizer, factor=0.5, patience=2, min_lr=args.min_lr, verbose=True)
    wait_before_change = args.change_round

    is_complete = False
    if len(poly_activations.get_relu_activations(model)) == 0:  # there are no more relu activations to replace
        logger.info("All changes completed")
        is_complete = True

    return scheduler, optimizer, wait_before_change, is_complete


def replace_activations_smooth(model, activation_gen, start_epoch, epoch, wait_before_change, optimizer, scheduler, args):
    """Replaces relu activations in a smooth manner

    Args:
        model (nn.Module): the input model
        activation_gen (lambda): A lambda function to generate the required activation
        start_epoch (int): start epoch
        epoch (int): current epoch
        wait_before_change (int): _description_
        optimizer (torch.optim): optimizer
        scheduler (ReduceLROnPlateau): scheduler
        args (Arguments): user arguments

    Returns:
        bool: True if no more Relu activations remained in the model
    """
    change_index, change_ratio = calc_relu_ratio(start_epoch + wait_before_change, epoch, args.change_round)
    new_activations, is_missing = poly_activations.create_or_update_weighted_activations(model, activation_gen,
                                                                                         change_index, change_ratio,
                                                                                         args.replace_all_at_once)
    if len(new_activations) == 0: #if no replacement was performed 
        logger.info(f"Transition phase: {change_index}:{change_ratio}" )
    else:
        if args.cuda:
            model = model.cuda()
        for name, activation in new_activations:
            # add new parameters to optimizer and scheduler
            optimizer.add_param_group({'params': activation.parameters(), 'lr': args.lr_new})
            scheduler.min_lrs.append(args.min_lr)
        logger.info(model)
        logger.debug(optimizer)
        logger.info(f"Started changing {change_index} with ratio {change_ratio}")

    is_complete = False
    if is_missing:
        logger.info("All changes completed")
        is_complete = True

    return is_complete


def replace_activations(args, model, activation_gen, start_epoch, epoch, wait_before_change, optimizer, scheduler):
    """Handles the entire replacement logic - depending on the arguments values and current epoch

    Args:
        args (object): The user arguments
        model (torch.nn.Module): Input model
        activation_gen (func): Function to generate activation
        start_epoch (int): Should be 0 at the first time the function is called, and the sequential calls should pass the start_epoch value that was returned by previous call
        epoch (int): The current training epoch
        wait_before_change (int): The epoch number, when the replacement of Relu activations should begin
        optimizer (Optimizer): Optimizer
        scheduler (ReduceLROnPlateau): Learning rate reduction schedualer

    Returns:
        boolean: True if no Relue activations left in the model, False otherwise
        int: This value should be used in subsequent call to this function
        int: number of epochs until next replacement will take place (relevant for non smooth not-all-at-ance)
        
    Example:
        >>> wait_before_change=5
        >>> is_complete, start_epoch, wait_before_change = replace_activations(args, model, activation_gen, 0, 0, wait_before_change, optimizer, scheduler)
        >>> is_complete, start_epoch, wait_before_change = replace_activations(args, model, activation_gen, start_epoch, 1, wait_before_change, optimizer, scheduler)
    """
    # condition to start activation modification
    act_change_needed = (args.activation_type != 'relu')
    is_time_to_change = (epoch > start_epoch + wait_before_change)

    if not act_change_needed:
        return True, start_epoch, wait_before_change  # done

    if act_change_needed and is_time_to_change:
        # two main cases - smooth and not smooth
        # 1 - smooth
        if args.smooth_transition:
             is_complete = replace_activations_smooth(model, activation_gen, start_epoch, epoch, wait_before_change, optimizer, scheduler, args)
        # 2 - not smooth
        else: 
            scheduler, optimizer, wait_before_change, is_complete = replace_all_activations(model, activation_gen, args)
            start_epoch = epoch

        return is_complete, start_epoch, wait_before_change
    return False, start_epoch, wait_before_change
