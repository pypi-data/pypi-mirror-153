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

from sklearn.model_selection import train_test_split
from torch.utils.data import Subset
import torch
from torchvision import transforms, datasets
from pyhelayers.mltoolbox.data_loader.dataset_wrapper import DatasetWrapper
from pyhelayers.mltoolbox.he_dl_lib.my_logger import get_logger
from pyhelayers.mltoolbox.data_loader.ds_factory import DSFactory

logger = get_logger()


class AddGaussianNoise(object):
    def __init__(self, mean, std):
        self.std = std
        self.mean = mean

    def __call__(self, tensor):
        return tensor + torch.randn(tensor.size()) * self.std + self.mean

    def __repr__(self):
        return self.__class__.__name__ + '(mean={0}, std={1})'.format(self.mean, self.std)


class AddUniformNoise(object):
    def __init__(self, range=6):
        self.range = range

    def __call__(self, tensor):
        return tensor + torch.FloatTensor(tensor.size()).uniform_(-self.range, self.range)

    def __repr__(self):
        return self.__class__.__name__ + '(range={0})'.format(self.range)


def per_image_standardization(image):
    """
    This function creates a custom per image standardization
    transform which is used for data augmentation.
    params:
        - image (torch Tensor): Image Tensor that needs to be standardized.

    returns:
        - image (torch Tensor): Image Tensor post standardization.
    """
    # get original data type
    orig_dtype = image.dtype
    # compute image mean
    image_mean = torch.mean(image, dim=(-1, -2, -3))
    # compute image standard deviation
    stddev = torch.std(image, axis=(-1, -2, -3))
    # compute number of pixels
    num_pixels = torch.tensor(torch.numel(image), dtype=torch.float32)
    # compute minimum standard deviation
    min_stddev = torch.rsqrt(num_pixels)
    # compute adjusted standard deviation
    adjusted_stddev = torch.max(stddev, min_stddev)

    # normalize image
    image -= image_mean
    image = torch.div(image, adjusted_stddev)

    # make sure that image output dtype  == input dtype
    assert image.dtype == orig_dtype

    return image


noise_transform_dict = {
                        'gaussian': [AddGaussianNoise(0, 1)],
                        'gaussian_3.2': [AddGaussianNoise(0, 3.2)],
                        'gaussian_2.2': [AddGaussianNoise(0, 2.2)],
                        'gaussian_10': [AddGaussianNoise(0, 10)],
                        'uniform_6': [AddUniformNoise(6)],
                        'uniform': [AddUniformNoise(1)],
                        'None': []
}



class Cifar10Dataset(DatasetWrapper):
    """A wrapper to the standard Cifar10 dataset, available at torchvision.datasets.CIFAR10. The current wrapper class supplyes
    the required transformations and augmentations, and also implements the required DatasetWrapper methods
    
    """
    def __init__(self, resize=False, data_path ='cifar_data', normalization_mode="per_dataset", augmentation="HFlip", input_noise="None"):
        assert normalization_mode in ["per_image", "per_dataset"]
        assert augmentation in ["HFlip", "None"]

        norm = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

        test_transformations = [
            transforms.ToTensor(),
            norm
        ]

        if resize:
            test_transformations = [transforms.Resize(256), transforms.CenterCrop(224)] + test_transformations

        self.path = data_path


        augment_transform = [
                                transforms.RandomHorizontalFlip(),  # FLips the image w.r.t horizontal axis
                                transforms.RandomRotation(10),  # Rotates the image to a specified angel
                                transforms.RandomAffine(0, shear=10, scale=(0.8, 1.2)),  # Performs actions like zooms, change shear angles.
                                transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),  # Set the color params
                            ]

        train_transformations = list([*augment_transform, *test_transformations])


        transform_test = transforms.Compose(test_transformations + noise_transform_dict[input_noise]) # for the end od the transform
        transform_train = transforms.Compose(train_transformations + noise_transform_dict[input_noise])

        self._train_data =  self.__get_dataset("train", transform_train,  path=data_path)
        self._test_data, self._val_data =  self.__test_val_dataset(transform_test, path=data_path, val_split=0.5)

    def get_class_labels_dict(self):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    
    def is_imbalanced(self):
        """Always returns False - Cifar10 dataset is balanced"""
        return False

    def get_train_data(self):
        """Returns the training data"""
        return self._train_data

    def get_test_data(self):
        """Returns the test data"""
        return self._test_data

    def get_val_data(self):
        """Returns the validation data"""
        return self._val_data


    def get_samples_per_class(self, ds):
        """Returns the number of samples in each class. 
        The Cifar10 dataset has the same number of images in each class.
        params:
                - dataset (VisionDataset): The dataset
        returns:
                - list<int>: the number of samples in each class.
        """
        assert (isinstance(ds, datasets.CIFAR10))
        data_len = len(ds)
        return  [data_len / 10] * 10



    def __test_val_dataset(self, transform, path, val_split=0.5):
        """Splits the data and returns validation and test sets"""
        ds = datasets.CIFAR10(root=path, train=False, download=True, transform=transform)

        test_idx, val_idx = train_test_split(list(range(len(ds))), test_size=val_split, random_state=42)
        val_ds = Subset(ds, val_idx)
        test_ds = Subset(ds, test_idx)

        val_ds.LABEL2NAME_DICT = ds.class_to_idx
        test_ds.LABEL2NAME_DICT = ds.class_to_idx

        return val_ds, test_ds


    def __get_dataset(self, mode, transform,  path):
        """returns the torchvision.datasets.CIFAR10 dataset"""
        ds = datasets.CIFAR10(root=path, train=(mode == 'train'), download=True, transform=transform)
        return ds


@DSFactory.register('CIFAR10')
class Cifar10Dataset_32(Cifar10Dataset):
    def __init__(self, path ='cifar_data', args = None, **kwargs):
        add_input_noise = getattr(args, 'add_input_noise', 'None')
        super(Cifar10Dataset_32,self).__init__(False, path, input_noise=add_input_noise)

@DSFactory.register('CIFAR10_224')
class Cifar10Dataset_224(Cifar10Dataset):
    def __init__(self, path ='cifar_data', args = None, **kwargs):
        add_input_noise = getattr(args, 'add_input_noise', 'None')
        super(Cifar10Dataset_224, self).__init__(True, path, input_noise=add_input_noise)