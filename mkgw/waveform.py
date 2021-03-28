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
a = 2.
b = 1.7


pa = './mass_%s_a%s' %(m_rate, int(a*10))    #- output path

#----
# Check path
#--
def mkdir_checkdir(pa):

    if os.path.exists(pa):
        print(pa + 'have existed!')
    if not os.path.exists(pa):
        os.mkdir(pa)
        print('MKDIR: ' + pa + ' successful!')

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
            
        if max_m-3 < y < max_m-1:
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

mkdir_checkdir(pa)

H5_FILE = '%s/bbh_%d_n%1d.h5' %(pa, RATE, m_rate)
f = h5py.File(H5_FILE, 'w', libver='latest')

main_grep = f.create_group('/waveform')
main_grep.attrs['srate'] = RATE
main_grep.attrs['model'] = apx
main_grep.attrs['desc'] = 'Spinless BBH waveform model'
    
step = 0

for i in range(0, m_rate):
    for j in range(i, m_rate):
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
np.save('%s/mass.npy' %pa, mass_)

plot = True
if plot:

    ca=0    #- counter
    cb=0
    cd=0
    ct=0

    l = len(mA_)

    for i in range(l):
        ct += 1

        if mA_[i]+mB_[i] <= 80:
            ca += 1
        if mA_[i]+mB_[i] <= 40:
            cb += 1
        if mA_[i]+mB_[i] <= 20:
            cd += 1

    print('total number: ', ct)
    print('total mass under 80: ', ca)
    print('total mass under 40: ', cb)
    print('total mass under 20: ', cd)

    ### mass ###
    plt.figure(figsize=(8,8))
    plt.plot(mB_, mA_, 'r.', markersize=2)

    plt.text(5, 70, 'total number: %s' %ct, fontsize=16)
    plt.text(5, 65, 'total mass less than 80: %s' %ca, fontsize=16)
    plt.text(5, 60, 'total mass less than 40: %s' %cb, fontsize=16)
    plt.text(5, 55, 'total mass less than 20: %s' %cd, fontsize=16)

    plt.xlabel('mB')
    plt.ylabel('mA')
    plt.xticks(np.arange(0,80,5))
    plt.yticks(np.arange(0,80,5))
    plt.title('mass')

    plt.savefig('%s/mass_plot.pdf' %pa)
    plt.savefig('%s/mass_plot.eps' %pa, format='eps', dpi=1000)
    plt.show()

    ### curve ###
    plt.figure()
    plt.plot(m, 'r.', markersize=2)

    plt.yticks(np.arange(0,80,5))
    plt.grid()

    plt.xlabel('number')
    plt.ylabel('mass')
    plt.title('curve of mass sample')

    plt.savefig('%s/mass_curve.pdf' %pa)
    plt.savefig('%s/mass_curve.eps' %pa, format='eps', dpi=1000)

print('Finished !!')


