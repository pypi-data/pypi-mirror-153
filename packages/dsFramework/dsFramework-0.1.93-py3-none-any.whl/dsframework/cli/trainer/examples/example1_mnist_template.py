import os

from trainer.data_module import generatedProjectNameDataModule
from trainer.network_module import generatedProjectNameNetworkModule
from trainer.model import generatedProjectNameModel
from dsframework.base.trainer import *


def train(config, train_config):

    mnist_full = datasets.MNIST(os.getcwd() + '/datasets', download=True, train=True, transform=transforms.ToTensor())
    mnist_test = datasets.MNIST(os.getcwd() + '/datasets', download=True, train=False, transform=transforms.ToTensor())

    mnist_data_module = generatedProjectNameDataModule(
        batch_size_train=config['batch_size_train'],
        batch_size_eval=config['batch_size_eval'],
        dataset=mnist_full,
        test_set=mnist_test,
        num_workers=config['num_workers'],
        seed=config['seed'],
        split_percent=0.8
    )

    model = generatedProjectNameModel(
        loss_function=config['loss_function'],
        num_classes=config['num_classes'],
        learn_rate=config['learning_rate'],
        nnetwork=config['nnetwork']
    )

    # automatically restores model, epoch, step, LR schedulers, apex, etc...
    # trainer.fit(model, ckpt_path="some/path/to/my_checkpoint.ckpt")
    trainer = pl.Trainer(**train_config)
    trainer.fit(model, mnist_data_module)

    trainer.test(model, mnist_data_module)


# saves top-K checkpoints based on "val_loss" metric
checkpoint_callback = ModelCheckpoint(
    save_top_k=10,
    save_last=True,
    monitor="val_loss",
    mode="max",
    filename="my-chkpnt-{epoch:02d}-{val_loss:.2f}",
)

if __name__ == '__main__':

    general_config = {
        'learning_rate': 1e-3,
        'loss_function': F.cross_entropy,
        'batch_size_train': 32,
        'batch_size_eval': 32,
        'num_classes': None,
        'num_workers': 1,
        'seed': 42,
        'nnetwork': generatedProjectNameNetworkModule.nnetwork
    }

    trainer_config = {
        'max_epochs': 10,
        'accelerator': None,  # 'cpu', 'gpu', 'tpu', 'ipu', 'auto', None
        'devices': None,  # number of accelerators: -1-all, 1, 3, 4...8, None, [1, 3]-gpu ids, None
        'strategy': None,  # 'dp', 'ddp', 'ddp2', 'ddp_spawn'
        'num_processes': None,  # number of cpus
        'enable_checkpointing': True,
        'default_root_dir': './',  # root dir to save checkpoints
        'callbacks': [checkpoint_callback],
        'enable_progress_bar': False
    }

    train(general_config, trainer_config)
