import matplotlib.pyplot as plt

a = sum([16, 18, 21, 11, 18])/5
print(a)

per_10 = {1: 0.105, 2: 0.037, 3: 0.007, 4: 0.003}
per_20 = {1: 0.292, 2: 0.142, 3: 0.058, 4: 0.046}
per_30 = {1: 0.36, 2: 0.235, 3: 0.193, 4: 0.168}
per_40 = {1: 0.489, 2: 0.42, 3: 0.396, 4: 0.346}
plt.plot(list(per_10.keys()), list(per_10.values()), linestyle='-.', linewidth=1, color='b', label="10%attack")
plt.plot(list(per_20.keys()), list(per_20.values()), linestyle='-.', linewidth=1, color='r', label="20%attack")
plt.plot(list(per_30.keys()), list(per_30.values()), linestyle='-.', linewidth=1, color='g', label="30%attack")
plt.plot(list(per_40.keys()), list(per_40.values()), linestyle='-.', linewidth=1, color='c', label="40%attack")
# plt.grid(True)  # 网格
plt.legend(bbox_to_anchor=(0.5, -0.31), loc=8, ncol=4)
plt.tick_params(labelsize=10)  # 坐标刻度字体大小
font2 = {'family': 'SimSun',
         'weight': 'heavy',
         'size': 14,
         }
plt.ylabel("成功率", font2)  # 坐标名与大小
plt.xlabel("攻击长度", font2)
plt.tight_layout()

plt.show()

# 30, 0.01: [0.2299, 0.3279, 0.3509, 0.2532, 0.2299]
# 40, 0.01: [0.3175, 0.303, 0.2985, 0.3571, 0.4444]
#
# 20, 0.01: [0.198, 0.202, 0.2326, 0.146, 0.2083]
# 20, 0.02: [0.3774, 0.4082, 0.2817, 0.2899, 0.339, 0.3125, 0.303]
# 20, 0.25: [0.3922, 0.4, 0.556, 0.3922, 0.4255, 0.3704, 0.4444, 0.339]
# 20, 0.04: [0.4878, 0.6667, 0.4545, 0.5128, 0.5128, 0.5714, 0.5714]
