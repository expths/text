import numpy as np
from scipy.signal import convolve2d

# 定义一个二维数组
array2d = np.array([[1, 2, 3,9],
                    [4, 5, 6,0],
                    [7, 8, 9,8]])

# 定义一个卷积核
kernel = np.array([[0, 1, 0],
                   [1, -4, 1],
                   [0, 1, 0]])

# 执行二维卷积操作
result = convolve2d(array2d, kernel,mode='valid')

print("Original 2D Array:")
print(array2d)
print("\nConvolution Kernel:")
print(kernel)
print("\nResult of 2D Convolution:")
print(result)