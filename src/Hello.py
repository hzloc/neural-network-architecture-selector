import streamlit as st
import torch
import wandb
from pathlib import Path
from models.tcnecanetlstm import TCNETANetLSTM

CONFIG = dict(
            features=['timestamp', 'Weather_Temperature_Celsius', 'Weather_Relative_Humidity', 'Global_Horizontal_Radiation', 'Active_Power'],
            label='Active_Power',
            input_size=72,
            horizon=1,
            batch_size=32,
            cv_iter=[0.5, 0.7, 0.9],
            train_dataset_size = 0.6,
            val_dataset_size=0.2,
            test_dataset_size=0.2,
            num_channels = [32] * 4,
            in_channels = 4,
            learning_rate=0.001,
            train=False
            )

model_checkpoint_path = Path("src/artifacts/model-1in2lrkk-v11/model.ckpt")

model = TCNETANetLSTM.load_from_checkpoint(model_checkpoint_path, in_channels=CONFIG['in_channels'], num_channels=CONFIG['num_channels'])

st.write("Predict for Australia..")
