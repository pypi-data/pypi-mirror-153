from data_module import generatedProjectNameDataModule
from network_module import generatedProjectNameNetworkModule
from model import generatedProjectNameModel
from dsframework.base.trainer import *

##
# Steps to work with the trainer.py:
#
# 1. Datasets:
#   a. Load dataset
#   b. Parse it - override parse_dataset() method in data_module.py.
#
# 2. Model:
#   a. Define your network in NetworkModule class in network.py.
#   b. Check model methods in model.py.
#
# 3. Callbacks:
#   a. Checkpoint - Adjust ModelCheckpoint callback parameters in this file - trainer.py.
#   b. Early stopping - Adjust EarlyStopping callback parameters in this file - trainer.py.
#
# 4. Configuration:
#   a. Adjust general config in this file - trainer.py
#   b. Adjust trainer config in this file - trainer.py


def train(config, train_config):

    # either load the dataset,
    full_dataset = None
    test_dataset = None
    # or provide a path
    data_path = './path to dataset'
    file_type = 'csv'

    data_module = generatedProjectNameDataModule(
        data_path=data_path,
        file_type=file_type,
        batch_size_train=config['batch_size_train'],
        batch_size_eval=config['batch_size_eval'],
        dataset=full_dataset,
        test_set=test_dataset,
        num_workers=config['num_workers'],
        seed=config['seed'],
        split_percent=0.9,  # Split between train and validation datasets
        test_set_out_of_dataset=False  # Split a test data out of the dataset.
    )

    model = generatedProjectNameModel(
        loss_function=config['loss_function'],
        num_classes=config['num_classes'],
        learn_rate=config['learning_rate'],
        nnetwork=config['nnetwork']
    )

    # To automatically restores model, epoch, step, LR schedulers, apex, etc... use the following:
    # trainer.fit(model, ckpt_path="some/path/to/my_checkpoint.ckpt")
    trainer = pl.Trainer(**train_config)
    trainer.fit(model, data_module)

    trainer.test(model, data_module)


# Define checkpoint callback
# saves top-K checkpoints based on "val_loss" metric
checkpoint_callback = ModelCheckpoint(
    save_top_k=3,
    save_last=True,
    monitor="val_loss",
    mode="min",
    filename="my-chkpnt-{epoch:02d}-{val_loss:.2f}",
)

early_stopping_callback = EarlyStopping(
    monitor='val_loss',
    patience=10,  # number of val checks with no improvement
    mode='max'
)

if __name__ == '__main__':

    general_config = {
        'learning_rate': 1e-3,
        'loss_function': F.cross_entropy,
        'batch_size_train': 32,
        'batch_size_eval': 32,
        'num_classes': None,
        'num_workers': 1,  # Number of workers assigned to DataLoader (number of cpus)
        'seed': 42,
        'nnetwork': generatedProjectNameNetworkModule.nnetwork
    }

    trainer_config = {
        'max_epochs': 1,
        'accelerator': None,  # 'cpu', 'gpu', 'tpu', 'ipu', 'auto', None
        'devices': None,  # number of accelerators: -1-all, 1, 3, 4...8, None, [1, 3]-gpu ids, None
        'strategy': None,  # 'dp', 'ddp', 'ddp2', 'ddp_spawn'
        'num_processes': None,  # number of cpus
        'enable_checkpointing': True,
        'default_root_dir': './',  # root dir to save checkpoints
        'callbacks': [early_stopping_callback, checkpoint_callback],
        'enable_progress_bar': False  # Set to 'True' to see logs and progress bar in console
    }

    train(general_config, trainer_config)
