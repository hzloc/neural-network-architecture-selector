import lightning.pytorch as pl
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from typing import Optional, List, Callable
import torch


class DKACS(Dataset):
    def __init__(self, path: str, horizon: int, input_size: int, transform: Optional[List[Callable]]=None, target_transform: Optional[List[Callable]]=None,  data_path='./'):
        self.data: pd.DataFrame = pd.read_csv(path).values
#         self.data = data.values.astype(np.float32)
        self.h = horizon
        self.w = input_size
        self.transform = transform
        self.target_transform = target_transform
        self.features, self.label = self.create_windows()
        
        
    def create_windows(self):
        total_possible_window_size = len(self.data) - self.w - self.h - 1
        features = np.zeros(shape=(total_possible_window_size, self.data.shape[1], self.w), dtype=np.float32)
        label = np.zeros(shape=(total_possible_window_size, self.h), dtype=np.float32)
        for i in range(total_possible_window_size):
            features[i] = np.transpose(self.data[i:i+self.w])
            label[i] = self.data[i+self.w+self.h-1, -1]
        return features, label
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        features = torch.from_numpy(self.features[idx].astype(np.float32))
        label = torch.from_numpy(self.label[idx].astype(np.float32))
        
        return features, label



class DKASCDataModule(pl.LightningDataModule):
    def __init__(self, input_size: int, horizon: int, batch_size: int = 32, num_workers: int = 3):
        """Creates the data module for the DKASC data which also known as source dataset

        Args:
            input_size (int): number of past steps 
            horizon (int): prediction step to the future
            batch_size (int, optional): batch size Defaults to 32.
            num_workers (int, optional): Dataloader woreker count. Defaults to 3.
        """
        super().__init__()
        self.horizon = horizon
        self.input_size = input_size
        self.save_hyperparameters()
        self.batch_size = batch_size
    
    def prepare_data(self):
        pass
        
    def setup(self, stage=None):
        """

        Args:
            stage (_type_, optional): _description_. Defaults to None.
        """
        if stage == 'fit':
            self.dkasc_train = DKACS("/kaggle/input/dkasc-dataset/DKASC_train.csv", self.horizon, self.input_size)
            self.dkasc_val = DKACS("/kaggle/input/dkasc-dataset/DKASC_val.csv", self.horizon, self.input_size)
        
        if stage == 'test':
            self.dkasc_test = DKACS("/kaggle/input/dkasc-dataset/DKASC_test.csv", self.horizon, self.input_size)
        
        if stage == 'predict':
            self.dkasc_test = DKACS("/kaggle/input/dkasc-dataset/DKASC_test.csv", self.horizon, self.input_size)

    
    def train_dataloader(self):
        return DataLoader(self.dkasc_train, shuffle=False, pin_memory=True, num_workers=self.num_workers, batch_size=self.batch_size)
    
    def val_dataloader(self):
        return DataLoader(self.dkasc_val, shuffle=False, pin_memory=True, num_workers=self.num_workers, batch_size=self.batch_size)
    
    def test_dataloader(self):
        return DataLoader(self.dkasc_test, shuffle=False, pin_memory=True, num_workers=self.num_workers, batch_size=self.batch_size)
    
    def predict_dataloader(self):
        return DataLoader(self.dkasc_test, shuffle=False, pin_memory=True, num_workers=self.num_workers, batch_size=self.batch_size)
    
    def teardown(self, stage):
        if stage == 'fit':
            del self.dkasc_train
            del self.dkasc_val
            
        if stage == 'test':
            del self.dkasc_test