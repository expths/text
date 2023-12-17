import torch
from torch import nn
import numpy
import matplotlib.pyplot as plt

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")



def game(mods:list[nn.Module])->None:
    """
    让所有算法在[0,1]猜测均值。最后计算实际上的均值。

    使用计算图时，默认情况下更新一个模型会影响其他的模型。

    在进行多次反向传播时，中间值和梯度信息可能会被释放。
    因此会出现出现 RuntimeError: Trying to backward through the graph a second time 
    此时需要使用 retain_graph=True
    确保在需要保留计算图的情况下使用此参数，但也要注意潜在的内存占用问题。
    """
    loss_function = nn.MSELoss()
    optimizers = [torch.optim.SGD(mod.parameters(), lr=0.001)for mod in mods]

    outputs = [mod() for mod in mods]
    mean = sum(output.item() for output in outputs)/len(outputs)
    mean = torch.tensor(mean)
    # a = torch.stack(outputs)
    # s = torch.mean(a)
    for output,optimizer in zip(outputs,optimizers):
        loss = loss_function(output,mean)
        optimizer.zero_grad()
        loss.backward(retain_graph=True) # 存在多次反向传播
        optimizer.step()
        
    # loss_list = [loss_function(output,s) for output in outputs]
    # print(loss_list)


class Mean_NN(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(1, 64),
            nn.Sigmoid(),
            nn.Linear(64,1)
        )

    def forward(self):
        x = torch.rand(1)
        logits = self.linear_relu_stack(x)
        return logits
    

mods = [Mean_NN()for _ in range(100)]
game(mods)