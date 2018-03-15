import cv2
import numpy as np
import matplotlib.pyplot as plt
import struct


im1 = cv2.imread('Cv04_porucha2.bmp')
et1 = cv2.imread('Cv04_porucha2_etalon.bmp')

im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
et1 = cv2.cvtColor(et1, cv2.COLOR_BGR2RGB)

res = np.zeros(np.shape(et1)).astype('double')


# in double
im = im1.astype('double')
im = np.multiply(im,(1.0/255))
et = et1.astype('double')
et = np.multiply(et,(1.0/255))
et = np.multiply(1.0/et, 1.0)

for i in range(0,3):
    #print(np.shape(res[:,:,i]))
    res[:,:,i] = np.multiply(et[:,:,i],im[:,:,i])

c = 255.0
res = np.multiply(res, c)
res = res.astype('uint8')


plt.figure()
plt.subplot(2,3,1)
plt.imshow(et1)

plt.subplot(2,3,2)
plt.imshow(im1)

plt.subplot(2,3,3)
plt.imshow(res)


plt.subplot(2,3,4)
plt.imshow(et1)

plt.subplot(2,3,5)
plt.imshow(im1)

plt.subplot(2,3,6)
plt.imshow(res)

plt.show()

