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

import torch.nn as nn

class TrainingDebug:
    def __init__(self, writer):
        self.__writer = writer
        self.__old_data = {}
        self.__old_data_batch = {}
        self.__batch_id = 0

    def batch_end(self,model, acc, scalars_only=True):
        self.__batch_id +=1
        nparams = model.named_parameters()
        for name, tensor in nparams:

            self.__writer.add_scalar(f"debug/train_batch_acc", acc, self.__batch_id)

            # self.__writer.add_histogram(name + "_batch_val", tensor.data, self.__batch_id)
            self.__writer.add_scalar(f"debug/{name}_batch_val_max", tensor.data.detach().max(), self.__batch_id)
            self.__writer.add_scalar(f"debug/{name}_batch_val_min", tensor.data.detach().min(), self.__batch_id)
            self.__writer.add_scalar(f"debug/{name}_batch_val_abs", tensor.data.detach().abs().max(), self.__batch_id)

            if not scalars_only:
                if name in self.__old_data_batch:
                    diff = (tensor.data - self.__old_data_batch[name]).detach()
                    self.__writer.add_scalar(f"debug/{name}_diff_max", diff.max(), self.__batch_id)
                    self.__writer.add_scalar(f"debug/{name}_diff_min", diff.min(), self.__batch_id)
                    self.__writer.add_histogram(name + "_batch_diff", diff, self.__batch_id)
                self.__old_data_batch[name] = tensor.data.detach().clone()
                if hasattr(tensor, "grad"):
                    self.__writer.add_scalar(f"debug/{name}_grad_max", tensor.grad.detach().max(), self.__batch_id)
                    self.__writer.add_scalar(f"debug/{name}_grad_min", tensor.grad.detach().min(), self.__batch_id)

                    self.__writer.add_histogram(name + "_batch_grad", tensor.grad, self.__batch_id)



    def epoch_end(self, model, optimizer, epoch):
        # histogram values and gradients of all parameters
        nparams = model.named_parameters()
        for name, tensor in nparams:
            self.__writer.add_histogram(name+ "_val", tensor.data, epoch)
            if name in self.__old_data:
                self.__writer.add_histogram(name + "_diff", tensor.data - self.__old_data[name], epoch)
            self.__old_data[name] = tensor.data.detach().clone()
            if hasattr(tensor, "grad"):
                self.__writer.add_histogram(name + "_grad", tensor.grad, epoch)
        for _id, ogroup in enumerate(optimizer.param_groups):
            self.__writer.add_scalar(f"debug/lr{_id}", ogroup["lr"], epoch)

class OutputTracer():

    def __init__(self):
        self.results = []
        self.hooks = []

    def hook_fn(self,m, i, o):
        self.results.append((m, i, o))


    def register_hooks(self, net):
        for name, layer in net._modules.items():
            # If it is a sequential, don't register a hook on it
            # but recursively register hook on all it's module children
            if isinstance(layer, nn.Sequential) or len(layer._modules)>0:
                self.register_hooks(layer)
            else:
                hook = layer.register_forward_hook(lambda m,i,o: self.hook_fn(m,i,o))
                self.hooks.append(hook)

    def unregister_hooks(self):
        for hook in self.hooks:
            hook.remove()
        self.hooks=[]

    def show_max(self):
        for _id, elm in enumerate(self.results):
            print(_id, elm[0], elm[1][0].abs().max(), elm[2][0].abs().max(), len(elm[1]), len(elm[2]))


