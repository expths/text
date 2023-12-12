import psycopg
import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from config_manager import postgreSQL as db


table_name = lambda symbol:f"{symbol}_market_data"
rag = "minute_stamp>28269600 and minute_stamp<28315679"

def a(symbol):
    """
    读取数据返回Ndarray。
    """
    with psycopg.connect(**db) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name(symbol)} WHERE {rag} ORDER BY minute_stamp ASC")
            return np.array(cur.fetchall())

data = a('BTCUSDT')

kernel = np.array([[0, -0.3, 0, 0, 0, 0, 0],
                   [0, -0.7, 0, 0, 0, 0, 0],
                   [0, 1, 0, 0, 0, 0, 0]])

arr = convolve2d(data,kernel,mode='valid')

# 在（-100，100）之间划分2000个区间。
bins = np.linspace(-10000,10000,2000)

# 统计区间内的频数。
# x,p = np.unique(arr,return_counts=True)
p,bin = np.histogram(arr, bins=bins)

# 统计方差
# v = np.var(arr)
# print(v)

# 统计标准差
s = np.std(arr)

# 多次采样正态分布
# for i in range(1,100):
#     samples = np.random.normal(0, s, i)
#     print (np.sum(samples))

# 创建一个灰度图像，这里使用随机生成的数据
width, height = 100, 100
# gray_image = np.random.rand(width, height)

# 绘制灰度图
# plt.imshow(gray_image, cmap='gray', vmin=0, vmax=1)
# plt.colorbar()  # 添加颜色条
# plt.title('Gray Scale Image')
# plt.show()


# 绘制直方图
# plt.hist(arr, bins=bins, edgecolor='black')
# plt.show()

# with np.nditer(data,[],[])as it:
#     it

print(data.shape)
print(data.reshape((-1,15,46078)))

def tofile():
    """
    使用tofile方法将ndarray以二进制写入文件。
    """