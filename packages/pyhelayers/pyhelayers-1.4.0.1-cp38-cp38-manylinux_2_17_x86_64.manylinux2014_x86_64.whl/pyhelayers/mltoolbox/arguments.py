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
import json

class Arguments:
     """This class defines the user arguments object, and sets the default values for some parameters"""
     def __init__(self, model, dataset_name, classes, batch_size, num_epochs, root_path):
         self.model = model
         self.dataset_name = dataset_name
         self.classes = classes
         self.batch_size = batch_size
         self.num_epochs = num_epochs
         self.root_path = root_path #path to dataset
         
         #defaults:
         self.device=0  #gpu device
         self.seed=123  #select seed number for reproducibility
         self.lr=0.001  #learning rate
         self.cuda=False
         self.opt='adam'
         self.save='outputs/mltoolbox/'                     #path to checkpoint save directory
         self.save_freq=-1                        #how frequently save checkpoint
         self.pooling_type="max"  #max or average pooling, choices=('max', 'avg')
         self.activation_type="relu"   #activation type', choices=('non_trainable_poly','approx_relu', '20_relu', 'relu', 'square', 'softplus', 'trainable_2nd'))
         self.debug_mode=False         #breaks a training epoch after loading only a few batches.
         self.replace_all_at_once=False   #changes the activation layers at once or layer by layer
         self.epoch_to_start_change=3     #epoch number to start changing the activation function
         self.change_round=3              #number of epochs per change
         self.smooth_transition=True      #change each activation layer in a smooth change or at once
         self.gradient_clip=-1.0          #gradient clipping value
         self.change_bn_or_add=True
         self.bn_before_activation=False
         self.no_conv_pad=False
         self.log_string='lenet_cifar10_notebook'
         self.from_checkpoint=''
         self.coeffs_scale=[[0.1, 0.1],[1.,1.]]  #coefficients scale for trainable poly activation optionally including initial value of coefs
         self.distillation_path=""               #path for a distillation model file
         self.distillationT=10.0
         self.distillation_alpha=0.1
         self.continue_with_nans=False
         self.local_rank=0
         self.ddp=False
         self.distillation_model=None
         self.lr_new=0.0002
         self.validation_freq=1
         self.disable_scheduler=False
         self.min_lr = 1e-5         # minimal learning rate for scheduler
         
     def dump_to_file(self, path):
        with open(os.path.join(path, 'training_arguments.json'), 'w') as f:
            json.dump(self.__dict__, f, indent=2, default=lambda x: str(type(x)))