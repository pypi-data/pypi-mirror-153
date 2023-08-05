from typing import Any, Optional, Union, List
from dsframework.base.trainer import *


class ZIDSModel(pl.LightningModule):
    """! Trainer base class inherits from LightningModule, which organizes your code into 6 sections:

        - Computations (init).
        - Train Loop (training_step)
        - Validation Loop (validation_step)
        - Test Loop(test_step)
        - Prediction Loop (predict_step)
        - Optimizers and LR Schedulers(configure_optimizers)

        Log parameters:
        - For single value, use:
            self.log("test_loss", test_loss)  # prog_bar=True

        - For multiple values use dictionary, use:
            values = {"loss": loss, "acc": acc, "metric_n": metric_n}  # add more items if needed
            self.log_dict(values)

        View results in tensorboard:
            tensorboard --logdir=lightning_logs/

        Loading datasets:

            example:
            @code{.py}
            train_set = datasets.MNIST(os.getcwd() + '/data', download=True, train=True, transform=transform)
            test_set = datasets.MNIST(os.getcwd() + '/data', download=True, train=False, transform=transform)

            # use 20% of training data for validation
            train_set_size = int(len(train_set) * 0.8)
            valid_set_size = len(train_set) - train_set_size

            # split the train set into two
            seed = torch.Generator().manual_seed(42)
            train_set, valid_set = random_split(train_set, [train_set_size, valid_set_size], generator=seed)

            train_set_loader = DataLoader(train_set, num_workers=2)
            val_set_loader = DataLoader(valid_set, num_workers=2)
            test_set_loader = DataLoader(test_set, num_workers=2)
            @endcode


        Training:
            example:
            @code{.py}
            trainer = pl.Trainer(max_epochs=1, callbacks=[checkpoint_callback])
            trainer.fit(model=autoencoder, train_dataloaders=train_set_loader, val_dataloaders=val_set_loader)
            @endcode

        Testing:
            example:
            @code{.py}
            trainer.test(model=autoencoder, dataloaders=test_set_loader)
            @endcode

        Loading a trained model, use:
            - load_from_checkpoint

                example:
                @code{.py}
                model = MyTrainer.load_from_checkpoint('lightning_logs/epoch=0-step=48000.ckpt')
                @endcode


        Saving a model, use:
            - save_checkpoint

                for example:
                @code{.py}
                trainer.save_checkpoint("my_checkpoint.ckpt")
                @endcode

            - ModelCheckpoint - define automated checkpoint saving, use:
                for example:
                @code{.py}
                checkpoint_callback = ModelCheckpoint(dirpath="lightning_logs/", save_top_k=2, monitor="val_loss")
                @endcode


    """

    def __init__(self, nnetwork, loss_function):
        super().__init__()

        self.nnetwork = nnetwork
        self.loss_function = loss_function

    def configure_optimizers(self):
        """! Choose what optimizers and learning-rate schedulers to use in your optimization. Normally you’d need one.
        But in the case of GANs or similar you might have multiple.

            Returns: Any of this 6 options
                - Single optimizer.
                - List or Tuple of optimizers.
                - Two lists - The first list has multiple optimizers, and the second has multiple LR schedulers
                    (or multiple lr_scheduler_config).
                - Dictionary, with an "optimizer" key, and (optionally) a "lr_scheduler" key whose value
                    is a single LR scheduler or lr_scheduler_config.
                - Tuple of dictionaries as described above, with an optional "frequency" key.
                - None - Fit will run without any optimizer.

        Example:
            @code{.py}
            optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
            return optimizer
            @endcode

        Another example:
            @code{.py}
            SGD_optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.7)
            return SGD_optimizer
            @endcode

        """
        pass

    def forward(self, *args, **kwargs) -> Any:
        """! Defines the computation performed at every call.

        Implementation example:
            @code{.py}
            return self.network(x)
            @endcode
        """
        pass

    def training_step(self, batch, batch_idx) -> STEP_OUTPUT:
        """! Override to enable training loop

        Implementation example:
            @code{.py}
            def training_step(self, batch, batch_idx):
                x, y = batch
                x = x.view(x.size(0), -1)
                z = self.encoder(x)
                x_hat = self.decoder(z)
                loss = function.mse_loss(x_hat, x)
                return loss
            @endcode

        If you need to do something with all the outputs of each training_step(), override the
        training_epoch_end() method.
        """
        x, y = batch
        y_hat = self.network(x)
        loss = self.loss_function(y_hat, y)
        self.log("train_loss", loss, prog_bar=True, logger=True)

        return loss

    def validation_step(self, batch, batch_idx) -> Optional[STEP_OUTPUT]:
        """! Override to enable validation loop

        Implementation example:
            @code{.py}
            def validation_step(self, batch, batch_idx):
                x, y = batch
                x = x.view(x.size(0), -1)
                z = self.encoder(x)
                x_hat = self.decoder(z)
                test_loss = function.mse_loss(x_hat, x)
                self.log("val_loss", test_loss, prog_bar=True)
            @endcode
        """
        x, y = batch
        y_hat = self.network(x)
        loss = self.loss_function(y_hat, y)

        self.log("val_loss", loss)

    def test_step(self, batch, batch_idx) -> Optional[STEP_OUTPUT]:
        """! Override to enable test loop.

        Implementation example:
            @code{.py}
            x, y = batch
            x = x.view(x.size(0), -1)
            z = self.encoder(x)
            x_hat = self.decoder(z)
            test_loss = function.mse_loss(x_hat, x)
            self.log("test_loss", test_loss)  # prog_bar=True
            @endcode
        """
        x, y = batch
        y_hat = self.network(x)
        loss = self.loss_function(y_hat, y)
        self.log("test_loss", loss)  # prog_bar=True

    def training_epoch_end(self, outputs: EPOCH_OUTPUT) -> None:
        """! Override method to implement functionality related to training_step() outputs.

        training step accumulated returns:
            @code
            all_preds = torch.stack(training_step_outputs)
            @endcode
        """
        pass

    def validation_epoch_end(self, outputs: Union[EPOCH_OUTPUT, List[EPOCH_OUTPUT]]) -> None:
        """! Override method to implement functionality related to validation_step() outputs."""
        pass

    def training_step_end(self, step_output: STEP_OUTPUT) -> STEP_OUTPUT:
        """! When the data is split across multiple GPUs, this method will have outputs from all devices that can be
        accumulated to get the effective results.
        """
        pass

    def validation_step_end(self, *args, **kwargs) -> Optional[STEP_OUTPUT]:
        """! When the data is split across multiple GPUs, this method will have outputs from all devices that can be
        accumulated to get the effective results.
        """
        pass
