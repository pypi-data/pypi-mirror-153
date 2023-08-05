from dsframework.base.trainer import *


class generatedClass(ZIDSCustomDataset):
    """! Template for loading an external custom dataset"""
    def __init__(self, x_ds, y_ds):
        super().__init__(x_ds, y_ds)
