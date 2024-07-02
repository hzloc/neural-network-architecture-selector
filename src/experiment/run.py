import lightning.pytorch as pl
from lightning import Trainer
from typing import Dict, Literal, Optional, List, Mapping
from lightning.pytorch.loggers import CSVLogger, WandbLogger
from lightning.pytorch.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    StochasticWeightAveraging,
)
from pathlib import Path


class Experiment:
    def __init__(
        self,
        model: pl.LightningModule,
        datamodule: pl.LightningDataModule,
        experiment_config: dict,
        mode: Literal["train", "evaluate"] = "train",
        logger: Literal["wandb"] = "wandb",
    ) -> None:

        self._model = model
        self._dm = datamodule

        if logger == "wandb":
            logger = WandbLogger()
        else:
            logger = CSVLogger()

        self._trainer = pl.Trainer(
            logger=logger,
            callbacks=[
                StochasticWeightAveraging(swa_lrs=1e-2),
                EarlyStopping(monitor="val_loss"),
                ModelCheckpoint("../models/ckpts/"),
            ],
        )

    def train(self) -> None:
        self._trainer.fit(model=self._model, datamodule=self._dm)

    def eval(self, ckpt_path: Optional[str | Path]) -> List[Mapping[str, float]]:
        evaluation = self._trainer.test(
            model=self._model, dataloaders=self._dm, ckpt_path=ckpt_path
        )
        return evaluation
