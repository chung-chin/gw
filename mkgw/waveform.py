import numpy as np
import matplotlib.pyplot as plt
import random
import math
import pylab
from pycbc.waveform import get_td_waveform
import h5py
import os,sys

apx = 'SEOBNRv4'   #- model of gravitational wave

RATE = 8192        #- sampling rate(Hz)
dt = 1. / RATE

max_m = 75.    #- maximum mass
min_m = 5.     #- minimum mass

m_rate = 150   #- sampling rate of mass

#---
# constants of mass function
#---
a = 3
b = 1.7    #- slop


#----
# Build a mass list via hyperbolic tangent
# to get more low mass sample
#--
def get_mass(max_m, min_m, m_rate, a, b):
    
    max_x = b * np.log( ((max_m-min_m)/a) + math.sqrt( ((max_m-min_m)/a)**2 + 1 ) )
    #min_x = b * np.log( ((min_m-min_m)/a) + math.sqrt( ((min_m-min_m)/a)**2 + 1 ) )
    min_x = 0.
    
    #print('max_x=',max_x, 'min_x=', min_x, '\n')  #- check
    
    d = (max_x - min_x)/m_rate
    #print('d=', d, '\n')  #- check
    
    cnt = 0    # counter

    while 1:
        x = min_x
        y = 0

        m_ = []
        m_.append(min_m)
        
        for i in range(m_rate-2):
            dx = random.uniform(d*0.9, d*1.1)
            x = x + dx
            y = round(a*np.sinh(x/b)+min_m, 2)
        
            m_.append(y)
            
        #print(y, '\n')  # check
        
        cnt += 1
        if cnt > 100:
            sys.exit('Can not fit with small m_rate.')
            
        if max_m-4 < y < max_m-1:
            break
        
    m_.append(max_m)
        
    return m_

m = np.array(get_mass(max_m, min_m, m_rate, a, b))

print('mass list: ', m)



#----
# getting low frequency
#--
GM0 = 6.674e-11 * 1.9891e30    #- mass of sun
c   = 299792458.    #- speed of light
C1=5**(3/8.)/(8*np.pi) * ((c**3)/GM0)**(5./8) 

def time2lowfreq(m1,m2,t):
    Mcf= (m1*m2)**(-0.375) * (m1+m2)**(0.125)
    freq = C1 * Mcf * (t*1.4)**(-0.375)    #- add factor 1.4 to get a longer waveform
    
    return freq


#----
# make gravitational wave via pycbc
#--
mA = []    #- mass A
mB = []    #- mass B

H5_FILE = 'bbh_%d_n%1d.h5' %(RATE, n)
f = h5py.File(H5_FILE, 'w', libver='latest')

main_grep = f.create_group('/waveform')
main_grep.attrs['srate'] = RATE
main_grep.attrs['model'] = apx
main_grep.attrs['desc'] = 'Spinless BBH waveform model'
    
step = 0

for i in range(0, n):
    for j in range(i, n):
        ma = m[i]
        mb = m[j]
        
        #----
        # drop some small mass ratio cases
        #--
        #if 1 < (mb/ma) < 1.05:
            #j = j + 1
        #    continue
        

        f_low = time2lowfreq(ma, mb, 2.0)
        
        mA.append(ma)
        mB.append(mb)
        
        hp, hc = get_td_waveform(approximant=apx,
                    mass1=ma, mass2=mb, spin1z=0, delta_t=dt, f_lower=f_low)
        hp_len = np.array(hp).shape[0] - RATE -1
        hp_ = hp[hp_len:-1]
        hc_len = np.array(hc).shape[0] - RATE -1
        hc_ = hc[hc_len:-1]
        
        print('#%s with m1: %.1f, m2: %.1f, f_low = %.1f, t=[%f %f], len= %d'
              %(step,ma,mb,f_low,hp_.sample_times[0],hp_.sample_times[-1],np.array(hp_).shape[0]))

        gname = '%s' %(step)
        
        grp = main_grep.create_group(gname)
        grp.attrs['m'] = [ma, mb]
        grp.attrs['sz'] = [0,0]
        grp.attrs['F_low'] = f_low
        grp.create_dataset('hp', data=hp_, dtype='f')
        grp.create_dataset('hc', data=hc_, dtype='f')

        step = step + 1

f.close()

mA_ = np.array(mA)
mB_ = np.array(mB)
#print(np.array(mA).shape)  #- check
#print(np.array(mB).shape)  #- check

mass_ = []
mass_.append(mA_)
mass_.append(mB_)
mass_.append(m)
np.save('./mass_%s_%sb.npy' %(m_rate, int(b*10)), mass_)

print('Finished !!')


