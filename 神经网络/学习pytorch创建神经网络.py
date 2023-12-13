import torch
from torch import nn
import numpy
import matplotlib.pyplot as plt
from random import randint


# Get cpu, gpu or mps device for training.
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")

# 官方例程
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()# flatten函数将多维数组转换为一维数组。
        self.linear_relu_stack = nn.Sequential(# Sequential是一个模型容器，将输入数据按顺序调用内部的每一层模型。
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

# model = NeuralNetwork().to(device)
# print(model)


################################################################

# 创建一个简易神经网络判断一组数据是否存在相关性。

##################### 数据生成器 ###############################

data_li = []
def data_g(func=None):
    """
    随机生成数据并附带其类型。

    同时可以作为装饰器将数据生成函数加入生成类型列表。
    """
    if func:
        data_li.append(func)
        return
    data_type = randint(0,2)
    data = data_li[data_type]()
    return data,data_type

@data_g
def irrelevant_data():
    """
    生成一组完全无关的随机数据。

    返回形状为(500,2)的数组。
    """
    data = numpy.random.normal(500,200,1000).astype(numpy.int16)
    data.shape = (500,2)
    return data

@data_g
def positive_correlation_data():
    """
    生成一组正相关的数据。
    """
    data = numpy.arange(start=0,stop=1000,step=1)
    shock = numpy.random.normal(0,100,1000).astype(numpy.int16)
    data = data + shock
    data.shape = (500,2)
    return data

@data_g
def negatively_correlated_data():
    """
    生成一组负相关的数据。
    """
    data = numpy.arange(start=1000,stop=0,step=-1)
    shock = numpy.random.normal(0,100,1000).astype(numpy.int16)
    data = data + shock
    data.shape = (500,2)
    return data

###################### 定义网络 ############################

class MyNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()# flatten函数将多维数组转换为一维数组。
        self.linear_relu_stack = nn.Sequential(# Sequential是一个模型容器，将输入数据按顺序调用内部的每一层模型。
            nn.Linear(20*20, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 3)
        )

    def forward(self, x):
        x = x.float().view(1,-1)
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = MyNN().to(device)# 神经网络的to方法，用于配置缓冲区等参数。

##################### 训练模型 #############################

# 创建损失函数和优化器。
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

model.train()# 将模型配置为训练模式。
for _ in range(10000):
    # 生成数据
    X,y = data_g()
    Y = [[0.01,0.01,0.01]]
    Y[0][y] = 0.99
    # 转换为张量
    X = torch.from_numpy(numpy.histogram2d(X[:,0],X[:,1],bins=20)[0])
    Y = torch.tensor(Y)

    pred = model(X)
    loss = loss_fn(pred,Y)

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

####################### 保存读取模型文件 ###########################

model_file_path = "models/test_model.pth"
torch.save(model.state_dict(), model_file_path)
print(f"将模型保存到{model_file_path}")

model = MyNN().to(device)
model.load_state_dict(torch.load(model_file_path))
print(f"从{model_file_path}导入模型")

####################### 测试 #################################

# 绘制散点图
# data = data_g()[0]
# plt.scatter(data[:,0],data[:,1],marker='o',s=10)
# plt.show()

# 统计数据生成灰度
# data = data_g()[0]
# hist,x_edges,y_edges = numpy.histogram2d(data[:,0],data[:,1],bins=20)
# print(hist)

# 绘制灰度图
# plt.imshow(hist, extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]], origin='lower', cmap='viridis')
# plt.colorbar(label='Counts')
# plt.title('2D Histogram')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.show()

# 测试数据
model.eval()# 将模型配置为评估模式。
for i in range(3):
    # 注意输入的张量需要转换为一维向量。
    # NdArray数据需要转换为张量数据。
    data = data_li[i]()
    data = torch.from_numpy(numpy.histogram2d(data[:,0],data[:,1],bins=20)[0])
    print("类型",i,"输出",model(data))

