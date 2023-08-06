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

from types import SimpleNamespace
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm

from pyhelayers.mltoolbox.he_dl_lib.distillation import nd_loss
from pyhelayers.mltoolbox.utils.util import accuracy, top_k_acc
from pyhelayers.mltoolbox.utils import util
from pyhelayers.mltoolbox.utils.util import print_summary, get_optimizer, load_checkpoint
from pyhelayers.mltoolbox.utils.metrics_tracker import MetricsTracker
from pyhelayers.mltoolbox.utils.cf_matrix import make_confusion_matrix
import numpy as np
import threading
from pyhelayers.mltoolbox.he_dl_lib.my_logger import get_logger
from pyhelayers.mltoolbox.he_dl_lib.timers import Timer
from pyhelayers.mltoolbox.data_loader.ds_factory import DSFactory
from pyhelayers.mltoolbox.model.DNN_factory import get_model_by_name

##this imports cause the standard datasets to get registered into factory
from pyhelayers.mltoolbox.data_loader.cifar10_dataset import Cifar10Dataset_32, Cifar10Dataset_224
from pyhelayers.mltoolbox.data_loader.covidCT_dataset import CovidCTDataset
from pyhelayers.mltoolbox.data_loader.covidXray_dataset import CovidXrayDataset
from pyhelayers.mltoolbox.data_loader.places205_dataset import places205Dataset

from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP


def get_train_state(start_epoch: int, epoch: int, wait_before_change: int):
    """Returns a namespace that groupps the passed in arguments together

    Args:
        start_epoch (int): the start epoch
        epoch (int): the current epoch
        wait_before_change (int): the number of epochs until next change

    Returns:
        SimpleNamespace: a namespace that groupps the passed in arguments together
    """
    return SimpleNamespace(start_epoch=start_epoch, epoch=epoch, wait_before_change=wait_before_change)
    
class Trainer:
    """This class represents a training object, that has all the needed components for a training, like dataLoaders, optimizer, model etc.
    
    """
    def __get_normed_weights(self, args, datasetSplit):
        """For an imbalanced dataset, returns a list of weights, to be used to normalize the data distribution. 
        For an imbalanced dataset, the samples_per_cls attribute should contain a list of integers, representing the number of samples 
        in each of the classes. 

        Args:
            args (Arguments): user arguments
            datasetSplit (dataLoader.dataset): The data to be normalized

        Returns:
            list<float>: A list of weights
        """
        if self.ds.is_imbalanced():
            samples_per_class = np.array(self.ds.get_samples_per_class(datasetSplit))

            normed_weights = 1.0 / samples_per_class
            normed_weights = normed_weights / normed_weights.sum()

            return torch.FloatTensor(normed_weights).cuda(args.local_rank if args.ddp else  None)
        return None

    def get_train_state(self):
        """Returns the train state

        Returns:
            SimpleNamespace: train state
        """
        return self.train_state
    
    def get_was_completed(self):
        """Returns the completion state

        Returns:
            bool: the completion state
        """
        return self.was_completed
    
    def get_model(self):
        """Returns the model to be trained

        Returns:
            nn.model: the model to be trained
        """
        return self.model
        
    def get_optimizer(self):
        """Returns the optimizer of the training

        Returns:
            optimizer: the optimizer of the training
        """
        return self.optimizer
    
    def get_loss(self):
        """Returns the current loss 

        Returns:
            float: the current loss 
        """
        return self.loss
           
           
    def __init__(self, args):
        """Initializes the model, optimizer and data generators, based on user defined arguments

        Args:
            args (Arguments): user defined arguments
        """
        self.logger = get_logger()
        if args.from_checkpoint:
            self.model, self.optimizer, self.train_state, self.loss, metrics, self.was_completed = load_checkpoint(args)
        else:
            self.was_completed = False
            self.model = get_model_by_name(args)
            self.optimizer = get_optimizer(args, self.model)
            if args.activation_type == 'relu':
                args.epoch_to_start_change = 1000

            start_epoch = 0
            epoch = 0
            self.loss = 1000.0
            self.train_state = get_train_state(start_epoch, epoch, args.epoch_to_start_change)
        self.logger.info(self.train_state)

        self.ds = DSFactory.get_ds(args.dataset_name, classes=args.classes, path=args.root_path, args=args)
        print(self.ds)
        train_data = self.ds.get_train_data()
        val_data = self.ds.get_val_data()
        test_data = self.ds.get_test_data()
        self.logger.debug("----train,val,test-------")
        self.logger.debug(len(train_data))
        self.logger.debug(len(val_data))
        self.logger.debug(len(test_data))
        self.logger.debug("-----------")

        train_params = {'batch_size': args.batch_size,
                        'shuffle': False,#True,
                        'num_workers': 4,
                        'pin_memory': True,
                        'drop_last': True
                        }
        test_params = {'batch_size': args.batch_size,
                    'shuffle': False,
                    'num_workers': 4,
                    'pin_memory': True,
                    'drop_last': True
                    }
        if args.ddp:
            torch.cuda.set_device(args.local_rank)
            self.model = DDP(self.model.cuda(args.local_rank)) 
            train_sampler = DistributedSampler(train_data,shuffle=True)
            train_params['sampler'] = train_sampler
            #if the test is ddp, use dist.all_gather and dist.all_gather_object to gather results from all instances
            #test_sampler = DistributedSampler(test_data,shuffle=False)
            #test_params['sampler'] = test_sampler
        elif args.cuda:
            self.model = nn.DataParallel(self.model).cuda()
            train_params['shuffle'] = True
        

        self.training_generator = DataLoader(train_data, **train_params)
        self.val_generator = DataLoader(val_data, **test_params)
        self.test_generator = DataLoader(test_data, **test_params)



    def train_step(self, args, epoch: int, t: tqdm):
        """performs a single train step (a single forward and backward pass)

        Args:
            args (Arguments): user arguments
            epoch (int): _description_
            t (tqdm): training progress

        Raises:
            Exception: Exit because of NaNs, if Nan values are present in the output, and args.continue_with_nans=False

        Returns:
            MetricsTracker: metrics
            np.array: confusion matrix
        """
        timer_train = Timer("train")
        timer_postproc = Timer("postproc")
        timer_batch = Timer("batch")
        timer_fwd_bp_batch = Timer("fwd_bp_batch")
        timer_misc_in_batch = Timer("misc_in_batch")
        timer_acc_in_batch = Timer("acc_in_batch")
        timer_dist_in_batch = Timer("dist_in_batch")

        timers = [timer_train, timer_postproc,timer_batch,timer_fwd_bp_batch,timer_misc_in_batch,
                timer_acc_in_batch,timer_dist_in_batch]
        timer_train.start()
        self.model.train()

        confusion_matrix = torch.zeros((args.classes, args.classes), dtype=int)
        normed_weights = self.__get_normed_weights(args, self.training_generator.dataset)

        criterion = nn.CrossEntropyLoss(reduction='mean', weight=normed_weights)

        metric_ftns = ['loss', 'accuracy', 'top_5_acc']
        train_metrics = MetricsTracker(*[m for m in metric_ftns], mode='train')
        train_metrics.reset()

        sum_correct = 0.0
        sum_total = 0.0
        sum_loss = 0.0
        sum_acc = 0.0
        sum_top5_acc = 0.0
        preds = []
        gt = []

        self.logger.debug(f"Starting training epoch {epoch}")
        timer_batch.start()
        for batch_idx, input_tensors in enumerate(self.training_generator):
            if args.debug_mode:
                if batch_idx > 10:
                    break
            timer_fwd_bp_batch.start()
            self.optimizer.zero_grad()
            timer_fwd_bp_batch.stop()
            input_data, target = input_tensors
            timer_misc_in_batch.start()
            if args.cuda:
                input_data = input_data.cuda(args.local_rank if args.ddp else  None)
                target = target.cuda(args.local_rank if args.ddp else  None)
            timer_misc_in_batch.stop()
            timer_fwd_bp_batch.start()
            output = self.model(input_data)
            timer_fwd_bp_batch.stop()
            timer_misc_in_batch.start()
            if util.has_nan(output):
                self.logger.info(f"Nans in training {epoch}/{batch_idx} {(output != output).any(axis=1).sum()}")
                if not args.continue_with_nans:
                    raise Exception("Exit because of NaNs")
            timer_misc_in_batch.stop()
            timer_fwd_bp_batch.start()
            max_output = output.abs().max()
            loss = criterion(output, target)
            if args.distillation_model:
                timer_dist_in_batch.start()
                in_t = args.distillation_model(input_data)
                timer_dist_in_batch.stop()
                loss = loss + args.distillation_alpha * nd_loss(output, in_t, T=args.distillationT)
            timer_misc_in_batch.start()
            timer_fwd_bp_batch.stop()
            sum_loss += loss.item()
            timer_misc_in_batch.stop()
            timer_fwd_bp_batch.start()
            loss.backward()

            if args.gradient_clip > 0:
                torch.nn.utils.clip_grad_value_(self.model.parameters(), args.gradient_clip)

            self.optimizer.step()
            timer_fwd_bp_batch.stop()

            timer_acc_in_batch.start()
            correct, total, acc = accuracy(output, target)
            _, preds_t = torch.max(output, 1)
            top_5_acc = top_k_acc(output, target, 5)

            gt.extend(target)
            preds.append(preds_t)

            sum_acc += acc
            sum_correct += correct
            sum_total += total
            sum_top5_acc += top_5_acc

            num_samples = batch_idx * args.batch_size + 1

            t.set_description('T {} loss={:.3f}, acc={:.3f}, avr_acc={:.0f}, max_out={:.2f}, top5={:.2f}'.
                            format(batch_idx, loss, acc, sum_correct / float(num_samples) ,max_output, top_5_acc))
            timer_acc_in_batch.stop()

        timer_batch.stop()
        timer_postproc.start()
        self.logger.debug(f"Finished training epoch {epoch}")
        preds = torch.cat(preds).cpu()

        for t, p in zip(gt, preds):
            confusion_matrix[t.long(), p.long()] += 1

        train_metrics.update_all({
                                        'loss': sum_loss/(batch_idx+1),
                                        'accuracy': sum_acc/(batch_idx+1),
                                        'top_5_acc': sum_top5_acc / (batch_idx + 1)
                                        })
        print_summary(args, epoch, num_samples, train_metrics, mode="Training")
        confusion_matrix_numpy = confusion_matrix.cpu().numpy()
        timer_train.stop()
        timer_postproc.stop()

        for timer in timers:
            self.logger.debug(f"{timer.name} - {timer.report()}")

        return train_metrics, confusion_matrix_numpy

    def test(self, args, epoch: int):
        return self.__validation( args, self.test_generator, epoch, mode='test')
    
    def validation(self, args, epoch: int):
         return self.__validation(args, self.val_generator, epoch, mode='val')
            
    def __validation(self, args, dataGenerator, epoch: int, mode: str ='val'):
        """tests the model on the given data

        Args:
            args (Arguments): user arguments
            dataGenerator (dataLoader): the data to test the model
            epoch (int): epoch number
            mode (str, optional): A short label (can be 'test' or 'val') . Defaults to 'val'.

        Raises:
            Exception: Exit because of NaNs, if Nan values are present in the output, and args.continue_with_nans=False

        Returns:
            MetricsTracker: metrics
            np.array: confusion matrix
        """
        self.logger.debug(f"Start {mode} phase")
        self.model.eval()

        normed_weights = self.__get_normed_weights(args, dataGenerator.dataset)

        criterion = nn.CrossEntropyLoss(reduction='mean', weight=normed_weights)

        metric_ftns = ['loss', 'accuracy', 'auc', 'auc-pneumonia', 'auc-negative', 'auc-covid', 'top_5_acc']
        val_metrics = MetricsTracker(*[m for m in metric_ftns], mode=mode)
        val_metrics.reset()
        confusion_matrix = torch.zeros(args.classes, args.classes, dtype=int)

        sum_correct = 0.0
        sum_total = 0.0
        sum_loss = 0.0
        sum_acc = 0.0
        sum_top5_acc = 0.0
        gt = []
        pred_probs = []
        preds = []

        self.logger.debug("Start validation batch loop")
        with torch.no_grad():
            for batch_idx, input_tensors in enumerate(dataGenerator):
                input_data, target_l = input_tensors
                target = target_l
                if (args.cuda):
                    input_data = input_data.cuda(args.local_rank if args.ddp else  None)
                    target = target_l.cuda(args.local_rank if args.ddp else  None)

                output = self.model(input_data)
                if util.has_nan(output):
                    self.logger.warning(f"Nans in {mode}  {epoch}/{batch_idx}")
                    if not args.continue_with_nans:
                        raise Exception("Exit because of NaNs")
                    return val_metrics, confusion_matrix

                loss = criterion(output, target)
                sum_loss += loss.item()

                correct, total, acc = accuracy(output, target)
                sum_acc += acc
                sum_correct += correct
                sum_total += total
                top_5_acc = top_k_acc(output, target, 5)
                sum_top5_acc += top_5_acc

                num_samples = batch_idx * args.batch_size + 1
                _, preds_t = torch.max(output, 1)
                pred_probs_t = nn.functional.softmax(torch.clamp(output, max=20))
                preds.append(preds_t)
                pred_probs.append(pred_probs_t)
                gt.extend(target_l)

            self.logger.debug("Done validation batch loop")
            preds = torch.cat(preds).cpu()
            for t, p in zip(gt, preds):
                confusion_matrix[t.long(), p.long()] += 1

            self.logger.debug("Threading to make_confusion_matrix start")


            values_to_update_dict = {'loss': sum_loss / (batch_idx + 1),
                                    'accuracy': sum_acc / (batch_idx + 1),
                                    'top_5_acc': sum_top5_acc / (batch_idx + 1)
                                    }
            val_metrics.update_all(values_to_update_dict)
        print_summary(args, epoch, num_samples, val_metrics, mode=mode)
        confusion_matrix_numpy = confusion_matrix.cpu().numpy()

        self.logger.debug('Confusion Matrix\n{}'.format(confusion_matrix_numpy))
        return val_metrics, confusion_matrix_numpy