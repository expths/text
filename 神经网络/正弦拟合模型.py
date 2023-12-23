# 目标：通过神经网络拟合正弦函数。
import torch
from torch import nn
import numpy
import matplotlib.pyplot as plt


# 配置训练机器
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")


class MyNN(nn.Module):
    """
    通过正弦函数拟合数据。

    这个模型的实际效果很不好。无论是增加梯度还是增加采样。
    它甚至无法在无噪声的环境中识别曲线。

    我猜测这是因为神经网络缺乏采样数据的顺序信息，从而难以识别数据中的周期。
    在全连接层中，任何一个输出都是全体输入加减乘除的结果，这导致输入的一系列采样数据与顺序无关。
    """
    def __init__(self,sampling:int ,hidden_layer:int):
        """
        输入采样率和隐藏层尺寸构建神经网络。
        """
        super().__init__()
        # self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(sampling,hidden_layer),
            nn.Sigmoid(),
            nn.Linear(hidden_layer,hidden_layer),
            nn.Sigmoid(),
            nn.Linear(hidden_layer, 2) # 输出频率和初相
        )

    def forward(self, x):
        """
        关于输入维度：
        
        神经网络层的输入张量的形状通常由该层的设计和网络的架构决定。
        一般而言，神经网络中的第一层的输入张量形状由数据集决定。
        对于后续的隐藏层和输出层，需要确保它们的输入形状与前一层的输出形状相匹配。

        通常需要将输入张量的形状转换为(batch_size, input_size)，其中batch_size是批处理中的样本数，input_size是输入特征的数量。
        对于卷积层，输入张量的形状通常是(batch_size, channels, height, width)，其中channels是通道数，height和width是图像的高度和宽度。

        如果直接将一维向量输入到期望二维或更高维输入的神经网络层中，通常会导致维度不匹配的错误。
        神经网络的层通常期望输入张量具有特定的维度，以便进行权重矩阵的乘法等操作。

        为了解决这个问题，你可以使用 view 或 reshape 方法来改变一维张量的形状，使其变为二维。

        ---

        关于batch_size

        通常在一次训练中，输入神经网络的是一个批次的样本，而不是单个样本。
        这样做的主要原因之一是为了利用硬件加速，批处理允许并行处理多个样本，提高了训练效率。
        对于一个批次中的每个样本，损失函数和梯度都是分别计算的。
        这些损失值被求平均，梯度也被相加，最后通过反向传播算法更新神经网络的参数。
        """
        # x = x.view(1,-1)
        # x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

# 模型，损失函数，优化器
model = MyNN(1000,1000).to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

# 训练函数
def train():
    """
    训练数据
    """
    model.train()# 将模型配置为训练模式。
    for _ in range(10000):
        # 生成数据
        data,answer = data_g()

        # 计算损失
        pred = model(data)
        loss = loss_fn(pred,answer)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

# 生成数据
def data_g()->tuple[torch.tensor]:
    """
    随机产生正弦函数并加入噪声。

    返回采样数据和真实值。
    """
    data:torch.tensor
    answer:torch.tensor

    with torch.no_grad():
        data = torch.arange(0,10*1000,1)
        data = data.view(10,1000)
        answer = torch.rand(10,2)
        answer[:,1] = answer[:,1]*100 % (6.28/answer[:,0])
        data = 10 * torch.sin(data * answer[:,0].view(-1,1) + answer[:,1].view(-1,1))

    return data,answer

train()

# 测试成果
model.eval()# 将模型配置为评估模式。
data,answer = data_g()
output = model(data)
print("输出",output,"\n答案",answer)
