from os.path import exists
from typing import Optional, Union, Any
import csv
from dsframework.base.trainer import *


class ZIDSDataModule(pl.LightningDataModule):
    """! This class inherits from LightningDataModule"""

    def __init__(self, batch_size, seed=42, num_workers=1):
        """! Define required parameters here."""
        super().__init__()
        self.dataset = None
        self.batch_size = batch_size
        self.seed = seed
        self.num_workers = num_workers
        self.dataset = None
        self.ds_train = None
        self.ds_val = None
        self.ds_test = None
        self.ds_predict = None

    def prepare_data(self):
        """! Define steps that should be done on only one GPU, like getting data."""
        pass

    def setup(self, stage: Optional[str] = None) -> None:
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
        pass

    def train_dataloader(self) -> TRAIN_DATALOADERS:
        """! Return DataLoader for Training Data here

        Example:
            @code
            train_split = Dataset(...)
            return DataLoader(train_split)
            @endcode
        """
        return DataLoader(self.ds_train, batch_size=self.batch_size, num_workers=self.num_workers)

    def val_dataloader(self) -> EVAL_DATALOADERS:
        """! Return DataLoader for data validation.

        Example:
            @code
            val_split = Dataset(...)
            return DataLoader(val_split)
            @endcode
        """
        return DataLoader(self.ds_val, batch_size=self.batch_size, num_workers=self.num_workers)

    def test_dataloader(self) -> EVAL_DATALOADERS:
        """! Return DataLoader for data testing.

        Example:
            @code
            val_split = Dataset(...)
            return DataLoader(test_split)
            @endcode
        """
        return DataLoader(self.ds_test, batch_size=self.batch_size, num_workers=self.num_workers)

    def predict_dataloader(self) -> EVAL_DATALOADERS:
        return DataLoader(self.ds_predict, batch_size=self.batch_size)

    def teardown(self, stage: Optional[str] = None) -> None:
        """! Called at the end of fit(train + validate), validate, test, or predict.
            called on every process in DDP
        """
        pass

    def load_dataset(self, file_path, file_type, remove_header=True):
        """! Loads an external dataset, NOT FINISHED YET."""
        if file_type == 'csv':
            with open(file_path) as csv_file:
                self.dataset = list(csv.reader(csv_file))

        return self.dataset

    def parse_dataset(self, remove_header) -> Union[Any, Any]:
        """! Parse your data here, it needs to return x, y.
            Returns:
                x: dataset
                y: target

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

