from dsframework.base.trainer import *


class ZIDSCustomDataset(Dataset):
    """! Base class for loading an external custom dataset"""
    x_data = []
    y_data = []

    def __init__(self, x, y):
        self.x_data = x
        self.y_data = y

    def __len__(self):
        return len(self.y_data)

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
