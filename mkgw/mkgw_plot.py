import numpy as np
import matplotlib.pyplot as plt

filename = 'mass_150'

mass = np.load('./%s.npy' %filename, encoding='latin1', allow_pickle=True)

mA = np.array(mass[0])
mB = np.array(mass[1])
m = np.array(mass[2])

### count ###
a = 0
t = 0
c = 0
d = 0

l = len(mA)

for i in range(l):
    t += 1
    if mA[i]+mB[i] <= 80:
        a += 1
    if mA[i]+mB[i] <= 40:
        c += 1
    if mA[i]+mB[i] <= 20:
        d += 1

print('total unmber: ', t)
print('total mass under 80: ', a)
print('total mass under 40: ', c)
print('total mass under 20: ', d)


### mass ###
plt.figure(figsize=(8,8))
plt.plot(mB, mA, 'r.', markersize=2)
plt.text(5, 70, 'total number: %s' %t, fontsize=16)
plt.text(5, 65, 'total mass less than 80: %s' %a, fontsize=16)
plt.text(5, 60, 'total mass less than 40: %s' %c, fontsize=16)
plt.text(5, 55, 'total mass less than 20: %s' %d, fontsize=16)
plt.xlabel('mB')
plt.ylabel('mA')
plt.xticks(np.arange(0,80,5))
plt.yticks(np.arange(0,80,5))
plt.title('mass')
plt.savefig('%s.pdf' %filename)
plt.savefig('%s.eps' %filename, format='eps', dpi=1000)
plt.show()


### curve ###
plt.figure()
plt.plot(m, 'r.', markersize=2)
plt.yticks(np.arange(0,80,5))
plt.grid()
plt.xlabel('number')
plt.ylabel('mass')
plt.title('curve of mass sample')
plt.savefig('%s_curve.pdf' %filename)
plt.savefig('%s_curve.eps' %filename, format='eps', dpi=1000)





#80   6500
#40   4000
#signal 20000