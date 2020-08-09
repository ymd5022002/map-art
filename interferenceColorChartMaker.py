#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2020/8/7 
# 作成　みんなの地図アート研究所　やまだこーじ
# https://ymd5022002.github.io/map-art-jp/


from PIL import Image
from PIL import ImageDraw
import math

#膜厚　d[nm]
end_film_thickness = 15000.0
start_film_thickness = 0.0


#屈折率 nγ,　nα
start_delta_n = 0
end_delta_n = 0.2

#波長　λ[nm]
start_wavelength = 380
end_wavelength = 780
pitch_wavelength = 5
number_wavelength = (end_wavelength-start_wavelength)//pitch_wavelength + 1

color_code = ""

#光源の定義　D65
#380nm~780nm 5nm刻み
#出典 http://www.rit-mcsl.org/UsefulData/D65_and_A.htm
light_source=[
49.9755,
52.3118,
54.6482,
68.7015,
82.7549,
87.1204,
91.486,
92.4589,
93.4318,
90.057,
86.6823,
95.7736,
104.865,
110.936,
117.008,
117.41,
117.812,
116.336,
114.861,
115.392,
115.923,
112.367,
108.811,
109.082,
109.354,
108.578,
107.802,
106.296,
104.79,
106.239,
107.689,
106.047,
104.405,
104.225,
104.046,
102.023,
100,
98.1671,
96.3342,
96.0611,
95.788,
92.2368,
88.6856,
89.3459,
90.0062,
89.8026,
89.5991,
88.6489,
87.6987,
85.4936,
83.2886,
83.4939,
83.6992,
81.863,
80.0268,
80.1207,
80.2146,
81.2462,
82.2778,
80.281,
78.2842,
74.0027,
69.7213,
70.6652,
71.6091,
72.979,
74.349,
67.9765,
61.604,
65.7448,
69.8856,
72.4863,
75.087,
69.3398,
63.5927,
55.0054,
46.4182,
56.6118,
66.8054,
65.0941,
63.3828
]

#等色関数 x_(λ) , y_(λ) , z_(λ)の定義
#380nm~780nm 5nm刻み
#出典 https://www.uni-kiel.de/psychologie/golz/publications/2003a/XYZ_CIE_2.dat
x_eq =[
0.001368,
0.002236,
0.004243,
0.00765,
0.01431,
0.02319,
0.04351,
0.07763,
0.13438,
0.21477,
0.2839,
0.3285,
0.34828,
0.34806,
0.3362,
0.3187,
0.2908,
0.2511,
0.19536,
0.1421,
0.09564,
0.05795001,
0.03201,
0.0147,
0.0049,
0.0024,
0.0093,
0.0291,
0.06327,
0.1096,
0.1655,
0.2257499,
0.2904,
0.3597,
0.4334499,
0.5120501,
0.5945,
0.6784,
0.7621,
0.8425,
0.9163,
0.9786,
1.0263,
1.0567,
1.0622,
1.0456,
1.0026,
0.9384,
0.8544499,
0.7514,
0.6424,
0.5419,
0.4479,
0.3608,
0.2835,
0.2187,
0.1649,
0.1212,
0.0874,
0.0636,
0.04677,
0.0329,
0.0227,
0.01584,
0.01135916,
0.008110916,
0.005790346,
0.004109457,
0.002899327,
0.00204919,
0.001439971,
0.0009999493,
0.0006900786,
0.0004760213,
0.0003323011,
0.0002348261,
0.0001661505,
0.000117413,
0.00008307527,
0.00005870652,
0.00004150994
]

y_eq =[
0.000039,
0.000064,
0.00012,
0.000217,
0.000396,
0.00064,
0.00121,
0.00218,
0.004,
0.0073,
0.0116,
0.01684,
0.023,
0.0298,
0.038,
0.048,
0.06,
0.0739,
0.09098,
0.1126,
0.13902,
0.1693,
0.20802,
0.2586,
0.323,
0.4073,
0.503,
0.6082,
0.71,
0.7932,
0.862,
0.9148501,
0.954,
0.9803,
0.9949501,
1,
0.995,
0.9786,
0.952,
0.9154,
0.87,
0.8163,
0.757,
0.6949,
0.631,
0.5668,
0.503,
0.4412,
0.381,
0.321,
0.265,
0.217,
0.175,
0.1382,
0.107,
0.0816,
0.061,
0.04458,
0.032,
0.0232,
0.017,
0.01192,
0.00821,
0.005723,
0.004102,
0.002929,
0.002091,
0.001484,
0.001047,
0.00074,
0.00052,
0.0003611,
0.0002492,
0.0001719,
0.00012,
0.0000848,
0.00006,
0.0000424,
0.00003,
0.0000212,
0.00001499
]

z_eq =[
0.006450001,
0.01054999,
0.02005001,
0.03621,
0.06785001,
0.1102,
0.2074,
0.3713,
0.6456,
1.0390501,
1.3856,
1.62296,
1.74706,
1.7826,
1.77211,
1.7441,
1.6692,
1.5281,
1.28764,
1.0419,
0.8129501,
0.6162,
0.46518,
0.3533,
0.272,
0.2123,
0.1582,
0.1117,
0.07824999,
0.05725001,
0.04216,
0.02984,
0.0203,
0.0134,
0.008749999,
0.005749999,
0.0039,
0.002749999,
0.0021,
0.0018,
0.001650001,
0.0014,
0.0011,
0.001,
0.0008,
0.0006,
0.00034,
0.00024,
0.00019,
0.0001,
0.00004999999,
0.00003,
0.00002,
0.00001,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0
]

#yの等色関数y_eqの合計(k:sum_y_eq)を求める
sum_y_eq =0.0
for i in range(number_wavelength):
    sum_y_eq = sum_y_eq + ( y_eq[i] * light_source[i] ) / 100         # k = （1/100）∫S(λ)y(λ) dλ
    
def drawing(img, gap):
    """
    描画（ファイルに書く画像データを編集する）
    点を打つ
    """
    x,y = img.size
    #print(x,y)
    #配列に0を入れて初期化
    r = [0]*y*x
    X = [0]*x
    Y = [0]*x
    Z = [0]*x
    var_X = [0]*x
    var_Y = [0]*x
    var_Z = [0]*x
    var_R = [0]*x
    var_G = [0]*x
    var_B = [0]*x
    sR = [0]*x
    sG = [0]*x
    sB = [0]*x

    draw = ImageDraw.Draw(img)

    for m in range(0,y,gap):
        percent = round(m/y *1000)/10
        print("画像を作成中です",percent,"%")
        delta_n = m * (end_delta_n - start_delta_n) / y 
        X = [0]*x
        Y = [0]*x
        Z = [0]*x
        #XYZ表色値(X,Y,Z)を求める
        for n in range(0,x,gap):
            film_thickness = start_film_thickness + n * ( end_film_thickness - start_film_thickness ) / x 
            #print(film_thickness)
            for j in range(number_wavelength):
                wavelength = start_wavelength + j * pitch_wavelength
                r[j] = (math.sin(math.pi * delta_n * film_thickness / wavelength )) ** 2        # R(λ,d) = sin^2(π Δn d / λ)
                X[n] = X[n] + light_source[j] * r[j] * x_eq[j] / sum_y_eq           # X(d) = (1/k)∫S(λ)R(λ,d)x(λ) dλ
                Y[n] = Y[n] + light_source[j] * r[j] * y_eq[j] / sum_y_eq           # Y(d) = (1/k)∫S(λ)R(λ,d)y(λ) dλ
                Z[n] = Z[n] + light_source[j] * r[j] * z_eq[j] / sum_y_eq           # Z(d) = (1/k)∫S(λ)R(λ,d)z(λ) dλ
                #print(delta_n, film_thickness , wavelength , r[j], X , Y , Z)
            #print(r[j],X[j],Y[j],Z[j])
            #カラーコードへの変換
            #print("film_thickness" ,"R" , "G" , "B", "color_code","X","Y","Z" )

        for n in range(0,x,gap):
            #sRGB表色値(sR,sG,sB)に変換＋ガンマ変換
            #出典　https://www.easyrgb.com/en/math.php の　XYZ → Standard-RGB
            var_X[n] = X[n] / 100
            var_Y[n] = Y[n] / 100
            var_Z[n] = Z[n] / 100

            var_R[n] = var_X[n] *  3.2406 + var_Y[n] * -1.5372 + var_Z[n] * -0.4986
            var_G[n] = var_X[n] * -0.9689 + var_Y[n] *  1.8758 + var_Z[n] *  0.0415
            var_B[n] = var_X[n] *  0.0557 + var_Y[n] * -0.2040 + var_Z[n] *  1.0570

            if var_R[n] > 0.0031308:
                var_R[n] = 1.055 * ( var_R[n] ** ( 1 / 2.4 ) ) - 0.055
            else:
                var_R[n] = 12.92 * var_R[n]
            if var_G[n] > 0.0031308:
                var_G[n] = 1.055 * ( var_G[n] ** ( 1 / 2.4 ) ) - 0.055
            else:
                var_G[n] = 12.92 * var_G[n]
            if var_B[n] > 0.0031308:
                var_B[n] = 1.055 * ( var_B[n] ** ( 1 / 2.4 ) ) - 0.055
            else:
                var_B[n] = 12.92 * var_B[n]

            sR[n] = int(var_R[n] * 255)
            sG[n] = int(var_G[n] * 255)
            sB[n] = int(var_B[n] * 255)

            #sRGBのオーバーフロー処理
            if sR[n] < 0:
                sR[n] = 0
            elif sR[n] > 255:
                sR[n] = 255
            if sG[n] < 0:
                sG[n] = 0
            elif sG[n] > 255:
                sG[n] = 255
            if sB[n] < 0:
                sB[n] = 0
            elif sB[n] > 255:
                sB[n] = 255
            
            R = sR[n]
            G = sG[n]
            B = sB[n]
            
            draw.rectangle([(n, y-m),(n+gap-1, y-(m+gap-1))], fill=(R,G,B), outline=(R,G,B))

            #draw.point((n, m),fill=(R,G,B))
            #print(n,m,delta_n,R,G,B)
        

    return img
def make_image(screen, bgcolor, filename):
    """
    画像ファイルを作成
    """
    img = Image.new('RGB', screen, bgcolor)

    # 間隔（5～32くらい）
    gap = 1

    img = drawing(img, gap)
    print("完了しました。ルートディレクトリの",filename,"をご覧ください")
    img.save(filename)

if __name__ == '__main__':
    # 画像のサイズ
    screen = (640,1024)

    # 画像の背景色（RGB）
    bgcolor=(119 ,119 ,119)

    # 保存するファイル名（ファイル形式は、拡張子から自動的に判別する）
    filename = "rainbow.png"

    make_image(screen, bgcolor, filename)

#EOF
