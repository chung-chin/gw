import pycbc.noise
import pycbc.psd
import pylab

import numpy as np
import pickle

import os,sys

sys.path.append('..')

#----
#- The color of the noise matches a PSD which you provide
rate = 8192
flow = 30.0
delta_f = 1.0 / 16
flen = int(rate / delta_f)

psd = pycbc.psd.aLIGOZeroDetHighPower(flen, delta_f, flow)


#----
#- Generate 1 seconds of noise at 8192 Hz
delta_t = 1.0 / rate
tsamples = int(1 / delta_t)

num_ = 5000    #- number of samples


for j in range(4):
    noise_ = []
    for i in range(num_):
        ts = pycbc.noise.noise_from_psd(tsamples, delta_t, psd, seed=None)
    
        noise_.append(ts)

        print('Compelete percent: %.2f/100' %(1.0 * i/num_ * 100))
        sys.stdout.write('\r')
    
    
    noise_ = np.array(noise_)
    print(noise_.shape)
    print(noise_[0])


    np.save('./pycbc_noise%s_%s.npy' %(str(j+1),str(num_)), noise_)
