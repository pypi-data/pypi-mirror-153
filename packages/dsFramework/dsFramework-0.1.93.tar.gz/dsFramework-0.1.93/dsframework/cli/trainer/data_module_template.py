from typing import Optional, Union
import numpy as np
from dsframework.base.trainer import *
from trainer.custom_dataset import generatedProjectNameCustomDataset


class generatedClass(ZIDSDataModule):
    """! Template for a Data Module, this is where we return the correct dataloader for every dataset:
    training, validation and test."""

    def __init__(self, data_path: str = '',
                 file_type='csv',
                 batch_size_train: int = 32,
                 batch_size_eval: int = 32,
                 seed=42,
                 num_workers=1,
                 dataset: Union[Dataset, generatedProjectNameCustomDataset] = None,
                 test_set: Union[Dataset, generatedProjectNameCustomDataset] = None,
                 test_set_out_of_dataset: bool = False,
                 split_percent=0.8):
        super().__init__(batch_size_train)
        self.data_path = data_path
        self.file_type = file_type
        self.batch_size_train = batch_size_train
        self.batch_size_eval = batch_size_eval
        self.seed = seed
        self.num_workers = num_workers
        self.split_percent = split_percent
        self.train_valid_len = 0
        self.train_valid_set = dataset
        self.valid_set = None
        self.train_set = None
        self.test_set = test_set
        self.test_set_out_of_dataset = test_set_out_of_dataset

    def prepare_data(self):
        """! Define steps that should be done on only one GPU, like getting data."""

        if self.data_path != '':
            ds_x, ds_y = self.parse_dataset(super().load_dataset(self.data_path, self.file_type))
            self.train_valid_set = generatedProjectNameCustomDataset(ds_x, ds_y)

    def setup(self, stage: Optional[str] = None):
        """! Make assignments here (val/train/test split)
                called on every process in DDP
                Define steps that should be done on
                every GPU, like splitting data, applying
                transform etc.


            Example:
                @code
                # Assign train/val datasets for use in dataloaders:
                if stage in (None, "fit"):
                    mnist_full = MNIST(self.data_dir, train=True, transform=self.transform)
                    self.ds_train, self.ds_val = random_split(mnist_full, [55000, 5000])

                # Assign test dataset for use in dataloader(s):
                if stage in (None, "test"):
                    self.ds_test = MNIST(self.data_dir, train=False, transform=self.transform)

                @endcode
            """
        if self.test_set is None and self.test_set_out_of_dataset:
            self.train_valid_set, self.test_set = self.split_dataset(self.train_valid_set, self.seed, train_size_percent=self.split_percent)

        if stage in (None, "fit") and self.train_valid_set is not None:
            self.train_set, self.valid_set = self.split_dataset(self.train_valid_set, self.seed, train_size_percent=self.split_percent)

    def train_dataloader(self):
        """! Return DataLoader for Training Data here

        Example:
            @code
            train_split = Dataset(...)
            return DataLoader(train_split)
            @endcode
        """
        return DataLoader(self.train_set, batch_size=self.batch_size_train, num_workers=self.num_workers)

    def val_dataloader(self):
        """! Return DataLoader for data validation.

        Example:
            @code
            val_split = Dataset(...)
            return DataLoader(val_split)
            @endcode
        """
        return DataLoader(self.valid_set, batch_size=self.batch_size_eval, num_workers=self.num_workers)

    def test_dataloader(self):
        """! Return DataLoader for data testing.

        Example:
            @code
            val_split = Dataset(...)
            return DataLoader(test_split)
            @endcode
        """
        return DataLoader(self.test_set, batch_size=self.batch_size_eval, num_workers=self.num_workers)

    def split_dataset(self, dataset, seed, train_size_percent):
        """! Splits the data based on specified percentage."""

        self.train_valid_len = len(dataset)
        len_train = int(self.train_valid_len * train_size_percent)
        len_val_test = self.train_valid_len - len_train

        return random_split(dataset, [len_train, len_val_test], generator=torch.Generator().manual_seed(seed))

    def parse_dataset(self, remove_header):
        """! Here you need to parse your dataset, return the dataset and target.

        Example:
            @code{.py}
            if remove_header:
                self.dataset = self.dataset[1:]

            x = np.array(self.dataset, dtype=np.float32)[:, :-1]
            y = np.array(self.dataset, dtype=np.float32)[:, -1].reshape(-1, 1)

            return x, y
            @endcode
        """
        raise Exception("Not implemented exception (parse_dataset).")
