import lightning.pytorch as pl
import torch
import torch.nn as nn
from utils.plot import plot_pred_vs_act
from typing import Iterable, Tuple, Optional
import torch.nn.functional as F
from pathlib import Path
from models.tcnecanetlstm import TCNETANetLSTM


class TL(pl.LightningModule):
    def __init__(self, learning_rate=0.001):
        super().__init__()
        self.learning_rate = learning_rate
        model = TCNETANetLSTM.load_from_checkpoint(
            Path("artifacts/model-1in2lrkk:v11") / "model.ckpt"
        )
        model.freeze()
        self.feature_extractor = nn.Sequential(
            model.network, model.permute_layer, model.gru
        )

        self.criterion = nn.L1Loss()
        self.output_layer = nn.Linear(1152, 1)

    def _forward_features(self, x):
        x = self.feature_extractor(x)
        x = x[0]
        return x

    def _get_conv_output(self, shape):
        batch_size = 1
        tmp_input = torch.autograd.Variable(torch.rand(batch_size, *shape))
        output_feat = self._forward_features(tmp_input)
        n_size = output_feat.data.view(batch_size, -1).size(1)
        return n_size

    def forward(self, x):
        x = x[0]
        x = self._forward_features(x)
        x = x.contiguous().view(x.size(0), -1)
        x = self.output_layer(x)
        return x

    def training_step(self, batch):
        batch, gt = batch[0], batch[1]
        out = self.forward(batch)
        loss = self.criterion(out, gt)
        self.log(
            "loss_epoch", loss, prog_bar=True, on_step=False, on_epoch=True, logger=True
        )
        return loss

    def validation_step(self, batch, batch_idx):
        batch, gt = batch[0], batch[1]
        out = self.forward(batch)
        loss = self.criterion(out, gt)
        self.log("val_loss", loss, on_epoch=True, prog_bar=True)
        return loss

    def test_step(self, *args, **kwargs):
        batch = kwargs.get("batch", args[0])
        predictions = self(batch)
        actual_values = batch[1]
        loss = self.criterion(predictions, actual_values)
        loss_mse = nn.functional.mse_loss(predictions, actual_values)
        self.log("test_MAE_loss", loss, logger=True)
        self.log("test_mse_loss", loss_mse, logger=True)
        return {
            "prediction": predictions,
            "actual": actual_values,
            "loss_mae": loss,
            "loss_mse": loss_mse,
        }

    def predict_step(self, *args, **kwargs):
        batch = kwargs.get("batch", args[0])
        predictions = self(batch)
        actual_values = batch[1]
        print(predictions, actual_values)
        return predictions, actual_values

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)

    def on_test_batch_end(self, outputs, batch, batch_idx, dataloader_idx=0):
        plot_pred_vs_act(outputs["prediction"], outputs["actual"])
