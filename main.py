import math
import webbrowser

#配色標高設定
min_height = -5             #最低標高デフォルト値
max_height = 4000           #最大標高デフォルト値
pitch_color_cycle = 100     #色1サイクルが何メートルピッチか、デフォルト値

try:
    min_height = int(input("最低標高は？(デフォルト：-5)"))     #入力
except: pass
try:
    max_height = int(input("最大標高は？(デフォルト：4000)"))   #入力
except: pass
try:
    pitch_color_cycle = int(input("何メートル毎に色を繰返す？(100以上、デフォルト：100)"))  #入力
except: pass

pitch_height = pitch_color_cycle // 100   #1色が何メートルピッチか

#地理院地図のURLのヘッダ部
URL='https://maps.gsi.go.jp/#12/35.715370/139.840268/&base_grayscale=1&'\
    'ls=std%2C0.71%7Cslopemap%2C0.37%7Chillshademap%2C0.58%7Crelief_free&'\
    'blend=111&disp=0111&lcd=slopemap&vs=c0j0h0k0l0u0t0z0r0s0m0f1&d=m&reliefdata=2'

#膜厚　d[nm]
pitch_film_thickness = 37.95
#end_film_thickness = 5000
start_film_thickness = 189.75
number_film_thickness = 101 #(end_film_thickness-start_film_thickness) // pitch_film_thickness + 1
end_film_thickness = start_film_thickness + ( number_film_thickness - 1 ) * pitch_film_thickness
#print(start_film_thickness,end_film_thickness,pitch_film_thickness)

#屈折率 nγ,　nα
ng = 1.5
na = 1
delta_n = ng - na

#波長　λ[nm]
start_wavelength = 380
end_wavelength = 780
pitch_wavelength = 5
number_wavelength = (end_wavelength-start_wavelength) // pitch_wavelength + 1

#配列に0を入れて初期化
r = [0]*(number_wavelength*number_film_thickness)
X = [0]*number_film_thickness
Y = [0]*number_film_thickness
Z = [0]*number_film_thickness
var_X = [0]*number_film_thickness
var_Y = [0]*number_film_thickness
var_Z = [0]*number_film_thickness
var_R = [0]*number_film_thickness
var_G = [0]*number_film_thickness
var_B = [0]*number_film_thickness
sR = [0]*number_film_thickness
sG = [0]*number_film_thickness
sB = [0]*number_film_thickness
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
sum_y_eq =0
for i in range(number_wavelength):
    sum_y_eq = sum_y_eq + y_eq[i]           # k = ∫y(λ) dλ
    #(y_eq[i])
#print(sum_y_eq)

#XYZ表色値(X,Y,Z)を求める
for i in range(number_film_thickness): 
    film_thickness = start_film_thickness + i *  pitch_film_thickness
    for j in range(number_wavelength):
        wavelength = start_wavelength + j * pitch_wavelength
        r[i * number_wavelength + j] = (math.sin(math.pi * delta_n * film_thickness / wavelength )) ** 2        # R(λ,d) = π Δn d / λ
        X[i] = X[i] + light_source[j] * r[i * number_wavelength + j] * x_eq[j] / sum_y_eq           # X(d) = (1/k)∫S(λ)R(λ,d)x(λ) dλ
        Y[i] = Y[i] + light_source[j] * r[i * number_wavelength + j] * y_eq[j] / sum_y_eq           # Y(d) = (1/k)∫S(λ)R(λ,d)y(λ) dλ
        Z[i] = Z[i] + light_source[j] * r[i * number_wavelength + j] * z_eq[j] / sum_y_eq           # Z(d) = (1/k)∫S(λ)R(λ,d)z(λ) dλ
        #print(film_thickness , wavelength , r[i * number_wavelength + j], X[i] , Y[i] , Z[i])
        j+=1
    i+=1

#カラーコードへの変換
#print("film_thickness" ,"R" , "G" , "B", "color_code","X","Y","Z" )
for i in range(number_film_thickness): 
    film_thickness = start_film_thickness + i *  pitch_film_thickness

    #sRGB表色値(sR,sG,sB)に変換＋ガンマ変換
    #出典　https://www.easyrgb.com/en/math.php の　XYZ → Standard-RGB
    var_X[i] = X[i] / 100
    var_Y[i] = Y[i] / 100
    var_Z[i] = Z[i] / 100

    var_R[i] = var_X[i] *  3.2406 + var_Y[i] * -1.5372 + var_Z[i] * -0.4986
    var_G[i] = var_X[i] * -0.9689 + var_Y[i] *  1.8758 + var_Z[i] *  0.0415
    var_B[i] = var_X[i] *  0.0557 + var_Y[i] * -0.2040 + var_Z[i] *  1.0570

    if var_R[i] > 0.0031308:
        var_R[i] = 1.055 * ( var_R[i] ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_R[i] = 12.92 * var_R[i]
    if var_G[i] > 0.0031308:
        var_G[i] = 1.055 * ( var_G[i] ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_G[i] = 12.92 * var_G[i]
    if var_B[i] > 0.0031308:
        var_B[i] = 1.055 * ( var_B[i] ** ( 1 / 2.4 ) ) - 0.055
    else:
        var_B[i] = 12.92 * var_B[i]

    sR[i] = int(var_R[i] * 255)
    sG[i] = int(var_G[i] * 255)
    sB[i] = int(var_B[i] * 255)

    #sRGBのオーバーフロー処理
    if sR[i] < 0:
        sR[i] = 0
    elif sR[i] > 255:
        sR[i] = 255
    if sG[i] < 0:
        sG[i] = 0
    elif sG[i] > 255:
        sG[i] = 255
    if sB[i] < 0:
        sB[i] = 0
    elif sB[i] > 255:
        sB[i] = 255

    #カラーコード生成
    color_code += '{0:02x}{1:02x}{2:02x}'.format(sR[i], sG[i], sB[i])
    color_code  = color_code.replace('0x', '')
    #print(film_thickness ,sR[i] , sG[i] , sB[i], color_code[i] , X[i] , Y[i], Z[i])
    i+=1

#URL生成
height = 0
if pitch_height == 0 : pitch_height = 1     #標高ピッチが小数の場合は1にする（エラー回避）
end_height = ( (max_height-min_height) // pitch_height ) * pitch_height  
number_cycle = ( end_height - min_height ) // pitch_height

for i in range (0 , number_cycle ):
    number_color = min_height // pitch_height  + i
    height = min_height + i * pitch_height

    #高さコード生成
    if height < 0:
        height_code = '-{0:x}'.format(abs(height))
    else:
        height_code = '{0:x}'.format(height)
    height_code = height_code.replace('0x', '')

    #URL生成
    if height < 0:
        number_film_thickness = 100 + number_color
    else:
        number_film_thickness = number_color % 100
    if ( i > 0 and i< number_cycle-1 )  :
        URL = URL + 'G' + height_code + 'G' + color_code[number_film_thickness*6:(number_film_thickness+1)*6]
    elif i == 0 :
        URL = URL + height_code + 'G' + color_code[number_film_thickness*6:(number_film_thickness+1)*6]
    elif i == number_cycle-1  :
        URL = URL + "GG" + color_code[number_film_thickness*6:(number_film_thickness+1)*6]
    i+=1

#地理院地図をブラウザで開く
webbrowser.open(URL)
#print(URL)
