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
from datetime import datetime
import numpy as np
import torch
import torch.optim as optim
import warnings
from pyhelayers.mltoolbox.he_dl_lib.my_logger import get_logger
import csv


logger = get_logger()


def create_log_title(args, date_str: str, uniq_id: str):
    """Convinience function that creates a string of most of the arguments, together with date and unique-id
    This can be used to distinguish the run
    Args:
            args (Arguments): The user arguments
            date_str (String): A string representing the current date and time in 'Ymd_HM' format
            uniq_id (String): Some unique id
    Returns:
        String: the generated string
    """
    arg_list = []

    arg_list.append(f"{date_str}")
    arg_list.append(uniq_id)

    if args.log_string is not '':
        if args.log_string.find('-') > -1:
            warnings.warn("args.log_string cannot contain '-'. changes to '_' instead.")
            args.log_string = args.log_string.replace('-', '_')

        arg_list.append(args.log_string)

    arg_list.append(f"{args.pooling_type}pool")
    arg_list.append(f"{args.activation_type}")

    if args.replace_all_at_once:
        arg_list.append("at_once")
    else:
        arg_list.append(f"round_{args.change_round}")

    if args.epoch_to_start_change > 0:
        arg_list.append(f"replace_epoch_{args.epoch_to_start_change}")

    if args.smooth_transition:
        arg_list.append('smooth')

    if args.change_bn_or_add:
        arg_list.append("change_bn")

    if args.bn_before_activation:
        arg_list.append("bn_on_conv")

    arg_list.append(f"lr_{args.lr}")

    if args.gradient_clip is not -1.0:
        arg_list.append(f"grad_clip_{args.gradient_clip}")

    #if args.disable_scheduler:
    #    arg_list.append("no_sched")

    if args.activation_type == 'trainable_2nd':
        if len(args.coeffs_scale) == 2:
            if args.coeffs_scale[1] != [1., 1., 1., 1.]:
                coeffs_list = '_'.join(str(e) for e in args.coeffs_scale[1])
                arg_list.append(f"coeffs_[{coeffs_list}]")

    arg_list.append(f"{args.classes}_classes")
    arg_list.append(f"batch_{args.batch_size}")

    if args.no_conv_pad:
        arg_list.append("no_conv_pad")

    if hasattr(args, 'add_input_noise') and not(args.add_input_noise == "None"):
        arg_list.append(f"noise_{args.add_input_noise}")

    if args.distillation_path is not "":
        arg_list.append(f"dist_T_{args.distillationT}")
        arg_list.append(f"dist_{args.distillation_alpha}")

    arg_list.append(f"seed_{args.seed}")

    arg_list.append(args.dataset_name)

    log_title = '-'.join(arg_list)

    return log_title


def has_nan(tensor: torch.Tensor):
    """Returns Tensor(True) if the input tensor has any Nan values, and Tensor(False) otherwise

    Args:
        tensor (Tensor): tensor

    Returns:
        Tensor: Tensor(True) if the input tensor has any Nan values, and Tensor(False) otherwise
    """
    return torch.any(tensor != tensor)


def date_str():
    """Creates a string from the current date

    Returns:
        String: 'Ymd_HM' string
    """
    return datetime.utcnow().strftime('%Y%m%d_%H%M')


def load_checkpoint(args):
    """Loads the checkpoint into memory, if the args.from_checkpoint is set to a valid checkpoint path

    Args:
        args (Arguments): user arguments

    Returns:
        nn.Module: saved model
        torch.optim:  optimizer
        SimpleNamespace: train_state
        float: loss
        MetricsTracker: metrics
        bool: is_complete state (should be True if there are no Relu activations in the model)
    """
    checkpoint = torch.load(os.path.join(args.from_checkpoint))
    model = checkpoint['model']
    # because the updates of optimizer create new groups, the "optimizer.load_state_dict" doesn't work
    try:
        optimizer = checkpoint['optimizer']
    except Exception as e:
        logger.info(f"Loading optimizer from checkpoint process failed - using default {e}")
        optimizer = get_optimizer(args, model)

    train_state = checkpoint['train_state']
    loss = checkpoint.get("loss", 1000)
    metrics = checkpoint['metrics']

    is_complete = checkpoint["is_complete"]

    # hacking to enable overwrite checkpoint start_epoch and wait_before_change (e.g., for case of direction change)
    if args.epoch_to_start_change < 0:
        train_state.start_epoch = -args.epoch_to_start_change
        train_state.wait_before_change = 0

    return model, optimizer, train_state, loss, metrics, is_complete


def save_checkpoint(chp: set, path: str, filename: str):
    """Saves the input checkpoint chp into a file

    Args:
        chp (set): state object
        path (String): path location to save to
        filename (String): filename prefix
    """
    file_name = os.path.join(path, filename + '_checkpoint.pth.tar')
    logger.info(file_name)
    torch.save(chp, file_name)


def save_model(model: torch.nn.Module, is_complete: bool, optimizer, args, metrics, epoch: int, train_state, best_pred_loss: float, confusion_matrix):
    """Saves the model and other train-state related parameters into a file

    Args:
        model (nn.Module): model to save
        is_complete (bool): is_complete state
        optimizer (torch.optim): optimizer
        args (Arguments): user arguments
        metrics (MetricsTracker): current metrics
        epoch (int): trsining epoch
        train_state (SimpleNamespace): train state
        best_pred_loss (float): best loss value found by now in current training (rellevant only if the model is fully FHE friendly - has no Relu activations)
        confusion_matrix (_type_): confusion matrix

    Returns:
        float: best loss is updated
    """
    if args.local_rank != 0: return

    loss = metrics.get_avg('loss')
    save_path = args.save
    os.makedirs(save_path, exist_ok=True)

    args.dump_to_file(save_path)

    save_model = model
    if args.cuda:
        save_model = model.module
    if args.save_freq != 0:
        state = {'train_state': train_state,
                 'model': save_model,
                 'optimizer': optimizer,
                 'metrics': metrics.get_avg('loss'),
                 'loss': loss,
                 'is_complete': is_complete}
        
        #mark checkpoint as best (possible only if the model is fully FHE friendly)
        if (loss < best_pred_loss) and is_complete:        
            best_pred_loss = loss
            save_checkpoint(state,
                            path=save_path, filename=args.model + "_best")
            np.save(os.path.join(save_path, 'best_confusion_matrix.npy'), confusion_matrix)

        elif args.save_freq == -1:  # overwrite last checkpoint each period
            save_checkpoint(state,
                            save_path, args.model + f"_last")
        if args.save_freq > 0:  # write checkpoint for a given freq only
            if epoch % args.save_freq == 0:
                save_checkpoint(state,
                                save_path, args.model + f"_curr{epoch:03}")

        return best_pred_loss



def postproc_model(args, is_complete: bool, rank: int = 0):
    """post-procces an FHE friendly model to replace any WeightedRelu activations by the actual activation

    Args:
        args (Arguments): user arguments
        is_complete (bool): True if the model is fully FHE friendly
        rank (int, optional): local rank, if DDP is used. Defaults to 0.
    """
    if rank!=0:
        return

    if not is_complete:
        logger.info("The activation replacement has not completed, hence no best model to post-process.")
        return

    save_path = args.save
    os.makedirs(save_path, exist_ok=True)

    #load best model
    checkpoint = torch.load(os.path.join(save_path, args.model + "_best_checkpoint.pth.tar"))
    #convert activations
    checkpoint['model'].post_process_activations()

    #save modified model as new file
    save_checkpoint(checkpoint, path=save_path, filename=args.model + "_postproc")


def read_filepaths(file):
    paths, labels = [], []
    with open(file, 'r') as f:
        lines = f.read().splitlines()

        for line in lines:
            if ('/ c o' in line):
                break
            try:
                splitted_line = line.split(' ')
                if len(splitted_line) == 4:
                    subjid, path, label, source =splitted_line
                else: # for sirm
                    subjid = splitted_line[0] + ' ' + splitted_line[1]
                    path, label,source = splitted_line[2:]
            except:
                logger.info(f"{file} {splitted_line}")
            paths.append(path)
            labels.append(label)
    return paths, labels



def get_optimizer(args, model: torch.nn.Module):
    """Return the user defined optimizer object

    Args:
        args (Arguments): user arguments
        model (nn.Module): model

    Returns:
        torch.optim: optimizer object
    """
    weight_decay=1e-7
    if args.opt == 'sgd':
        return optim.SGD(model.parameters(), lr=args.lr, momentum=0.5, weight_decay=weight_decay)
    elif args.opt == 'adam':
        return optim.Adam(model.parameters(), lr=args.lr, weight_decay=weight_decay)


def print_summary(args, epoch: int, num_samples: int, metrics, mode: str):
    """Prints the epoch summary

    Args:
        args (Arguments): user arguments
        epoch (int): epoch number
        num_samples (int): number of processed sumples
        metrics (MetricsTracker): current metrics
        mode (String): "Train"/"Test"/"Validation"
    """
    msg = (
    f'\n {mode}:\n EPOCH: {epoch}\t'
    f'Samples: {num_samples}\t'
    f'Loss: {metrics.get_avg("loss"):.4f}\t'
    f'Accuracy: {metrics.get_avg("accuracy"):.2f}\t'
    f'Top5_Acc: {metrics.get_avg("top_5_acc"):.2f}\n'
    )

    logger.info(msg)


def accuracy(output: torch.Tensor, target: torch.Tensor):
    """Accuracy classification score. This metric computes the number of times where the correct label is equal to the predicted label

    Args:
        output (list): List of predictions
        target (list): True labels
    Returns:
        int: number of correct predictions
        int: number of samples
        float: The top-1 accuracy score
    """
    '''returns: number of correct classifications, total number of clussifications, accuracy (correct divided by total)'''
    samples = len(target)
    
    with torch.no_grad():
        pred = torch.argmax(output, dim=1)
        correct = torch.sum(pred == target).item()
        
    return correct, samples, correct / samples


def top_k_acc(output: torch.Tensor, target: torch.Tensor, k: int =3):
    """Top-k Accuracy classification score. 
    This metric computes the number of times where the correct label is among the top k labels predicted (ranked by predicted scores)

    Args:
        output (list): List of predictions
        target (list): True labels
        k (int, optional): Number of most likely outcomes considered to find the correct label. Defaults to 3.

    Returns:
        float: top_k accuracy: The top-k accuracy score
    """
    if output.shape[1] < k:
        k = 1

    with torch.no_grad():
        pred = torch.topk(output, k, dim=1)[1]
        correct = 0
        for i in range(k):
            correct += torch.sum(pred[:, i] == target).item()
        
    return correct / len(target)
    
                
    
def write_to_csv(rowData: list, dir: str, fname: str, header:list =[]):
    """Write data row into CSV file

    Args:
        rowData (list): data
        dir (String): path to write to
        fname (String): file name
        header (list, optional): headers row. Defaults to [].
    """
    os.makedirs(dir, exist_ok=True)
    full_path = os.path.join(dir, fname)
    
    with open(full_path, 'a+') as f:
        writer = csv.writer(f, delimiter=',')
        
        file_is_empty = os.stat(full_path).st_size == 0
        if file_is_empty and header is not '':
            writer.writerow(header)
            
        writer.writerow(rowData)
