# -*- coding:utf-8 -*-
from PIL import Image

# アニメーションの最初の画像のオブジェクト作成
before = Image.open("001.png")

# "read of closed file" エラー回避用
before = before.copy()

# アニメーションの最後の画像のオブジェクト作成
after2 = Image.open("002.png")
after3 = Image.open("003.png")
after4 = Image.open("004.png")
after5 = Image.open("005.png")
after6 = Image.open("006.png")
after7 = Image.open("007.png")
after8 = Image.open("008.png")
after9 = Image.open("009.png")
after10 = Image.open("010.png")
after11 = Image.open("011.png")
after12 = Image.open("012.png")

"""
after1 = Image.open("001.png")
"""
# "read of closed file" エラー回避用
after2 = after2.copy()
after3 = after3.copy()
after4 = after4.copy()
after5 = after5.copy()
after6 = after6.copy()
after7 = after7.copy()
after8 = after8.copy()
after9 = after9.copy()
after10 = after10.copy()
after11 = after11.copy()
after12 = after12.copy()

"""
after1 = after1.copy()
"""

# アニメーション GIF として保存
before.save(
    # ファイル名
    "anime.gif",

    # アニメーションとして保存
    save_all=True,

    # アニメーションに含ませる画像のリスト
    append_images=[after2,after3,after4,after5,after6,after7,after8,after9,after10,after11,after12],#,after6,after5,after4,after3,after2,after1,

    # 画像の表示時間
    duration=150,

    # ３回表示
    loop=0
)