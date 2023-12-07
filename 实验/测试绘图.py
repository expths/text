import numpy as np
import matplotlib.pyplot as plt

# 创建一个灰度图像，这里使用随机生成的数据
width, height = 100, 100
gray_image = np.random.rand(width, height)

# 绘制灰度图
plt.imshow(gray_image, cmap='gray', vmin=0, vmax=1)
plt.colorbar()  # 添加颜色条
plt.title('Gray Scale Image')
plt.show()
