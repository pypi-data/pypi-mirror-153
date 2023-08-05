from dsframework.base.trainer import *
from abc import ABC, abstractmethod


class ModuleBase(ABC, nn.Module):
    """! Base class for a module inherits from torch nn.module."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def forward(self, x):
        pass
