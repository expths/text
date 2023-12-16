import torch
import numpy
import torch.nn as nn


def test():
    """
    创建张量：
    可以通过位置参数依次输入每个维度的大小，也可以使用序列类型输入。
    通过dtype参数可以设置元素类型。
    empty
    zeros
    ones
    rand

    根据已有的张量创建一个形状维度相同的张量：
    参数为模板张量。
    empty_like
    *_like

    配置随机数的种子：
    torch.manual_seed(<种子>)

    --------------------------------------------

    数据类型：
    - torch.bool
    - torch.int8
    - torch.uint8
    - torch.int16
    - torch.int32
    - torch.int64
    - torch.half
    - torch.float
    - torch.double
    - torch.bfloat

    标量运算：
    张量和张量之间、张量和标量之间可以进行加减乘除幂等标量运算。
    张量和张量之间的标量运算要求张量的形状相同，对应位置上的元素计算。
    张量和标量之间的运算会发生广播，标量和张量的每个元素进行一次计算。

    特别地，张量和张量之间也可以进行广播，但要满足如下要求：
    - 每个张量必须至少有一个维度
    - 一个张量的某一维度长度为1或该维度不存在
    - 其他维度尺寸相等。

    对张量调用数学函数需要使用pytorch库中的函数：
    https://pytorch.org/docs/stable/torch.html#math-operations

    ------------------------------------------

    ## 损失值对象

    通常情况下，loss 是一个标量张量。
    这是因为损失函数的目标是度量模型输出与真实标签之间的差距，得到一个单一的值。
    所以，损失通常是通过一些损失函数计算得到的标量张量。
    如果使用一些张量运算手动计算了表示偏差的张量，同样可以使用这个张量进行反向传播。
    
    ## 优化参数对象

    model.parameters() 返回的是模型中所有需要学习的参数的生成器（Generator）。
    这个生成器会产生模型中每个需要学习的参数的张量。
    这些张量通常是 torch.nn.Parameter 类型，是一种特殊的张量，表示模型参数，并且可以通过梯度进行优化。

    torch.nn.Parameter 对象是张量的子类，其主要作用是告诉 PyTorch 这是模型的参数，需要被优化。
    调用 model.parameters() 时会返回一个包含所有模型参数的生成器，可以用这个生成器迭代并访问每个参数的张量。

    模型参数对象的data字段就是参数m，而grad字段是反向传播得到的误差。
    通常调用优化器会自动更新参数，但也可以手动更新。

    ```
    loss.backward() # 反向传播

    with torch.no_grad(): # 自定义参数更新规则（这里简化为梯度下降）
        for param in model.parameters():
            param.data -= learning_rate * param.grad

    model.zero_grad()
    ```

    """

    # 生成权重矩阵
    A = torch.empty(20,5)
    A.requires_grad = True

    # 生成输入向量
    B = torch.empty(1,20)

    # 计算输出向量
    C = torch.matmul(B,A)

    # 手动计算损失率
    # 损失率是一个标量，指示自动微分程序输出偏离预期的大小。
    # 在计算图中损失函数和一般的函数、神经网络没有区别。
    # 可以手动实现复杂的损失函数。
    D = torch.empty(5,1)
    loss = torch.matmul(C,D)
    print(loss)

    # 反向传播
    # 自动微分程序会通过计算图反向寻找需要优化的张量，为它生成优化矩阵。
    loss.backward()

    # 手动更新参数
    # 张量的grad属性就是反向传播产生的需要更新的权重。
    # 计算结束后需要清理grad。
    with torch.no_grad():
        print(A.grad)
        A -= A.grad
        A.grad.zero_()


if __name__ == "__main__":
    test()