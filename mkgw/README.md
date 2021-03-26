# 產生重力波與雜訊

----

## 重力波

為了取得更多高頻波形，以雙曲函數

![](http://latex.codecogs.com/svg.latex?y=asinh(x/b)+min_m)

決定質量。

<img src="https://github.com/chung-chin/gw/blob/master/mkgw/plots/mass_function.png" alt="FIG 1" title="FIG. 1:雙曲函數。a=3, b-1.7, min_m=5" width="800"></p>

##### FIG. 1:雙曲函數。a=3, b-1.7, min_m=5

<img src="https://github.com/chung-chin/gw/blob/master/mkgw/plots/mass_150_curve.png" alt="FIG 2" title="FIG 2" width="600"></p>

##### FIG. 2:質量分布

<img src="https://github.com/chung-chin/gw/blob/master/mkgw/plots/mass_150.png" alt="FIG 3" title="FIG 3" width="600"></p>

##### FIG. 3:質量mA, mB

## 雜訊

透過pycbc套件，根據不同的Power Spectral Density（PSD）產生雜訊[1]



[1 "LIGO-PSD"](https://dcc.ligo.org/public/0002/T0900288/002/AdvLIGO%20noise%20curves.pdf)