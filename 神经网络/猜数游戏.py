import torch
from torch import nn
import numpy
import matplotlib.pyplot as plt


# Get cpu, gpu or mps device for training.
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")

nn_list = []
def game(x,y):
    li = torch.stack([nn(x,y) for nn in nn_list])
    std = torch.mean(li)
    print("获胜数字",std*2/3)

class MyNN(nn.Module):
    def __init__(self,n:int):
        super().__init__()
        self.flatten = nn.Flatten()
        [nn.Linear() for i in range(n)]
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(20*20, 32),
        )

    def forward(self, x):
        x = x.float().view(1,-1)
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = MyNN().to(device)