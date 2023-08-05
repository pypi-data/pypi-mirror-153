from dsframework.base.trainer import *


class ZIDSIterableDataset(IterableDataset):
    """! This is the base class for iterable datasets, override __iter__ method."""

    def __init__(self, data):
        self.data_source = data

    def __iter__(self):
        return self.data_source


def worker_init_fn(worker_id):
    pass
