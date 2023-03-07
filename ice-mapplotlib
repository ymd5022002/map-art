# パイソンで干渉色段彩 ( by 千葉達朗 先生＠Facebook )
# カラーテーブルはソースの中に直置きで、DEMは10mメッシュ、等高線間隔は5m
# https://www.facebook.com/arukazan/posts/pfbid0acx49ZW5HjATeHqNyJphCLP2r8WiEx8wN5WM21JzVrqTd3oTd2tgGhirGeybQ9Xpl

import numpy as np
import matplotlib.pyplot as plt
data = np.loadtxt('ttp://arukazan.jp/test/10m.asc', skiprows=6)  # 標高ファイルのpathを指定する
x = np.arange(0, data.shape[1])
y = np.arange(0, data.shape[0])
xx, yy = np.meshgrid(x, y)
z = data[::-1]
# カスタムカラーテーブルの作成　R,G,B　最大値は1　行数は適当
colors = [
[0,0,0],
[0.03125,0.04296875,0.0625],
[0.09375,0.1171875,0.15234375],
[0.15625,0.1875,0.234375],
[0.2109375,0.25390625,0.30859375],
[0.265625,0.3125,0.37890625],
[0.31640625,0.37109375,0.44921875],
[0.36328125,0.4296875,0.51171875],
[0.41015625,0.48046875,0.5703125],
[0.45703125,0.53125,0.62890625],
[0.5,0.578125,0.6796875],
####### (　8000文字を越えるので　中　略　) #######  #要修正
[0.54296875,0.625,0.73046875]
]
cmap = ListedColormap(colors)
norm = plt.Normalize(vmin=z.min(), vmax=z.max())
colors = cmap(norm(z))
# 等高線図と段彩図の作成
fig, ax = plt.subplots(figsize=(14, 10), dpi=72)
cont = ax.contour(xx, yy, z, levels=np.arange(0, 140, 5), colors='black')
pcol = ax.pcolor(xx, yy, z, cmap=cmap, shading='auto')
fig.colorbar(pcol, ax=ax)
# 等高線図の色を変更する
for c in cont.collections:
c.set_edgecolor('black')
c.set_linewidth(0.5)
plt.show()
