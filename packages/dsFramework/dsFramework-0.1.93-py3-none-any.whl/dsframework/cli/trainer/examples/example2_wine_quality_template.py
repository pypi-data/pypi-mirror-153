from trainer.data_module import generatedProjectNameDataModule
from trainer.network_module import generatedProjectNameNetworkModule
from trainer.model import generatedProjectNameModel
from dsframework.base.trainer import *


def train(config, train_config):
    data_path = '/Users/yuvalbechor/Develop/ds-framework/dsframework/cli/trainer/datasets/wine_quality/wine-quality.csv'

    wine_data_module = generatedProjectNameDataModule(
        data_path=data_path,
        batch_size_train=config['batch_size_train'],
        batch_size_eval=config['batch_size_eval'],
        num_workers=config['num_workers'],
        seed=config['seed'],
        split_percent=0.8,
        test_set_out_of_dataset=True
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
    trainer.fit(model, wine_data_module)

    trainer.test(model, wine_data_module)


if __name__ == '__main__':

    general_config = {
        'learning_rate': 1e-3,
        'loss_function': F.cross_entropy,
        'batch_size_train': 1,
        'batch_size_eval': 1,
        'num_classes': None,
        'num_workers': 1,
        'seed': 42,
        'nnetwork': generatedProjectNameNetworkModule.nnetwork_wine
    }

    trainer_config = {
        'max_epochs': 1,
        'accelerator': None,  # 'cpu', 'gpu', 'tpu', 'ipu', 'auto', None
        'devices': None,  # number of accelerators: -1-all, 1, 3, 4...8, None, [1, 3]-gpu ids, None
        'strategy': None,  # 'dp', 'ddp', 'ddp2', 'ddp_spawn'
        'num_processes': None  # number of cpus
    }

    train(general_config, trainer_config)
