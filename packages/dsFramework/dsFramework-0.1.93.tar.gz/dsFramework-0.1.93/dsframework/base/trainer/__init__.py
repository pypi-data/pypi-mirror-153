# ======= Torch imports =========
import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset, IterableDataset, random_split, get_worker_info
import torchmetrics
from torchvision import transforms, datasets
import pytorch_lightning as pl
from pytorch_lightning import Callback
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import LightningLoggerBase
from pytorch_lightning.accelerators import Accelerator
from pytorch_lightning.profiler import BaseProfiler
from pytorch_lightning.strategies import Strategy
from pytorch_lightning.plugins import PLUGIN_INPUT
from pytorch_lightning.utilities.types import (
    STEP_OUTPUT,
    EPOCH_OUTPUT,
    EVAL_DATALOADERS,
    TRAIN_DATALOADERS
)

# ======== DSF imports ========
from dsframework.base.trainer.optimizers import Optimizers
from dsframework.base.trainer.model.model import ZIDSModel
from dsframework.base.trainer.torch_module import ModuleBase
from dsframework.base.trainer.data.data_module import ZIDSDataModule
from dsframework.base.trainer.data.custom_dataset import ZIDSCustomDataset
from dsframework.base.trainer.data.iterable_dataset import ZIDSIterableDataset
from dsframework.base.trainer.model.n_network import ZIDSNetwork
# from dsframework.base.trainer.dataset_classes.custom_dataset_implemented import CustomDataset

# tensorboard --logdir=dsframework/cli/trainer/lightning_logs
#TODO
# Configuration class
