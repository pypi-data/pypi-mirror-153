import torchmetrics

from dsframework.base.trainer import *


class generatedClass(ZIDSModel):
    """! Trainer template class inherits from ZIDSModel(LightningModule), which organizes your code into 6 sections:

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
    def __init__(self, loss_function=F.mse_loss, batch_size=4, num_classes=None, learn_rate=1e-3, nnetwork=None):
        """! Model class initializer, receives the network and loss function, it initializes all parameter to be
        tracked. """
        super().__init__(nnetwork=nnetwork, loss_function=None)

        self.nnetwork = nnetwork
        self.loss_function = loss_function
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.learn_rate = learn_rate

        self.train_accuracy = torchmetrics.Accuracy(num_classes=self.num_classes)
        self.val_accuracy = torchmetrics.Accuracy(num_classes=self.num_classes)
        self.test_accuracy = torchmetrics.Accuracy(num_classes=self.num_classes)

        self.train_precision = torchmetrics.Precision(num_classes=self.num_classes)
        self.val_precision = torchmetrics.Precision(num_classes=self.num_classes)
        self.test_precision = torchmetrics.Precision(num_classes=self.num_classes)

        self.train_recall = torchmetrics.Recall(num_classes=self.num_classes)
        self.val_recall = torchmetrics.Recall(num_classes=self.num_classes)

        self.train_f1 = torchmetrics.F1Score(num_classes=self.num_classes)
        self.val_f1 = torchmetrics.F1Score(num_classes=self.num_classes)
        self.save_hyperparameters()

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
        optimizer = Optimizers.Adam(self.parameters(), lr=self.learn_rate)
        return optimizer

    def forward(self, x):
        """! Defines the computation performed at every call.

        Implementation example:
            @code{.py}
            return self.nnetwork(x)
            @endcode
        """
        x = x.view(x.size(0), -1)
        x = self.nnetwork(x)
        return x

    def training_step(self, batch, batch_idx):
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
        y_hat = self(x)
        loss = self.loss_function(y_hat, y)
        pred = torch.argmax(y_hat, dim=1)

        self.train_accuracy(pred, y)
        self.train_precision(pred, y)
        self.train_recall(pred, y)
        self.train_f1(pred, y)

        self.log("train_acc", self.train_accuracy, prog_bar=True, on_epoch=True)
        self.log("train_prec", self.train_precision, prog_bar=True, on_epoch=True)
        self.log("train_recall", self.train_recall, prog_bar=True, on_epoch=True)
        self.log("train_f1", self.train_f1, prog_bar=True, on_epoch=True)

        return loss

    def validation_step(self, batch, batch_idx):
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
        y_hat = self(x)
        loss = self.loss_function(y_hat, y)
        pred = torch.argmax(y_hat, dim=1)

        self.val_accuracy(pred, y)
        self.val_precision(pred, y)
        self.val_recall(pred, y)
        self.val_f1(pred, y)

        self.log("val_loss", loss, prog_bar=True)
        self.log("val_acc", self.val_accuracy, prog_bar=True, on_epoch=True)
        self.log("val_prec", self.val_precision, prog_bar=True, on_epoch=True)
        self.log("val_recall", self.val_recall, prog_bar=True, on_epoch=True)
        self.log("val_f1", self.val_f1, prog_bar=True, on_epoch=True)

    def test_step(self, batch, batch_idx):
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
        y_hat = self(x)
        loss = self.loss_function(y_hat, y)
        pred = torch.argmax(y_hat, dim=1)

        self.test_accuracy(pred, y)
        self.test_precision(pred, y)

        self.log("test_acc", self.test_accuracy, prog_bar=True, on_epoch=True)
        self.log("test_prec", self.test_precision, prog_bar=True, on_epoch=True)
        self.log("test_loss", loss)  # prog_bar=True
