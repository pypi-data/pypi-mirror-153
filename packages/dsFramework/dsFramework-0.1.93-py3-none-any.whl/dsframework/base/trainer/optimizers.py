from enum import Enum
from dsframework.base.trainer import *


class Optimizers(Enum):
    """! Wraps the most commonly used optimization algorithm. Direct usages of the optimizer is possible using
    torch.optim. class.
    """
    SGD = (torch.optim.SGD,)
    Adam = (torch.optim.Adam,)
    Adadelta = (torch.optim.Adadelta,)
    Adagrad = (torch.optim.Adagrad,)
    AdamW = (torch.optim.AdamW,)
    SparseAdam = (torch.optim.SparseAdam,)  # Implements lazy version of Adam algorithm suitable for sparse tensors.
    Adamax = (torch.optim.Adamax,)  # Implements Adamax algorithm (a variant of Adam based on infinity norm).
    ASGD = (torch.optim.ASGD,)  # Implements Averaged Stochastic Gradient Descent.
    LBFGS = (torch.optim.LBFGS,)
    NAdam = (torch.optim.NAdam,)
    RAdam = (torch.optim.RAdam,)
    RMSprop = (torch.optim.RMSprop,)
    Rprop = (torch.optim.Rprop,)  # Implements the resilient backpropagation algorithm.

    def __call__(self, *args, **kwargs):
        return self.value[0](*args, **kwargs)
